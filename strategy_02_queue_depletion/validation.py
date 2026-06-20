"""
Validation framework (Section 5): walk-forward analysis, grid-search optimization,
statistical significance tests, and final test-set evaluation.
"""

from typing import List, Tuple, Dict
from itertools import product
import numpy as np
import pandas as pd
from scipy import stats as scipy_stats

from strategy_02_queue_depletion.config import (
    DEV_SET_SIZE, WFA_IS_SIZE, WFA_OOS_SIZE, WFA_MAX_EVALS,
    DEFAULT_PARAMS, PARAM_GRID, ES_POINT_VALUE, TRANSACTION_COST_PER_TRADE,
    RANDOM_SEED,
)
from strategy_02_queue_depletion.features import compute_all_features
from strategy_02_queue_depletion.backtest import (
    extract_arrays, fast_metrics, run_backtest,
    compute_trade_statistics, compute_equity_metrics,
)


# ---------------------------------------------------------------------------
# Walk-forward windows
# ---------------------------------------------------------------------------
def generate_wfa_windows(dev_size: int = DEV_SET_SIZE, is_size: int = WFA_IS_SIZE,
                         oos_size: int = WFA_OOS_SIZE) -> List[Tuple[int, int, int, int]]:
    windows = []
    oos_start = is_size
    while oos_start + oos_size <= dev_size:
        windows.append((oos_start - is_size, oos_start, oos_start, oos_start + oos_size))
        oos_start += oos_size
    return windows


# ---------------------------------------------------------------------------
# Optimization
# ---------------------------------------------------------------------------
def objective_function(stats: dict, equity: dict) -> float:
    """Combined optimization objective (Section 5.2.2). Higher is better."""
    score = 0.0
    wr = stats['win_rate']
    if wr < 0.525:
        score -= 100
    else:
        score += 40 * min((wr - 0.50) / 0.10, 1.0)

    tpd = stats['trades_per_day']
    if tpd < 4.5:
        score -= 50
    else:
        score += 20 * min(tpd / 10.0, 1.0)

    wt_acc = stats.get('wide_thin_accuracy', 0)
    if wt_acc < 0.54:
        score -= 50
    else:
        score += 25 * min((wt_acc - 0.50) / 0.10, 1.0)

    sharpe = equity.get('sharpe_ratio', 0)
    score += 15 * min(max(sharpe, 0) / 2.0, 1.0)

    mdd = abs(equity.get('max_drawdown_pct', 0))
    if mdd > 15:
        score -= 50
    elif mdd > 10:
        score -= 20 * (mdd - 10) / 5
    return score


def optimize_parameters(df_is: pd.DataFrame, param_grid: dict = PARAM_GRID,
                        max_evals: int = WFA_MAX_EVALS) -> dict:
    """Grid search with early stopping. Features computed once (param-independent)."""
    df_feat = compute_all_features(df_is)
    a = extract_arrays(df_feat)
    trading_days = df_feat['date'].nunique()

    keys = list(param_grid.keys())
    values = [param_grid[k] for k in keys]

    best_score = -float('inf')
    best_params = None
    eval_count = 0
    for combo in product(*values):
        if eval_count >= max_evals:
            break
        params = dict(zip(keys, combo))
        stats, equity = fast_metrics(a, params, trading_days)
        if stats['total_trades'] == 0:
            eval_count += 1
            continue
        score = objective_function(stats, equity)
        if score > best_score:
            best_score = score
            best_params = params.copy()
        eval_count += 1

    if best_params is None:
        best_params = DEFAULT_PARAMS.copy()
    return best_params


def _evaluate_fast(df: pd.DataFrame, params: dict) -> Tuple[dict, dict]:
    """Compute fast metrics for a raw (un-featured) DataFrame slice."""
    df_feat = compute_all_features(df)
    a = extract_arrays(df_feat)
    trading_days = df_feat['date'].nunique()
    return fast_metrics(a, params, trading_days)


# ---------------------------------------------------------------------------
# Walk-forward loop
# ---------------------------------------------------------------------------
def run_walk_forward_analysis(df_dev: pd.DataFrame, param_grid: dict = PARAM_GRID) -> dict:
    windows = generate_wfa_windows()
    fold_results = []
    for fold_num, (is_start, is_end, oos_start, oos_end) in enumerate(windows, 1):
        print(f"  WFA Fold {fold_num}/{len(windows)}: IS [{is_start}:{is_end}] OOS [{oos_start}:{oos_end}]")
        df_is = df_dev.iloc[is_start:is_end].copy()
        df_oos = df_dev.iloc[oos_start:oos_end].copy()

        best_params = optimize_parameters(df_is, param_grid)
        is_stats, _ = _evaluate_fast(df_is, best_params)
        oos_stats, oos_equity = _evaluate_fast(df_oos, best_params)

        fold_results.append({
            'fold': fold_num, 'is_start': is_start, 'is_end': is_end,
            'oos_start': oos_start, 'oos_end': oos_end, 'best_params': best_params,
            'is_win_rate': is_stats['win_rate'], 'is_trades_per_day': is_stats['trades_per_day'],
            'oos_win_rate': oos_stats['win_rate'], 'oos_trades_per_day': oos_stats['trades_per_day'],
            'oos_sharpe': oos_equity['sharpe_ratio'], 'oos_max_dd': oos_equity['max_drawdown_pct'],
            'oos_total_pnl': oos_stats['total_net_pnl'],
            'wide_thin_accuracy': oos_stats['wide_thin_accuracy'],
            'tight_deep_accuracy': oos_stats['tight_deep_accuracy'],
        })
    return {'fold_results': fold_results, 'summary': summarize_wfa_results(fold_results)}


def summarize_wfa_results(fold_results: List[dict]) -> dict:
    s = {}
    wr = [f['oos_win_rate'] for f in fold_results]
    s['mean_oos_win_rate'] = float(np.mean(wr))
    s['std_oos_win_rate'] = float(np.std(wr))
    s['min_oos_win_rate'] = float(np.min(wr))
    s['pct_folds_above_52.5'] = float(np.mean([w > 0.525 for w in wr]))
    s['pct_folds_above_54'] = float(np.mean([w > 0.54 for w in wr]))
    tpd = [f['oos_trades_per_day'] for f in fold_results]
    s['mean_oos_trades_per_day'] = float(np.mean(tpd))
    s['min_oos_trades_per_day'] = float(np.min(tpd))
    sh = [f['oos_sharpe'] for f in fold_results]
    s['mean_oos_sharpe'] = float(np.mean(sh))
    s['pct_folds_sharpe_positive'] = float(np.mean([x > 0 for x in sh]))
    wta = [f['wide_thin_accuracy'] for f in fold_results]
    s['mean_wide_thin_accuracy'] = float(np.mean(wta))
    s['pct_folds_wt_above_54'] = float(np.mean([w > 0.54 for w in wta]))
    s['pct_folds_wt_above_56'] = float(np.mean([w > 0.56 for w in wta]))
    meets = [(f['oos_win_rate'] > 0.525 and f['oos_trades_per_day'] > 4.5 and
              f['wide_thin_accuracy'] > 0.54) for f in fold_results]
    s['consistency_score'] = float(np.mean(meets))
    s['num_folds'] = len(fold_results)
    return s


def check_parameter_stability(fold_results: List[dict]) -> dict:
    keys = list(DEFAULT_PARAMS.keys())
    out = {}
    for k in keys:
        vals = [f['best_params'][k] for f in fold_results]
        arr = np.array(vals, dtype=float)
        mean = arr.mean()
        out[k] = {'mean': float(mean), 'std': float(arr.std()),
                  'cv': float(arr.std() / mean) if mean != 0 else 0.0,
                  'mode': float(pd.Series(vals).mode().iloc[0])}
    return out


# ---------------------------------------------------------------------------
# Statistical tests (Section 5.4)
# ---------------------------------------------------------------------------
def _wilson_ci(k: int, n: int, alpha: float = 0.05) -> Tuple[float, float]:
    if n == 0:
        return 0.0, 0.0
    z = scipy_stats.norm.ppf(1 - alpha / 2)
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = (z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return float(center - half), float(center + half)


def test_win_rate_significance(num_wins: int, num_trades: int,
                               null_hypothesis_wr: float = 0.50) -> dict:
    res = scipy_stats.binomtest(num_wins, num_trades, null_hypothesis_wr, alternative='greater')
    p = res.pvalue
    lo, hi = _wilson_ci(num_wins, num_trades)
    return {'p_value': float(p), 'significant_at_5pct': p < 0.05,
            'significant_at_1pct': p < 0.01, 'ci_95_low': lo, 'ci_95_high': hi}


def test_sharpe_significance(sharpe: float, num_obs: int) -> dict:
    t_stat = sharpe * np.sqrt(num_obs)
    p_value = 1 - scipy_stats.t.cdf(t_stat, df=num_obs - 1)
    return {'t_statistic': float(t_stat), 'p_value': float(p_value),
            'significant_at_5pct': p_value < 0.05, 'significant_at_1pct': p_value < 0.01}


def permutation_test(df: pd.DataFrame, trades: List, n_permutations: int = 1000) -> dict:
    np.random.seed(RANDOM_SEED)
    actual_pnl = sum(t.net_pnl for t in trades)
    trade_info = [(t.bars_held, t.entry_idx, t.num_contracts) for t in trades]
    close = df['close'].to_numpy()
    n = len(close)
    permuted = np.empty(n_permutations)
    for j in range(n_permutations):
        perm_pnl = 0.0
        for bars_held, entry_idx, ncon in trade_info:
            direction = np.random.choice([-1, 1])
            ep = close[entry_idx]
            xi = min(entry_idx + bars_held, n - 1)
            xp = close[xi]
            pnl = (xp - ep) if direction == 1 else (ep - xp)
            perm_pnl += pnl * ES_POINT_VALUE * ncon - TRANSACTION_COST_PER_TRADE
        permuted[j] = perm_pnl
    p_value = float(np.mean(permuted >= actual_pnl))
    return {'actual_pnl': float(actual_pnl), 'perm_mean_pnl': float(permuted.mean()),
            'perm_std_pnl': float(permuted.std()), 'perm_95pct_pnl': float(np.percentile(permuted, 95)),
            'p_value': p_value, 'significant_at_5pct': p_value < 0.05}


# ---------------------------------------------------------------------------
# Final test-set evaluation
# ---------------------------------------------------------------------------
def check_targets(stats: dict, equity: dict, binomial: dict) -> dict:
    return {
        'overall_win_rate': stats['win_rate'] >= 0.525,
        'trades_per_day': stats['trades_per_day'] >= 4.5,
        'wide_thin_accuracy': stats.get('wide_thin_accuracy', 0) >= 0.54,
        'disrupted_trades_zero': stats.get('disrupted_trades', 0) == 0,
        'sharpe_ratio': equity['sharpe_ratio'] >= 0.7,
        'max_drawdown': abs(equity['max_drawdown_pct']) < 15.0,
        'profit_factor': stats['profit_factor'] >= 1.08,
        'binomial_significant': binomial['p_value'] < 0.05,
    }


def evaluate_on_test_set(df_test: pd.DataFrame, best_params: dict) -> dict:
    """FINAL evaluation on the test set. Run exactly once."""
    df_feat = compute_all_features(df_test)
    df_bt, trades = run_backtest(df_feat, best_params)
    trade_stats = compute_trade_statistics(trades, df_bt)
    equity_metrics = compute_equity_metrics(df_bt, trades)

    binomial = test_win_rate_significance(trade_stats['winning_trades'], trade_stats['total_trades'])
    sharpe_test = test_sharpe_significance(equity_metrics['sharpe_ratio'], len(df_bt))
    perm = permutation_test(df_bt, trades)
    passes = check_targets(trade_stats, equity_metrics, binomial)

    return {'trade_stats': trade_stats, 'equity_metrics': equity_metrics,
            'binomial_test': binomial, 'sharpe_test': sharpe_test,
            'permutation_test': perm, 'passes_targets': passes,
            'df_bt': df_bt, 'trades': trades}
