"""Pine-compatible indicators (ta.rma / ta.ema / ta.wma / ta.hma / ta.rsi / ta.atr) plus extra filters."""
import numpy as np
from numba import njit


@njit(cache=True)
def rma(x, n):
    out = np.full(x.size, np.nan)
    s = 0.0
    cnt = 0
    prev = np.nan
    for i in range(x.size):
        xi = x[i]
        if np.isnan(prev):
            if np.isnan(xi):
                cnt = 0
                s = 0.0
                continue
            s += xi
            cnt += 1
            if cnt == n:
                prev = s / n
                out[i] = prev
        else:
            if not np.isnan(xi):
                prev = (xi + (n - 1) * prev) / n
            out[i] = prev
    return out


@njit(cache=True)
def ema(x, n):
    # Pine: sum := na(sum[1]) ? src : alpha*src + (1-alpha)*nz(sum[1])
    out = np.full(x.size, np.nan)
    a = 2.0 / (n + 1)
    prev = np.nan
    for i in range(x.size):
        xi = x[i]
        if np.isnan(prev):
            prev = xi
        elif not np.isnan(xi):
            prev = a * xi + (1 - a) * prev
        out[i] = prev
    return out


@njit(cache=True)
def wma(x, n):
    out = np.full(x.size, np.nan)
    den = n * (n + 1) / 2.0
    for i in range(n - 1, x.size):
        s = 0.0
        ok = True
        for k in range(n):
            v = x[i - k]
            if np.isnan(v):
                ok = False
                break
            s += v * (n - k)
        if ok:
            out[i] = s / den
    return out


def hma(x, n):
    half = max(1, n // 2)
    sq = max(1, int(np.floor(np.sqrt(n))))
    return wma(2.0 * wma(x, half) - wma(x, n), sq)


@njit(cache=True)
def true_range(h, l, c):
    tr = np.empty(h.size)
    tr[0] = h[0] - l[0]
    for i in range(1, h.size):
        tr[i] = max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1]))
    return tr


def atr(h, l, c, n):
    return rma(true_range(h, l, c), n)


def rsi(c, n):
    ch = np.diff(c, prepend=np.nan)
    up = rma(np.where(np.isnan(ch), np.nan, np.maximum(ch, 0.0)), n)
    dn = rma(np.where(np.isnan(ch), np.nan, np.maximum(-ch, 0.0)), n)
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.where(dn == 0, 100.0, np.where(up == 0, 0.0, 100.0 - 100.0 / (1.0 + up / dn)))
    r[np.isnan(up) | np.isnan(dn)] = np.nan
    return r


@njit(cache=True)
def smart_trend(c, buffer):
    """Smart Trail: returns trail, regime (1/-1/0) exactly as the Pine block."""
    n = c.size
    trail = np.full(n, np.nan)
    regime = np.zeros(n, np.int64)
    t = np.nan
    r = 0
    for i in range(n):
        if np.isnan(t) and not np.isnan(buffer[i]):
            t = c[i]
            r = 1 if (i > 0 and c[i] > c[i - 1]) else -1
        if not np.isnan(t) and not np.isnan(buffer[i]):
            raw = max(t, c[i] - buffer[i]) if r == 1 else min(t, c[i] + buffer[i])
            nr = r
            if r == 1 and c[i] < raw:
                nr = -1
            elif r == -1 and c[i] > raw:
                nr = 1
            if nr != r:
                r = nr
                t = c[i] - buffer[i] if r == 1 else c[i] + buffer[i]
            else:
                t = raw
        trail[i] = t
        regime[i] = r
    return trail, regime


# ----------------------------------------------------------------------------- extra filters

def efficiency_ratio(c, n):
    out = np.full(c.size, np.nan)
    ad = np.abs(np.diff(c, prepend=np.nan))
    cs = np.nancumsum(ad)
    out[n:] = np.abs(c[n:] - c[:-n]) / np.maximum(cs[n:] - cs[:-n], 1e-12)
    return out


def adx(h, l, c, n):
    up = np.diff(h, prepend=np.nan)
    dn = -np.diff(l, prepend=np.nan)
    pdm = np.where((up > dn) & (up > 0), up, 0.0)
    mdm = np.where((dn > up) & (dn > 0), dn, 0.0)
    pdm[0] = np.nan
    mdm[0] = np.nan
    tr = true_range(h, l, c)
    tr[0] = np.nan
    atr_ = rma(tr, n)
    pdi = 100 * rma(pdm, n) / atr_
    mdi = 100 * rma(mdm, n) / atr_
    dx = 100 * np.abs(pdi - mdi) / np.maximum(pdi + mdi, 1e-12)
    return rma(dx, n), pdi, mdi


def session_vwap(h, l, c, v, day_id):
    tp = (h + l + c) / 3.0
    pv = tp * v
    out = np.empty(c.size)
    start = 0
    for i in range(1, c.size + 1):
        if i == c.size or day_id[i] != day_id[i - 1]:
            cpv = np.cumsum(pv[start:i])
            cv = np.cumsum(v[start:i])
            out[start:i] = np.where(cv > 0, cpv / np.maximum(cv, 1e-12), tp[start:i])
            start = i
    return out
