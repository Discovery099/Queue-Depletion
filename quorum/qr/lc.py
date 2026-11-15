"""Lorentzian Classification engine and kernel, re-implemented from the owner's merged script
("ARES LC + Smart Trend Sync": rolling training range, persistent neighbour arrays) and the public
MLExtensions / KernelFunctions formulas.  Everything is causal: bar t uses bars <= t only.
"""
import numpy as np
from numba import njit

from .common import F


@njit(cache=True)
def _normalize_expanding(x):
    """MLExtensions.normalize(src, 0, 1): scale by the running historic min and max."""
    out = np.full(len(x), np.nan)
    mn, mx = 10e10, -10e10
    for i in range(len(x)):
        v = x[i]
        if not np.isnan(v):
            mn = min(v, mn)
            mx = max(v, mx)
            out[i] = (v - mn) / max(mx - mn, 10e-10)
    return out


def n_rsi(src, n1, n2):
    return F.ema(F.rsi(src, n1), n2) / 100.0 if n2 > 1 else F.rsi(src, n1) / 100.0


def n_cci(src, n1, n2):
    cci = (src - F.sma(src, n1)) / (0.015 * F.meandev(src, n1))
    return _normalize_expanding(F.ema(cci, n2) if n2 > 1 else cci)


def n_wt(src, n1, n2):
    e1 = F.ema(src, n1)
    e2 = F.ema(np.abs(src - e1), n1)
    ci = (src - e1) / (0.015 * e2)
    wt1 = F.ema(ci, n2)
    wt2 = F.sma(wt1, 4)
    return _normalize_expanding(wt1 - wt2)


@njit(cache=True)
def n_adx(h, l, c, n):
    out = np.full(len(c), np.nan)
    trs = dmp = dmn = 0.0
    adx = np.nan
    cnt = 0
    s = 0.0
    for i in range(len(c)):
        pc = c[i - 1] if i > 0 else 0.0
        ph = h[i - 1] if i > 0 else 0.0
        pl = l[i - 1] if i > 0 else 0.0
        tr = max(max(h[i] - l[i], abs(h[i] - pc)), abs(l[i] - pc))
        up, dn = h[i] - ph, pl - l[i]
        p = max(up, 0.0) if up > dn else 0.0
        m = max(dn, 0.0) if dn > up else 0.0
        trs = trs - trs / n + tr
        dmp = dmp - dmp / n + p
        dmn = dmn - dmn / n + m
        dip, din = dmp / trs * 100.0, dmn / trs * 100.0
        dx = abs(dip - din) / (dip + din) * 100.0 if dip + din > 0 else np.nan
        if not np.isnan(dx):                       # ta.rma: SMA seed over the first n values
            if cnt < n:
                s += dx
                cnt += 1
                if cnt == n:
                    adx = s / n
            else:
                adx = (adx * (n - 1) + dx) / n
        out[i] = adx / 100.0
    return out


@njit(cache=True)
def _knn(f, lab, k, max_back):
    """The script's approximate neighbour search.  f: (5, n) features; lab: training labels."""
    n = f.shape[1]
    pred = np.zeros(n)
    dist = np.zeros(k + 2)
    prd = np.zeros(k + 2)
    m = 0
    q = int(np.floor(k * 3 / 4 + 0.5))
    for t in range(n):
        last = -1.0
        for i in range(max(0, t - max_back + 1), t + 1):
            if i % 4 == 0:
                continue
            d = 0.0
            for j in range(f.shape[0]):
                d += np.log(1.0 + abs(f[j, t] - f[j, i]))
            if np.isnan(d) or d < last:
                continue
            last = d
            dist[m] = d
            prd[m] = lab[i]
            m += 1
            if m > k:
                last = dist[q]
                for z in range(m - 1):
                    dist[z] = dist[z + 1]
                    prd[z] = prd[z + 1]
                m -= 1
        s = 0.0
        for z in range(m):
            s += prd[z]
        pred[t] = s
    return pred


@njit(cache=True)
def rational_quadratic(src, lookback, rw, start):
    n = len(src)
    out = np.full(n, np.nan)
    m = start + 2                                   # i = 0 .. size + start, size = 1
    w = np.empty(m)
    for i in range(m):
        w[i] = (1.0 + i * i / (lookback * lookback * 2.0 * rw)) ** (-rw)
    for t in range(m - 1, n):
        a = 0.0
        for i in range(m):
            a += src[t - i] * w[i]
        out[t] = a / w.sum()
    return out


@njit(cache=True)
def _regime_filter(src, h, l, thr):
    n = len(src)
    ok = np.zeros(n, np.bool_)
    v1 = v2 = klmf = 0.0
    e = np.nan
    a = 2.0 / 201.0
    prev_klmf = np.nan
    for i in range(n):
        if i == 0:
            v2 = 0.1 * (h[i] - l[i])
            prev_klmf = np.nan
            continue
        v1 = 0.2 * (src[i] - src[i - 1]) + 0.8 * v1
        v2 = 0.1 * (h[i] - l[i]) + 0.8 * v2
        om = abs(v1 / v2) if v2 != 0 else 0.0
        al = (-om * om + np.sqrt(om ** 4 + 16.0 * om * om)) / 8.0
        new = al * src[i] + (1.0 - al) * klmf
        if i > 1:
            sl = abs(new - klmf)
            e = sl if np.isnan(e) else a * sl + (1.0 - a) * e
            ok[i] = e > 0 and (sl - e) / e >= thr
        klmf = new
    return ok


def lorentzian(b, k=8, max_back=2000, regime_thr=-0.1, h=8, r=8.0, x=25):
    """Returns dict with prediction, signal, lc_long, lc_short, kernel estimate and kernel-turn events."""
    c, hi, lo = b.c, b.h, b.l
    hlc3 = (hi + lo + c) / 3.0
    f = np.vstack([n_rsi(c, 14, 1), n_wt(hlc3, 10, 11), n_cci(c, 20, 1), n_adx(hi, lo, c, 20), n_rsi(c, 9, 1)])
    c4 = F.shift(c, 4)
    lab = np.where(c4 < c, -1.0, np.where(c4 > c, 1.0, 0.0))
    pred = _knn(np.ascontiguousarray(f), lab, k, max_back)
    tr = F.true_range(hi, lo, c)
    vol_ok = tr > F.atr(hi, lo, c, 10)
    reg_ok = _regime_filter((b.o + hi + lo + c) / 4.0, hi, lo, regime_thr)
    ok = vol_ok & reg_ok
    sig = np.zeros(b.n, np.int8)
    s = 0
    for i in range(b.n):
        if pred[i] > 0 and ok[i]:
            s = 1
        elif pred[i] < 0 and ok[i]:
            s = -1
        sig[i] = s
    chg = np.r_[False, sig[1:] != sig[:-1]]
    y = rational_quadratic(c, h, r, x)
    y1 = F.shift(y, 1)
    y2 = F.shift(y, 2)
    up, dn = y > y1, y < y1
    return dict(pred=pred, sig=sig, lc_long=(sig == 1) & chg & up, lc_short=(sig == -1) & chg & dn,
                kern=y, kern_up=up, kern_dn=dn,
                kturn_long=up & (y2 > y1), kturn_short=dn & (y2 < y1))


def smart_arrows(b, n=14, factor=3.0, adapt=10, confirm=1):
    """Smart Trend V1 trail, regime and arrows (owner defaults; min strength 1 = every arrow)."""
    buf = factor * F.ema(F.atr(b.h, b.l, b.c, n), adapt)
    trail, reg = F.smart_trail(b.c, buf, confirm)
    prev = np.r_[np.int8(0), reg[:-1]]
    return trail, reg, (reg == 1) & (prev == -1), (reg == -1) & (prev == 1)
