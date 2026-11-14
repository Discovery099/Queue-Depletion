"""Island exchange (SPEC 15.9): each island's leaders are evaluated on the OTHER island's test folds,
data that never influenced their design.  Every evaluation is logged as a trial first.
Writes reports/exchange_<generation>.md and .json.  Usage: python tools/exchange.py [leaders per island]"""
import json
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from audit import canary  # noqa: E402
from engine import path, read_json, write_json, write_text  # noqa: E402
from gates import stage1 as S1  # noqa: E402
from orchestrator.ledger import Ledger  # noqa: E402
from tools.frontier import short  # noqa: E402

canary.install()
k = int(sys.argv[1]) if len(sys.argv) > 1 else 10
st = read_json(path("state/checkpoint.json"))
gen_now = st["next_generation"] - 1
db = sqlite3.connect(path("ledger/lineage.sqlite"))
led = Ledger()
rows = []
for isl in ("A", "B"):
    seen, picked = set(), []
    for gen, js, score, n, wr, pf, alpha in db.execute(
            "SELECT generation, genome, score, n_trades, win_rate, pf, alpha FROM genomes WHERE island=? AND n_trades>=150 ORDER BY score DESC LIMIT 400", [isl]):
        key = (n, round(wr, 4))                       # behavioural duplicate: same trades, same wins
        if key in seen:
            continue
        seen.add(key)
        picked.append((gen, json.loads(js), score, n, wr, pf, alpha))
        if len(picked) >= k:
            break
    away = "B" if isl == "A" else "A"
    for gen, g, score, n, wr, pf, alpha in picked:
        tid = led.open(generation=gen, stage="1e", genome_id=g["genome_id"], lineage_id="exchange", operator="ISLAND_EXCHANGE",
                       data_slice=f"away_folds_island_{away}", instrument="ES+YM", timeframe_min=g["primary_timeframe_min"], cost_level="base",
                       stress_mode="candidate+twins", seed=gen, code_hash="n/a", data_hash=st["frozen"]["partition"][:16])
        led.commit()
        res, _ = S1.stage1(g, away, gen, n_twins=200)
        m, tw = res["pooled"], res["twin"]
        led.close(tid, n_trades=m["n"], win_rate=m["win_rate"], profit_factor=m["profit_factor"], expectancy_ticks=m.get("expectancy_ticks"), score=res["score"])
        led.commit()
        rows.append({"generation": gen, "home": isl, "tf": g["primary_timeframe_min"], "strategy": short(json.dumps(g)),
                     "home_score": score, "home_wr": wr, "home_pf": pf, "home_alpha": alpha, "home_n": n,
                     "away_score": res["score"], "away_wr": m["win_rate"], "away_pf": m["profit_factor"], "away_alpha": tw["win_rate_alpha_pts"],
                     "away_n": m["n"], "away_exp_costs": m.get("expectancy_costs", 0.0), "away_failed": len(res["failed_gates"]), "away_passed": res["passed"]})
import numpy as np
hs, as_ = np.array([r["home_score"] for r in rows]), np.array([r["away_score"] for r in rows])
summ = {"generation": gen_now, "leaders": len(rows), "mean_home_score": float(hs.mean()), "mean_away_score": float(as_.mean()),
        "retention": float(as_.mean() / hs.mean()), "mean_home_pf": float(np.mean([r["home_pf"] for r in rows])),
        "mean_away_pf": float(np.mean([r["away_pf"] for r in rows])), "mean_home_wr": float(np.mean([r["home_wr"] for r in rows])),
        "mean_away_wr": float(np.mean([r["away_wr"] for r in rows])), "away_pf_above_1": int(sum(r["away_pf"] > 1 for r in rows)),
        "away_passes": int(sum(r["away_passed"] for r in rows))}
write_json(path(f"reports/exchange_{gen_now:06d}.json"), {"summary": summ, "rows": rows})
L = [f"# Island exchange at generation {gen_now}", "",
     f"The {k} highest-scoring distinct strategies of each island, re-scored on the other island's three test folds (data that never "
     "influenced their design; 200 geometry-matched twins). Research data only.", "",
     f"- Mean composite score: {summ['mean_home_score']:.3f} at home, {summ['mean_away_score']:.3f} away (retention {100 * summ['retention']:.0f}%).",
     f"- Mean win rate: {100 * summ['mean_home_wr']:.1f}% at home, {100 * summ['mean_away_wr']:.1f}% away.",
     f"- Mean profit factor: {summ['mean_home_pf']:.2f} at home, {summ['mean_away_pf']:.2f} away; {summ['away_pf_above_1']} of {len(rows)} stay above 1.0 away.",
     f"- Leaders passing the stage 1 screen on the away folds: {summ['away_passes']} of {len(rows)}.", "",
     "| Generation | Home | Timeframe | Home: score / win rate / PF / alpha | Away: score / win rate / PF / alpha / trades | Strategy |", "|---|---|---|---|---|---|"]
for r in rows:
    L.append(f"| {r['generation']} | {r['home']} | {r['tf']} min | {r['home_score']:.3f} / {100 * r['home_wr']:.1f}% / {r['home_pf']:.2f} / {r['home_alpha']:+.1f} | "
             f"{r['away_score']:.3f} / {100 * r['away_wr']:.1f}% / {r['away_pf']:.2f} / {r['away_alpha']:+.1f} / {r['away_n']} | {r['strategy']} |")
write_text(path(f"reports/exchange_{gen_now:06d}.md"), "\n".join(L) + "\n")
print("\n".join(L[4:8]))
for r in rows:
    print(r["generation"], r["home"], f"tf{r['tf']}", f"home {r['home_score']:.3f} wr {100*r['home_wr']:.1f} pf {r['home_pf']:.2f} a {r['home_alpha']:+.1f} | away {r['away_score']:.3f} wr {100*r['away_wr']:.1f} pf {r['away_pf']:.2f} a {r['away_alpha']:+.1f} n {r['away_n']}")
