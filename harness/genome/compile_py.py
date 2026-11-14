"""Genome -> expressions -> simulator plan (SPEC 7.1 signal layer, 9.1, 11.2).

`build(genome)` returns expression trees only; it knows nothing about fills.  The same trees feed
the numpy evaluator here and the Pine emitter in compile_pine.py, so the two cannot drift apart.

Structural limits applied to every entry (SPEC 11.2, Article 9):
  * the stop price is fixed at the signal bar, at most 2.5 ATR and 0.6% of price from the reference
    entry price and at least 0.3 ATR from it;
  * if there is a profit target, the stop-to-target ratio is at most 2.5 and the target is at least
    three round-trip costs away; an entry that cannot meet this is not taken.
"""
import math
from types import SimpleNamespace

import numpy as np

from engine.sim import Plan, MARKET, LIMIT, STOP
from genome.dsl import C, FALSE, MINTGT, TRUE, E, any_in, maxx, minx, shift, w
from library.atoms import catalog as K
from library.atoms.catalog import ATOMS, A, D

MIN_STOP_ATR, MAX_STOP_ATR, MAX_STOP_PCT, MAX_RATIO = 0.3, 2.5, 0.006, 2.5
ETYPE = {"market": MARKET, "limit": LIMIT, "stop": STOP}


def _and(xs):
    out = None
    for x in xs:
        out = x if out is None else (out & x)
    return out if out is not None else TRUE


def _or(xs):
    out = None
    for x in xs:
        out = x if out is None else (out | x)
    return out if out is not None else FALSE


def _side(e, name):
    """Condition and level of one atom entry for a side, honouring the INVERT flag."""
    o = ATOMS[e["atom"]].build(e["params"])
    if e.get("inv"):
        name = "short" if name == "long" else "long"
    return o[name], o["lvl_" + name]


def build(g):
    """Expression trees for both sides.  Keys: sig, raw, valid, ref, stp, tgt, ex (each a dict long/short),
    parts (per-atom conditions, for audits), scalars."""
    s = g["slots"]
    ent = s["entry"]
    out = {k: {} for k in ("sig", "raw", "valid", "ref", "stp", "tgt", "ex", "dist")}
    parts = []
    for name, dv in (("long", 1), ("short", -1)):
        d = D(dv)
        lvl = None
        ctx = []
        for slot in ("regime", "location", "filter"):
            for i, e in enumerate(s[slot]):
                c, lv = _side(e, name)
                ctx.append(c)
                parts.append((slot, i, e["atom"], name, c))
                if slot == "location" and lvl is None and lv is not None:
                    lvl = lv
        trg = []
        tlvl = None
        for i, e in enumerate(s["trigger"]["atoms"]):
            c, lv = _side(e, name)
            trg.append(c)
            parts.append(("trigger", i, e["atom"], name, c))
            if tlvl is None and lv is not None:
                tlvl = lv
        lvl = tlvl if tlvl is not None else lvl
        comb = s["trigger"]["combine"]
        if len(trg) == 1:
            trigger = trg[0]
        elif comb == "AND":
            trigger = trg[0] & trg[1]
        elif comb == "OR":
            trigger = trg[0] | trg[1]
        else:   # SEQ: the first fired within the last n bars, the second fires now
            trigger = any_in(trg[0], ("b", int(s["trigger"]["within_bars"]) + 1)) & trg[1]
        raw = _and(ctx) & trigger
        if ent["type"] == "market":
            ref = C
        elif ent["type"] == "limit":
            ref = d.dn(C, ent["offset_atr"] * A)
        else:
            ref = d.up(C, ent["offset_atr"] * A)
        st = s["risk"]["stop"]
        p = SimpleNamespace(**st["params"])
        rawdist = K.stop_distance(st["atom"], p, d, ref, lvl)
        dist = minx(maxx(rawdist, MIN_STOP_ATR * A), minx(MAX_STOP_ATR * A, MAX_STOP_PCT * ref))
        stp = d.dn(ref, dist)
        valid = dist > 0
        tgt = None
        inval = []
        for e in s["exit"]:
            a = ATOMS[e["atom"]]
            pe = SimpleNamespace(**e["params"])
            if a.kind == "target":
                tgt = K.target_level(e["atom"], pe, d, ref, dist, lvl)
                td = d.sg(tgt - ref)
                valid = valid & (td >= dist / MAX_RATIO) & (td >= MINTGT)
            elif a.kind == "inval":
                inval.append(K.exit_inval(e["atom"], pe, d))
        allowed = not ((g["direction"] == "long_only" and dv < 0) or (g["direction"] == "short_only" and dv > 0))
        out["raw"][name] = raw if allowed else FALSE
        out["valid"][name] = valid
        out["sig"][name] = (raw & valid) if allowed else FALSE
        out["ref"][name], out["stp"][name], out["tgt"][name], out["dist"][name] = ref, stp, tgt, dist
        out["ex"][name] = _or(inval)
    sc = {"time_stop_minutes": 0, "be_R": 0.0, "trail_start_R": 0.0, "trail_R": 0.0, "part_R": 0.0}
    for e in s["exit"]:
        a = ATOMS[e["atom"]]
        if a.kind == "time":
            sc["time_stop_minutes"] = e["params"]["m"]
        elif a.kind == "be":
            sc["be_R"] = e["params"]["r"]
        elif a.kind == "trail":
            sc["trail_start_R"], sc["trail_R"] = e["params"]["start"], e["params"]["dist"]
        elif a.kind == "partial":
            sc["part_R"] = e["params"]["r"]
    out["scalars"] = sc
    out["parts"] = parts
    return out


def bars_for_minutes(minutes, tf, lo=1):
    return max(lo, int(math.floor(minutes / tf + 0.5)))


def to_plan(g, ctx, exprs=None):
    """Evaluate the expression trees on one instrument/timeframe and fill a simulator Plan.

    Returns (plan, aux) where aux carries the arrays the twins and audits need."""
    x = exprs or build(g)
    b = ctx.b
    ev = ctx.ev
    p = Plan(b.n)
    p.sigL, p.sigS = ev(x["sig"]["long"]).copy(), ev(x["sig"]["short"]).copy()
    ent = g["slots"]["entry"]
    p.etype = ETYPE[ent["type"]]
    p.valid_bars = 1 if p.etype == MARKET else bars_for_minutes(ent["valid_minutes"], b.tf)
    if p.etype != MARKET:
        p.epxL, p.epxS = _round(ev(x["ref"]["long"]), b.tick), _round(ev(x["ref"]["short"]), b.tick)
    p.stpL, p.stpS = _round(ev(x["stp"]["long"]), b.tick), _round(ev(x["stp"]["short"]), b.tick)
    if x["tgt"]["long"] is not None:
        p.tgtL, p.tgtS = _round(ev(x["tgt"]["long"]), b.tick), _round(ev(x["tgt"]["short"]), b.tick)
    p.exL, p.exS = ev(x["ex"]["long"]), ev(x["ex"]["short"])
    sc = x["scalars"]
    p.time_stop_bars = bars_for_minutes(sc["time_stop_minutes"], b.tf) if sc["time_stop_minutes"] else 0
    p.be_R, p.trail_start_R, p.trail_R, p.part_R = sc["be_R"], sc["trail_start_R"], sc["trail_R"], sc["part_R"]
    q = g["sequencing"]
    p.cooldown_bars = max(2, int(math.ceil(q["cooldown_minutes"] / b.tf)))
    p.max_trades = q["max_trades_per_session"]
    p.loss_standdown = q["loss_standdown"]
    aux = {"validL": ev(x["valid"]["long"]), "validS": ev(x["valid"]["short"]),
           "atr": ev(A), "refL": ev(x["ref"]["long"]), "refS": ev(x["ref"]["short"])}
    return p, aux


def _round(a, tick):
    """Order prices sit on the tick grid, as they would at the exchange."""
    return np.round(a / tick) * tick


def python_source(g):
    """Text of the per-generation strategy.py: a self-contained description of the compiled strategy.
    The static audit scans this text together with the genome."""
    import json
    return (
        '"""Generated strategy (genome ' + g["genome_id"][:16] + ').  Compiled by genome/compile_py.py.\n\n'
        + K_describe(g) + '\n"""\n'
        "import json\n\n"
        "from genome import compile_py\n\n"
        "GENOME = json.loads(r'''" + json.dumps(g, sort_keys=True) + "''')\n\n\n"
        "def plan(ctx):\n"
        "    # ctx is the feature-store context for one instrument and timeframe; every value it returns at bar t\n"
        "    # uses data up to the close of bar t only.\n"
        "    return compile_py.to_plan(GENOME, ctx)\n"
    )


def K_describe(g):
    from genome.genome import describe
    return describe(g)
