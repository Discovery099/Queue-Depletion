"""Frontier report (SPEC 20.2): win rate against profit factor and trade frequency across every generation,
the highest win-rate alpha at each frequency level, and which constraint binds.  Research data only.
Writes reports/frontier.md and reports/frontier.json."""
import json
import os
import sqlite3
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import path, read_json, write_json, write_text  # noqa: E402
from engine.data import partition  # noqa: E402
from orchestrator import evaluate as EV  # noqa: E402


def short(js):
    g = json.loads(js)
    s = g["slots"]
    ctx = [e["atom"] for k in ("regime", "location", "filter") for e in s[k]]
    t = (" " + s["trigger"]["combine"] + " ").join(e["atom"] + ("[inv]" if e.get("inv") else "") for e in s["trigger"]["atoms"])
    return f"{t}" + (f" with {', '.join(ctx)}" if ctx else "") + f"; {s['risk']['stop']['atom']}; {', '.join(e['atom'] for e in s['exit'])}; {s['entry']['type']}"


def main():
    st = read_json(path("state/checkpoint.json"))
    db = sqlite3.connect(path("ledger/lineage.sqlite"))
    rows = db.execute("SELECT generation, island, tf, complexity, score, n_trades, win_rate, pf, alpha, genome, status FROM genomes "
                      "WHERE status NOT IN ('VOID','ERROR') AND n_trades > 0").fetchall()
    n_sess = len(EV.fold_sessions(EV.ISLAND_FOLDS["A"]))
    yrs = n_sess / 252.0
    R = [{"gen": r[0], "island": r[1], "tf": r[2], "cx": r[3], "score": r[4] or 0.0, "n": r[5], "wr": r[6] or 0.0, "pf": r[7] or 0.0,
          "alpha": r[8] or 0.0, "tpy": r[5] / 2.0 / yrs, "desc": short(r[9]), "status": r[10]} for r in rows]
    big = [r for r in R if r["n"] >= 150]
    L = ["# Frontier report", "", f"- Generations completed: {st['next_generation'] - 1}", "- Best certified tier: " +
         (max((t for t, c in st["tier_counts"].items() if c), key=["bronze", "silver", "gold"].index) if any(st["tier_counts"].values()) else "none"),
         f"- Vault queries used: {st['vault']['a_used']} of 60 (Vault-A), {st['vault']['b_used']} of 5 (Vault-B)",
         "- Pipeline false-discovery rate, latest placebo run: see reports/milestones/placebo_latest.md", "",
         f"All figures are research walk-forward out-of-sample results on an island's three home test folds ({n_sess} sessions, both "
         "instruments pooled, base costs). They are stage 1 screening numbers, the best of many attempts, and none has passed a gate. "
         "Win-rate alpha before generation 2,001 used a twin without geometry matching and is overstated for level-based targets.", "",
         f"Genomes evaluated: {len(R)}; with at least 150 out-of-sample trades: {len(big)}.", "",
         "## Counts by outcome", "", "| Outcome | Generations |", "|---|---|"]
    for k, v in sorted(st["counts"].items()):
        L.append(f"| {k} | {v} |")
    L += ["", "## How many reach each headline level (at least 150 trades)", "", "| Win rate at least | PF at least 1.0 | 1.2 | 1.4 | 1.6 | 1.8 |", "|---|---|---|---|---|---|"]
    grid = {}
    for w in (0.55, 0.60, 0.65, 0.70, 0.75, 0.80):
        cells = [sum(1 for r in big if r["wr"] >= w and r["pf"] >= p) for p in (1.0, 1.2, 1.4, 1.6, 1.8)]
        grid[w] = cells
        L.append(f"| {100 * w:.0f}% | " + " | ".join(map(str, cells)) + " |")
    L += ["", "## Best profit factor at each win-rate level, by trade frequency", "",
          "| Trades per year per instrument | Win rate 55-65% | 65-72% | 72-80% | 80%+ |", "|---|---|---|---|---|"]
    for lo, hi in ((50, 100), (100, 150), (150, 200), (200, 400), (400, 5000)):
        row = []
        for wl, wh in ((0.55, 0.65), (0.65, 0.72), (0.72, 0.80), (0.80, 1.01)):
            c = [r for r in R if lo <= r["tpy"] < hi and wl <= r["wr"] < wh and r["n"] >= 100 and r["gen"] > 2000]
            row.append(f"{max(r['pf'] for r in c):.2f} (of {len(c)})" if c else "none")
        L.append(f"| {lo} to {hi if hi < 5000 else 'more'} | " + " | ".join(row) + " |")
    L += ["", "## Highest geometry-matched win-rate alpha at each frequency level (generation 2,001 onward, profit factor above 1.0)", "",
          "| Trades per year per instrument | Alpha (points) | Win rate | Profit factor | Trades | Timeframe | Generation | Strategy |", "|---|---|---|---|---|---|---|---|"]
    for lo, hi in ((50, 100), (100, 150), (150, 200), (200, 400), (400, 5000)):
        c = [r for r in R if lo <= r["tpy"] < hi and r["pf"] > 1.0 and r["n"] >= 100 and r["gen"] > 2000]
        if c:
            b = max(c, key=lambda r: r["alpha"])
            L.append(f"| {lo} to {hi if hi < 5000 else 'more'} | {b['alpha']:+.1f} | {100 * b['wr']:.1f}% | {b['pf']:.2f} | {b['n']} | {b['tf']} min | {b['gen']} | {b['desc']} |")
    L += ["", "## Leading candidates by composite score (not certified)", "",
          "| Generation | Island | Timeframe | Score | Win rate | Alpha | Profit factor | Trades | Per year | Complexity | Strategy |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    top = sorted(big, key=lambda r: -r["score"])[:15]
    for r in top:
        L.append(f"| {r['gen']} | {r['island']} | {r['tf']} min | {r['score']:.3f} | {100 * r['wr']:.1f}% | {r['alpha']:+.1f} | {r['pf']:.2f} | {r['n']} | {r['tpy']:.0f} | {r['cx']} | {r['desc']} |")
    fails = {}
    f = path("ledger/graveyard.jsonl")
    if os.path.exists(f):
        for ln in open(f):
            for gname in json.loads(ln)["failed_gates"]:
                fails[gname] = fails.get(gname, 0) + 1
    L += ["", "## Which constraint binds", "", "Among the 15 leading candidates above, gates failed (from each generation's gates.json):", ""]
    lead = {}
    for r in top:
        gj = os.path.join(path("runs"), f"{r['gen'] // 1000:03d}", f"gen_{r['gen']:06d}", "gates.json")
        if os.path.exists(gj):
            for x in read_json(gj)["stage1"]:
                if not x["pass"]:
                    lead[x["gate"]] = lead.get(x["gate"], 0) + 1
    for k, v in sorted(lead.items(), key=lambda kv: -kv[1]):
        L.append(f"- {k}: {v} of {len(top)}")
    write_text(path("reports/frontier.md"), "\n".join(L) + "\n")
    write_json(path("reports/frontier.json"), {"generations": st["next_generation"] - 1, "grid_wr_pf": grid, "top": top, "leading_failed_gates": lead})
    print("\n".join(L[:14]))


if __name__ == "__main__":
    main()
