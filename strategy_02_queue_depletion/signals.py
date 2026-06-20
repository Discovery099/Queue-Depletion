"""
Signal generation engine (Section 3). The bar-by-bar entry/exit logic is
implemented in the shared numpy core (`backtest._simulate`); `generate_signals`
populates the sig_* columns from that single source of truth. The explicit
per-row functions below mirror the specification exactly and are used for
unit-level verification.
"""

from typing import Tuple
import numpy as np
import pandas as pd

from strategy_02_queue_depletion.backtest import extract_arrays, _simulate


# ---------------------------------------------------------------------------
# Spec-faithful per-row reference functions (Section 3.3 / 3.4)
# ---------------------------------------------------------------------------
def check_entry_guards(df: pd.DataFrame, idx: int, params: dict) -> bool:
    row = df.iloc[idx]
    if row['f_liquidity_regime'] == 2:
        return False
    if abs(row['f_depletion_ma_5']) < params['dep_threshold']:
        return False
    if abs(row['f_toxicity_ma_5']) < params['tox_threshold']:
        return False
    vol_window = df['volume'].iloc[max(0, idx - 99):idx + 1]
    vol_pctile = (row['volume'] - vol_window.min()) / (vol_window.max() - vol_window.min() + 1e-10)
    if vol_pctile < params['min_volume_pctile'] / 100.0:
        return False
    if row['bar_in_day'] == 0:
        return False
    if row['bar_in_day'] >= 75:
        return False
    if row['f_atr_20'] < 1.0:
        return False
    critical = ['f_depletion_ma_5', 'f_toxicity_ma_5', 'f_liquidity_regime', 'f_atr_20', 'f_momentum_3']
    if any(pd.isna(row[f]) for f in critical):
        return False
    return True


def entry_tight_deep(df: pd.DataFrame, idx: int, params: dict) -> int:
    row = df.iloc[idx]
    if not check_entry_guards(df, idx, params) or row['f_liquidity_regime'] != 0:
        return 0
    if row['f_depletion_ma_5'] > 0 and row['f_momentum_3'] > params['momentum_confirm'] and row['f_ema_diff'] > 0:
        return 1
    if row['f_depletion_ma_5'] < 0 and row['f_momentum_3'] < -params['momentum_confirm'] and row['f_ema_diff'] < 0:
        return -1
    return 0


def entry_wide_thin(df: pd.DataFrame, idx: int, params: dict) -> int:
    row = df.iloc[idx]
    if not check_entry_guards(df, idx, params) or row['f_liquidity_regime'] != 1:
        return 0
    if (row['f_depletion_diff'] > params['breakthrough_threshold']
            and row['f_bar_range'] > row['f_atr_20_pct'] * 1.2 and row['f_volume_ratio'] > 1.5):
        return 1
    if (row['f_depletion_diff'] < -params['breakthrough_threshold']
            and row['f_bar_range'] > row['f_atr_20_pct'] * 1.2 and row['f_volume_ratio'] > 1.5):
        return -1
    return 0


# ---------------------------------------------------------------------------
# Vectorized signal column population (consistent with the backtest engine)
# ---------------------------------------------------------------------------
def generate_signals(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    """Populate sig_direction, sig_strength, sig_regime, sig_action columns."""
    df = df.copy()
    n = len(df)
    a = extract_arrays(df)
    rec, _, _, position, _ = _simulate(a, params)

    sig_direction = position.astype(int).copy()
    sig_action = np.array(['none'] * n, dtype=object)
    sig_regime = np.full(n, -1, dtype=int)
    sig_strength = np.zeros(n)

    dep5 = df['f_depletion_ma_5'].to_numpy()
    tox5 = df['f_toxicity_ma_5'].to_numpy()
    p_dep, p_tox = params['dep_threshold'], params['tox_threshold']

    # Hold bars = in position (will be overwritten on entry/exit bars)
    in_pos = position != 0
    sig_action[in_pos] = 'hold'

    for (ei, xi, d, ep, xp, er, nc, gross, net, bh, rc, mae, mfe) in rec:
        sig_action[ei] = 'enter_long' if d == 1 else 'enter_short'
        sig_direction[ei] = d
        sig_regime[ei] = er
        dep_c = min(abs(dep5[ei]) / (p_dep * 3), 1.0)
        tox_c = min(abs(tox5[ei]) / (p_tox * 3), 1.0)
        sig_strength[ei] = max(0.1, min(1.0, 0.5 * dep_c + 0.5 * tox_c))
        # mark hold bars between entry and exit with entry regime
        for k in range(ei + 1, xi):
            sig_regime[k] = er
        sig_action[xi] = 'exit'
        sig_direction[xi] = 0
        sig_regime[xi] = er

    df['sig_direction'] = sig_direction
    df['sig_strength'] = sig_strength
    df['sig_regime'] = sig_regime
    df['sig_action'] = sig_action
    return df


def validate_signals(df: pd.DataFrame) -> dict:
    """Validate generated signals and return statistics (Section 3.6)."""
    stats = {}
    entries = df[df['sig_action'].isin(['enter_long', 'enter_short'])]
    stats['total_entries'] = len(entries)
    for regime, name in [(0, 'tight_deep'), (1, 'wide_thin'), (2, 'disrupted')]:
        stats[f'entries_{name}'] = len(entries[entries['sig_regime'] == regime])
    stats['long_entries'] = len(entries[entries['sig_action'] == 'enter_long'])
    stats['short_entries'] = len(entries[entries['sig_action'] == 'enter_short'])
    stats['signal_rate'] = stats['total_entries'] / len(df) if len(df) else 0
    trading_days = df['date'].nunique()
    stats['trades_per_day'] = stats['total_entries'] / trading_days if trading_days else 0
    rc = df['f_liquidity_regime'].value_counts(normalize=True)
    stats['regime_0_pct'] = rc.get(0, 0)
    stats['regime_1_pct'] = rc.get(1, 0)
    stats['regime_2_pct'] = rc.get(2, 0)

    assert stats['entries_disrupted'] == 0, "Entries detected in Disrupted regime!"
    return stats
