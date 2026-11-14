"""Informational stage 2 run on a named generation (SPEC 20.2: evidence for the frontier).

For a candidate that did NOT pass stage 1, so it cannot be promoted; this only measures how it behaves
across timeframes, costs, decoys and transforms.  Every block of backtests is opened in the trial
ledger first.  Writes reports/candidates/gen_<n>_stage2.{json,md}.  Usage: python tools/inspect_candidate.py <generation>"""
import json
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from audit import canary  # noqa: E402
from engine import path, write_json, write_text  # noqa: E402
from gates import stage2 as S2  # noqa: E402
from genome import genome as GN  # noqa: E402
from orchestrator.ledger import Ledger  # noqa: E402

canary.install()
gen = int(sys.argv[1])
db = sqlite3.connect("file:" + path("ledger/lineage.sqlite") + "?mode=ro", uri=True)
g = json.loads(db.execute("SELECT genome FROM genomes WHERE generation=?", [gen]).fetchone()[0])
led = Ledger()
ids = []


def log(label, k):
    ids.append(led.open(generation=gen, stage="2i", genome_id=g["genome_id"], lineage_id="informational", operator="INSPECT", data_slice="search_all_folds",
                        instrument="ES+YM", timeframe_min=g["primary_timeframe_min"], cost_level="base", stress_mode=label, seed=gen, code_hash="n/a", data_hash="n/a"))
    led.commit()


r = S2.stage2(g, gen, "bronze", log=log)
for t in ids:
    led.close(t)
led.commit()
os.makedirs(path("reports/candidates"), exist_ok=True)
r.pop("simplified", None)
write_json(path(f"reports/candidates/gen_{gen:06d}_stage2.json"), r)
S = r["sections"]
L = [f"# Informational stage 2 run: generation {gen}", "",
     "This candidate did not pass stage 1, so nothing here promotes it. The run measures how it behaves outside the conditions it was "
     "selected on. Research data only; base costs unless stated; both instruments pooled over the six walk-forward test folds.", "",
     "```", GN.describe(g), "```", "", "## Gates", "", "| Gate | Value | Needs | Pass |", "|---|---|---|---|"]
for x in r["gates"]:
    L.append(f"| {x['gate']} | {x['value']} | {x['op']} {x['threshold']} | {'yes' if x['pass'] else 'NO'} |")
if "timeframes" in S:
    L += ["", "## Core timeframes (one parameter set)", "", "| Timeframe | Win rate | Alpha | Profit factor | Trades | Per year per instrument | Expectancy (round-trip costs) |", "|---|---|---|---|---|---|---|"]
    for tf, v in S["timeframes"].items():
        L.append(f"| {tf} min | {100 * v['win_rate']:.1f}% | {v['alpha_pts']:+.1f} | {v['profit_factor']:.2f} | {v['n']} | {v['trades_per_year']:.0f} | {v['expectancy_costs']:+.2f} |")
for k in ("intrabar", "parity_mode", "stress_costs", "long_short", "drift_neutral", "inverted_market", "transfer", "divergence_days", "synthetic_relatives", "decoys", "cpcv", "pbo"):
    if k in S:
        L += ["", f"## {k.replace('_', ' ')}", "", "```", json.dumps(S[k], indent=1, default=float)[:1500], "```"]
if "parameter_robustness" in S:
    p = S["parameter_robustness"]
    L += ["", "## Parameter neighbours", "", f"One-step neighbours: {len(p['one_step'])}; their profit factors: " +
          ", ".join(f"{x['pf']:.2f}" for x in p["one_step"]) + f". Fog 25th-percentile score {p['fog_p25']:.3f} "
          f"(retention {100 * p['fog_retention']:.0f}% of the nominal score, {p['fog_variants']} variants)."]
write_text(path(f"reports/candidates/gen_{gen:06d}_stage2.md"), "\n".join(L) + "\n")
print("\n".join(L[10:]))
