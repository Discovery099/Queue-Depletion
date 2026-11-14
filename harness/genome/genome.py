"""Strategy genome: schema helpers, identity, complexity, distance and search operators (SPEC 9, A.3).

A genome is plain JSON.  Seven slots hold atoms with parameters taken from each atom's coarse grid.
Long and short rules are mirror images by construction (the atoms are written for a direction `d`).
"""
import copy
import math

from engine import canon, sha256_bytes
from library.atoms.catalog import ATOMS

CEILING = 22
ENTRY_OFFSETS = [0.1, 0.25, 0.5, 0.75, 1.0]
ENTRY_VALID_MIN = [10, 15, 30, 60]
COOLDOWN_MIN = [10, 15, 30, 60]
MAX_TRADES = [2, 3, 4, 6]
PRIMARY_TF = [(5, 0.30), (10, 0.15), (15, 0.25), (30, 0.15), (60, 0.15)]
SLOT_LIMITS = {"regime": (0, 2), "location": (0, 2), "filter": (0, 3), "exit": (1, 3)}
SLOT_TYPE = {"regime": "STATE", "location": "LOCATION", "filter": "FILTER", "trigger": "TRIGGER"}
EXIT_KINDS_SINGLE = ("target", "time", "trail", "be", "partial")
DEFAULT_SEQ = {"cooldown_minutes": 10, "max_trades_per_session": 6, "loss_standdown": 3}


def A(atom_id, **params):
    a = ATOMS[atom_id]
    return {"atom": atom_id, "params": {**a.default, **params}}


def new_genome(trigger, stop=None, exits=None, regime=(), location=(), filters=(), entry=None,
               combine="AND", within=3, tf=5, direction="both_mirrored", seq=None):
    g = {
        "version": 1, "direction": direction, "holding_mode": "INTRADAY_FLAT",
        "slots": {
            "regime": list(regime), "location": list(location),
            "trigger": {"combine": combine, "within_bars": within, "atoms": list(trigger)},
            "filter": list(filters),
            "entry": entry or {"type": "market", "offset_atr": 0.0, "valid_minutes": 0},
            "risk": {"stop": stop or A("r_stop_atr")},
            "exit": list(exits or [A("x_target_r")]),
        },
        "sequencing": dict(seq or DEFAULT_SEQ),
        "primary_timeframe_min": tf, "context_tf_multiples": [4, 12],
    }
    return finalize(g)


def body(g):
    return {k: g[k] for k in ("version", "direction", "holding_mode", "slots", "sequencing", "context_tf_multiples")}


def finalize(g):
    """Recompute the derived fields.  The id covers logic only, not the primary timeframe."""
    g["complexity"] = complexity(g)
    g["genome_id"] = sha256_bytes(canon(body(g)).encode())
    return g


def atom_entries(g, with_slot=False):
    s = g["slots"]
    out = []
    for slot in ("regime", "location", "filter", "exit"):
        out += [(slot, e) for e in s[slot]]
    out += [("trigger", e) for e in s["trigger"]["atoms"]]
    out.append(("risk", s["risk"]["stop"]))
    return out if with_slot else [e for _, e in out]


def complexity(g):
    """1 per atom, 1 per free numeric parameter, 2 per asymmetry, 2 per session-time window (SPEC 9.2)."""
    c = 0
    for e in atom_entries(g):
        a = ATOMS[e["atom"]]
        c += 1 + sum(1 for k in e["params"] if len(a.grid.get(k, [])) > 1) + 2 * a.tw
    ent = g["slots"]["entry"]
    if ent["type"] != "market":
        c += 2
    if g["direction"] in ("long_only", "short_only", "both_asymmetric"):
        c += 2
    if len(g["slots"]["trigger"]["atoms"]) > 1 and g["slots"]["trigger"]["combine"] == "SEQ":
        c += 1
    return c


def validate(g):
    """Structural checks.  Returns a list of problems (empty when valid)."""
    p = []
    s = g["slots"]
    for slot, (lo, hi) in SLOT_LIMITS.items():
        if not lo <= len(s[slot]) <= hi:
            p.append(f"{slot}: {len(s[slot])} atoms outside {lo}..{hi}")
    if not 1 <= len(s["trigger"]["atoms"]) <= 2:
        p.append("trigger: needs 1 or 2 atoms")
    for slot, e in atom_entries(g, True):
        a = ATOMS.get(e["atom"])
        if a is None:
            p.append(f"unknown atom {e['atom']}")
            continue
        want = SLOT_TYPE.get(slot, "EXIT")
        if a.typ != want:
            p.append(f"{e['atom']} is {a.typ}, slot {slot} needs {want}")
        if slot == "risk" and getattr(a, "kind", None) != "stop":
            p.append("risk slot needs a stop rule")
        if slot == "exit" and getattr(a, "kind", None) == "stop":
            p.append("stop rule in exit slot")
        for k, v in e["params"].items():
            if k not in a.grid or v not in a.grid[k]:
                p.append(f"{e['atom']}.{k}={v} is off its grid")
    kinds = [ATOMS[e["atom"]].kind for e in s["exit"] if e["atom"] in ATOMS and hasattr(ATOMS[e["atom"]], "kind")]
    for k in EXIT_KINDS_SINGLE:
        if kinds.count(k) > 1:
            p.append(f"more than one {k} exit")
    ids = [e["atom"] for e in atom_entries(g)]
    if len(ids) != len(set(ids)):
        p.append("same atom used twice")
    ent = s["entry"]
    if ent["type"] not in ("market", "limit", "stop"):
        p.append("bad entry type")
    if ent["type"] != "market" and (ent["offset_atr"] not in ENTRY_OFFSETS or ent["valid_minutes"] not in ENTRY_VALID_MIN):
        p.append("entry parameters off grid")
    if g["holding_mode"] != "INTRADAY_FLAT":
        p.append("only INTRADAY_FLAT is offered to the search (data/DATA_QUALITY.md)")
    q = g["sequencing"]
    if q["cooldown_minutes"] not in COOLDOWN_MIN or q["max_trades_per_session"] not in MAX_TRADES or q["loss_standdown"] != 3:
        p.append("sequencing off grid")
    if complexity(g) > CEILING:
        p.append(f"complexity {complexity(g)} above ceiling {CEILING}")
    return p


# ------------------------------------------------------------------ distance (SPEC 9.7)
def _slot_sets(g):
    s = g["slots"]
    d = {k: {e["atom"] + ("!" if e.get("inv") else "") for e in s[k]} for k in ("regime", "location", "filter", "exit")}
    d["trigger"] = {e["atom"] + ("!" if e.get("inv") else "") for e in s["trigger"]["atoms"]}
    d["risk"] = {s["risk"]["stop"]["atom"]}
    d["entry"] = {s["entry"]["type"]}
    return d


def _param_index(g):
    """Grid index of every free parameter."""
    out = {}
    for e in atom_entries(g):
        a = ATOMS[e["atom"]]
        for k, v in e["params"].items():
            grid = a.grid[k]
            if len(grid) > 1:
                out[(e["atom"], k)] = grid.index(v)
    ent = g["slots"]["entry"]
    if ent["type"] != "market":
        out[("entry", "offset")] = ENTRY_OFFSETS.index(ent["offset_atr"])
        out[("entry", "valid")] = ENTRY_VALID_MIN.index(ent["valid_minutes"])
    q = g["sequencing"]
    out[("seq", "cool")] = COOLDOWN_MIN.index(q["cooldown_minutes"])
    out[("seq", "max")] = MAX_TRADES.index(q["max_trades_per_session"])
    return out


def distance(g1, g2):
    """0 = identical logic, 1 = nothing shared.  0.6 * structure + 0.4 * parameters.

    The parameter part is the total number of grid steps between the two genomes divided by 8
    (a parameter present in only one of them counts as 2 steps), capped at 1.  One grid step is
    therefore 0.05, the novelty threshold, and three steps are 0.15, the 'same strategy' threshold."""
    a, b = _slot_sets(g1), _slot_sets(g2)
    js = []
    for k in a:
        u = a[k] | b[k]
        js.append(1.0 if not u else len(a[k] & b[k]) / len(u))
    structure = 1.0 - sum(js) / len(js)
    pa, pb = _param_index(g1), _param_index(g2)
    steps = sum(abs(pa[k] - pb[k]) if k in pa and k in pb else 2 for k in set(pa) | set(pb))
    pd_ = min(1.0, steps / 8.0)
    extra = 0.0
    if g1["direction"] != g2["direction"]:
        extra += 0.1
    if g1["slots"]["trigger"]["combine"] != g2["slots"]["trigger"]["combine"] and len(g1["slots"]["trigger"]["atoms"]) > 1:
        extra += 0.05
    return min(1.0, 0.6 * structure + 0.4 * pd_ + extra)


# ------------------------------------------------------------------ search operators (SPEC 9.4)
def _pick(rng, seq):
    return seq[int(rng.integers(len(seq)))]


def _atoms_of(typ, kind=None, exclude=(), weights=None, rng=None):
    c = [a for a in ATOMS.values() if a.typ == typ and (kind is None or getattr(a, "kind", None) == kind)
         and a.id not in exclude and not getattr(a, "blocked", False)]
    return c


def _wpick(rng, cands, weights):
    if not cands:
        return None
    w = [max(1e-6, (weights or {}).get(a.id, 1.0)) for a in cands]
    t = sum(w)
    r = rng.random() * t
    for a, x in zip(cands, w):
        r -= x
        if r <= 0:
            return a
    return cands[-1]


def rand_atom(rng, typ, kind=None, exclude=(), weights=None, fam_not=None, randomize=True):
    c = _atoms_of(typ, kind, exclude)
    if fam_not:
        c2 = [a for a in c if a.fam not in fam_not]
        c = c2 or c
    a = _wpick(rng, c, weights)
    if a is None:
        return None
    e = {"atom": a.id, "params": dict(a.default)}
    if randomize:
        for k, grid in a.grid.items():
            if len(grid) > 1 and rng.random() < 0.5:
                e["params"][k] = _pick(rng, grid)
    return e


def used_ids(g):
    return {e["atom"] for e in atom_entries(g)}


def minimal_genome(rng, trigger_id=None, weights=None, tf=5, with_context=None):
    """Survey-phase genome: one trigger, an ATR stop and an R target, optionally one context atom
    from a different mechanism family (SPEC 10.4)."""
    t = A(trigger_id) if trigger_id else rand_atom(rng, "TRIGGER", weights=weights)
    fam = ATOMS[t["atom"]].fam
    stop = rand_atom(rng, "EXIT", "stop", weights=weights)
    tgt = rand_atom(rng, "EXIT", "target", weights=weights)
    kw = {}
    ctx = with_context if with_context is not None else rng.random() < 0.6
    if ctx:
        slot = _pick(rng, ["regime", "location", "filters"])
        typ = {"regime": "STATE", "location": "LOCATION", "filters": "FILTER"}[slot]
        e = rand_atom(rng, typ, weights=weights, fam_not={fam})
        if e:
            kw[slot] = [e]
    return new_genome([t], stop=stop, exits=[tgt], tf=tf, **kw)


def op_param_step(rng, g, weights=None):
    g = copy.deepcopy(g)
    cands = []
    for e in atom_entries(g):
        a = ATOMS[e["atom"]]
        cands += [(e, k) for k, grid in a.grid.items() if len(grid) > 1]
    extra = ["cool", "max"] + (["off", "valid"] if g["slots"]["entry"]["type"] != "market" else [])
    n = len(cands) + len(extra)
    i = int(rng.integers(n))
    step = 1 if rng.random() < 0.5 else -1
    if i < len(cands):
        e, k = cands[i]
        grid = ATOMS[e["atom"]].grid[k]
        j = min(len(grid) - 1, max(0, grid.index(e["params"][k]) + step))
        e["params"][k] = grid[j]
    else:
        name = extra[i - len(cands)]
        tab = {"cool": (g["sequencing"], "cooldown_minutes", COOLDOWN_MIN),
               "max": (g["sequencing"], "max_trades_per_session", MAX_TRADES),
               "off": (g["slots"]["entry"], "offset_atr", ENTRY_OFFSETS),
               "valid": (g["slots"]["entry"], "valid_minutes", ENTRY_VALID_MIN)}[name]
        dct, key, grid = tab
        dct[key] = grid[min(len(grid) - 1, max(0, grid.index(dct[key]) + step))]
    return finalize(g)


def op_atom_swap(rng, g, weights=None):
    """Replace an atom with another of the same type from a different mechanism family."""
    g = copy.deepcopy(g)
    slot, e = _pick(rng, atom_entries(g, True))
    a = ATOMS[e["atom"]]
    new = rand_atom(rng, a.typ, getattr(a, "kind", None), exclude=used_ids(g), weights=weights, fam_not={a.fam})
    if new is None:
        return None
    e.clear()
    e.update(new)
    return finalize(g)


def op_atom_add(rng, g, weights=None):
    g = copy.deepcopy(g)
    s = g["slots"]
    opts = [k for k, (lo, hi) in SLOT_LIMITS.items() if len(s[k]) < hi]
    if len(s["trigger"]["atoms"]) < 2:
        opts.append("trigger")
    if not opts:
        return None
    slot = _pick(rng, opts)
    fams = {ATOMS[e["atom"]].fam for e in atom_entries(g)}
    if slot == "exit":
        have = {ATOMS[e["atom"]].kind for e in s["exit"]}
        kinds = [k for k in ("target", "time", "trail", "be", "partial", "inval") if k == "inval" or k not in have]
        new = rand_atom(rng, "EXIT", _pick(rng, kinds), exclude=used_ids(g), weights=weights)
        if new:
            s["exit"].append(new)
    elif slot == "trigger":
        new = rand_atom(rng, "TRIGGER", exclude=used_ids(g), weights=weights, fam_not=fams)
        if new:
            s["trigger"]["atoms"].append(new)
            s["trigger"]["combine"] = _pick(rng, ["AND", "OR", "SEQ"])
            s["trigger"]["within_bars"] = _pick(rng, [2, 3, 5, 8])
    else:
        new = rand_atom(rng, SLOT_TYPE[slot], exclude=used_ids(g), weights=weights, fam_not=fams)
        if new:
            s[slot].append(new)
    return finalize(g) if new else None


def op_atom_drop(rng, g, weights=None):
    g = copy.deepcopy(g)
    s = g["slots"]
    opts = [(k, i) for k in ("regime", "location", "filter") for i in range(len(s[k]))]
    if len(s["exit"]) > 1:
        opts += [("exit", i) for i in range(len(s["exit"]))]
    if len(s["trigger"]["atoms"]) > 1:
        opts += [("trigger", i) for i in range(2)]
    if not opts:
        return None
    k, i = _pick(rng, opts)
    (s["trigger"]["atoms"] if k == "trigger" else s[k]).pop(i)
    return finalize(g)


def op_simplify(rng, g, weights=None):
    """Remove one context atom, filters first.  (The score-aware version runs at stage 2 as ablation.)"""
    g = copy.deepcopy(g)
    s = g["slots"]
    for k in ("filter", "location", "regime"):
        if s[k]:
            s[k].pop(int(rng.integers(len(s[k]))))
            return finalize(g)
    return op_atom_drop(rng, g)


def op_slot_crossover(rng, g, other, weights=None):
    g = copy.deepcopy(g)
    for k in ("regime", "location", "trigger", "filter", "entry", "risk", "exit"):
        if rng.random() < 0.5:
            g["slots"][k] = copy.deepcopy(other["slots"][k])
    return finalize(g)


def op_exit_transplant(rng, g, other, weights=None):
    g = copy.deepcopy(g)
    g["slots"]["exit"] = copy.deepcopy(other["slots"]["exit"])
    g["slots"]["risk"] = copy.deepcopy(other["slots"]["risk"])
    return finalize(g)


def op_entry_transplant(rng, g, other, weights=None):
    g = copy.deepcopy(g)
    for k in ("regime", "location", "trigger"):
        g["slots"][k] = copy.deepcopy(other["slots"][k])
    return finalize(g)


def op_invert(rng, g, weights=None):
    """Reverse a trigger or regime condition: test whether the opposite of an idea wins."""
    g = copy.deepcopy(g)
    c = g["slots"]["trigger"]["atoms"] + g["slots"]["regime"]
    e = _pick(rng, c)
    if e.get("inv"):
        e.pop("inv")
    else:
        e["inv"] = True
    return finalize(g)


def op_entry_type(rng, g, weights=None):
    g = copy.deepcopy(g)
    t = _pick(rng, ["market", "limit", "stop"])
    g["slots"]["entry"] = {"type": "market", "offset_atr": 0.0, "valid_minutes": 0} if t == "market" else \
        {"type": t, "offset_atr": _pick(rng, ENTRY_OFFSETS), "valid_minutes": _pick(rng, ENTRY_VALID_MIN)}
    return finalize(g)


def one_step_neighbours(g, steps=1):
    """Every single-parameter move of `steps` grid steps (SPEC 12.6)."""
    out = []
    for idx, e in enumerate(atom_entries(g)):
        a = ATOMS[e["atom"]]
        for k, grid in a.grid.items():
            if len(grid) < 2:
                continue
            j = grid.index(e["params"][k])
            for s in (-steps, steps):
                if 0 <= j + s < len(grid):
                    h = copy.deepcopy(g)
                    atom_entries(h)[idx]["params"][k] = grid[j + s]
                    out.append(finalize(h))
    return out


def fog_variant(rng, g):
    """Every parameter drawn independently from its one-step neighbourhood (SPEC 12.6 parameter fog)."""
    h = copy.deepcopy(g)
    for e in atom_entries(h):
        a = ATOMS[e["atom"]]
        for k, grid in a.grid.items():
            if len(grid) > 1:
                j = grid.index(e["params"][k]) + int(rng.integers(-1, 2))
                e["params"][k] = grid[min(len(grid) - 1, max(0, j))]
    return finalize(h)


def describe(g):
    s = g["slots"]
    f = lambda e: e["atom"] + ("[inverted]" if e.get("inv") else "") + "(" + ", ".join(f"{k}={v}" for k, v in e["params"].items()) + ")"  # noqa: E731
    lines = [f"direction: {g['direction']}; holding: {g['holding_mode']}; complexity: {g['complexity']}"]
    for k in ("regime", "location", "filter"):
        if s[k]:
            lines.append(f"{k}: " + "; ".join(f(e) for e in s[k]))
    t = s["trigger"]
    lines.append("trigger: " + (f" {t['combine']} ".join(f(e) for e in t["atoms"])) +
                 (f" (within {t['within_bars']} bars)" if t["combine"] == "SEQ" and len(t["atoms"]) > 1 else ""))
    e = s["entry"]
    lines.append("entry: " + (e["type"] if e["type"] == "market" else f"{e['type']} at {e['offset_atr']} ATR, valid {e['valid_minutes']} min"))
    lines.append("stop: " + f(s["risk"]["stop"]))
    lines.append("exit: " + "; ".join(f(x) for x in s["exit"]))
    q = g["sequencing"]
    lines.append(f"sequencing: cool-down {q['cooldown_minutes']} min, max {q['max_trades_per_session']} trades per session, "
                 f"stand down after {q['loss_standdown']} straight losses")
    return "\n".join(lines)
