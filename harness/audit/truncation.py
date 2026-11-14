"""Dynamic truncation audit (SPEC 14.3): the decisive lookahead test, independent of how code is written.

For each chosen bar t the data is cut at t, every signal-layer value is recomputed from scratch, and
the values at t are compared with the full-data run.  Any difference proves a value at t depends on
data after t.  The auditor never looks at performance.
"""
import copy

import numpy as np

from genome import compile_py
from genome.dsl import Ctx

FIELDS = ("sigL", "sigS", "epxL", "epxS", "stpL", "stpS", "tgtL", "tgtS", "exL", "exS")
TOL = 1e-9


def truncate(b, t):
    """Bars as they would exist if the data ended at the close of bar t."""
    s = copy.copy(b)
    for k in ("ts", "date", "sess", "slot", "o", "h", "l", "c", "v", "first", "last", "mopen", "mclose", "edge10", "partial", "filler"):
        setattr(s, k, getattr(b, k)[: t + 1].copy())
    s.n = t + 1
    s.last = s.last.copy()
    s.last[-1] = True
    s.key = f"{b.key}|trunc{t}"
    return s


def _values(g, b, other, ext_provider, exprs):
    oth = {k: v[: b.n] for k, v in other.items()} if other is not None else None
    ctx = Ctx(b, other=oth, ext=ext_provider(b) if ext_provider else {})
    plan, aux = compile_py.to_plan(g, ctx, exprs)
    out = {k: getattr(plan, k) for k in FIELDS}
    out.update({"validL": aux["validL"], "validS": aux["validS"]})
    for slot, i, aid, side, cond in exprs["parts"]:
        out[f"{slot}[{i}].{aid}.{side}"] = ctx.ev(cond)
    return out


def _same(a, b):
    if isinstance(a, (bool, np.bool_)):
        return bool(a) == bool(b)
    if np.isnan(a) and np.isnan(b):
        return True
    if np.isnan(a) or np.isnan(b):
        return False
    return abs(a - b) <= TOL * max(1.0, abs(a))


def choose_bars(b, n, seed, htf_multiples=(4, 12), warmup=600):
    """Random bars stratified across sessions and times of day, plus the last bar of higher-timeframe
    periods and the bar before it, where higher-timeframe leaks appear."""
    rng = np.random.default_rng(seed)
    idx = np.arange(warmup, b.n - 1)
    pick = set(rng.choice(idx, min(n, len(idx)), replace=False).tolist())
    cnt = np.zeros(b.n, np.int64)
    c = 0
    for i in range(b.n):
        c = 1 if b.first[i] else c + 1
        cnt[i] = c
    for k in htf_multiples:
        conf = np.flatnonzero((cnt % k == 0) & (np.arange(b.n) >= warmup))
        for t in rng.choice(conf, min(max(4, n // 20), len(conf)), replace=False):
            pick.add(int(t))
            pick.add(int(t) - 1)
    ends = np.flatnonzero(b.last & (np.arange(b.n) >= warmup))
    for t in rng.choice(ends, min(max(4, n // 20), len(ends)), replace=False):
        pick.add(int(t))
        pick.add(int(t) - 1)
    return sorted(pick)


def audit(g, b, other=None, ext_provider=None, n=300, seed=0, bars_idx=None):
    """Returns {'clean': bool, 'bars_checked': n, 'first_divergence': {...} or None, 'mismatches': count}."""
    exprs = compile_py.build(g)
    full = _values(g, b, other, ext_provider, exprs)
    idx = bars_idx if bars_idx is not None else choose_bars(b, n, seed)
    first = None
    mism = 0
    for t in idx:
        cut = _values(g, truncate(b, t), other, ext_provider, exprs)
        for name in full:
            if not _same(full[name][t], cut[name][t]):
                mism += 1
                if first is None:
                    first = {"feature": name, "bar": int(t), "session": int(b.sess[t]), "slot": int(b.slot[t]),
                             "full_value": float(full[name][t]), "truncated_value": float(cut[name][t])}
    return {"clean": mism == 0, "bars_checked": len(idx), "mismatches": mism, "first_divergence": first}


def audit_expr(node, b, other=None, ext_provider=None, n=40, seed=0):
    """Truncation audit of a single expression (atom admission, SPEC 8.4)."""
    def val(bb):
        oth = {k: v[: bb.n] for k, v in other.items()} if other is not None else None
        return Ctx(bb, other=oth, ext=ext_provider(bb) if ext_provider else {}).ev(node)
    full = val(b)
    for t in choose_bars(b, n, seed, warmup=min(600, b.n // 3)):
        if not _same(full[t], val(truncate(b, t))[t]):
            return {"clean": False, "bar": int(t)}
    return {"clean": True}
