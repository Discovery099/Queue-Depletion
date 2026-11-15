"""Full statistics for a genome on a set of folds / block, wording helpers."""
import numpy as np

from . import search as Q
from .common import SYMS, N_SEARCH, COSTS, S


def tstats(net, win, ts, nsess):
    n = len(net)
    if n == 0:
        return dict(n=0, tpd=0.0, wr=np.nan, pf=np.nan, net=0.0, dd=0.0, dd_pct=np.nan, exp=0.0, payoff=np.nan)
    o = np.argsort(ts, kind="stable")
    net, win = net[o], win[o]
    eq = np.r_[0.0, np.cumsum(net)]
    dd = float((np.maximum.accumulate(eq) - eq).max())
    gp, gl = net[net > 0].sum(), -net[net < 0].sum()
    aw = net[win].mean() if win.any() else np.nan
    al = -net[~win].mean() if (~win).any() else np.nan
    return dict(n=n, tpd=n / nsess, wr=100.0 * win.mean(), pf=float(gp / gl) if gl > 0 else np.inf, net=float(net.sum()),
                dd=dd, dd_pct=100.0 * dd / net.sum() if net.sum() > 0 else np.nan, exp=float(net.mean()),
                payoff=float(aw / al) if al and al > 0 else np.nan)


def full(g, e, folds=None, holdout=False, level="base", Ts=None, **kw):
    """Per-instrument and pooled statistics.  folds: tuple of fold indices, or holdout=True for sessions >= N_SEARCH."""
    Ts = Q.run(g, e, level, **kw) if Ts is None else Ts
    out, allnet, allwin, allts = {}, [], [], []
    for sym in SYMS:
        c, T = e[sym], Ts[sym]
        b = c["b"]
        ei = T[:, 1].astype(np.int64) if len(T) else np.zeros(0, np.int64)
        if holdout:
            sel = b.sess[ei] >= N_SEARCH
            ns = len(np.unique(b.sess[b.sess >= N_SEARCH]))
        else:
            sel = np.isin(c["fold"][ei], folds)
            ns = int(c["nsess"][list(folds)].sum())
        net, win, ts = T[sel, 13] * b.pv, T[sel, 17] > 0, b.ts[ei[sel]]
        out[sym] = tstats(net, win, ts, ns)
        allnet.append(net); allwin.append(win); allts.append(ts)
    out["pooled"] = tstats(np.concatenate(allnet), np.concatenate(allwin), np.concatenate(allts), ns)
    out["pooled"]["tpd"] = out["pooled"]["n"] / ns / 2.0          # per instrument per day
    return out


def words(g, e):
    names = e["names"]
    ex = tuple(g["exit"])
    if ex[0] == "atr":
        x = f"stop {ex[1]:g} ATR, target {ex[1] * ex[2]:g} ATR ({ex[2]:g}R)" + (f", max {ex[3]} bars" if ex[3] else "")
        if g["be"]:
            x += f", stop to entry after {g['be']:g}R"
        if g["part"]:
            x += f", half off at {g['part']:g}R"
    elif ex[0] == "bars":
        x = f"exit after {ex[1]} bars (8 ATR emergency stop)"
    elif ex[0] == "trail":
        x = "stop at the Smart Trail, exit when the trail flips" + (f", max {ex[1]} bars" if ex[1] else "")
    else:
        x = "exit on the opposite agreement (8 ATR emergency stop)"
    base = (f"Smart Trend arrow (factor {g['factor']:g}) within {g['W']} bars" if g["mode"] == "arrow"
            else f"Smart Trend regime (factor {g['factor']:g}) agrees")
    return f"{base} + {g['m']} of [{', '.join(names[v] for v in g['panel'])}] within {g['W']} bars; {x}"


def line(s):
    if not s["n"]:
        return "no trades"
    dd = f"DD {s['dd_pct']:.0f}% of net" if s["net"] > 0 else f"net loss ${-s['net']:,.0f}"
    return f"{s['tpd']:.2f}/d {s['wr']:.0f}% PF {s['pf']:.2f} ${s['exp']:+.0f}/tr {dd}"
