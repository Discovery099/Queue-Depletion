"""Generation 0, step 7: reproduce Smart Trend V1 and record the reference metrics (SPEC 4.3).

Scored on the search sessions of the Research block (the inner holdout stays untouched).
Every backtest is opened in the trial ledger before it runs (Article 13)."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import read_json, write_json, path, sha256_file, ENGINE_VERSION  # noqa: E402
from engine.data import research_bars, fold_bounds, partition, INSTRUMENTS  # noqa: E402
from engine import metrics as M  # noqa: E402
from orchestrator.ledger import Ledger  # noqa: E402
from baseline import smart_trend_v1 as st  # noqa: E402

BASE = read_json(path("config/costs.lock.json"))["levels"]["base"]
TV = {s: partition()["instruments"][s]["tick_value"] for s in INSTRUMENTS}


def main():
    led = Ledger()
    folds = fold_bounds()
    n_search = partition()["research"]["search_sessions"]
    slices = {"search_all": (0, n_search), "wf_oos_folds_3_8": (folds[2][0], folds[7][1])}
    out = {"engine_version": ENGINE_VERSION, "cost_level": "base", "note":
           "Always in the market, no stop: violates Article 9, reference only. Positions carry overnight, so "
           "results include overnight gaps and any unadjusted roll jumps (data/DATA_QUALITY.md).", "rows": []}
    code_hash = sha256_file(path("baseline/smart_trend_v1.py"))
    for tf in (5, 15, 60):
        for mode, at_close in (("PINE_PARITY", True), ("DEFAULT", False)):
            frames = {}
            tids = {}
            for sym in INSTRUMENTS:
                tids[sym] = led.open(generation=0, stage="baseline", genome_id="smart_trend_v1", lineage_id="baseline",
                                     operator="BASELINE", data_slice="search_all", instrument=sym, timeframe_min=tf,
                                     cost_level="base", stress_mode=mode, seed=0, code_hash=code_hash,
                                     data_hash=partition()["blocks"][sym]["research_sha256"])
            led.commit()
            for sym in INSTRUMENTS:
                b = research_bars(sym, tf)
                T, eq = st.run(b, BASE, at_close)
                frames[sym] = M.trades_frame(T, b, generation=0)
            for name, (lo, hi) in slices.items():
                per = {}
                import pandas as pd
                sel = {s: f[(f.sess >= lo) & (f.sess < hi)] for s, f in frames.items()}
                for sym in INSTRUMENTS:
                    per[sym] = M.evaluate(sel[sym], np.arange(lo, hi), TV)
                pooled = M.evaluate(pd.concat(sel.values(), ignore_index=True), np.arange(lo, hi), TV)
                keep = ["n", "win_rate", "wilson_lo", "wilson_hi", "profit_factor", "payoff", "expectancy_usd",
                        "expectancy_ticks", "expectancy_costs", "net_usd", "trades_per_year", "largest_loss_in_avg_wins",
                        "max_dd_daily_usd", "sharpe"]
                out["rows"].append({"timeframe_min": tf, "mode": mode, "slice": name, "sessions": hi - lo,
                                    "pooled": {k: pooled.get(k) for k in keep},
                                    **{s: {k: per[s].get(k) for k in keep} for s in INSTRUMENTS}})
                if name == "search_all":
                    for sym in INSTRUMENTS:
                        m = per[sym]
                        led.close(tids[sym], n_trades=m["n"], win_rate=m["win_rate"], profit_factor=m["profit_factor"],
                                  expectancy_ticks=m["expectancy_ticks"], score=None)
            led.commit()
    write_json(path("baseline/reference_metrics.json"), out)
    print(f"{'tf':>3} {'mode':<12} {'slice':<18} {'inst':<6} {'n':>5} {'win%':>6} {'PF':>5} {'exp$':>8} {'tr/yr':>6} {'net$':>9}")
    for r in out["rows"]:
        for k in ("pooled",) + INSTRUMENTS:
            m = r[k]
            print(f"{r['timeframe_min']:>3} {r['mode']:<12} {r['slice']:<18} {k:<6} {m['n']:>5} {100*m['win_rate']:>6.1f} "
                  f"{m['profit_factor']:>5.2f} {m['expectancy_usd']:>8.1f} {m['trades_per_year']:>6.0f} {m['net_usd']:>9.0f}")


if __name__ == "__main__":
    main()
