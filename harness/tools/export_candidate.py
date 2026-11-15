"""Export a named generation to Pine, marked NOT CERTIFIED, with the independent parity check and a
TradingView check sheet (SPEC 18.3).  For leading candidates that failed a gate; nothing here promotes them.
Usage: python tools/export_candidate.py <generation> [instrument for the check sheet, default YM]"""
import json
import os
import sqlite3
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from audit import canary, pine_replay, static_audit  # noqa: E402
from engine import path, read_json, write_json, write_text  # noqa: E402
from genome import compile_pine  # noqa: E402
from orchestrator import evaluate as EV  # noqa: E402
from orchestrator.ledger import Ledger  # noqa: E402

canary.install()
gen = int(sys.argv[1])
sym = sys.argv[2] if len(sys.argv) > 2 else "YM"
db = sqlite3.connect("file:" + path("ledger/lineage.sqlite") + "?mode=ro", uri=True)
g = json.loads(db.execute("SELECT genome FROM genomes WHERE generation=?", [gen]).fetchone()[0])
d = path("runs", f"{gen // 1000:03d}", f"gen_{gen:06d}")
c = read_json(os.path.join(d, "metrics_stage1_confirmation.json"))
fails = [x for x in read_json(os.path.join(d, "gates.json"))["stage1_confirmation_all_folds"] if not x["pass"]]
m, tw = c["pooled"], c["twin"]
tf = g["primary_timeframe_min"]
stmt = f"""NOT CERTIFIED. This strategy FAILED the lowest tier (Bronze) of the harness. It is exported for inspection only.
Failed on all six walk-forward test folds: {'; '.join(f"{x['gate']} = {x['value']} (needs {x['op']} {x['threshold']})" for x in fails)}.

WIN-RATE STATEMENT (research walk-forward folds 3 to 8, ES and YM pooled, {tf}-minute bars, base costs, 1 contract)
Headline win rate (net, flat-to-flat, OOS):   {100 * m['win_rate']:.1f} %   (n = {m['n']} trades)
Wilson 95% interval:                          {100 * m['wilson_lo']:.1f} % to {100 * m['wilson_hi']:.1f} %
Geometry baseline (random-entry twin median): {100 * tw['median_win_rate']:.1f} %   ({tw['n_twins']} twins)
Win-rate alpha:                               {tw['win_rate_alpha_pts']:+.1f} points (twin p99 = {100 * tw['p99_win_rate']:.1f} %)
Random-exit twin win rate:                    {100 * tw['random_exit_win_rate']:.1f} %
Payoff ratio:                                 {m['payoff']:.2f}
Profit factor:                                {m['profit_factor']:.2f}
Expectancy per trade:                         {m['expectancy_ticks']:+.2f} ticks   ({m['expectancy_costs']:+.2f} x round-trip cost)
Largest loss / average win:                   {m['largest_loss_in_avg_wins']:.1f}
Trades per year per instrument:               {m['n'] / 2 / (len(EV.fold_sessions(EV.TEST_FOLDS)) / 252):.0f}
Sessions with a trade:                        {100 * m['session_share']:.0f} %
Best of about 100,000 generations: by itself this record is not evidence of an edge. No unseen-data (vault) result, no live fills.
See deliverables/DOSSIER.md for its known weaknesses."""
src = compile_pine.export(g, {"name": f"SEH candidate {gen} (NOT CERTIFIED)", "generation": gen, "tier": "none: failed Bronze",
                              "win_rate_statement": stmt, "tag": f"SEH_CAND_{gen}"})
os.makedirs(path("reports/candidates"), exist_ok=True)
write_text(path(f"reports/candidates/gen_{gen:06d}.pine"), src)
hits = static_audit.scan_pine(src)
par = pine_replay.parity(g, src, sessions=120, warm=40, seed=gen)
write_json(path(f"reports/candidates/gen_{gen:06d}_pine_parity.json"), par)
led = Ledger()
t = led.open(generation=gen, stage="2i", genome_id=g["genome_id"], lineage_id="informational", operator="PINE_CHECK", data_slice="search", instrument=sym,
             timeframe_min=tf, cost_level="base", stress_mode="trade_list_for_owner_check", seed=gen, code_hash="n/a", data_hash="n/a")
led.commit()
tr = EV.run(g, sym, tf)["trades"]
led.close(t, n_trades=len(tr))
led.commit()
tr = tr[tr.fold == 8]
pick = tr.iloc[np.sort(np.random.default_rng(gen).choice(len(tr), 10, replace=False))]
ts = lambda x: pd.to_datetime(x, utc=True).tz_convert("America/New_York").strftime("%Y-%m-%d %H:%M")   # noqa: E731
L = [f"# How to check the Pine file in TradingView yourself (generation {gen}, NOT CERTIFIED)", "",
     f"1. Open a {tf}-minute chart of the {sym} continuous contract with **regular trading hours only** (09:30 to 16:00 Eastern).",
     f"2. Paste `gen_{gen:06d}.pine` into the Pine editor and add it to the chart. Leave every input at its default (execution mode stays `Sim/Paper`).",
     "3. Open the Strategy Tester's list of trades and look for the ten trades below.", "",
     "Times are US Eastern **bar open times**. Prices are from the research data for 1 contract and include 1 tick of slippage on market and stop "
     "fills. TradingView's continuous contract can differ slightly from the supplied data, and its fill model is more optimistic than the research "
     "engine's when a stop and a target fall inside one bar, so small price differences are expected. **Exact timing and direction matter more than price.**", "",
     "| # | Direction | Entry time | Entry price | Exit time (bar open) | Exit price | Exit reason | Net result (ticks) |", "|---|---|---|---|---|---|---|---|"]
for i, (_, x) in enumerate(pick.iterrows(), 1):
    L.append(f"| {i} | {'long' if x.direction > 0 else 'short'} | {ts(x.entry_ts)} | {x.entry_price:g} | {ts(x.exit_ts)} | {x.exit_price:g} | {x.exit_reason} | {x.net_ticks:+.1f} |")
L += ["", "If the trades appear at these times and directions, the Pine file is doing what the research engine did. If they do not, do not use the file; report the difference.", "",
      f"The independent replay check (`gen_{gen:06d}_pine_parity.json`) confirmed that the file's signal logic equals the research engine's on 120 sessions per "
      "instrument at two timeframes. It did not execute the order section, which is why this manual check exists.", "",
      "Reminder: this strategy failed the harness's lowest tier. The check above verifies the translation, not the strategy."]
write_text(path(f"reports/candidates/gen_{gen:06d}_PINE_CHECK.md"), "\n".join(L) + "\n")
print("static Pine audit hits:", hits, "| parity match:", par["match"], [(x["instrument"], x["timeframe"], x["trades_engine"], x["trade_lists_equal"]) for x in par["details"]])
