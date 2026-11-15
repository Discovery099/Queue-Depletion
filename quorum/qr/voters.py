"""Voters: every portable trigger technique in the library catalogue, as a stream of buy/sell events.

Portable = written in bars and ATR units with no session-anchored input (no session VWAP, opening range,
prior-day level, clock time, companion instrument), so the same rule runs on any chart, day or overnight.
"""
import os
import re

import numpy as np

from .common import ROOT, SYMS, bars
from . import lc

from library.atoms import catalog as CAT          # noqa: E402  (harness on sys.path via common)
from genome.dsl import Ctx                         # noqa: E402

SESSION_OPS = re.compile(r"scumsum|scummax|scummin|sfirst|prevlast|frozen|mso|htf|first|scount|dow|roundlvl|ext|other|mtc")
EXCLUDE = {"tr_round_number_reject"}


def _keystr(e):
    return str(e.key()).lower()


def portable_atoms():
    out = []
    for a in CAT.ATOMS.values():
        if a.typ != "TRIGGER" or a.id in EXCLUDE or a.fam in ("open", "close", "intermarket"):
            continue
        ex = a.build()
        if SESSION_OPS.search(_keystr(ex["long"])) or SESSION_OPS.search(_keystr(ex["short"])):
            continue
        out.append(a)
    return out


def variants(a):
    """Default parameters plus, for the first numeric grid, one faster and one slower setting."""
    v = [("", dict(a.default))]
    for k, g in a.grid.items():
        if len(g) >= 3 and all(isinstance(x, (int, float)) for x in g):
            i = g.index(a.default[k])
            if i - 1 >= 0:
                v.append((f"[{k}={g[i - 1]}]", {**a.default, k: g[i - 1]}))
            if i + 1 < len(g):
                v.append((f"[{k}={g[i + 1]}]", {**a.default, k: g[i + 1]}))
            break
    return v


def build(sym, tf, block="search", with_variants=True):
    """Returns (names, families, EV int8 (V, n)).  Cached on disk."""
    fn = os.path.join(ROOT, "cache", f"voters_{sym}_{tf}_{block}_{int(with_variants)}.npz")
    if os.path.exists(fn):
        z = np.load(fn, allow_pickle=True)
        return list(z["names"]), list(z["fams"]), z["EV"], list(z["ids"]), list(z["params"])
    b = bars(sym, tf, block)
    ctx = Ctx(b)
    names, fams, rows, ids, params = [], [], [], [], []
    for a in portable_atoms():
        for tag, p in (variants(a) if with_variants else [("", dict(a.default))]):
            try:
                ex = a.build(p)
                L = np.asarray(ctx.ev(ex["long"]), bool)
                Sx = np.asarray(ctx.ev(ex["short"]), bool)
            except Exception as e:           # a length too short for this timeframe disables the variant
                continue
            ev = np.zeros(b.n, np.int8)
            ev[L & ~Sx] = 1
            ev[Sx & ~L] = -1
            names.append(a.id[3:] + tag)
            fams.append(a.fam)
            rows.append(ev)
            ids.append(a.id)
            params.append(p)
    r = lc.lorentzian(b)
    for nm, L, Sx in (("lorentzian", r["lc_long"], r["lc_short"]), ("kernel_turn", r["kturn_long"], r["kturn_short"])):
        ev = np.zeros(b.n, np.int8)
        ev[L & ~Sx] = 1
        ev[Sx & ~L] = -1
        names.append(nm); fams.append("ml"); rows.append(ev); ids.append(nm); params.append({})
    EV = np.vstack(rows)
    np.savez_compressed(fn, names=np.array(names, object), fams=np.array(fams, object), EV=EV,
                        ids=np.array(ids, object), params=np.array(params, object))
    return names, fams, EV, ids, params


if __name__ == "__main__":
    import time
    for tf in (5, 10, 15, 30):
        for sym in SYMS:
            t = time.time()
            names, fams, EV, ids, params = build(sym, tf)
            ns = len(np.unique(bars(sym, tf).sess))
            print(sym, tf, EV.shape, round(time.time() - t, 1), "s; median events/day", np.median((EV != 0).sum(1) / ns).round(2))
    names, fams, EV, ids, params = build("ES", 5)
    ns = 947
    for n_, f_, r in zip(names, fams, EV):
        print(f"{n_:40s} {f_:8s} {(r != 0).sum() / ns:6.2f}")
