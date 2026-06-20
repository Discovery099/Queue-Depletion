"""
Diagnostic harness for STRAT-02.

Checks whether the strategy's edge is merely sign-inverted, and sweeps a few
feature/threshold variants to see whether any profitable configuration exists on
this ES data. Read-only analysis — does not change the strategy.

Run: python -m strategy_02_queue_depletion.diagnostics
"""

import os
import json
from itertools import product

import numpy as np

from strategy_02_queue_depletion.config import DEFAULT_PARAMS, OUTPUT_DIR, RANDOM_SEED
from strategy_02_queue_depletion.data_pipeline import load_data, split_data
from strategy_02_queue_depletion.validation import _evaluate_fast


def _metrics(df, params):
    stats, equity = _evaluate_fast(df, params)
    return {
        'trades': stats['total_trades'],
        'win_rate_pct': round(stats['win_rate'] * 100, 2),
        'trades_per_day': round(stats['trades_per_day'], 2),
        'wt_acc_pct': round(stats['wide_thin_accuracy'] * 100, 2),
        'td_acc_pct': round(stats['tight_deep_accuracy'] * 100, 2),
        'profit_factor': round(stats['profit_factor'], 3),
        'net_pnl': round(stats['total_net_pnl'], 0),
        'sharpe': round(equity['sharpe_ratio'], 3),
        'max_dd_pct': round(equity['max_drawdown_pct'], 2),
    }


def _row(label, m):
    return (f"  {label:34s} trades={m['trades']:>5d}  wr={m['win_rate_pct']:>6.2f}%  "
            f"tpd={m['trades_per_day']:>5.2f}  pf={m['profit_factor']:>6.3f}  "
            f"pnl=${m['net_pnl']:>10,.0f}  sharpe={m['sharpe']:>6.3f}")


def run_diagnostics():
    np.random.seed(RANDOM_SEED)
    df = load_data()
    df_dev, df_test = split_data(df)

    loose = dict(dep_threshold=0.05, tox_threshold=0.05, momentum_confirm=0.0,
                 breakthrough_threshold=0.02, exit_bars=4, profit_target_pct=0.8,
                 stop_loss_pct=0.6, min_volume_pctile=10.0)

    presets = {'default': DEFAULT_PARAMS, 'loose': loose}
    results = {'sign_inversion': {}, 'threshold_sweep': {}}

    print("=" * 90)
    print("STRAT-02 DIAGNOSTIC 1 — Sign Inversion (baseline vs. flipped long/short)")
    print("=" * 90)
    for pname, base in presets.items():
        for split_name, dfx in [('DEV', df_dev), ('TEST', df_test)]:
            normal = _metrics(dfx, {**base, 'invert_signal': False})
            inverted = _metrics(dfx, {**base, 'invert_signal': True})
            key = f"{pname}_{split_name}"
            results['sign_inversion'][key] = {'normal': normal, 'inverted': inverted}
            print(f"\n[{pname.upper()} params | {split_name}]")
            print(_row("normal", normal))
            print(_row("inverted", inverted))

    print("\n" + "=" * 90)
    print("STRAT-02 DIAGNOSTIC 2 — Threshold sweep on DEV (best by Sharpe), validated on TEST")
    print("=" * 90)
    grid = {
        'dep_threshold': [0.05, 0.10, 0.20],
        'tox_threshold': [0.05, 0.20, 0.40],
        'min_volume_pctile': [10.0, 30.0, 50.0],
        'invert_signal': [False, True],
    }
    fixed = dict(momentum_confirm=0.0, breakthrough_threshold=0.05,
                 exit_bars=4, profit_target_pct=0.8, stop_loss_pct=0.6)
    keys = list(grid.keys())
    best = None
    for combo in product(*[grid[k] for k in keys]):
        params = {**fixed, **dict(zip(keys, combo))}
        m = _metrics(df_dev, params)
        if m['trades'] < 200:  # require statistical mass
            continue
        if best is None or m['sharpe'] > best[1]['sharpe']:
            best = (params, m)
    if best:
        bp, dev_m = best
        test_m = _metrics(df_test, bp)
        results['threshold_sweep'] = {'params': {k: bp[k] for k in keys},
                                      'dev': dev_m, 'test': test_m}
        print(f"\n  Best DEV config: { {k: bp[k] for k in keys} }")
        print(_row("  -> DEV", dev_m))
        print(_row("  -> TEST", test_m))
    else:
        print("  No configuration produced >=200 trades.")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, "strategy_02_diagnostics.json")
    with open(path, "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 90)
    print("CONCLUSION")
    di = results['sign_inversion']['default_TEST']
    print(f"  Default TEST: normal Sharpe {di['normal']['sharpe']} vs inverted "
          f"{di['inverted']['sharpe']}.")
    print("  If inverted Sharpe is strongly positive, the published signal direction is")
    print("  likely backwards on this data; otherwise no simple sign edge exists.")
    print(f"  Full results written to {path}")
    print("=" * 90)
    return results


if __name__ == "__main__":
    run_diagnostics()
