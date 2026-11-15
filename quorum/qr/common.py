"""Shared plumbing: bars restricted to the search sessions, splits, costs, trade statistics."""
import functools
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HARNESS = os.path.join(os.path.dirname(ROOT), "harness")
sys.path.insert(0, HARNESS)

from engine import data as D            # noqa: E402
from engine import features as F        # noqa: E402
from engine import sim as S             # noqa: E402

SYMS = ("ES", "YM")
N_SEARCH = D.partition()["research"]["search_sessions"]          # 947
FOLDS = D.fold_bounds()
COSTS = json.load(open(os.path.join(HARNESS, "config/costs.lock.json")))["levels"]
RT_USD = {"ES": 27.5, "YM": 12.5}


@functools.lru_cache(maxsize=32)
def bars(sym, tf=5, block="search"):
    """Bars for one block.  'holdout' is refused unless QUORUM_OPEN_HOLDOUT=1 (one-shot final test)."""
    df = D.load_frame(sym)
    if block == "search":
        df = df[df["sess"] < N_SEARCH]
    elif block == "holdout":
        if os.environ.get("QUORUM_OPEN_HOLDOUT") != "1":
            raise PermissionError("holdout is opened once, by qr/phase5_holdout.py")
        # keep 60 sessions of warm-up before the holdout; trades are counted from session N_SEARCH on
        df = df[df["sess"] >= N_SEARCH - 60]
    else:
        raise ValueError(block)
    return D.frame_to_bars(df.reset_index(drop=True), sym, tf)


def fold_of_session(sess):
    f = np.full(len(sess), -1, np.int32)
    for k, (lo, hi) in enumerate(FOLDS):
        f[(sess >= lo) & (sess < hi)] = k
    return f


def split_mask(b, which):
    """Boolean mask over bars: 'discover' = folds 1,3,5,7 (index 0,2,4,6); 'confirm' = folds 2,4,6,8."""
    f = fold_of_session(b.sess)
    if which == "discover":
        return (f >= 0) & (f % 2 == 0)
    if which == "confirm":
        return (f >= 0) & (f % 2 == 1)
    if which == "all":
        return np.ones(b.n, np.bool_)
    if which == "holdout":
        return b.sess >= N_SEARCH
    raise ValueError(which)


def n_sessions(b, mask):
    return len(np.unique(b.sess[mask]))


def stats(T, b, mask=None):
    """Trade statistics in USD for 1 contract.  T is the simulator's trade matrix; mask selects bars by entry."""
    if mask is not None and len(T):
        T = T[mask[T[:, 1].astype(np.int64)]]
    ns = n_sessions(b, mask if mask is not None else np.ones(b.n, np.bool_))
    n = len(T)
    if n == 0:
        return dict(n=0, tpd=0.0, wr=np.nan, pf=np.nan, exp_usd=0.0, net_usd=0.0, dd_usd=0.0, dd_pct=np.nan,
                    payoff=np.nan, sessions=ns)
    net = T[:, 13] * b.pv
    win = T[:, 17] > 0
    gp, gl = net[net > 0].sum(), -net[net < 0].sum()
    eq = np.cumsum(net)
    dd = float((np.maximum.accumulate(np.r_[0.0, eq]) - np.r_[0.0, eq]).max())
    aw = net[win].mean() if win.any() else np.nan
    al = -net[~win].mean() if (~win).any() else np.nan
    return dict(n=n, tpd=n / ns, wr=100.0 * win.mean(), pf=float(gp / gl) if gl > 0 else np.inf,
                exp_usd=float(net.mean()), net_usd=float(net.sum()), dd_usd=dd,
                dd_pct=100.0 * dd / net.sum() if net.sum() > 0 else np.nan,
                payoff=float(aw / al) if al and al > 0 else np.nan, sessions=ns)


def pool(stat_list):
    """Pool per-instrument stats dicts that carry '_net' arrays."""
    raise NotImplementedError


def atr14(b):
    return F.atr(b.h, b.l, b.c, 14)
