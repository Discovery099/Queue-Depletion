"""
Feature engineering (Section 2). Fully vectorized for speed; numerically identical
to the per-row specification. Features computed in the exact dependency order.
"""

import numpy as np
import pandas as pd

from strategy_02_queue_depletion.config import (
    ATR_WINDOW, VOL_WINDOW_SHORT, VOL_WINDOW_LONG, VOLUME_MA_WINDOW,
    DEPLETION_MA_FAST, DEPLETION_MA_SLOW, LIQUIDITY_QUANTILE_WINDOW,
    POSITION_SCALE_WINDOW, MOMENTUM_SHORT, MOMENTUM_LONG, EMA_FAST, EMA_SLOW,
    ANNUALIZATION,
)

REQUIRED_FEATURES = [
    'f_returns', 'f_log_returns', 'f_true_range', 'f_bar_range',
    'f_body_size', 'f_body_direction', 'f_upper_shadow', 'f_lower_shadow',
    'f_bvc_ratio', 'f_bvc_buy_vol', 'f_bvc_sell_vol', 'f_bvc_imbalance', 'f_bvc_sign',
    'f_atr_20', 'f_atr_20_pct', 'f_vol_realized_20', 'f_vol_realized_60', 'f_vol_ratio',
    'f_volume_sma_20', 'f_volume_ratio', 'f_volume_zscore_20', 'f_relative_volume',
    'f_depletion_raw', 'f_depletion_abs', 'f_depletion_ma_5', 'f_depletion_ma_10', 'f_depletion_diff',
    'f_liquidity_score', 'f_liquidity_q33', 'f_liquidity_q66', 'f_liquidity_regime',
    'f_regime_tight_deep', 'f_regime_wide_thin', 'f_regime_disrupted',
    'f_toxicity_raw', 'f_toxicity_ma_5', 'f_toxicity_zscore',
    'f_ema_12', 'f_ema_26', 'f_ema_diff', 'f_price_vs_ema20', 'f_momentum_3', 'f_momentum_6',
    'f_regime_adjusted_signal', 'f_position_scale',
]


def _raw_price_features(df: pd.DataFrame) -> None:
    c, h, l, o = df['close'], df['high'], df['low'], df['open']
    df['f_returns'] = c.pct_change()
    df['f_log_returns'] = np.log(c / c.shift(1))
    prev_close = c.shift(1)
    tr = np.maximum(h - l, np.maximum((h - prev_close).abs(), (l - prev_close).abs()))
    df['f_true_range'] = tr.fillna(h - l)
    df['f_bar_range'] = (h - l) / c
    df['f_body_size'] = (c - o).abs() / c
    df['f_body_direction'] = np.sign(c - o).astype('int8')
    df['f_upper_shadow'] = (h - np.maximum(o, c)) / c
    df['f_lower_shadow'] = (np.minimum(o, c) - l) / c


def _bvc_features(df: pd.DataFrame) -> None:
    hl = df['high'] - df['low']
    df['f_bvc_ratio'] = np.where(hl > 0, (df['close'] - df['low']) / hl.replace(0, np.nan), 0.5)
    df['f_bvc_ratio'] = pd.Series(df['f_bvc_ratio'], index=df.index).fillna(0.5).clip(0.0, 1.0)
    df['f_bvc_buy_vol'] = df['f_bvc_ratio'] * df['volume']
    df['f_bvc_sell_vol'] = (1 - df['f_bvc_ratio']) * df['volume']
    df['f_bvc_imbalance'] = 2 * df['f_bvc_ratio'] - 1
    df['f_bvc_sign'] = np.sign(df['f_bvc_imbalance']).astype('int8')


def _volatility_features(df: pd.DataFrame) -> None:
    df['f_atr_20'] = df['f_true_range'].rolling(ATR_WINDOW, min_periods=1).mean()
    df['f_atr_20_pct'] = df['f_atr_20'] / df['close']
    df['f_vol_realized_20'] = np.sqrt(
        ANNUALIZATION * df['f_log_returns'].rolling(VOL_WINDOW_SHORT, min_periods=5).var())
    df['f_vol_realized_60'] = np.sqrt(
        ANNUALIZATION * df['f_log_returns'].rolling(VOL_WINDOW_LONG, min_periods=20).var())
    ratio = df['f_vol_realized_20'] / df['f_vol_realized_60']
    df['f_vol_ratio'] = ratio.replace([np.inf, -np.inf], np.nan).fillna(1.0)


def _volume_features(df: pd.DataFrame) -> None:
    df['f_volume_sma_20'] = df['volume'].rolling(VOLUME_MA_WINDOW, min_periods=1).mean()
    ratio = df['volume'] / df['f_volume_sma_20'].replace(0, np.nan)
    df['f_volume_ratio'] = ratio.fillna(1.0)
    vstd = df['volume'].rolling(VOLUME_MA_WINDOW, min_periods=5).std()
    z = (df['volume'] - df['f_volume_sma_20']) / vstd.replace(0, np.nan)
    df['f_volume_zscore_20'] = z.fillna(0.0)
    df['f_relative_volume'] = df['f_volume_ratio']


def _depletion_features(df: pd.DataFrame) -> None:
    f_bvc_signed = 2 * df['f_bvc_ratio'] - 1
    range_expansion = (df['f_bar_range'] / df['f_atr_20_pct'].replace(0, np.nan)).fillna(1.0).clip(upper=10.0)
    vol_indicator = (df['volume'] > df['f_volume_sma_20']).astype(float)
    df['f_depletion_raw'] = f_bvc_signed * range_expansion * vol_indicator
    df['f_depletion_abs'] = df['f_depletion_raw'].abs()
    df['f_depletion_ma_5'] = df['f_depletion_raw'].rolling(DEPLETION_MA_FAST, min_periods=1).mean()
    df['f_depletion_ma_10'] = df['f_depletion_raw'].rolling(DEPLETION_MA_SLOW, min_periods=3).mean()
    df['f_depletion_diff'] = df['f_depletion_ma_5'] - df['f_depletion_ma_10']


def _liquidity_features(df: pd.DataFrame) -> None:
    rel_vol = (df['volume'] / df['f_volume_sma_20'].replace(0, np.nan)).fillna(1.0).clip(lower=0.1)
    score = df['f_bar_range'] * (rel_vol ** (-0.5))
    df['f_liquidity_score'] = score.fillna(score.median())
    q33 = df['f_liquidity_score'].rolling(LIQUIDITY_QUANTILE_WINDOW, min_periods=50).quantile(0.33)
    q66 = df['f_liquidity_score'].rolling(LIQUIDITY_QUANTILE_WINDOW, min_periods=50).quantile(0.66)
    df['f_liquidity_q33'] = q33
    df['f_liquidity_q66'] = q66

    s = df['f_liquidity_score']
    regime = np.full(len(df), 1, dtype=np.int8)  # default Wide-Thin where thresholds unavailable
    valid = q33.notna().values & q66.notna().values
    sv, q33v, q66v = s.values, q33.values, q66.values
    regime[valid & (sv < q33v)] = 0
    regime[valid & (sv >= q33v) & (sv < q66v)] = 1
    regime[valid & (sv >= q66v)] = 2
    df['f_liquidity_regime'] = regime
    df['f_regime_tight_deep'] = (regime == 0).astype('int8')
    df['f_regime_wide_thin'] = (regime == 1).astype('int8')
    df['f_regime_disrupted'] = (regime == 2).astype('int8')


def _toxicity_features(df: pd.DataFrame) -> None:
    denom = df['f_vol_realized_20'].replace(0, np.nan).fillna(0.1).clip(lower=0.001)
    tox = df['f_depletion_raw'] * df['f_depletion_abs'] / denom
    df['f_toxicity_raw'] = tox.clip(lower=-100, upper=100)
    df['f_toxicity_ma_5'] = df['f_toxicity_raw'].rolling(5, min_periods=1).mean()
    mean60 = df['f_toxicity_raw'].rolling(60, min_periods=20).mean()
    std60 = df['f_toxicity_raw'].rolling(60, min_periods=20).std()
    z = (df['f_toxicity_raw'] - mean60) / std60.replace(0, np.nan)
    df['f_toxicity_zscore'] = z.fillna(0.0)


def _trend_features(df: pd.DataFrame) -> None:
    c = df['close']
    df['f_ema_12'] = c.ewm(span=EMA_FAST, min_periods=3).mean()
    df['f_ema_26'] = c.ewm(span=EMA_SLOW, min_periods=5).mean()
    df['f_ema_diff'] = (df['f_ema_12'] - df['f_ema_26']) / c
    df['f_price_vs_ema20'] = (c - c.ewm(span=20, min_periods=5).mean()) / c
    df['f_momentum_3'] = (c - c.shift(MOMENTUM_SHORT)) / c.shift(MOMENTUM_SHORT)
    df['f_momentum_6'] = (c - c.shift(MOMENTUM_LONG)) / c.shift(MOMENTUM_LONG)


def _composite_signal(df: pd.DataFrame) -> None:
    regime = df['f_liquidity_regime'].values
    dep5 = df['f_depletion_ma_5'].values
    tox5 = df['f_toxicity_ma_5'].values
    dep_diff = df['f_depletion_diff'].values
    mom3 = np.nan_to_num(df['f_momentum_3'].values)
    mom6 = np.nan_to_num(df['f_momentum_6'].values)

    out = np.zeros(len(df))
    nan_mask = np.isnan(dep5) | np.isnan(tox5)

    # Tight-Deep (regime 0): continuation
    m0 = (regime == 0) & ~nan_mask
    mult0 = np.maximum(1.0 + 0.5 * mom3, 0.1)
    out[m0] = np.sign(dep5[m0]) * tox5[m0] * mult0[m0]

    # Wide-Thin (regime 1): breakthrough
    m1 = (regime == 1) & ~nan_mask
    mult1 = np.maximum(1.0 + 0.3 * np.abs(mom6), 0.1)
    out[m1] = np.sign(dep_diff[m1]) * tox5[m1] * mult1[m1]

    # Disrupted (regime 2) and NaN -> 0 (already zero)
    df['f_regime_adjusted_signal'] = out


def _position_sizing(df: pd.DataFrame) -> None:
    dep_mean = df['f_depletion_abs'].rolling(POSITION_SCALE_WINDOW, min_periods=20).mean()
    scale = (df['f_depletion_abs'] / dep_mean.replace(0, np.nan)).fillna(1.0)
    df['f_position_scale'] = scale.clip(upper=2.0, lower=0.1)


def _helper_columns(df: pd.DataFrame) -> None:
    """Engine helpers (not part of the spec feature list). Rolling 100-bar volume percentile."""
    vmin = df['volume'].rolling(100, min_periods=1).min()
    vmax = df['volume'].rolling(100, min_periods=1).max()
    df['tmp_vol_pctile_100'] = (df['volume'] - vmin) / (vmax - vmin + 1e-10)


def compute_all_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute every feature in dependency order (Section 2.11)."""
    df = df.copy()
    _raw_price_features(df)
    _bvc_features(df)
    _volatility_features(df)
    _volume_features(df)
    _depletion_features(df)
    _liquidity_features(df)
    _toxicity_features(df)
    _trend_features(df)
    _composite_signal(df)
    _position_sizing(df)
    _helper_columns(df)
    return df


def validate_features(df: pd.DataFrame) -> None:
    """Validate all features (Section 2.12)."""
    for feat in REQUIRED_FEATURES:
        assert feat in df.columns, f"Missing feature: {feat}"

    feature_cols = [c for c in df.columns if c.startswith('f_')]
    for feat in feature_cols:
        assert not np.isinf(df[feat].to_numpy(dtype='float64', na_value=0.0)).any(), \
            f"Infinite values in {feat}"

    assert (df['f_bvc_ratio'] >= 0).all() and (df['f_bvc_ratio'] <= 1).all(), "f_bvc_ratio out of [0,1]"
    assert df['f_liquidity_regime'].isin([0, 1, 2]).all(), "f_liquidity_regime not in {0,1,2}"
    assert (df['f_position_scale'] >= 0.1).all() and (df['f_position_scale'] <= 2.0).all(), \
        "f_position_scale out of bounds"

    regime_pcts = df['f_liquidity_regime'].value_counts(normalize=True)
    for r in [0, 1, 2]:
        pct = regime_pcts.get(r, 0)
        assert 0.10 <= pct <= 0.60, f"Regime {r} has {pct:.2%} — outside [10%, 60%]"

    print(f"  Feature validation passed ({len(REQUIRED_FEATURES)} features).")
