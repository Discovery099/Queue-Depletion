"""Research data access and session-anchored resampling (SPEC 4.2, 5, 13.1).

Research code may load only data/research (and synthetic decoys).  Any attempt to
load a path under data/vault raises.  The Vault Keeper has its own loader.
"""
import functools
import os

import numpy as np
import pandas as pd

from . import path, read_json

INSTRUMENTS = ("ES", "YM")
CORE_TFS = (5, 10, 15, 30, 60)
HIDDEN_TFS = (20, 25, 35, 45, 65, 90, 130)


@functools.lru_cache(maxsize=None)
def partition():
    return read_json(path("config/partition.lock.json"))


def spec(sym):
    return partition()["instruments"][sym]


class Bars:
    """Column arrays for one instrument at one timeframe.  All arrays are aligned to bar close."""
    __slots__ = ("sym", "tf", "offset", "n", "ts", "date", "sess", "slot", "o", "h", "l", "c", "v",
                 "first", "last", "mopen", "mclose", "edge10", "partial", "filler", "tick", "pv", "tick_value",
                 "sess_start", "sess_end", "key")

    def session_ids(self):
        return self.sess[self.first]

    def mask_sessions(self, lo, hi):
        """Boolean mask of bars whose session index is in [lo, hi)."""
        return (self.sess >= lo) & (self.sess < hi)


def _check_research_path(p):
    rp = os.path.realpath(p)
    ok = (os.path.realpath(path("data/research")), os.path.realpath(path("data/decoys")))
    if not rp.startswith(ok):
        raise PermissionError(f"research code may not read {p} (Constitution Article 2)")


@functools.lru_cache(maxsize=8)
def load_frame(sym):
    p = path("data/research", f"{sym}.parquet")
    _check_research_path(p)
    return pd.read_parquet(p)


def frame_to_bars(df, sym, tf=5, offset=0, tick=None, pv=None):
    """Build Bars from a 5-minute frame.  tf must be a multiple of 5.

    Resampling is anchored to the 09:30 session open and never crosses a session
    boundary.  `offset` (in 5-minute bars) shifts the anchor for the bar-alignment
    test (SPEC 13.4): bars before the anchor form one leading partial bar.
    A final partial bar on short sessions is kept and flagged.
    """
    k = tf // 5
    assert tf % 5 == 0 and k >= 1 and 0 <= offset < k
    sess = df["sess"].values.astype(np.int64)
    slot = df["slot"].values.astype(np.int64)
    grp = np.where(slot >= offset, (slot - offset) // k + 1, 0)
    gid = sess * 1000 + grp
    start = np.r_[True, gid[1:] != gid[:-1]]
    idx = np.flatnonzero(start)
    end = np.r_[idx[1:], len(df)] - 1
    b = Bars()
    b.sym, b.tf, b.offset = sym, tf, offset
    b.n = len(idx)
    b.ts = df["ts_utc_ns"].values[idx]
    b.date = df["date"].values[idx].astype(np.int32)
    b.sess = sess[idx].astype(np.int32)
    b.slot = slot[idx].astype(np.int32)
    b.o = df["open"].values[idx].astype(np.float64)
    b.c = df["close"].values[end].astype(np.float64)
    b.h = np.maximum.reduceat(df["high"].values.astype(np.float64), idx)
    b.l = np.minimum.reduceat(df["low"].values.astype(np.float64), idx)
    b.v = np.add.reduceat(df["volume"].values.astype(np.float64), idx)
    b.filler = np.minimum.reduceat(df["filler"].values.astype(np.int8), idx).astype(np.bool_)  # all members filler
    b.first = np.r_[True, b.sess[1:] != b.sess[:-1]]
    b.last = np.r_[b.sess[1:] != b.sess[:-1], True]
    b.mopen = (b.slot * 5).astype(np.int32)
    b.mclose = ((slot[end] + 1) * 5).astype(np.int32)
    nb = end - idx + 1
    b.partial = (nb < k) | ((b.mclose - b.mopen) != tf)
    # session bounds and first/last 10 minutes flag (shock cost level)
    sstart = np.flatnonzero(b.first)
    send = np.flatnonzero(b.last)
    b.sess_start = np.repeat(sstart, send - sstart + 1).astype(np.int64)
    b.sess_end = np.repeat(send, send - sstart + 1).astype(np.int64)
    sess_len = b.mclose[b.sess_end]
    b.edge10 = (b.mopen < 10) | (b.mclose > sess_len - 10)
    s = spec(sym) if tick is None else {"tick": tick, "point_value": pv, "tick_value": tick * pv}
    b.tick, b.pv, b.tick_value = float(s["tick"]), float(s["point_value"]), float(s["tick_value"])
    b.key = f"{sym}|{tf}|{offset}|{b.n}|{float(b.c.sum()):.6f}"
    return b


@functools.lru_cache(maxsize=64)
def research_bars(sym, tf=5, offset=0):
    return frame_to_bars(load_frame(sym), sym, tf, offset)


def fold_bounds(n_folds=8):
    """Walk-forward folds over the search sessions (Research minus inner holdout).

    Returns a list of (lo, hi) session-index ranges; fold k is index k-1."""
    n = partition()["research"]["search_sessions"]
    edges = np.linspace(0, n, n_folds + 1).round().astype(int)
    return [(int(edges[i]), int(edges[i + 1])) for i in range(n_folds)]


def inner_holdout_bounds():
    r = partition()["research"]
    return (r["search_sessions"], r["sessions"])


def cpcv_groups(n_groups=10):
    n = partition()["research"]["search_sessions"]
    edges = np.linspace(0, n, n_groups + 1).round().astype(int)
    return [(int(edges[i]), int(edges[i + 1])) for i in range(n_groups)]
