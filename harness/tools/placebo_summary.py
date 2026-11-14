"""Summarise a placebo run (SPEC 15.4): every promotion on a decoy market is a false discovery.
Usage: python tools/placebo_summary.py <tag>"""
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import ENGINE_VERSION, path, read_json, write_json, write_text  # noqa: E402

tag = sys.argv[1]
root = path("state", "placebo", tag)
st = read_json(os.path.join(root, "state/checkpoint.json"))
db = sqlite3.connect(os.path.join(root, "ledger/lineage.sqlite"))
n = st["next_generation"] - 1
by = dict(db.execute("SELECT status, COUNT(*) FROM genomes GROUP BY status").fetchall())
best = db.execute("SELECT MAX(score) FROM genomes").fetchone()[0]
big = db.execute("SELECT COUNT(*), AVG(alpha), MAX(alpha), AVG(pf), MAX(pf) FROM genomes WHERE n_trades >= 150").fetchone()
out = {"tag": tag, "decoy": st["decoy"], "generations": n, "engine_version": ENGINE_VERSION, "promotions": st["tier_counts"],
       "stage1_passes": by.get("STAGE1_PASS", 0) + by.get("HOME_ONLY", 0) + sum(v for k, v in by.items() if k.startswith(("STAGE2", "STAGE3", "STAGE4", "CONFIRMED"))),
       "outcomes": by, "best_composite_score": best, "requirement": "zero Gold, zero Silver, at most 2 Bronze in 1,000 generations",
       "holds": st["tier_counts"]["gold"] == 0 and st["tier_counts"]["silver"] == 0 and st["tier_counts"]["bronze"] <= 2,
       "genomes_with_150_trades": {"count": big[0], "mean_alpha_pts": big[1], "max_alpha_pts": big[2], "mean_pf": big[3], "max_pf": big[4]}}
write_json(path("reports/milestones/placebo_latest.json"), out)
write_text(path("reports/milestones/placebo_latest.md"), f"""# Placebo pipeline run `{tag}`

The whole search loop was run for {n} generations on a decoy market ({st['decoy'][0]} number {st['decoy'][1]}) built from research data
with no exploitable directional structure. Every promotion on such a market is a false discovery.

- Promotions: {st['tier_counts']['bronze']} Bronze, {st['tier_counts']['silver']} Silver, {st['tier_counts']['gold']} Gold.
- Stage 1 passes (before confirmation and stage 2): {out['stage1_passes']}.
- Requirement (zero Gold, zero Silver, at most 2 Bronze per 1,000 generations): {'HOLDS' if out['holds'] else 'DOES NOT HOLD'}.
- Outcomes: {by}.
- Best composite score reached on the decoy: {best:.3f}. Among {big[0]} decoy genomes with at least 150 trades: mean win-rate alpha
  {big[1]:+.2f} points (maximum {big[2]:+.1f}), mean profit factor {big[3]:.2f} (maximum {big[4]:.2f}).

Statement to place next to any real certification: "this pipeline promoted {st['tier_counts']['silver']} strategies to Silver and
{st['tier_counts']['bronze']} to Bronze in {n} generations on markets with no edge".

Limit: the decoy genomes all stopped at the stage 1 screen, so this measures the false-discovery rate of the screen and its
confirmation. Stages 2 to 4 were not reached and are therefore not separately calibrated by this run.
""")
print(out)
