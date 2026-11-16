"""Published intraday rules on the harness simulator.  Every input at bar t uses bars <= t only."""
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(ROOT), "quorum"))
from qr.common import SYMS, bars, F, S, COSTS, fold_of_session, N_SEARCH   # noqa: E402

WIDE = 10.0


def session_frame(b):
    """Per-bar session quantities: session open, previous session close, running VWAP, ATR."""
    so = b.o[b.sess_start]
    last_close = b.c[b.sess_end]
    sid = np.cumsum(b.first) - 1
    closes = b.c[np.flatnonzero(b.last)]
    prev_close = np.r_[np.nan, closes[:-1]][sid]
    hlc3 = (b.h + b.l + b.c) / 3.0
    vwap = F.sess_cumsum(hlc3 * b.v, b.first) / np.maximum(F.sess_cumsum(b.v, b.first), 1e-9)
    return so, prev_close, vwap, F.atr(b.h, b.l, b.c, 14), sid


def noise_sigma(b, so, sid, lookback):
    """Average absolute move from the open at this time of day over the previous `lookback` sessions."""
    move = np.abs(b.c / so - 1.0)
    df = pd.DataFrame({"s": sid, "m": b.mclose, "v": move})
    pv = df.pivot_table(index="s", columns="m", values="v", aggfunc="last")
    sig = pv.rolling(lookback, min_periods=lookback).mean().shift(1)
    return sig.stack(future_stack=True).reindex(pd.MultiIndex.from_arrays([sid, b.mclose])).values


def rt(b, x):
    return np.round(x / b.tick) * b.tick


def plan_s1(b, lookback=14, vm=1.0, interval=30, stop_atr=WIDE, use_vwap=True, max_trades=1000, last_entry=390,
            first_check=30):
    so, pc, vwap, atr, sid = session_frame(b)
    sig = noise_sigma(b, so, sid, lookback)
    ub = np.fmax(so, pc) * (1.0 + vm * sig)
    lb = np.fmin(so, pc) * (1.0 - vm * sig)
    ok = ~np.isnan(sig) & ~np.isnan(atr) & ~np.isnan(pc)
    chk = (b.mclose % interval == 0) & (b.mclose >= first_check) & ~b.last & ok
    p = S.Plan(b.n)
    p.sigL = chk & (b.c > ub) & (b.mclose <= last_entry)
    p.sigS = chk & (b.c < lb) & (b.mclose <= last_entry)
    xl = np.fmax(ub, vwap) if use_vwap else ub
    xs = np.fmin(lb, vwap) if use_vwap else lb
    p.exL = chk & (b.c < xl)
    p.exS = chk & (b.c > xs)
    p.stpL, p.stpS = rt(b, b.c - stop_atr * atr), rt(b, b.c + stop_atr * atr)
    p.cooldown_bars, p.max_trades, p.loss_standdown = 0, max_trades, 0
    return p, dict(ub=ub, lb=lb, vwap=vwap)


def plan_s2(b):
    so, pc, vwap, atr, sid = session_frame(b)
    c10 = np.where(b.mclose == 30, b.c, np.nan)
    c10 = pd.Series(c10).groupby(sid).ffill().values          # value known from 10:00 on, within the session
    r = c10 / pc - 1.0
    at = (b.mclose == 360) & ~b.last & ~np.isnan(r) & ~np.isnan(atr)
    p = S.Plan(b.n)
    p.sigL, p.sigS = at & (r > 0), at & (r < 0)
    p.stpL, p.stpS = rt(b, b.c - WIDE * atr), rt(b, b.c + WIDE * atr)
    p.cooldown_bars, p.max_trades, p.loss_standdown = 0, 1000, 0
    return p, {}


def plan_s3(b, target_r=10.0):
    at = b.first & ~b.last
    rng = b.h - b.l
    p = S.Plan(b.n)
    p.sigL, p.sigS = at & (b.c > b.o), at & (b.c < b.o)
    p.stpL, p.stpS = rt(b, b.l - b.tick), rt(b, b.h + b.tick)
    p.tgtL, p.tgtS = rt(b, b.c + target_r * (b.c - b.l)), rt(b, b.c - target_r * (b.h - b.c))
    p.sigL &= (b.c - b.l) > 2 * b.tick
    p.sigS &= (b.h - b.c) > 2 * b.tick
    p.cooldown_bars, p.max_trades, p.loss_standdown = 0, 1000, 0
    return p, {}


def trades(plan_fn, tf=5, block="search", level="base", syms=SYMS, **kw):
    """Run on both instruments; returns a DataFrame of trades (1 contract each)."""
    out = []
    for sym in syms:
        b = bars(sym, tf, block)
        p, _ = plan_fn(b, **kw)
        T = S.run(b, p, COSTS[level])[0]
        if not len(T):
            continue
        ei = T[:, 1].astype(np.int64)
        out.append(pd.DataFrame({"sym": sym, "sess": b.sess[ei], "date": b.date[ei], "ts": b.ts[ei], "mopen": b.mopen[ei],
                                 "dir": T[:, 3], "entry": T[:, 4], "exit": T[:, 5], "reason": T[:, 8], "bars": T[:, 15],
                                 "net": T[:, 13] * b.pv, "win": T[:, 17] > 0}))
    df = pd.concat(out, ignore_index=True) if out else pd.DataFrame(columns=["sym", "sess", "date", "ts", "net", "win"])
    df["fold"] = fold_of_session(df["sess"].values)
    return df


def summ(df, nsess):
    n = len(df)
    if n == 0:
        return dict(n=0, tpd=0, wr=np.nan, pf=np.nan, net=0, exp=0, dd=0, dd_pct=np.nan, payoff=np.nan)
    d = df.sort_values("ts")
    net = d["net"].values
    eq = np.r_[0.0, np.cumsum(net)]
    dd = float((np.maximum.accumulate(eq) - eq).max())
    gp, gl = net[net > 0].sum(), -net[net < 0].sum()
    w = d["win"].values
    return dict(n=n, tpd=n / nsess, wr=100 * w.mean(), pf=gp / gl if gl > 0 else np.inf, net=float(net.sum()), exp=float(net.mean()),
                dd=dd, dd_pct=100 * dd / net.sum() if net.sum() > 0 else np.nan,
                payoff=float(net[w].mean() / -net[~w].mean()) if w.any() and (~w).any() else np.nan)


def line(s):
    if not s["n"]:
        return "no trades"
    dd = f"DD {s['dd_pct']:.0f}% of net" if s["net"] > 0 else "net loss"
    return f"{s['n']:5d} tr {s['tpd']:.2f}/d win {s['wr']:.0f}% PF {s['pf']:.2f} ${s['exp']:+.0f}/tr net ${s['net']:+,.0f} {dd} payoff {s['payoff']:.2f}"
