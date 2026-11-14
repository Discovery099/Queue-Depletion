"""Causal feature primitives (SPEC 7.1, 14.8).  Every function uses data up to the current bar only.

Conventions
  * arrays are aligned to bar close; NaN means "not yet defined" (Pine `na`);
  * rolling windows include the current bar and are NaN until the window is full;
  * rolling indicators run continuously across sessions, so the overnight gap enters the true range
    as one observation (SPEC 4.2 rule 1); session-anchored functions reset at the session's first bar;
  * recursive averages follow Pine: ta.ema / ta.rma are seeded with the simple average of the
    first `n` values.
"""
import numpy as np
from numba import njit


@njit(cache=True)
def sma(x, n):
    m = len(x)
    out = np.full(m, np.nan)
    s = 0.0
    bad = 0
    for i in range(m):
        if np.isnan(x[i]):
            bad += 1
        else:
            s += x[i]
        if i >= n:
            if np.isnan(x[i - n]):
                bad -= 1
            else:
                s -= x[i - n]
        if i >= n - 1 and bad == 0:
            out[i] = s / n
    return out


@njit(cache=True)
def rsum(x, n):
    return sma(x, n) * n


@njit(cache=True)
def _recursive(x, n, alpha):
    m = len(x)
    out = np.full(m, np.nan)
    s = 0.0
    cnt = 0
    prev = np.nan
    for i in range(m):
        v = x[i]
        if np.isnan(prev):
            if np.isnan(v):
                s = 0.0
                cnt = 0
            else:
                s += v
                cnt += 1
                if cnt == n:
                    prev = s / n
                    out[i] = prev
        else:
            if not np.isnan(v):
                prev = alpha * v + (1.0 - alpha) * prev
            out[i] = prev
    return out


def ema(x, n):
    return _recursive(x, n, 2.0 / (n + 1.0))


def rma(x, n):
    return _recursive(x, n, 1.0 / n)


@njit(cache=True)
def stdev(x, n):
    m = len(x)
    out = np.full(m, np.nan)
    for i in range(n - 1, m):
        s = 0.0
        ok = True
        for j in range(i - n + 1, i + 1):
            if np.isnan(x[j]):
                ok = False
                break
            s += x[j]
        if ok:
            mu = s / n
            q = 0.0
            for j in range(i - n + 1, i + 1):
                q += (x[j] - mu) ** 2
            out[i] = np.sqrt(q / n)
    return out


@njit(cache=True)
def highest(x, n):
    m = len(x)
    out = np.full(m, np.nan)
    for i in range(n - 1, m):
        v = -np.inf
        for j in range(i - n + 1, i + 1):
            if np.isnan(x[j]):
                v = np.nan
                break
            if x[j] > v:
                v = x[j]
        out[i] = v
    return out


@njit(cache=True)
def lowest(x, n):
    m = len(x)
    out = np.full(m, np.nan)
    for i in range(n - 1, m):
        v = np.inf
        for j in range(i - n + 1, i + 1):
            if np.isnan(x[j]):
                v = np.nan
                break
            if x[j] < v:
                v = x[j]
        out[i] = v
    return out


def shift(x, k):
    """Value k bars ago (k >= 0 only; the DSL cannot express a negative shift)."""
    if k < 0:
        raise ValueError("negative shift is lookahead")
    if k == 0:
        return x
    if x.dtype == np.bool_:
        out = np.zeros(len(x), np.bool_)
    else:
        out = np.full(len(x), np.nan)
    out[k:] = x[:-k]
    return out


def true_range(h, l, c):
    pc = shift(c, 1)
    tr = np.maximum(h - l, np.maximum(np.abs(h - pc), np.abs(l - pc)))
    tr[0] = h[0] - l[0]
    return tr


def atr(h, l, c, n):
    return rma(true_range(h, l, c), n)


def rsi(x, n):
    ch = x - shift(x, 1)
    up = rma(np.where(np.isnan(ch), np.nan, np.maximum(ch, 0.0)), n)
    dn = rma(np.where(np.isnan(ch), np.nan, np.maximum(-ch, 0.0)), n)
    with np.errstate(divide="ignore", invalid="ignore"):
        r = 100.0 - 100.0 / (1.0 + up / dn)
    r = np.where(dn == 0, np.where(up == 0, 50.0, 100.0), r)
    return np.where(np.isnan(up), np.nan, r)


@njit(cache=True)
def barssince(cond):
    m = len(cond)
    out = np.full(m, np.nan)
    last = -1
    for i in range(m):
        if cond[i]:
            last = i
        if last >= 0:
            out[i] = i - last
    return out


@njit(cache=True)
def valuewhen(cond, x):
    m = len(cond)
    out = np.full(m, np.nan)
    v = np.nan
    for i in range(m):
        if cond[i]:
            v = x[i]
        out[i] = v
    return out


@njit(cache=True)
def percentrank(x, n):
    """Percent of the previous n values that are <= the current value (Pine ta.percentrank)."""
    m = len(x)
    out = np.full(m, np.nan)
    for i in range(n, m):
        if np.isnan(x[i]):
            continue
        cnt = 0
        ok = True
        for j in range(i - n, i):
            if np.isnan(x[j]):
                ok = False
                break
            if x[j] <= x[i]:
                cnt += 1
        if ok:
            out[i] = 100.0 * cnt / n
    return out


@njit(cache=True)
def meandev(x, n):
    m = len(x)
    out = np.full(m, np.nan)
    for i in range(n - 1, m):
        s = 0.0
        ok = True
        for j in range(i - n + 1, i + 1):
            if np.isnan(x[j]):
                ok = False
                break
            s += x[j]
        if ok:
            mu = s / n
            q = 0.0
            for j in range(i - n + 1, i + 1):
                q += abs(x[j] - mu)
            out[i] = q / n
    return out


# ------------------------------------------------------------------ session-anchored
@njit(cache=True)
def sess_cumsum(x, first):
    m = len(x)
    out = np.empty(m)
    s = 0.0
    for i in range(m):
        if first[i]:
            s = 0.0
        if not np.isnan(x[i]):
            s += x[i]
        out[i] = s
    return out


@njit(cache=True)
def sess_cummax(x, first):
    m = len(x)
    out = np.empty(m)
    v = -np.inf
    for i in range(m):
        if first[i]:
            v = -np.inf
        if x[i] > v:
            v = x[i]
        out[i] = v
    return out


@njit(cache=True)
def sess_cummin(x, first):
    m = len(x)
    out = np.empty(m)
    v = np.inf
    for i in range(m):
        if first[i]:
            v = np.inf
        if x[i] < v:
            v = x[i]
        out[i] = v
    return out


@njit(cache=True)
def sess_first(x, first):
    m = len(x)
    out = np.empty(m)
    v = np.nan
    for i in range(m):
        if first[i]:
            v = x[i]
        out[i] = v
    return out


@njit(cache=True)
def prev_sess_last(x, first):
    """Final value of x in the previous session, available from the first bar of the new session."""
    m = len(x)
    out = np.full(m, np.nan)
    v = np.nan
    for i in range(m):
        if first[i] and i > 0:
            v = x[i - 1]
        out[i] = v
    return out


@njit(cache=True)
def sess_count(first):
    m = len(first)
    out = np.empty(m)
    k = 0
    for i in range(m):
        if first[i]:
            k = 0
        out[i] = k
        k += 1
    return out


@njit(cache=True)
def frozen_after(x, first, mclose, minutes):
    """Value of x at the bar that closes `minutes` after the open, held for the rest of the session.
    NaN before that bar has closed (opening-range style levels)."""
    m = len(x)
    out = np.full(m, np.nan)
    v = np.nan
    for i in range(m):
        if first[i]:
            v = np.nan
        if np.isnan(v) and mclose[i] >= minutes:
            v = x[i]
        out[i] = v
    return out


# ------------------------------------------------------------------ stateful regimes
@njit(cache=True)
def smart_trail(c, buf, confirm):
    """The owner's Smart Trail state machine (baseline/smart_trend_v1.pine, CORE ALGORITHM).

    Returns (trail level, regime in {-1, 0, +1}).  `buf` is factor * (smoothed) ATR."""
    n = len(c)
    trail = np.full(n, np.nan)
    reg = np.zeros(n, np.int8)
    tl = np.nan
    regime = 0
    cc = 0
    for i in range(n):
        b = buf[i]
        if np.isnan(tl) and not np.isnan(b):
            tl = c[i]
            regime = 1 if (i > 0 and c[i] > c[i - 1]) else -1
            cc = 0
        if not np.isnan(tl) and not np.isnan(b):
            raw_regime = regime
            if regime == 1:
                raw = max(tl, c[i] - b)
                if c[i] < raw:
                    raw_regime = -1
            else:
                raw = min(tl, c[i] + b)
                if c[i] > raw:
                    raw_regime = 1
            if raw_regime != regime:
                cc += 1
                if cc >= confirm:
                    regime = raw_regime
                    cc = 0
                    tl = c[i] - b if regime == 1 else c[i] + b
                else:
                    tl = max(tl, c[i] - b) if regime == 1 else min(tl, c[i] + b)
            else:
                cc = 0
                tl = max(tl, c[i] - b) if regime == 1 else min(tl, c[i] + b)
        trail[i] = tl
        reg[i] = regime
    return trail, reg


@njit(cache=True)
def supertrend_dir(h, l, c, atr_, mult):
    """Classic supertrend direction: +1 up, -1 down, 0 undefined."""
    n = len(c)
    out = np.zeros(n)
    ub = np.nan
    lb = np.nan
    d = 0
    for i in range(n):
        a = atr_[i]
        if np.isnan(a):
            continue
        mid = (h[i] + l[i]) / 2.0
        nub = mid + mult * a
        nlb = mid - mult * a
        if d == 0:
            ub, lb, d = nub, nlb, 1
        else:
            if nub < ub or c[i - 1] > ub:
                ub = nub
            if nlb > lb or c[i - 1] < lb:
                lb = nlb
            if d == 1 and c[i] < lb:
                d = -1
            elif d == -1 and c[i] > ub:
                d = 1
        out[i] = d
    return out


# ------------------------------------------------------------------ higher timeframe (SPEC 14.8)
@njit(cache=True)
def htf_confirm(first, k):
    """True on the base bar that completes a higher-timeframe bar of k base bars, counted from the
    session open.  A trailing partial group is never confirmed, so nothing is published from it."""
    m = len(first)
    out = np.zeros(m, np.bool_)
    cnt = 0
    for i in range(m):
        if first[i]:
            cnt = 0
        cnt += 1
        if cnt % k == 0:
            out[i] = True
    return out


@njit(cache=True)
def htf_ohlc(o, h, l, c, first, k):
    """Open/high/low/close of the most recently CONFIRMED higher-timeframe bar, forward-filled.
    The value changes only on the base bar whose close completes the higher-timeframe bar."""
    m = len(c)
    ho = np.full(m, np.nan); hh = np.full(m, np.nan); hl = np.full(m, np.nan); hc = np.full(m, np.nan)
    co = np.nan; ch = -np.inf; cl = np.inf
    po = np.nan; ph = np.nan; pl = np.nan; pc = np.nan
    cnt = 0
    for i in range(m):
        if first[i]:
            cnt = 0
        if cnt % k == 0:
            co = o[i]; ch = h[i]; cl = l[i]
        else:
            if h[i] > ch:
                ch = h[i]
            if l[i] < cl:
                cl = l[i]
        cnt += 1
        if cnt % k == 0:
            po = co; ph = ch; pl = cl; pc = c[i]
        ho[i] = po; hh[i] = ph; hl[i] = pl; hc[i] = pc
    return ho, hh, hl, hc


@njit(cache=True)
def ema_on_event(x, ev, n):
    """EMA updated only when ev is true, seeded with the first event value; held otherwise."""
    m = len(x)
    out = np.full(m, np.nan)
    a = 2.0 / (n + 1.0)
    e = np.nan
    for i in range(m):
        if ev[i] and not np.isnan(x[i]):
            e = x[i] if np.isnan(e) else a * x[i] + (1.0 - a) * e
        out[i] = e
    return out


@njit(cache=True)
def nth_event_value(x, ev, k):
    """Value of x at the k-th most recent event (k=0 is the latest), held between events."""
    m = len(x)
    out = np.full(m, np.nan)
    buf = np.full(k + 1, np.nan)
    for i in range(m):
        if ev[i]:
            for j in range(k, 0, -1):
                buf[j] = buf[j - 1]
            buf[0] = x[i]
        out[i] = buf[k]
    return out


@njit(cache=True)
def wma(x, n):
    """Linearly weighted average, weight n on the current bar down to 1 on the oldest (Pine ta.wma)."""
    m = len(x)
    out = np.full(m, np.nan)
    den = n * (n + 1) / 2.0
    for i in range(n - 1, m):
        s = 0.0
        ok = True
        for j in range(n):
            v = x[i - j]
            if np.isnan(v):
                ok = False
                break
            s += v * (n - j)
        if ok:
            out[i] = s / den
    return out


def hma(x, n):
    """Hull average as Pine ta.hma: wma(2*wma(x, n/2) - wma(x, n), floor(sqrt(n)))."""
    h = max(1, n // 2)
    r = max(1, int(np.floor(np.sqrt(n))))
    return wma(2.0 * wma(x, h) - wma(x, n), r)
