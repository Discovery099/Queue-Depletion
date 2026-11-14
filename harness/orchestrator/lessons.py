"""Graveyard distillation (SPEC 15.8): at most 100 lessons, each with its supporting failure count.
Programmatic and deterministic; the Strategist reads the result before proposing."""
import collections
import json
import os

import numpy as np

from engine import write_text
from library.atoms.catalog import ATOMS, FAMILIES


def distil(run):
    f = run.p("ledger/graveyard.jsonl")
    if not os.path.exists(f):
        return 0
    rows = [json.loads(x) for x in open(f)]
    rows = [r for r in rows if r.get("n", 0) >= 100 and r.get("alpha") is not None]
    by = collections.defaultdict(list)
    for r in rows:
        trig = r["structure"]["trigger"].split("+")[0]
        fam = ATOMS[trig].fam if trig in ATOMS else "?"
        tk = next((ATOMS[a].kind for a in r["atoms"] if a in ATOMS and getattr(ATOMS[a], "kind", "") == "target"), "none")
        tgt = next((a for a in r["atoms"] if a in ATOMS and getattr(ATOMS[a], "kind", "") == "target"), "no target")
        by[("family", fam)].append(r)
        by[("trigger", trig)].append(r)
        by[("target", tgt)].append(r)
        by[("timeframe", str(r["structure"]["tf"]))].append(r)
        by[("entry", r["structure"]["entry"])].append(r)
    gates = collections.Counter(g for r in rows for g in r["failed_gates"])
    L = ["# Lessons (distilled from the graveyard)", "",
         f"Built from {len(rows)} failed generations with at least 100 out-of-sample trades. Each line is a description of what failed, "
         "with its supporting count; none is a rule. Lessons learned on one timeframe or exit family may be wrong in general and are "
         "re-tested every 10,000 generations (SPEC 15.8).", "",
         "Note: win-rate alpha recorded before generation 2001 used a twin that did not match target-to-stop geometry and is overstated "
         "for level-based targets (reports/gate_changes.md).", "", "## Most common failed gates", ""]
    L += [f"- {g}: {c} failures" for g, c in gates.most_common(12)]
    out = []
    for (kind, key), rs in by.items():
        if len(rs) < 15:
            continue
        a = np.array([r["alpha"] for r in rs])
        pf = np.array([r["pf"] or 0 for r in rs])
        wr = np.array([r["win_rate"] or 0 for r in rs])
        out.append((kind, key, len(rs), float(np.median(a)), float(np.median(pf)), float((pf > 1).mean()), float(np.median(wr))))
    for kind in ("family", "target", "timeframe", "entry", "trigger"):
        sel = sorted([o for o in out if o[0] == kind], key=lambda o: -o[2])[: (30 if kind == "trigger" else 15)]
        if not sel:
            continue
        L += ["", f"## By {kind}", ""]
        for _, key, n, ma, mpf, share, mwr in sel:
            name = FAMILIES.get(key, key) if kind == "family" else key
            verdict = "no edge after costs" if mpf < 0.95 else "near break-even" if mpf < 1.05 else "weakly positive, below the gates"
            L.append(f"- {name}: median win rate {100 * mwr:.0f}%, median alpha {ma:+.1f} points, median profit factor {mpf:.2f}, "
                     f"{100 * share:.0f}% above 1.0; {verdict} ({n} failures)")
    write_text(run.p("ledger/lessons.md"), "\n".join(L[:140]) + "\n")
    return len(rows)
