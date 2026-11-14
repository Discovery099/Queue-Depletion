"""Evaluator (SPEC 17.4): plain code that runs backtests exactly as configured.

Search-stage code sees only the search sessions of the Research block: the bars of the inner
holdout are cut off before any feature is computed (SPEC 5.4), and nothing here can open the vault.
"""
import functools
import math

import numpy as np
import pandas as pd
import yaml

from engine import path, read_json
from engine import metrics as M
from engine import sim
from engine.data import (INSTRUMENTS, fold_bounds, frame_to_bars, inner_holdout_bounds, load_frame, partition)
from genome import compile_py
from genome.dsl import Ctx

COSTS = read_json(path("config/costs.lock.json"))["levels"]
GATES = yaml.safe_load(open(path("config/gates.yaml")))
SEARCH = yaml.safe_load(open(path("config/search.yaml")))
TV = {s: partition()["instruments"][s]["tick_value"] for s in INSTRUMENTS}
N_SEARCH = partition()["research"]["search_sessions"]
FOLDS = fold_bounds(SEARCH["walk_forward_folds"])
PURGE = SEARCH["purge_sessions"]
TEST_FOLDS = (3, 4, 5, 6, 7, 8)
ISLAND_FOLDS = {"A": (3, 5, 7), "B": (4, 6, 8), "ALL": TEST_FOLDS}
EXT_PROVIDER = None        # set by audit.canary: supplies store-only series (canaries, honeypot)
FRAME_OVERRIDE = {}        # {(sym): frame} used by decoy markets and stress data


def fold_of_session():
    f = np.zeros(N_SEARCH, np.int16)
    for k, (lo, hi) in enumerate(FOLDS, 1):
        f[lo:hi] = k
    return f


FOLD_OF = fold_of_session()


def _frame(sym, scope):
    df = FRAME_OVERRIDE[sym] if sym in FRAME_OVERRIDE else load_frame(sym)
    if scope == "search":
        return df[df["sess"] < N_SEARCH]
    if scope == "holdout":          # stage 4 only: features warm up on the search sessions, scored on the holdout
        return df
    raise ValueError(scope)


@functools.lru_cache(maxsize=48)
def bars_for(sym, tf, offset=0, scope="search"):
    return frame_to_bars(_frame(sym, scope), sym, tf, offset)


def set_frames(frames=None):
    """Swap the market under evaluation (decoy markets, stress series).  None restores the research data."""
    FRAME_OVERRIDE.clear()
    if frames:
        FRAME_OVERRIDE.update(frames)
    clear_caches()


def other_arrays(b, o):
    idx = pd.Index(o.ts).get_indexer(b.ts)
    ok = idx >= 0
    j = np.maximum(idx, 0)
    return {k: np.where(ok, a[j], np.nan) for k, a in (("close", o.c), ("high", o.h), ("low", o.l), ("volume", o.v))}


_CTX = {}


def ctx_for(sym, tf, offset=0, scope="search"):
    key = (sym, tf, offset, scope)
    c = _CTX.get(key)
    if c is None:
        if len(_CTX) > 12:
            _CTX.clear()
        b = bars_for(sym, tf, offset, scope)
        ob = bars_for("YM" if sym == "ES" else "ES", tf, offset, scope)
        c = Ctx(b, other=other_arrays(b, ob), ext=EXT_PROVIDER(b) if EXT_PROVIDER else {})
        _CTX[key] = c
    if len(c.cache) > 500:          # bound memory: the cache is an optimisation only
        c.cache.clear()
    return c


def clear_caches():
    _CTX.clear()
    bars_for.cache_clear()
    regime_cells.cache_clear()


@functools.lru_cache(maxsize=8)
def regime_cells(sym):
    """Scheme C labels (SPEC 5.3): for each session, the realised-volatility tercile and the trend sign
    over the PRIOR 20 sessions, using only data before the session.  Terciles are expanding ranks, so
    the label of a session never depends on later sessions.  Cell = tercile * 2 + (trend up)."""
    b = bars_for(sym, 5)
    close = pd.Series(b.c[b.last], index=b.sess[b.last])
    r = np.log(close).diff()
    vol = r.rolling(20).std().shift(1)
    trend = (close.shift(1) - close.shift(21))
    rank = vol.expanding(min_periods=60).apply(lambda x: (x[:-1] <= x[-1]).mean() if len(x) > 1 else np.nan, raw=True)
    cell = np.full(N_SEARCH, -1, np.int16)
    ok = rank.notna() & trend.notna()
    t = np.where(rank < 1 / 3, 0, np.where(rank < 2 / 3, 1, 2))
    cell[close.index[ok]] = (t * 2 + (trend > 0).astype(int))[ok.values]
    return cell


def run(g, sym, tf, cost="base", offset=0, scope="search", optimistic=False, fill_at_close=False,
        loss_standdown=None, transform=None, generation=-1):
    """One backtest of a genome on one instrument.  Returns a dict with trades, equity and the plan."""
    ctx = ctx_for(sym, tf, offset, scope)
    b = ctx.b
    plan, aux = compile_py.to_plan(g, ctx)
    if transform:
        plan = transform(plan, b)
    T, eq, inpos, liq = sim.run(b, plan, COSTS[cost], optimistic=optimistic, fill_at_close=fill_at_close,
                                loss_standdown=loss_standdown)
    fo = FOLD_OF if scope == "search" else np.r_[FOLD_OF, np.full(partition()["research"]["sessions"] - N_SEARCH, 9, np.int16)]
    rc = regime_cells(sym) if scope == "search" else None
    df = M.trades_frame(T, b, generation, fo, rc, g["slots"]["entry"]["type"])
    return {"trades": df, "T": T, "eq": eq, "inpos": inpos, "liq_miss": int(liq), "plan": plan, "aux": aux, "bars": b}


# ------------------------------------------------------------------ twins (SPEC 11.4)
def subset(b, mask):
    """A copy of Bars restricted to whole sessions selected by `mask` (bars of complete sessions)."""
    import copy
    s = copy.copy(b)
    for k in ("ts", "date", "sess", "slot", "o", "h", "l", "c", "v", "first", "last", "mopen", "mclose", "edge10", "partial", "filler"):
        setattr(s, k, getattr(b, k)[mask])
    s.n = int(mask.sum())
    return s


def subset_plan(p, mask):
    q = p.copy()
    for k, v in p.__dict__.items():
        if isinstance(v, np.ndarray):
            setattr(q, k, v[mask])
    return q


def twin_runs(r, sess_mask, n, seed, cost="base"):
    """Random-entry twins for one instrument's run `r`, restricted to bars in `sess_mask`.

    Identical direction mix, order type, stop, target, exit and time rules, costs and sequencing;
    entry times are random, matched to the candidate's time-of-day distribution and long/short mix,
    drawn from bars where the candidate was flat and the structural limits allow an entry.
    Returns arrays (n twins): wins, trades, sum of net/cost, gross profit, gross loss."""
    b, plan, aux = r["bars"], r["plan"], r["aux"]
    sb, sp = subset(b, sess_mask), subset_plan(r["plan"], sess_mask)
    pos = np.cumsum(sess_mask) - 1
    T = r["T"]
    keep = sess_mask[T[:, sim.C["sig_idx"]].astype(np.int64)] if len(T) else np.zeros(0, bool)
    sig = pos[T[keep, sim.C["sig_idx"]].astype(np.int64)]
    dr = T[keep, sim.C["dir"]]
    slot = sb.slot
    flat = ~r["inpos"][sess_mask] & ~sb.last
    pools, counts = {}, {}
    for d_, valid in ((1, aux["validL"][sess_mask]), (-1, aux["validS"][sess_mask])):
        ok = flat & valid
        s_sel = slot[sig[dr == d_]]
        for sl, c in zip(*np.unique(s_sel, return_counts=True)):
            pools[(d_, sl)] = np.flatnonzero(ok & (slot == sl))
            counts[(d_, sl)] = int(c)
    rng = np.random.default_rng(seed)
    comm = 2.0 * COSTS[cost]["commission_per_side_usd"] / b.pv
    rt = M.RT_COST_USD[b.sym] / b.pv
    out = np.zeros((n, 5))
    base = sp.copy()
    for i in range(n):
        L = np.zeros(sb.n, np.bool_)
        S = np.zeros(sb.n, np.bool_)
        for (d_, sl), pool in pools.items():
            c = min(counts[(d_, sl)], len(pool))
            if c:
                pick = rng.choice(pool, c, replace=False)
                (L if d_ == 1 else S)[pick] = True
        base.sigL, base.sigS = L, S
        Tt, _, _, _ = sim.run(sb, base, COSTS[cost])
        if len(Tt):
            net = Tt[:, sim.C["net_pts"]]
            w = Tt[:, sim.C["is_win"]] > 0
            out[i] = (w.sum(), len(Tt), (net / rt).sum(), net[w].sum() * b.pv, -net[~w].sum() * b.pv)
    return out


def random_exit_twin(r, sess_mask, cost="base"):
    """The candidate's entries with every exit replaced by a symmetric 1 ATR stop and target."""
    b, aux = r["bars"], r["aux"]
    p = r["plan"].copy()
    a = aux["atr"]
    p.stpL, p.tgtL = np.round((aux["refL"] - a) / b.tick) * b.tick, np.round((aux["refL"] + a) / b.tick) * b.tick
    p.stpS, p.tgtS = np.round((aux["refS"] + a) / b.tick) * b.tick, np.round((aux["refS"] - a) / b.tick) * b.tick
    p.exL[:] = False
    p.exS[:] = False
    p.time_stop_bars, p.be_R, p.trail_start_R, p.trail_R, p.part_R = 0, 0.0, 0.0, 0.0, 0.0
    T, _, _, _ = sim.run(subset(b, sess_mask), subset_plan(p, sess_mask), COSTS[cost])
    return (int((T[:, sim.C["is_win"]] > 0).sum()), len(T)) if len(T) else (0, 0)


def sessions_mask(b, folds):
    return np.isin(FOLD_OF[b.sess], folds)


def fold_sessions(folds):
    return np.flatnonzero(np.isin(FOLD_OF, folds))
