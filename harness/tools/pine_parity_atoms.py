"""Per-atom Pine parity (SPEC 8.1 step 6: every atom has a Pine snippet with identical semantics).
Each atom is placed in a minimal genome, exported to Pine, replayed from text by the independent
interpreter and compared with the research engine.  Writes library/pine_parity_atoms.json."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from audit import canary, pine_replay  # noqa: E402
from engine import path, write_json  # noqa: E402
from genome import compile_pine  # noqa: E402
from genome.genome import A, new_genome, validate  # noqa: E402
from library.atoms.catalog import ATOMS  # noqa: E402

real = [a for a in ATOMS.values()]
canary.install()
skip = set(canary.canary_ids()) | {canary.HONEYPOT_ID}
out = {}
for a in real:
    if a.id in skip:
        continue
    base = dict(trigger=[A("tr_donchian_break")], stop=A("r_stop_atr"), exits=[A("x_target_r")])
    if a.typ == "TRIGGER":
        base["trigger"] = [A(a.id)]
    elif a.typ == "STATE":
        base["regime"] = [A(a.id)]
    elif a.typ == "LOCATION":
        base["location"] = [A(a.id)]
        base["exits"] = [A("x_target_location_level")]
        base["stop"] = A("r_stop_level")
    elif a.typ == "FILTER":
        base["filters"] = [A(a.id)]
    elif a.kind == "stop":
        base["stop"] = A(a.id)
    elif a.kind == "target":
        base["exits"] = [A(a.id)]
    else:
        base["exits"] = [A("x_target_r"), A(a.id)]
    g = new_genome(base.pop("trigger"), **base)
    assert not validate(g), (a.id, validate(g))
    try:
        r = pine_replay.parity(g, compile_pine.export(g), sessions=20, warm=30, tfs=[5], seed=len(a.id))
        out[a.id] = {"match": r["match"], "trades": sum(d["trades_engine"] for d in r["details"]),
                     "mismatches": [m for d in r["details"] for m in d["series_mismatches"]][:3]}
    except Exception as e:
        out[a.id] = {"match": False, "error": f"{type(e).__name__}: {e}"}
bad = {k: v for k, v in out.items() if not v["match"]}
write_json(path("library/pine_parity_atoms.json"), {"atoms_checked": len(out), "matching": len(out) - len(bad), "failures": bad, "results": out,
                                                    "scope": "signal layer replayed from Pine text; 20 sessions per instrument at 5 minutes"})
print(len(out), "checked;", len(bad), "failures:", list(bad)[:20])
