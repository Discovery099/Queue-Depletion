"""Decoy markets (SPEC 15.3): synthetic price files with the research data's schema, session structure,
volatility clustering and intraday volume shape, but no exploitable directional structure.

Three types, generated deterministically from (type, index) so nothing large needs to be stored:
  bootstrap : real research sessions in random order, each bar's return sign-randomised (the same
              flip for ES and YM on a given bar, so the two stay correlated bar by bar while any
              lead-lag or directional pattern is destroyed);
  phase     : returns with the same spectrum and volatility envelope, Fourier phases scrambled
              independently per instrument;
  model     : simulated from a GARCH(1,1) with intraday seasonality fitted on research data, zero
              conditional mean, fat-tailed shocks.
All inputs are Research-block data only.  These are not new markets and are never described as such.
"""
import functools

import numpy as np
import pandas as pd

from .data import INSTRUMENTS, load_frame, spec

TYPES = ("bootstrap", "phase", "model")
N_PER_TYPE = 20


def _logparts(df):
    """Per-bar log moves relative to the previous close: open, high, low, close."""
    c = df["close"].values
    pc = np.r_[df["open"].values[0], c[:-1]]
    return (np.log(df["open"].values / pc), np.log(df["high"].values / pc),
            np.log(df["low"].values / pc), np.log(c / pc), pc[0])


def _assemble(src, lo, lh, ll, lc, p0, tick, order=None):
    """Rebuild a price frame from log moves.  `order` re-orders whole sessions."""
    out = src.copy()
    if order is not None:
        sess = src["sess"].values
        starts = np.flatnonzero(np.r_[True, sess[1:] != sess[:-1]])
        ends = np.r_[starts[1:], len(src)]
        idx = np.concatenate([np.arange(starts[k], ends[k]) for k in order])
        lens = (ends - starts)[order]
        out = src.iloc[idx].reset_index(drop=True)
        lo, lh, ll, lc = lo[idx], lh[idx], ll[idx], lc[idx]
        uniq = src["sess"].values[starts]
        dates = src["date"].values[starts]
        out["sess"] = np.repeat(uniq, lens).astype(np.int32)           # k-th session keeps the k-th calendar slot
        out["date"] = np.repeat(dates, lens).astype(np.int32)
        base = src["ts_utc_ns"].values[starts] - src["slot"].values[starts].astype(np.int64) * 300_000_000_000
        out["ts_utc_ns"] = np.repeat(base, lens) + out["slot"].values.astype(np.int64) * 300_000_000_000
    cum = np.cumsum(lc)
    pc = p0 * np.exp(np.r_[0.0, cum[:-1]])
    o, h, l, c = pc * np.exp(lo), pc * np.exp(lh), pc * np.exp(ll), pc * np.exp(lc)
    r = lambda x: np.round(x / tick) * tick   # noqa: E731
    o, c = r(o), r(c)
    out["open"], out["close"] = o, c
    out["high"] = np.maximum(r(h), np.maximum(o, c))
    out["low"] = np.minimum(r(l), np.minimum(o, c))
    return out


def _bootstrap(i):
    rng = np.random.default_rng([4242, 1, i])
    ref = load_frame("ES")
    n_sess = ref["sess"].nunique()
    order = rng.permutation(n_sess)
    flips = {}
    out = {}
    for sym in INSTRUMENTS:
        df = load_frame(sym)
        lo, lh, ll, lc, p0 = _logparts(df)
        key = df["sess"].values.astype(np.int64) * 1000 + df["slot"].values
        u = np.unique(key)
        if not flips:
            allk = np.unique(np.concatenate([load_frame(s)["sess"].values.astype(np.int64) * 1000 + load_frame(s)["slot"].values
                                             for s in INSTRUMENTS]))
            flips = dict(zip(allk.tolist(), (rng.random(len(allk)) < 0.5).tolist()))
        f = np.array([flips[k] for k in key.tolist()])
        lo2, lc2 = np.where(f, -lo, lo), np.where(f, -lc, lc)
        lh2, ll2 = np.where(f, -ll, lh), np.where(f, -lh, ll)
        sess = df["sess"].values
        starts = np.flatnonzero(np.r_[True, sess[1:] != sess[:-1]])
        o = order if len(starts) == n_sess else rng.permutation(len(starts))
        out[sym] = _assemble(df, lo2, lh2, ll2, lc2, p0, spec(sym)["tick"], o)
    return out


def _envelope(df, lc):
    """Volatility envelope: intraday seasonal scale times a slow EWMA of absolute returns."""
    slot = df["slot"].values
    a = np.abs(lc)
    seas = pd.Series(a).groupby(slot).transform("median").values
    seas = np.where(seas > 0, seas, np.median(a[a > 0]))
    x = a / seas
    slow = pd.Series(x).ewm(span=390, adjust=False).mean().values
    return np.maximum(seas * np.maximum(slow, 0.2), 1e-7)


def _wicks(lo, lh, ll, lc):
    top = np.maximum(lo, lc)
    bot = np.minimum(lo, lc)
    return np.maximum(lh - top, 0.0), np.maximum(bot - ll, 0.0)


def _from_returns(df, lc_new, lo_gap, uw, lw, p0, tick):
    lo = lo_gap
    top, bot = np.maximum(lo, lc_new), np.minimum(lo, lc_new)
    return _assemble(df, lo, top + uw, bot - lw, lc_new, p0, tick)


def _phase(i):
    out = {}
    for j, sym in enumerate(INSTRUMENTS):
        rng = np.random.default_rng([4242, 2, i, j])
        df = load_frame(sym)
        lo, lh, ll, lc, p0 = _logparts(df)
        env = _envelope(df, lc)
        z = lc / env
        f = np.fft.rfft(z - z.mean())
        ph = rng.uniform(0, 2 * np.pi, len(f))
        ph[0] = 0.0
        z2 = np.fft.irfft(np.abs(f) * np.exp(1j * ph), n=len(z))
        uw, lw = _wicks(lo, lh, ll, lc)
        perm = rng.permutation(len(lc))
        scale = env / env[perm]
        first = df["slot"].values == 0
        gap = np.where(first, lo, 0.0) * rng.choice(np.array([-1.0, 1.0]), len(lc))
        out[sym] = _from_returns(df, z2 * env, gap * 0.0, uw[perm] * scale, lw[perm] * scale, p0, spec(sym)["tick"])
    return out


@functools.lru_cache(maxsize=4)
def _garch_fit(sym):
    df = load_frame(sym)
    _, _, _, lc, _ = _logparts(df)
    slot = df["slot"].values
    seas = pd.Series(np.abs(lc)).groupby(slot).transform("median").values
    seas = np.where(seas > 0, seas, np.median(np.abs(lc)[np.abs(lc) > 0]))
    e = lc / seas
    var = float(np.var(e))
    best = None
    for alpha in (0.03, 0.05, 0.08, 0.12):
        for beta in (0.85, 0.90, 0.94):
            if alpha + beta >= 0.999:
                continue
            omega = var * (1 - alpha - beta)
            s2 = np.empty(len(e))
            s2[0] = var
            for t in range(1, len(e)):
                s2[t] = omega + alpha * e[t - 1] ** 2 + beta * s2[t - 1]
            ll = -0.5 * np.sum(np.log(s2) + e * e / s2)
            if best is None or ll > best[0]:
                best = (ll, omega, alpha, beta)
    return {"omega": best[1], "alpha": best[2], "beta": best[3], "var": var}


def _model(i):
    out = {}
    for j, sym in enumerate(INSTRUMENTS):
        rng = np.random.default_rng([4242, 3, i, j])
        df = load_frame(sym)
        lo, lh, ll, lc, p0 = _logparts(df)
        g = _garch_fit(sym)
        slot = df["slot"].values
        seas = pd.Series(np.abs(lc)).groupby(slot).transform("median").values
        seas = np.where(seas > 0, seas, np.median(np.abs(lc)[np.abs(lc) > 0]))
        n = len(lc)
        shocks = rng.standard_t(5, n) / np.sqrt(5.0 / 3.0)
        e = np.empty(n)
        s2 = g["var"]
        for t in range(n):
            e[t] = np.sqrt(s2) * shocks[t]
            s2 = g["omega"] + g["alpha"] * e[t] ** 2 + g["beta"] * s2
        r = e * seas
        uw, lw = _wicks(lo, lh, ll, lc)
        perm = rng.permutation(n)
        scale = np.abs(r) / np.maximum(np.abs(lc[perm]), 1e-7)
        scale = np.clip(scale, 0.2, 5.0)
        out[sym] = _from_returns(df, r, np.zeros(n), uw[perm] * scale, lw[perm] * scale, p0, spec(sym)["tick"])
    return out


@functools.lru_cache(maxsize=6)
def decoy(kind, i):
    """Frames {ES: df, YM: df} for decoy number i of a type."""
    assert kind in TYPES and 0 <= i < N_PER_TYPE
    return {"bootstrap": _bootstrap, "phase": _phase, "model": _model}[kind](i)


def sample(n, seed):
    """n distinct (type, index) pairs, deterministic for a seed (stage 2 runs each candidate on 30)."""
    rng = np.random.default_rng([777, seed])
    allp = [(k, i) for k in TYPES for i in range(N_PER_TYPE)]
    return [allp[j] for j in rng.permutation(len(allp))[:n]]
