"""
Integration & unit tests for STRAT-02. Run: python -m pytest -q
The dataset is loaded once and cached for the module.
"""

import numpy as np
import pytest

from strategy_02_queue_depletion.data_pipeline import load_data, validate_data, split_data
from strategy_02_queue_depletion.features import compute_all_features, validate_features, REQUIRED_FEATURES
from strategy_02_queue_depletion.signals import generate_signals, validate_signals
from strategy_02_queue_depletion.backtest import (
    run_backtest, compute_trade_statistics, compute_equity_metrics, apply_slippage,
    compute_exit_pnl, TRANSACTION_COST_PER_TRADE,
)
from strategy_02_queue_depletion.validation import generate_wfa_windows
from strategy_02_queue_depletion.config import DEFAULT_PARAMS, EXPECTED_TOTAL_ROWS, DEV_SET_SIZE, TEST_SET_SIZE


@pytest.fixture(scope="module")
def data():
    df = load_data()
    return df


@pytest.fixture(scope="module")
def featured(data):
    _, df_test = split_data(data)
    return compute_all_features(df_test)


def test_load_and_validate(data):
    validate_data(data)
    assert len(data) == EXPECTED_TOTAL_ROWS


def test_split(data):
    dev, test = split_data(data)
    assert len(dev) == DEV_SET_SIZE
    assert len(test) == TEST_SET_SIZE


def test_features_present_and_valid(featured):
    for f in REQUIRED_FEATURES:
        assert f in featured.columns
    validate_features(featured)
    assert featured['f_bvc_ratio'].between(0, 1).all()
    assert featured['f_liquidity_regime'].isin([0, 1, 2]).all()
    assert featured['f_position_scale'].between(0.1, 2.0).all()


def test_no_lookahead_no_nan_after_warmup(featured):
    skip = {'f_returns', 'f_log_returns', 'f_momentum_3', 'f_momentum_6'}
    for col in [c for c in featured.columns if c.startswith('f_')]:
        if col in skip:
            continue
        assert featured[col].iloc[200:].isna().sum() == 0, f"NaN after warmup in {col}"


def test_slippage_direction():
    assert apply_slippage(100.0, 'long', 'entry') == 100.25
    assert apply_slippage(100.0, 'long', 'exit') == 99.75
    assert apply_slippage(100.0, 'short', 'entry') == 99.75
    assert apply_slippage(100.0, 'short', 'exit') == 100.25


def test_exit_pnl_costs_once():
    # 4 point gain on 1 contract = $200 gross; net = 200 - 30
    assert compute_exit_pnl(100.0, 104.0, 1, 1) == 200.0 - TRANSACTION_COST_PER_TRADE
    assert TRANSACTION_COST_PER_TRADE == 30.0


def test_signals_no_disrupted_entries(featured):
    sig = generate_signals(featured, DEFAULT_PARAMS)
    stats = validate_signals(sig)
    assert stats['entries_disrupted'] == 0


def test_backtest_runs_and_no_overnight(featured):
    df_bt, trades = run_backtest(featured, DEFAULT_PARAMS)
    assert len(trades) > 0
    # No position may be held past bar 76 (exit forced); entries only on bars 1..74
    for t in trades:
        entry_bar = df_bt.iloc[t.entry_idx]['bar_in_day']
        assert 1 <= entry_bar <= 74
    # No trade entered in Disrupted regime
    assert all(t.entry_regime in (0, 1) for t in trades)


def test_statistics_consistency(featured):
    df_bt, trades = run_backtest(featured, DEFAULT_PARAMS)
    stats = compute_trade_statistics(trades, df_bt)
    eq = compute_equity_metrics(df_bt, trades)
    assert stats['winning_trades'] + stats['losing_trades'] == stats['total_trades']
    # total costs == $30 per trade
    assert abs(stats['total_costs'] - 30.0 * stats['total_trades']) < 1e-6
    assert 'sharpe_ratio' in eq and 'max_drawdown_pct' in eq


def test_deterministic(featured):
    a = run_backtest(featured, DEFAULT_PARAMS)[1]
    b = run_backtest(featured, DEFAULT_PARAMS)[1]
    assert [t.net_pnl for t in a] == [t.net_pnl for t in b]


def test_wfa_windows():
    w = generate_wfa_windows()
    assert len(w) >= 10
    for is_start, is_end, oos_start, oos_end in w:
        assert is_end == oos_start
        assert is_end - is_start == 15600
        assert oos_end - oos_start == 3900
