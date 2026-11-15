"""Agreement engines, plan builder, event study and random-entry twin."""
import numpy as np
from numba import njit

from .common import F, S, COSTS, RT_USD, stats, split_mask, n_sessions


@njit(cache=True)
def owner_sync(aL, aS, bL, bS, window):
    """The owner's ticket logic from 'ARES LC + Smart Trend Sync', for two engines A and B.

    Each event is a single-use ticket valid for `window` bars; an opposite event from the other engine cancels a
    pending ticket; conflicting events on one bar cancel both; a match consumes both tickets."""
    n = len(aL)
    mL = np.zeros(n, np.bool_)
    mS = np.zeros(n, np.bool_)
    pa = pb = 0
    ta = tb = -1
    for t in range(n):
        if pa != 0 and t - ta > window:
            pa = 0
        if pb != 0 and t - tb > window:
            pb = 0
        if (aL[t] or bL[t]) and (aS[t] or bS[t]):
            pa = pb = 0
            continue
        ea = 1 if aL[t] else (-1 if aS[t] else 0)
        eb = 1 if bL[t] else (-1 if bS[t] else 0)
        if ea != 0:
            if pb != 0 and pb != ea:
                pb = 0
            pa, ta = ea, t
        if eb != 0:
            if pa != 0 and pa != eb:
                pa = 0
            pb, tb = eb, t
        if pa != 0 and pa == pb:
            if pa == 1:
                mL[t] = True
            else:
                mS[t] = True
            pa = pb = 0
    return mL, mS


@njit(cache=True)
def quorum(EV, panel, window, m, need_base, baseL, baseS):
    """Generalised agreement.  EV: (V, n) int8 events (+1 buy, -1 sell).  A long fires at bar t when
    at least m panel voters had a buy event in bars [t-window, t], one of them at t, no panel voter had a
    sell event in that span, the base condition holds, and the condition was not already true at t-1."""
    n = EV.shape[1]
    k = len(panel)
    outL = np.zeros(n, np.bool_)
    outS = np.zeros(n, np.bool_)
    lastL = np.full(k, -10 ** 9)
    lastS = np.full(k, -10 ** 9)
    prevL = prevS = False
    for t in range(n):
        nowL = nowS = False
        cL = cS = 0
        for j in range(k):
            e = EV[panel[j], t]
            if e > 0:
                lastL[j] = t
                nowL = True
            elif e < 0:
                lastS[j] = t
                nowS = True
            if t - lastL[j] <= window:
                cL += 1
            if t - lastS[j] <= window:
                cS += 1
        okL = cL >= m and cS == 0 and (not need_base or baseL[t])
        okS = cS >= m and cL == 0 and (not need_base or baseS[t])
        outL[t] = okL and nowL and not prevL
        outS[t] = okS and nowS and not prevS
        prevL, prevS = okL, okS
    return outL, outS


def make_plan(b, sigL, sigS, exit_spec, atr, entry_until=None, max_trades=1000, cooldown=0,
              exL=None, exS=None, trail=None):
    """exit_spec: ('bars', N) | ('atr', stop_mult, target_R) | ('opp',) | ('trail', N)."""
    p = S.Plan(b.n)
    ok = ~np.isnan(atr)
    if entry_until is not None:
        ok &= b.mclose <= entry_until
    p.sigL, p.sigS = sigL & ok, sigS & ok
    kind = exit_spec[0]
    rt = lambda x: np.round(x / b.tick) * b.tick
    wide = 8.0
    if kind == "bars":
        p.stpL, p.stpS = rt(b.c - wide * atr), rt(b.c + wide * atr)
        p.time_stop_bars = int(exit_spec[1])
    elif kind == "atr":
        s, r = exit_spec[1], exit_spec[2]
        p.stpL, p.stpS = rt(b.c - s * atr), rt(b.c + s * atr)
        p.tgtL, p.tgtS = rt(b.c + s * r * atr), rt(b.c - s * r * atr)
        if len(exit_spec) > 3:
            p.time_stop_bars = int(exit_spec[3])
    elif kind == "opp":
        p.stpL, p.stpS = rt(b.c - wide * atr), rt(b.c + wide * atr)
        p.exL, p.exS = (sigS if exL is None else exL).copy(), (sigL if exS is None else exS).copy()
    elif kind == "trail":
        # stop at the base Smart Trail level (clamped to 0.5..4 ATR), exit when the base regime flips
        dL = np.clip(b.c - trail, 0.5 * atr, 4.0 * atr)
        dS = np.clip(trail - b.c, 0.5 * atr, 4.0 * atr)
        p.stpL, p.stpS = rt(b.c - dL), rt(b.c + dS)
        p.exL, p.exS = exL.copy(), exS.copy()
        if len(exit_spec) > 1 and exit_spec[1]:
            p.time_stop_bars = int(exit_spec[1])
    else:
        raise ValueError(kind)
    p.cooldown_bars, p.max_trades, p.loss_standdown = cooldown, max_trades, 0
    return p


def backtest(b, plan, level="base", **kw):
    T, eq, inpos, miss = S.run(b, plan, COSTS[level], **kw)
    return T


def event_study(b, evL, evS, atr, horizons=(1, 2, 4, 8, 12), mask=None):
    """Signed move from the next bar's open to the open k bars later (or the session close), in ATR units."""
    idx = np.flatnonzero((evL | evS) & ~b.last & ~np.isnan(atr) & (mask if mask is not None else True))
    d = np.where(evL[idx], 1.0, -1.0)
    ent = b.o[idx + 1]
    out = {"n": len(idx), "per_day": len(idx) / max(1, n_sessions(b, mask if mask is not None else np.ones(b.n, bool)))}
    sess = b.sess[idx]
    cost_atr = RT_USD[b.sym] / b.pv / atr[idx]
    out["cost_atr"] = float(np.mean(cost_atr)) if len(idx) else np.nan
    for k in horizons:
        j = idx + 1 + k
        end = b.sess_end[idx]
        px = np.where(j <= end, b.o[np.minimum(j, b.n - 1)], b.c[end])
        r = d * (px - ent) / atr[idx]
        if len(r) < 5:
            out[k] = (np.nan, np.nan)
            continue
        # cluster by session: t-statistic of the mean of session sums over events
        u, inv = np.unique(sess, return_inverse=True)
        ssum = np.bincount(inv, r)
        cnt = np.bincount(inv)
        mean = r.mean()
        resid = ssum - cnt * mean
        se = np.sqrt((resid ** 2).sum()) / len(r)
        out[k] = (float(mean), float(mean / se) if se > 0 else np.nan)
    return out


def twin(b, plan, rng, n_twins=100, mask=None, level="base"):
    """Random-entry twins: same number of signals per direction and time-of-day slot, same exits."""
    res = []
    slots = b.slot
    valid = ~np.isnan(plan.stpL) & ~b.last
    by_slot = {}
    for s in np.unique(slots):
        by_slot[s] = np.flatnonzero((slots == s) & valid)
    for _ in range(n_twins):
        p = plan.copy()
        p.sigL = np.zeros(b.n, np.bool_)
        p.sigS = np.zeros(b.n, np.bool_)
        for sig, dst in ((plan.sigL, p.sigL), (plan.sigS, p.sigS)):
            for t in np.flatnonzero(sig):
                pool_ = by_slot[slots[t]]
                if len(pool_):
                    dst[pool_[rng.integers(len(pool_))]] = True
        res.append(stats(backtest(b, p, level), b, mask))
    return res
