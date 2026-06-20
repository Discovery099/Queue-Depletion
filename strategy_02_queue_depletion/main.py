"""
Main execution script for Strategy 2.
Run: python -m strategy_02_queue_depletion.main
"""

import os
import json
import time
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from strategy_02_queue_depletion.config import (
    DATA_PATH, OUTPUT_DIR, DEFAULT_PARAMS, EXPECTED_TOTAL_ROWS,
    DEV_SET_SIZE, TEST_SET_SIZE, RANDOM_SEED,
)
from strategy_02_queue_depletion.data_pipeline import load_data, validate_data, split_data
from strategy_02_queue_depletion.features import compute_all_features, validate_features
from strategy_02_queue_depletion.signals import generate_signals, validate_signals
from strategy_02_queue_depletion.validation import (
    run_walk_forward_analysis, evaluate_on_test_set, check_parameter_stability,
    select_wfa_best_params,
)
from strategy_02_queue_depletion.reporting import save_all_reports


def _write_param_stability_csv(fold_results, stability, path):
    keys = list(stability.keys())
    rows = []
    for k in keys:
        row = {'parameter': k, 'mean': stability[k]['mean'], 'std': stability[k]['std'],
               'cv': stability[k]['cv'], 'mode': stability[k]['mode']}
        for f in fold_results:
            row[f"fold_{f['fold']}"] = f['best_params'][k]
        rows.append(row)
    pd.DataFrame(rows).to_csv(path, index=False)


def _write_wfa_csv(wfa_results: dict, path: str) -> None:
    rows = []
    for f in wfa_results['fold_results']:
        row = {k: v for k, v in f.items() if k != 'best_params'}
        for pk, pv in f['best_params'].items():
            row[f'param_{pk}'] = pv
        rows.append(row)
    pd.DataFrame(rows).to_csv(path, index=False)


def _write_summary_json(df_full, test_results, wfa_summary, best_params, path):
    ts = test_results['trade_stats']
    eq = test_results['equity_metrics']
    passes = test_results['passes_targets']
    summary = {
        "strategy": "Queue-Depletion Momentum with Liquidity Regime Filter",
        "strategy_code": "STRAT-02", "instrument": "ES", "bar_frequency": "5min",
        "data_range": {"start": str(df_full['ts_event'].iloc[0].date()),
                       "end": str(df_full['ts_event'].iloc[-1].date()),
                       "total_bars": int(len(df_full))},
        "train_test_split": {"dev_bars": DEV_SET_SIZE, "test_bars": TEST_SET_SIZE},
        "parameters": best_params,
        "test_set_results": {
            "total_trades": ts['total_trades'], "win_rate_pct": round(ts['win_rate']*100, 4),
            "trades_per_day": round(ts['trades_per_day'], 4),
            "wide_thin_accuracy_pct": round(ts.get('wide_thin_accuracy', 0)*100, 4),
            "tight_deep_accuracy_pct": round(ts.get('tight_deep_accuracy', 0)*100, 4),
            "sharpe_ratio": round(eq['sharpe_ratio'], 4), "sortino_ratio": round(eq['sortino_ratio'], 4),
            "max_drawdown_pct": round(eq['max_drawdown_pct'], 4),
            "profit_factor": round(ts['profit_factor'], 4),
            "total_net_pnl": round(ts['total_net_pnl'], 2),
            "avg_pnl_per_trade": round(ts['avg_pnl_per_trade'], 2),
        },
        "statistical_tests": {
            "binomial_p_value": test_results['binomial_test']['p_value'],
            "sharpe_p_value": test_results['sharpe_test']['p_value'],
            "permutation_p_value": test_results['permutation_test']['p_value'],
        },
        "walk_forward": {
            "num_folds": wfa_summary['num_folds'],
            "mean_oos_win_rate_pct": round(wfa_summary['mean_oos_win_rate']*100, 4),
            "mean_oos_sharpe": round(wfa_summary['mean_oos_sharpe'], 4),
            "consistency_score_pct": round(wfa_summary['consistency_score']*100, 4),
        },
        "targets_met": {**{k: bool(v) for k, v in passes.items()},
                        "all_pass": bool(all(passes.values()))},
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(path, "w") as f:
        json.dump(summary, f, indent=2)
    return summary


def main():
    np.random.seed(RANDOM_SEED)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    t0 = time.time()

    print("=" * 70)
    print("STRATEGY 2: Queue-Depletion Momentum with Liquidity Regime Filter")
    print("=" * 70)

    print("\n[1/7] Loading data...")
    df = load_data(DATA_PATH)
    validate_data(df)
    print(f"  Loaded {len(df):,} rows")

    print("\n[2/7] Splitting data...")
    df_dev, df_test = split_data(df)
    print(f"  Development: {len(df_dev):,} rows | Test: {len(df_test):,} rows")

    print("\n[2b] Validating features & signals on development set (default params)...")
    df_dev_feat = compute_all_features(df_dev)
    validate_features(df_dev_feat)
    df_dev_sig = generate_signals(df_dev_feat, DEFAULT_PARAMS)
    dev_sig_stats = validate_signals(df_dev_sig)
    print(f"  Dev entries: {dev_sig_stats['total_entries']} "
          f"({dev_sig_stats['trades_per_day']:.2f}/day), disrupted entries: "
          f"{dev_sig_stats['entries_disrupted']}")

    print("\n[3/7] Running walk-forward analysis (full grid search per fold)...")
    wfa_results = run_walk_forward_analysis(df_dev)
    wfa = wfa_results['summary']
    print(f"  Folds: {wfa['num_folds']}")
    print(f"  Mean OOS Win Rate: {wfa['mean_oos_win_rate']*100:.2f}%")
    print(f"  Mean OOS Sharpe:   {wfa['mean_oos_sharpe']:.3f}")
    print(f"  Consistency Score: {wfa['consistency_score']*100:.1f}%")
    print(f"  Mean WT Accuracy:  {wfa['mean_wide_thin_accuracy']*100:.2f}%")

    # Final parameters: chosen from WFA, weighted by each fold's OOS objective
    # (development-set only; no test-set tuning).
    best_params = select_wfa_best_params(wfa_results['fold_results'], method='weighted')
    print(f"  WFA-selected params (OOS-objective weighted): {best_params}")

    print("\n[4/7] Evaluating on TEST set (final, run once)...")
    test_results = evaluate_on_test_set(df_test, best_params)
    ts, eq = test_results['trade_stats'], test_results['equity_metrics']
    print(f"  Test Trades:       {ts['total_trades']}")
    print(f"  Test Win Rate:     {ts['win_rate']*100:.2f}%")
    print(f"  Test Trades/Day:   {ts['trades_per_day']:.2f}")
    print(f"  Test WT Accuracy:  {ts.get('wide_thin_accuracy', 0)*100:.2f}%")
    print(f"  Test Sharpe:       {eq['sharpe_ratio']:.3f}")
    print(f"  Test Max DD:       {eq['max_drawdown_pct']:.2f}%")
    print(f"  Test Profit Factor:{ts['profit_factor']:.3f}")

    print("\n[5/7] Checking acceptance targets...")
    for target, passed in test_results['passes_targets'].items():
        print(f"  {target:24s}: {'PASS' if passed else 'FAIL'}")

    print("\n[6/7] Generating reports & charts...")
    df_bt = generate_signals(test_results['df_bt'], best_params)
    report = save_all_reports(df_bt, test_results['trades'])
    _write_wfa_csv(wfa_results, os.path.join(OUTPUT_DIR, "strategy_02_wfa_results.csv"))
    stability = check_parameter_stability(wfa_results['fold_results'])
    _write_param_stability_csv(wfa_results['fold_results'], stability,
                               os.path.join(OUTPUT_DIR, "strategy_02_param_stability.csv"))
    summary = _write_summary_json(
        df, test_results, wfa, best_params,
        os.path.join(OUTPUT_DIR, "strategy_02_summary.json"))
    print(report)

    print("\n[7/7] Statistical significance tests...")
    print(f"  Binomial p-value:    {test_results['binomial_test']['p_value']:.6f}")
    print(f"  Sharpe p-value:      {test_results['sharpe_test']['p_value']:.6f}")
    print(f"  Permutation p-value: {test_results['permutation_test']['p_value']:.6f}")

    print("\n" + "=" * 70)
    print(f"BACKTEST COMPLETE in {time.time()-t0:.1f}s — outputs in {OUTPUT_DIR}")
    print(f"ALL TARGETS PASS: {summary['targets_met']['all_pass']}")
    print("=" * 70)
    return test_results


if __name__ == "__main__":
    main()
