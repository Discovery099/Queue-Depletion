# STRATEGY 2: QUEUE-DEPLETION MOMENTUM WITH LIQUIDITY REGIME FILTER
## Complete Agentic Coding Problem Description
## Specification Version: 1.0.0 — IMPLEMENTATION-READY

---

# SECTION 0: EXECUTIVE SUMMARY

## Strategy Identity
- **Name**: Queue-Depletion Momentum with Liquidity Regime Filter
- **Strategy Code**: STRAT-02
- **Cross-Pollination Sources**: 
  - 0024/LOB-Delayed-Completion (queue depletion predicts directional completion)
  - 0038/LOB-Liquidity-Regimes (liquidity state determines signal validity)
  - 0021-prob/BVC-VIX-Toxicity (volume toxicity as momentum proxy)
- **Core Hypothesis**: Queue depletion dynamics, proxied through BVC volume signatures and OHLCV range patterns, predict short-term price direction. The predictive power is regime-dependent: queue-depletion signals are most reliable in Tight-Deep liquidity regimes (tight spreads, deep order books), produce breakthrough signals in Wide-Thin regimes, and must be suppressed in Disrupted regimes. By conditioning momentum signals on the prevailing liquidity state, the strategy achieves higher accuracy than unconditioned momentum with materially lower drawdown during toxic periods.
- **Instrument**: E-mini S&P 500 Futures (ES)
- **Bar Frequency**: 5-minute bars during Regular Trading Hours (RTH)
- **Position Direction**: Long/Short/Flat (no persistent bias)
- **Holding Period**: 1-6 bars (5-30 minutes typical)
- **Maximum Optimized Parameters**: 10 (strict anti-curve-fit limit)

## Performance Targets (Test Set)
| Metric | Target | Minimum Acceptable |
|--------|--------|-------------------|
| Overall Accuracy | >54% | >= 52.5% |
| Trades per Day | >5 | >= 4.5 |
| Wide-Thin Regime Accuracy | >56% | >= 54% |
| Sharpe Ratio (annualized) | >1.0 | >= 0.7 |
| Maximum Drawdown | <12% | <15% |
| Profit Factor | >1.15 | >= 1.08 |
| Win Rate | >54% | >= 52.5% |

## Key Design Decisions
1. **BVC Volume Proxy**: Since level-2 order book data is unavailable, the strategy uses the Buy-Volume-Classifier (BVC) approximation: classify each bar as buyer- or seller-initiated based on close position within the [low, high] range. This proxies queue depletion direction.
2. **Three-Regime Liquidity Filter**: The liquidity regime score L_t uses relative range and volume to classify each bar into Tight-Deep (high liquidity), Wide-Thin (low liquidity), or Disrupted (anomalous). Signal logic differs materially per regime.
3. **Vol-Scaled Toxicity**: The raw depletion signal is scaled by realized volatility to prevent oversized signals during calm periods and ensure signals during volatile periods are appropriately sized.
4. **Regime-Specific Signal Logic**: Tight-Deep → continuation (momentum); Wide-Thin → breakthrough (mean-reversion breakout); Disrupted → no trade (risk-off).
5. **Dynamic Position Sizing**: Position size scales linearly with the absolute depletion magnitude, capped at 2.0x base size.

## Data Summary
- **File**: `/mnt/agents/upload/ES_5min_RTH_6year.csv`
- **Total Rows**: 122,295 (indices 0 through 122,294)
- **Columns**: ts_event (datetime string with UTC offset), symbol (string), open (float), high (float), low (float), close (float), volume (int)
- **Date Range**: 2020-01-02 09:30:00-05:00 to 2026-03-06 15:55:00-05:00
- **Trading Days**: 1,594 days
- **Bars per Day**: 78 (5-minute bars from 09:30 to 16:00 ET), with 56 days having fewer bars (early market closes)
- **Development Set**: Indices 0 to 85,599 (85,600 bars, ~4.2 years, 2020-01-02 to 2024-04-26)
- **Test Set**: Indices 85,600 to 122,294 (36,695 bars, ~1.8 years, 2024-04-26 to 2026-03-06)

---

# SECTION 1: DATA SPECIFICATION & PIPELINE

## 1.1 Source Data Definition

Read the CSV file at path `/mnt/agents/upload/ES_5min_RTH_6year.csv` with the following exact specifications:

### Column Schema

| Column Name | Data Type | Description | Nullable |
|------------|-----------|-------------|----------|
| `ts_event` | string (datetime with timezone offset) | Timestamp of bar close in ISO 8601 format with UTC offset (e.g., `2020-01-02 09:30:00-05:00`) | NO |
| `symbol` | string | Instrument symbol (e.g., `ES.v.0`) | YES (7 rows contain NaN) |
| `open` | float64 | Opening price of the 5-minute bar | NO |
| `high` | float64 | Highest price during the bar | NO |
| `low` | float64 | Lowest price during the bar | NO |
| `close` | float64 | Closing price of the bar | NO |
| `volume` | int64 | Number of contracts traded during the bar | NO |

### Dataset Statistics (Reference)
- Total rows: 122,295
- Index range: 0 to 122,294
- Zero volume bars: 7 (indices 3536, 3770, 3771, 3925, 3926, 4122, 4123 — all from March 2020 circuit breaker events)
- NaN symbol rows: 7 (same rows as zero volume bars)
- Mean close price: 4,663.01
- Close price std: 1,094.44
- Min close: 2,183.50
- Max close: 7,029.50
- Mean volume: 15,377.34
- Volume std: 12,832.99
- Min volume: 0
- Max volume: 262,213
- 5-minute return std: 0.001438

## 1.2 Data Loading Procedure

Implement the data loading function with the following EXACT steps:

```python
def load_data(filepath: str = "/mnt/agents/upload/ES_5min_RTH_6year.csv") -> pd.DataFrame:
    """
    Load ES 5-minute RTH bar data from CSV.
    
    Returns:
        pd.DataFrame with columns [ts_event, symbol, open, high, low, close, volume]
        and integer index 0..N-1.
    """
    # Step 1: Read CSV
    df = pd.read_csv(filepath)
    
    # Step 2: Assert expected columns exist
    expected_cols = ['ts_event', 'symbol', 'open', 'high', 'low', 'close', 'volume']
    assert list(df.columns) == expected_cols, f"Expected columns {expected_cols}, got {list(df.columns)}"
    
    # Step 3: Parse ts_event to datetime with UTC normalization
    df['ts_event'] = pd.to_datetime(df['ts_event'], utc=True)
    
    # Step 4: Sort by ts_event to ensure chronological order
    df = df.sort_values('ts_event').reset_index(drop=True)
    
    # Step 5: Verify no duplicate timestamps
    assert df['ts_event'].is_unique, "Duplicate timestamps found in data"
    
    # Step 6: Verify bar frequency is 5 minutes (300 seconds) for intraday consecutive bars
    time_diffs = df['ts_event'].diff().dt.total_seconds().dropna()
    intraday_diffs = time_diffs[time_diffs < 86400]  # Only intraday gaps
    assert (intraday_diffs == 300.0).all(), f"Non-5-minute intraday gaps detected: {intraday_diffs[intraday_diffs != 300.0].unique()}"
    
    # Step 7: Verify no missing values in price/volume columns
    price_vol_cols = ['open', 'high', 'low', 'close', 'volume']
    assert df[price_vol_cols].notna().all().all(), "Missing values found in price/volume columns"
    
    # Step 8: Verify high >= low for all rows
    assert (df['high'] >= df['low']).all(), "Rows found where high < low"
    
    # Step 9: Verify high >= open, high >= close, low <= open, low <= close
    assert (df['high'] >= df['open']).all(), "Rows found where high < open"
    assert (df['high'] >= df['close']).all(), "Rows found where high < close"
    assert (df['low'] <= df['open']).all(), "Rows found where low > open"
    assert (df['low'] <= df['close']).all(), "Rows found where low > close"
    
    # Step 10: Handle zero-volume bars
    # Zero-volume bars have open==high==low==close and volume==0
    # These occurred during circuit breaker halts in March 2020
    # Replace zero-volume bars with NaN for all derived features (forward-fill prices, set volume features to 0)
    zero_vol_mask = df['volume'] == 0
    if zero_vol_mask.any():
        # Forward fill prices for zero-volume bars to avoid division by zero
        df.loc[zero_vol_mask, ['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].ffill()
        # Set volume to 1 to avoid division by zero in ratios (will be guarded by volume threshold anyway)
        df.loc[zero_vol_mask, 'volume'] = 1
    
    return df
```

## 1.3 Train/Test Split Definition

The split is FIXED and must not be altered. No hyperparameter tuning may use the test set.

```python
def split_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split data into development and test sets.
    
    Returns:
        (df_dev, df_test): Development and test DataFrames
    """
    SPLIT_INDEX = 85600  # First index of test set
    
    df_dev = df.iloc[:SPLIT_INDEX].copy()   # indices 0 to 85599 (85,600 bars)
    df_test = df.iloc[SPLIT_INDEX:].copy()   # indices 85600 to 122294 (36,695 bars)
    
    # Assertions
    assert len(df_dev) == 85600, f"Expected 85600 dev bars, got {len(df_dev)}"
    assert len(df_test) == 36695, f"Expected 36695 test bars, got {len(df_test)}"
    assert len(df_dev) + len(df_test) == len(df), "Split does not cover full dataset"
    
    return df_dev, df_test
```

### Development Set Characteristics
- **Indices**: 0 to 85,599 (inclusive)
- **Bar Count**: 85,600
- **Date Range**: 2020-01-02 14:30:00 UTC to 2024-04-26 17:00:00 UTC
- **Approximate Duration**: ~4.2 years
- **Purpose**: Feature engineering, hyperparameter optimization, model calibration, walk-forward validation
- **Sub-splits for Walk-Forward**: See Section 5

### Test Set Characteristics
- **Indices**: 85,600 to 122,294 (inclusive)
- **Bar Count**: 36,695
- **Date Range**: 2024-04-26 17:05:00 UTC to 2026-03-06 20:55:00 UTC
- **Approximate Duration**: ~1.8 years
- **Purpose**: FINAL EVALUATION ONLY. No hyperparameter tuning. No model selection. Report once.

## 1.4 Data Quality Checks

After loading, verify ALL of the following. Raise an exception if any check fails:

| Check # | Description | Assertion |
|---------|-------------|-----------|
| 1 | Total rows | `len(df) == 122295` |
| 2 | Index starts at 0 | `df.index[0] == 0` |
| 3 | Columns match schema | `list(df.columns) == ['ts_event','symbol','open','high','low','close','volume']` |
| 4 | No missing in price cols | `df[['open','high','low','close','volume']].isnull().sum().sum() == 0` (after zero-vol handling) |
| 5 | High >= Low | `(df['high'] >= df['low']).all()` |
| 6 | Volume >= 0 | `(df['volume'] >= 0).all()` |
| 7 | Timestamps unique | `df['ts_event'].is_unique` |
| 8 | Chronological order | `df['ts_event'].is_monotonic_increasing` |
| 9 | RTH session | All timestamps between 09:30 and 16:00 ET |
| 10 | No weekends | `df['ts_event'].dt.dayofweek.isin([0,1,2,3,4]).all()` |

## 1.5 Date and Time Handling

All datetime operations must use UTC-normalized timestamps:

```python
# Extract date for grouping operations
df['date'] = df['ts_event'].dt.date

# Extract time for intraday patterns (in ET = UTC-5/-4)
# Use pandas tz_convert to 'America/New_York'
df['time_et'] = df['ts_event'].dt.tz_convert('America/New_York').dt.time

# Extract bar number within day (0 = 09:30, 1 = 09:35, ..., 77 = 15:55)
df['bar_in_day'] = df.groupby('date').cumcount()

# Day of week: Monday=0, ..., Friday=4
df['dow'] = df['ts_event'].dt.dayofweek
```

## 1.6 Overnight and Gap Handling

- **First bar of each day** (bar_in_day == 0): The `open` price may gap from prior day's `close`. This is normal and expected.
- **Overnight return**: Do NOT compute or use overnight returns. All features are computed bar-by-bar without reference to prior day's close.
- **Gap features**: The feature `overnight_gap_pct` = `(open - prior_close) / prior_close` may be computed for informational purposes but must NOT be used in signal generation (lookahead risk).
- **Session boundaries**: No position is held overnight. All positions are opened and closed within the same trading day. See Section 4 for exact position holding rules.

---

# SECTION 2: FEATURE ENGINEERING (COMPLETE)

This section defines EVERY feature used in the strategy. Compute features in the EXACT order specified, as later features depend on earlier ones. All rolling windows use a minimum of 1 observation (min_periods=1) unless otherwise specified. All features are computed on the development set and applied identically to the test set.

## Feature Naming Convention
- All feature columns are prefixed with `f_` (e.g., `f_atr_20`)
- All intermediate columns used only for feature computation are prefixed with `tmp_`
- All signal columns are prefixed with `sig_`
- All regime columns are prefixed with `regime_`

## 2.1 Raw Price Features (Base Features)

These are direct transformations of OHLCV data, computed first.

### Feature: f_returns
- **Formula**: `f_returns = (close - close.shift(1)) / close.shift(1)`
- **Description**: Bar-to-bar close return in decimal form
- **Type**: float64
- **First value**: NaN (no prior bar)
- **Edge case**: For the first bar of each new day, compute normally using the previous day's last close. The overnight gap is captured naturally.
- **Range**: Typically -0.03 to +0.03

### Feature: f_log_returns
- **Formula**: `f_log_returns = log(close / close.shift(1))`
- **Description**: Natural log of the close-to-close ratio
- **Type**: float64
- **First value**: NaN
- **Note**: Use `numpy.log()` for computation

### Feature: f_true_range
- **Formula**: `f_true_range = max(high - low, |high - close.shift(1)|, |low - close.shift(1)|)`
- **Description**: True range incorporating the previous close
- **Type**: float64
- **First value**: `high - low` (since close.shift(1) is NaN, treat the first term as the maximum)
- **Implementation**:
```python
df['f_true_range'] = np.maximum(
    df['high'] - df['low'],
    np.maximum(
        np.abs(df['high'] - df['close'].shift(1)),
        np.abs(df['low'] - df['close'].shift(1))
    )
)
# For first bar where close.shift(1) is NaN, fill with high-low
df['f_true_range'] = df['f_true_range'].fillna(df['high'] - df['low'])
```

### Feature: f_bar_range
- **Formula**: `f_bar_range = (high - low) / close`
- **Description**: Normalized bar range (high-low as fraction of close price)
- **Type**: float64
- **Edge case**: If `close == 0`, set to NaN and forward-fill (should never happen with ES)
- **Range**: Typically 0.0001 to 0.01

### Feature: f_body_size
- **Formula**: `f_body_size = |close - open| / close`
- **Description**: Absolute body size as fraction of close price
- **Type**: float64
- **Range**: Typically 0 to 0.01

### Feature: f_body_direction
- **Formula**: `f_body_direction = sign(close - open)` where sign(x) = 1 if x>0, -1 if x<0, 0 if x==0
- **Description**: Direction of the bar body: bullish (+1), bearish (-1), or doji (0)
- **Type**: int8
- **Values**: {-1, 0, 1}

### Feature: f_upper_shadow
- **Formula**: `f_upper_shadow = (high - max(open, close)) / close`
- **Description**: Upper shadow length normalized by close
- **Type**: float64
- **Range**: Non-negative

### Feature: f_lower_shadow
- **Formula**: `f_lower_shadow = (min(open, close) - low) / close`
- **Description**: Lower shadow length normalized by close
- **Type**: float64
- **Range**: Non-negative

## 2.2 BVC Volume Classification Features

The Buy-Volume Classifier (BVC) approximates buyer- vs seller-initiated volume using the position of the close within the [low, high] range. This proxies queue depletion direction.

### Feature: f_bvc_ratio
- **Formula**: `f_bvc_ratio = (close - low) / (high - low)`
- **Description**: Close position within the bar range. 0 = close at low (all selling), 1 = close at high (all buying), 0.5 = close at midpoint.
- **Type**: float64
- **Edge case**: If `high == low` (zero-range bar), set `f_bvc_ratio = 0.5`
- **Range**: [0, 1]
- **Implementation**:
```python
hl_range = df['high'] - df['low']
df['f_bvc_ratio'] = np.where(
    hl_range > 0,
    (df['close'] - df['low']) / hl_range,
    0.5
)
```

### Feature: f_bvc_buy_vol
- **Formula**: `f_bvc_buy_vol = f_bvc_ratio * volume`
- **Description**: Estimated buyer-initiated volume
- **Type**: float64
- **Range**: [0, volume]

### Feature: f_bvc_sell_vol
- **Formula**: `f_bvc_sell_vol = (1 - f_bvc_ratio) * volume`
- **Description**: Estimated seller-initiated volume
- **Type**: float64
- **Range**: [0, volume]

### Feature: f_bvc_imbalance
- **Formula**: `f_bvc_imbalance = (f_bvc_buy_vol - f_bvc_sell_vol) / (f_bvc_buy_vol + f_bvc_sell_vol)`
- **Description**: Volume imbalance ratio: +1 = all buying, -1 = all selling
- **Type**: float64
- **Simplification**: Since `f_bvc_buy_vol + f_bvc_sell_vol = volume`, this reduces to:
  `f_bvc_imbalance = (2 * f_bvc_ratio - 1)`
- **Range**: [-1, 1]

### Feature: f_bvc_sign
- **Formula**: `f_bvc_sign = sign(f_bvc_imbalance)`
- **Description**: Discrete BVC direction: +1 for buy-initiated, -1 for sell-initiated, 0 for neutral
- **Type**: int8
- **Values**: {-1, 0, 1}
- **Note**: Since f_bvc_imbalance == 0 only when f_bvc_ratio == 0.5 (exact midpoint), f_bvc_sign will rarely be 0.

## 2.3 ATR and Volatility Features

### Feature: f_atr_20
- **Formula**: `f_atr_20 = f_true_range.rolling(window=20, min_periods=1).mean()`
- **Description**: 20-bar Average True Range — primary volatility measure
- **Type**: float64
- **Window**: 20 bars (100 minutes = ~1.3 hours)
- **Min periods**: 1
- **First value**: `f_true_range` of first bar (since min_periods=1)
- **Range**: Typically 1.0 to 50.0 points for ES
- **Note**: Do NOT use Wilder's smoothing. Use simple rolling mean.

### Feature: f_atr_20_pct
- **Formula**: `f_atr_20_pct = f_atr_20 / close`
- **Description**: ATR as percentage of price
- **Type**: float64
- **Range**: Typically 0.0002 to 0.005

### Feature: f_vol_realized_20
- **Formula**: `f_vol_realized_20 = sqrt(252 * 78 * f_log_returns.rolling(window=20, min_periods=5).var())`
- **Description**: Annualized realized volatility proxy using 20-bar rolling variance of log returns. The factor `252 * 78` converts 5-min variance to annualized volatility (252 trading days * 78 bars/day).
- **Type**: float64
- **Window**: 20 bars, min_periods=5
- **First 4 values**: NaN (insufficient data)
- **Range**: Typically 0.05 to 1.0 (5% to 100% annualized)
- **Implementation**:
```python
df['f_vol_realized_20'] = np.sqrt(
    252 * 78 * df['f_log_returns'].rolling(window=20, min_periods=5).var()
)
```

### Feature: f_vol_realized_60
- **Formula**: `f_vol_realized_60 = sqrt(252 * 78 * f_log_returns.rolling(window=60, min_periods=20).var())`
- **Description**: Longer-horizon annualized realized volatility (60 bars = 5 hours)
- **Type**: float64
- **Window**: 60 bars, min_periods=20
- **First 19 values**: NaN
- **Purpose**: Smoother volatility estimate for regime classification

### Feature: f_vol_ratio
- **Formula**: `f_vol_ratio = f_vol_realized_20 / f_vol_realized_60`
- **Description**: Ratio of short-term to medium-term volatility. Values > 1 indicate recent volatility spike.
- **Type**: float64
- **Edge case**: If f_vol_realized_60 == 0 or NaN, set to 1.0
- **Range**: Typically 0.3 to 3.0

## 2.4 Volume Features

### Feature: f_volume_sma_20
- **Formula**: `f_volume_sma_20 = volume.rolling(window=20, min_periods=1).mean()`
- **Description**: 20-bar simple moving average of volume
- **Type**: float64
- **Window**: 20 bars
- **Min periods**: 1

### Feature: f_volume_ratio
- **Formula**: `f_volume_ratio = volume / f_volume_sma_20`
- **Description**: Current volume relative to recent average. >1 = above-average volume.
- **Type**: float64
- **Edge case**: If f_volume_sma_20 == 0, set to 1.0
- **Range**: Typically 0 to 10

### Feature: f_volume_zscore_20
- **Formula**: `f_volume_zscore_20 = (volume - f_volume_sma_20) / volume.rolling(window=20, min_periods=5).std()`
- **Description**: Volume z-score over 20-bar window
- **Type**: float64
- **Edge case**: If rolling std == 0, set to 0.0
- **Min periods**: 5

### Feature: f_relative_volume
- **Formula**: `f_relative_volume = volume / f_volume_sma_20`
- **Description**: Alias for f_volume_ratio, used in liquidity regime formula. Exact same computation.
- **Type**: float64
- **Note**: This is identical to f_volume_ratio. Define it separately for clarity in regime formulas.

## 2.5 Depletion Signature Features (Core Strategy Features)

### Feature: f_depletion_raw

This is the core bar depletion signature Δ_t. It measures the intensity of queue depletion in a single bar.

- **Formula**: 
  `f_depletion_raw = (f_bvc_buy_vol / volume) * (f_bar_range / f_atr_20_pct) * indicator(volume > f_volume_sma_20)`
- **Simplified**: 
  `f_depletion_raw = f_bvc_ratio * (f_bar_range / f_atr_20_pct) * indicator(volume > f_volume_sma_20)`
- **Description**: The depletion signature combines three elements:
  1. **BVC ratio** (`f_bvc_ratio`): Close position within the bar range — proxies whether buyers or sellers dominated
  2. **Range expansion** (`f_bar_range / f_atr_20_pct`): Whether this bar's range is large relative to recent ATR — captures depletion intensity
  3. **Volume confirmation** (`indicator(volume > f_volume_sma_20)`): Whether volume is above average — ensures depletion is significant
- **Type**: float64
- **Values**: 
  - 0 when volume <= average (no depletion signal)
  - Positive when close is near high with expanded range and above-average volume
  - Negative when close is near low with expanded range and above-average volume (the BVC ratio < 0.5 makes the product negative)
- **Edge cases**:
  - If `f_atr_20_pct == 0`, set ratio to 1.0 (avoid division by zero)
  - If `volume == 0`, set depletion to 0
- **Implementation**:
```python
# Volume threshold indicator
vol_above_avg = (df['volume'] > df['f_volume_sma_20']).astype(float)

# Range / ATR ratio, guarded
tmp_range_atr_ratio = df['f_bar_range'] / df['f_atr_20_pct'].replace(0, np.nan)
tmp_range_atr_ratio = tmp_range_atr_ratio.fillna(1.0)

# Cap the ratio at 10.0 to prevent extreme values
tmp_range_atr_ratio = tmp_range_atr_ratio.clip(upper=10.0)

# Depletion signature
df['f_depletion_raw'] = (df['f_bvc_ratio'] - 0.5) * 2 * tmp_range_atr_ratio * vol_above_avg
# The (f_bvc_ratio - 0.5) * 2 maps [0,1] to [-1,1] as the directional component
```

- **Correction to formula**: The raw depletion signature should be signed. Rewrite more carefully:

```python
# Signed BVC imbalance: -1 to +1
f_bvc_signed = 2 * df['f_bvc_ratio'] - 1  # Maps 0->-1, 0.5->0, 1->+1

# Range expansion factor
tmp_range_expansion = df['f_bar_range'] / df['f_atr_20_pct'].replace(0, np.nan)
tmp_range_expansion = tmp_range_expansion.fillna(1.0).clip(upper=10.0)

# Volume threshold indicator (1.0 if above average, 0.0 otherwise)
tmp_vol_indicator = (df['volume'] > df['f_volume_sma_20']).astype(float)

# Raw depletion signature
df['f_depletion_raw'] = f_bvc_signed * tmp_range_expansion * tmp_vol_indicator
```

- **Range**: Typically -5.0 to +5.0
- **Interpretation**: 
  - Positive values indicate buyer-initiated depletion with range expansion
  - Negative values indicate seller-initiated depletion with range expansion
  - Zero indicates no depletion (volume too low or no directional bias)

### Feature: f_depletion_abs
- **Formula**: `f_depletion_abs = abs(f_depletion_raw)`
- **Description**: Absolute depletion magnitude (used for position sizing)
- **Type**: float64
- **Range**: [0, +inf)

### Feature: f_depletion_ma_5
- **Formula**: `f_depletion_ma_5 = f_depletion_raw.rolling(window=5, min_periods=1).mean()`
- **Description**: 5-bar moving average of depletion — smooths noise
- **Type**: float64
- **Window**: 5 bars (25 minutes)
- **Purpose**: Primary signal input for momentum detection

### Feature: f_depletion_ma_10
- **Formula**: `f_depletion_ma_10 = f_depletion_raw.rolling(window=10, min_periods=3).mean()`
- **Description**: 10-bar moving average of depletion — slower confirmation
- **Type**: float64
- **Window**: 10 bars (50 minutes)
- **Min periods**: 3

### Feature: f_depletion_diff
- **Formula**: `f_depletion_diff = f_depletion_ma_5 - f_depletion_ma_10`
- **Description**: Difference between fast and slow depletion MAs. Positive = accelerating depletion.
- **Type**: float64
- **Purpose**: Momentum confirmation — trade in direction of depletion acceleration

## 2.6 Liquidity Regime Features

### Feature: f_liquidity_score

This is the liquidity regime score L_t used to classify the market into three liquidity states.

- **Formula**: `f_liquidity_score = f_bar_range * (f_relative_volume)^(-0.5)`
- **Expanded**: `f_liquidity_score = ((high - low) / close) * (volume / f_volume_sma_20)^(-0.5)`
- **Description**: The liquidity score combines:
  1. **Spread proxy** (`f_bar_range`): Wider ranges imply wider spreads = less liquid
  2. **Depth proxy** (`f_relative_volume^(-0.5)`): Higher volume implies deeper book = more liquid (negative exponent inverts this)
  
  The formula gives LOW scores for tight ranges with high volume (Tight-Deep = liquid) and HIGH scores for wide ranges with low volume (Wide-Thin = illiquid).
- **Type**: float64
- **Edge cases**:
  - If `f_relative_volume == 0`, set to NaN and forward-fill
  - If `f_relative_volume` is NaN, set score to the 66th percentile value (treat as Wide-Thin)
- **Implementation**:
```python
# Compute relative volume with floor at 0.1 to prevent extreme values
tmp_rel_vol = (df['volume'] / df['f_volume_sma_20'].replace(0, np.nan)).fillna(1.0)
tmp_rel_vol = tmp_rel_vol.clip(lower=0.1)

# Liquidity score
df['f_liquidity_score'] = df['f_bar_range'] * (tmp_rel_vol ** (-0.5))

# Handle NaN
median_liq = df['f_liquidity_score'].median()
df['f_liquidity_score'] = df['f_liquidity_score'].fillna(median_liq)
```
- **Range**: Typically 0.00005 to 0.005

### Feature: f_liquidity_q33

- **Formula**: `f_liquidity_q33 = f_liquidity_score.rolling(window=200, min_periods=50).quantile(0.33)`
- **Description**: Rolling 33rd percentile of liquidity score — boundary between Tight-Deep and Wide-Thin regimes
- **Type**: float64
- **Window**: 200 bars (~2.6 trading days)
- **Min periods**: 50
- **Purpose**: Adaptive threshold for regime classification

### Feature: f_liquidity_q66

- **Formula**: `f_liquidity_q66 = f_liquidity_score.rolling(window=200, min_periods=50).quantile(0.66)`
- **Description**: Rolling 66th percentile of liquidity score — boundary between Wide-Thin and Disrupted regimes
- **Type**: float64
- **Window**: 200 bars
- **Min periods**: 50

### Feature: f_liquidity_regime

- **Formula**:
  ```
  f_liquidity_regime = 
    0  if f_liquidity_score < f_liquidity_q33       (Tight-Deep)
    1  if f_liquidity_q33 <= f_liquidity_score < f_liquidity_q66   (Wide-Thin)
    2  if f_liquidity_score >= f_liquidity_q66      (Disrupted)
  ```
- **Description**: Discrete liquidity regime classification
- **Type**: int8
- **Values**: {0, 1, 2}
- **Meaning**:
  - 0 = Tight-Deep: Tight spreads, deep order book → continuation signals
  - 1 = Wide-Thin: Wide spreads, thin book → breakthrough signals  
  - 2 = Disrupted: Anomalous conditions → no trade
- **Implementation**:
```python
def classify_regime(row):
    if pd.isna(row['f_liquidity_q33']) or pd.isna(row['f_liquidity_q66']):
        return 1  # Default to Wide-Thin if thresholds not yet available
    if row['f_liquidity_score'] < row['f_liquidity_q33']:
        return 0  # Tight-Deep
    elif row['f_liquidity_score'] < row['f_liquidity_q66']:
        return 1  # Wide-Thin
    else:
        return 2  # Disrupted

df['f_liquidity_regime'] = df.apply(classify_regime, axis=1)
```

### Feature: f_regime_tight_deep
- **Formula**: `f_regime_tight_deep = (f_liquidity_regime == 0).astype(int)`
- **Description**: Binary indicator for Tight-Deep regime
- **Type**: int8
- **Values**: {0, 1}

### Feature: f_regime_wide_thin
- **Formula**: `f_regime_wide_thin = (f_liquidity_regime == 1).astype(int)`
- **Description**: Binary indicator for Wide-Thin regime
- **Type**: int8
- **Values**: {0, 1}

### Feature: f_regime_disrupted
- **Formula**: `f_regime_disrupted = (f_liquidity_regime == 2).astype(int)`
- **Description**: Binary indicator for Disrupted regime
- **Type**: int8
- **Values**: {0, 1}

## 2.7 Vol-Scaled Toxicity Features

### Feature: f_toxicity_raw

- **Formula**: `f_toxicity_raw = f_depletion_raw * abs(f_depletion_raw) / f_vol_realized_20`
- **Description**: Volatility-scaled toxicity metric. The numerator `depletion * |depletion|` gives signed quadratic depletion (amplifying large depletions). Dividing by realized volatility normalizes by market conditions.
- **Type**: float64
- **Edge cases**:
  - If `f_vol_realized_20 == 0` or NaN, set toxicity to 0
  - If `f_vol_realized_20` < 0.001 (1 bps annualized), cap denominator at 0.001
- **Implementation**:
```python
denom = df['f_vol_realized_20'].replace(0, np.nan).fillna(0.1)
denom = denom.clip(lower=0.001)
df['f_toxicity_raw'] = df['f_depletion_raw'] * df['f_depletion_abs'] / denom
# Cap at +/- 100 for numerical stability
df['f_toxicity_raw'] = df['f_toxicity_raw'].clip(lower=-100, upper=100)
```
- **Range**: Typically -50 to +50

### Feature: f_toxicity_ma_5
- **Formula**: `f_toxicity_ma_5 = f_toxicity_raw.rolling(window=5, min_periods=1).mean()`
- **Description**: Smoothed toxicity signal
- **Type**: float64
- **Window**: 5 bars

### Feature: f_toxicity_zscore
- **Formula**: `f_toxicity_zscore = (f_toxicity_raw - f_toxicity_raw.rolling(window=60, min_periods=20).mean()) / f_toxicity_raw.rolling(window=60, min_periods=20).std()`
- **Description**: Z-score of toxicity over 60-bar window
- **Type**: float64
- **Edge case**: If rolling std == 0, set to 0
- **Min periods**: 20

## 2.8 Trend and Momentum Features

### Feature: f_ema_12
- **Formula**: `f_ema_12 = close.ewm(span=12, min_periods=3).mean()`
- **Description**: 12-bar exponential moving average
- **Type**: float64
- **Span**: 12 bars (1 hour)

### Feature: f_ema_26
- **Formula**: `f_ema_26 = close.ewm(span=26, min_periods=5).mean()`
- **Description**: 26-bar exponential moving average
- **Type**: float64
- **Span**: 26 bars (~2 hours)

### Feature: f_ema_diff
- **Formula**: `f_ema_diff = (f_ema_12 - f_ema_26) / close`
- **Description**: Normalized EMA difference (MACD line equivalent)
- **Type**: float64

### Feature: f_price_vs_ema20
- **Formula**: `f_price_vs_ema20 = (close - close.ewm(span=20, min_periods=5).mean()) / close`
- **Description**: Price deviation from 20-bar EMA
- **Type**: float64

### Feature: f_momentum_3
- **Formula**: `f_momentum_3 = (close - close.shift(3)) / close.shift(3)`
- **Description**: 3-bar momentum (15 minutes)
- **Type**: float64
- **First 3 values**: NaN

### Feature: f_momentum_6
- **Formula**: `f_momentum_6 = (close - close.shift(6)) / close.shift(6)`
- **Description**: 6-bar momentum (30 minutes)
- **Type**: float64
- **First 6 values**: NaN

## 2.9 Composite Signal Features

### Feature: f_regime_adjusted_signal

This is the primary signal feature that combines depletion, toxicity, and regime.

- **Formula**: 
  ```
  f_regime_adjusted_signal = 
    CASE f_liquidity_regime:
      0 (Tight-Deep):   sign(f_depletion_ma_5) * f_toxicity_ma_5 * (1 + 0.5 * f_momentum_3)
      1 (Wide-Thin):    sign(f_depletion_diff) * f_toxicity_ma_5 * (1 + 0.3 * |f_momentum_6|)
      2 (Disrupted):    0
  ```
- **Description**: Regime-conditioned composite signal. 
  - In Tight-Deep: Trade continuation in direction of depletion MA, amplified by recent momentum.
  - In Wide-Thin: Trade breakthrough (acceleration) direction, amplified by momentum magnitude.
  - In Disrupted: No signal.
- **Type**: float64
- **Edge cases**: 
  - If any component is NaN, set signal to 0
  - If `(1 + 0.5 * f_momentum_3)` <= 0 in Tight-Deep, set multiplier to 0.1
  - If `(1 + 0.3 * |f_momentum_6|)` <= 0 in Wide-Thin, set multiplier to 0.1
- **Implementation**:
```python
def compute_regime_signal(row):
    regime = row['f_liquidity_regime']
    
    if regime == 2:  # Disrupted
        return 0.0
    
    if pd.isna(row['f_depletion_ma_5']) or pd.isna(row['f_toxicity_ma_5']):
        return 0.0
    
    if regime == 0:  # Tight-Deep
        dep_sign = np.sign(row['f_depletion_ma_5'])
        if dep_sign == 0:
            return 0.0
        mom_mult = 1.0 + 0.5 * (row['f_momentum_3'] if not pd.isna(row['f_momentum_3']) else 0)
        mom_mult = max(mom_mult, 0.1)
        return dep_sign * row['f_toxicity_ma_5'] * mom_mult
    
    elif regime == 1:  # Wide-Thin
        dep_diff_sign = np.sign(row['f_depletion_diff'])
        if dep_diff_sign == 0:
            return 0.0
        mom_mult = 1.0 + 0.3 * abs(row['f_momentum_6'] if not pd.isna(row['f_momentum_6']) else 0)
        mom_mult = max(mom_mult, 0.1)
        return dep_diff_sign * row['f_toxicity_ma_5'] * mom_mult

df['f_regime_adjusted_signal'] = df.apply(compute_regime_signal, axis=1)
```

## 2.10 Position Sizing Features

### Feature: f_position_scale

- **Formula**: `f_position_scale = min(2.0, f_depletion_abs / f_depletion_abs.rolling(window=100, min_periods=20).mean())`
- **Description**: Position size multiplier based on current depletion magnitude relative to recent average. Capped at 2.0x base size.
- **Type**: float64
- **Range**: [0, 2.0]
- **Edge case**: If rolling mean == 0 or NaN, set scale to 1.0
- **Implementation**:
```python
dep_mean = df['f_depletion_abs'].rolling(window=100, min_periods=20).mean()
df['f_position_scale'] = (df['f_depletion_abs'] / dep_mean.replace(0, np.nan)).fillna(1.0)
df['f_position_scale'] = df['f_position_scale'].clip(upper=2.0, lower=0.1)
```

## 2.11 Feature Computation Order

Features MUST be computed in this exact order due to dependencies:

| Order | Feature Group | Features |
|-------|--------------|----------|
| 1 | Raw Price | f_returns, f_log_returns, f_true_range, f_bar_range, f_body_size, f_body_direction, f_upper_shadow, f_lower_shadow |
| 2 | BVC Volume | f_bvc_ratio, f_bvc_buy_vol, f_bvc_sell_vol, f_bvc_imbalance, f_bvc_sign |
| 3 | Volatility | f_atr_20, f_atr_20_pct, f_vol_realized_20, f_vol_realized_60, f_vol_ratio |
| 4 | Volume | f_volume_sma_20, f_volume_ratio, f_volume_zscore_20, f_relative_volume |
| 5 | Depletion | f_depletion_raw, f_depletion_abs, f_depletion_ma_5, f_depletion_ma_10, f_depletion_diff |
| 6 | Liquidity Regime | f_liquidity_score, f_liquidity_q33, f_liquidity_q66, f_liquidity_regime, f_regime_tight_deep, f_regime_wide_thin, f_regime_disrupted |
| 7 | Toxicity | f_toxicity_raw, f_toxicity_ma_5, f_toxicity_zscore |
| 8 | Trend | f_ema_12, f_ema_26, f_ema_diff, f_price_vs_ema20, f_momentum_3, f_momentum_6 |
| 9 | Composite | f_regime_adjusted_signal |
| 10 | Sizing | f_position_scale |

## 2.12 Feature Validation

After computing all features, assert the following:

```python
def validate_features(df: pd.DataFrame) -> None:
    """Validate all features are correctly computed."""
    feature_cols = [c for c in df.columns if c.startswith('f_')]
    
    # 1. All feature columns exist
    required_features = [
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
        'f_regime_adjusted_signal', 'f_position_scale'
    ]
    for feat in required_features:
        assert feat in df.columns, f"Missing feature: {feat}"
    
    # 2. No infinite values
    for feat in feature_cols:
        assert not np.isinf(df[feat]).any(), f"Infinite values in {feat}"
    
    # 3. Feature ranges (spot checks)
    assert (df['f_bvc_ratio'] >= 0).all() and (df['f_bvc_ratio'] <= 1).all(), "f_bvc_ratio out of [0,1]"
    assert (df['f_liquidity_regime'].isin([0, 1, 2])).all(), "f_liquidity_regime not in {0,1,2}"
    assert (df['f_position_scale'] >= 0.1).all() and (df['f_position_scale'] <= 2.0).all(), "f_position_scale out of bounds"
    
    # 4. Regime distribution roughly balanced (allow 10-60% per regime)
    regime_pcts = df['f_liquidity_regime'].value_counts(normalize=True)
    for r in [0, 1, 2]:
        pct = regime_pcts.get(r, 0)
        assert 0.10 <= pct <= 0.60, f"Regime {r} has {pct:.2%} — outside [10%, 60%]"
    
    print(f"Feature validation passed. {len(required_features)} features computed.")
```



---

# SECTION 3: SIGNAL GENERATION ENGINE (COMPLETE)

This section defines the COMPLETE signal generation logic. Every condition, threshold, and branching decision is specified as executable pseudocode. The signal generation engine produces three outputs per bar:
1. `sig_direction`: {-1, 0, +1} — desired position direction
2. `sig_strength`: [0, 1] — normalized signal strength
3. `sig_regime`: {0, 1, 2} — liquidity regime at signal time

## 3.1 Signal Generation Parameters (Hyperparameters)

These are the ONLY parameters that may be optimized during development. Exactly 8 optimized parameters.

| Parameter ID | Name | Description | Default Value | Optimization Range | Type |
|-------------|------|-------------|---------------|-------------------|------|
| P1 | `dep_threshold` | Minimum |f_depletion_ma_5| to generate a signal | 0.15 | [0.05, 0.50] | float |
| P2 | `tox_threshold` | Minimum |f_toxicity_ma_5| to generate a signal | 0.20 | [0.05, 0.80] | float |
| P3 | `momentum_confirm` | Minimum |f_momentum_3| for Tight-Deep entry | 0.0002 | [0.0, 0.001] | float |
| P4 | `breakthrough_threshold` | Minimum |f_depletion_diff| for Wide-Thin entry | 0.10 | [0.02, 0.30] | float |
| P5 | `exit_bars` | Maximum holding period in bars | 4 | [2, 8] | int |
| P6 | `profit_target_pct` | Profit target as fraction of ATR | 0.8 | [0.3, 2.0] | float |
| P7 | `stop_loss_pct` | Stop loss as fraction of ATR | 0.6 | [0.2, 1.5] | float |
| P8 | `min_volume_pctile` | Minimum volume percentile to trade | 30.0 | [10.0, 50.0] | float |

**Parameter Count**: 8 optimized parameters (within the 10-parameter limit).

## 3.2 Signal Generation State Machine

The signal engine operates as a state machine with three states per bar:

```
States: FLAT (no position), LONG (+1), SHORT (-1)
Transitions: 
  FLAT -> LONG:  Entry condition met for long
  FLAT -> SHORT: Entry condition met for short
  LONG -> FLAT:  Exit condition met (profit target, stop loss, or max hold)
  SHORT -> FLAT: Exit condition met (profit target, stop loss, or max hold)
  LONG -> LONG:  Hold position (no action)
  SHORT -> SHORT: Hold position (no action)
  FLAT -> FLAT:  No signal (no action)
```

## 3.3 Entry Signal Logic

### 3.3.1 Universal Entry Guards

Before any entry signal is generated, ALL of the following guards must pass:

```python
def check_entry_guards(df: pd.DataFrame, idx: int, params: dict) -> bool:
    """
    Check universal entry conditions that apply to all regimes.
    Returns True if entry is allowed.
    """
    row = df.iloc[idx]
    
    # Guard 1: Not in Disrupted regime
    if row['f_liquidity_regime'] == 2:
        return False
    
    # Guard 2: Sufficient depletion magnitude
    if abs(row['f_depletion_ma_5']) < params['dep_threshold']:
        return False
    
    # Guard 3: Sufficient toxicity
    if abs(row['f_toxicity_ma_5']) < params['tox_threshold']:
        return False
    
    # Guard 4: Volume is above minimum percentile
    # Compute rolling volume percentile over 100-bar window
    vol_window = df['volume'].iloc[max(0, idx-99):idx+1]
    vol_pctile = (row['volume'] - vol_window.min()) / (vol_window.max() - vol_window.min() + 1e-10)
    if vol_pctile < params['min_volume_pctile'] / 100.0:
        return False
    
    # Guard 5: Not first bar of day (avoid overnight gap ambiguity)
    if row['bar_in_day'] == 0:
        return False
    
    # Guard 6: Not last 3 bars of day (must exit before close)
    # bar_in_day ranges 0-77, so last 3 are 75, 76, 77
    if row['bar_in_day'] >= 75:
        return False
    
    # Guard 7: Sufficient ATR (avoid dead markets)
    if row['f_atr_20'] < 1.0:  # Less than 1 point ATR
        return False
    
    # Guard 8: No NaN in critical features
    critical_feats = ['f_depletion_ma_5', 'f_toxicity_ma_5', 'f_liquidity_regime',
                      'f_atr_20', 'f_momentum_3']
    if any(pd.isna(row[f]) for f in critical_feats):
        return False
    
    return True
```

### 3.3.2 Tight-Deep Regime Entry (Regime = 0)

In Tight-Deep liquidity, signals trade **continuation** — go long when depletion is positive (buying pressure), go short when depletion is negative (selling pressure).

```python
def entry_tight_deep(df: pd.DataFrame, idx: int, params: dict) -> int:
    """
    Generate entry signal in Tight-Deep regime.
    Returns: +1 (long), -1 (short), or 0 (no signal)
    """
    row = df.iloc[idx]
    
    # Check universal guards first
    if not check_entry_guards(df, idx, params):
        return 0
    
    # Verify Tight-Deep regime
    if row['f_liquidity_regime'] != 0:
        return 0
    
    # Long entry: positive depletion MA with positive momentum confirmation
    if (row['f_depletion_ma_5'] > 0 and 
        row['f_momentum_3'] > params['momentum_confirm'] and
        row['f_ema_diff'] > 0):  # Price above EMA (bullish bias)
        return +1
    
    # Short entry: negative depletion MA with negative momentum confirmation
    if (row['f_depletion_ma_5'] < 0 and 
        row['f_momentum_3'] < -params['momentum_confirm'] and
        row['f_ema_diff'] < 0):  # Price below EMA (bearish bias)
        return -1
    
    return 0
```

### 3.3.3 Wide-Thin Regime Entry (Regime = 1)

In Wide-Thin liquidity, signals trade **breakthrough** — go long when depletion is accelerating upward (depletion_diff > 0), go short when depletion is accelerating downward. This captures the "breakthrough" moment when illiquid conditions are being overcome.

```python
def entry_wide_thin(df: pd.DataFrame, idx: int, params: dict) -> int:
    """
    Generate entry signal in Wide-Thin regime.
    Returns: +1 (long), -1 (short), or 0 (no signal)
    """
    row = df.iloc[idx]
    
    # Check universal guards first
    if not check_entry_guards(df, idx, params):
        return 0
    
    # Verify Wide-Thin regime
    if row['f_liquidity_regime'] != 1:
        return 0
    
    # Long entry: depletion accelerating upward (diff > threshold) with expanding range
    if (row['f_depletion_diff'] > params['breakthrough_threshold'] and
        row['f_bar_range'] > row['f_atr_20_pct'] * 1.2 and  # Range > 1.2x ATR
        row['f_volume_ratio'] > 1.5):  # Volume surge confirms breakthrough
        return +1
    
    # Short entry: depletion accelerating downward (diff < -threshold) with expanding range
    if (row['f_depletion_diff'] < -params['breakthrough_threshold'] and
        row['f_bar_range'] > row['f_atr_20_pct'] * 1.2 and
        row['f_volume_ratio'] > 1.5):
        return -1
    
    return 0
```

### 3.3.4 Disrupted Regime Entry (Regime = 2)

In Disrupted regime, NO entries are permitted.

```python
def entry_disrupted(df: pd.DataFrame, idx: int, params: dict) -> int:
    """No trading in Disrupted regime. Always returns 0."""
    return 0
```

### 3.3.5 Master Entry Function

```python
def generate_entry_signal(df: pd.DataFrame, idx: int, params: dict) -> Tuple[int, float, int]:
    """
    Generate entry signal at bar index idx.
    
    Returns:
        direction: +1 (long), -1 (short), 0 (no entry)
        strength: signal strength in [0, 1]
        regime: liquidity regime {0, 1, 2}
    """
    row = df.iloc[idx]
    regime = int(row['f_liquidity_regime'])
    
    # Route to regime-specific entry logic
    if regime == 0:
        direction = entry_tight_deep(df, idx, params)
    elif regime == 1:
        direction = entry_wide_thin(df, idx, params)
    else:  # regime == 2
        direction = entry_disrupted(df, idx, params)
    
    # Compute signal strength
    if direction == 0:
        strength = 0.0
    else:
        # Normalize strength by thresholds
        dep_component = min(abs(row['f_depletion_ma_5']) / (params['dep_threshold'] * 3), 1.0)
        tox_component = min(abs(row['f_toxicity_ma_5']) / (params['tox_threshold'] * 3), 1.0)
        strength = 0.5 * dep_component + 0.5 * tox_component
        strength = max(0.1, min(1.0, strength))
    
    return direction, strength, regime
```

## 3.4 Exit Signal Logic

Each position has three exit triggers. The FIRST one to fire determines the exit.

### 3.4.1 Exit Trigger 1: Profit Target

```python
def check_profit_target(df: pd.DataFrame, entry_idx: int, current_idx: int, 
                        direction: int, entry_price: float, params: dict) -> bool:
    """
    Check if profit target has been hit.
    For long:  current_price >= entry_price + profit_target
    For short: current_price <= entry_price - profit_target
    """
    atr_at_entry = df.iloc[entry_idx]['f_atr_20']
    profit_distance = params['profit_target_pct'] * atr_at_entry
    
    current_price = df.iloc[current_idx]['close']
    
    if direction == +1:  # Long
        return current_price >= entry_price + profit_distance
    elif direction == -1:  # Short
        return current_price <= entry_price - profit_distance
    return False
```

### 3.4.2 Exit Trigger 2: Stop Loss

```python
def check_stop_loss(df: pd.DataFrame, entry_idx: int, current_idx: int,
                    direction: int, entry_price: float, params: dict) -> bool:
    """
    Check if stop loss has been hit.
    For long:  current_price <= entry_price - stop_distance
    For short: current_price >= entry_price + stop_distance
    """
    atr_at_entry = df.iloc[entry_idx]['f_atr_20']
    stop_distance = params['stop_loss_pct'] * atr_at_entry
    
    # Use intraday low/high for more realistic stop checks
    if direction == +1:  # Long — check if low breached stop
        current_low = df.iloc[current_idx]['low']
        return current_low <= entry_price - stop_distance
    elif direction == -1:  # Short — check if high breached stop
        current_high = df.iloc[current_idx]['high']
        return current_high >= entry_price + stop_distance
    return False
```

### 3.4.3 Exit Trigger 3: Maximum Holding Period

```python
def check_max_hold(entry_idx: int, current_idx: int, params: dict) -> bool:
    """
    Check if maximum holding period has been exceeded.
    """
    bars_held = current_idx - entry_idx
    return bars_held >= params['exit_bars']
```

### 3.4.4 Exit Trigger 4: End of Day (Hard Constraint)

```python
def check_end_of_day(df: pd.DataFrame, current_idx: int) -> bool:
    """
    Force exit on bar 76 (15:50 ET) — second to last bar.
    This ensures position is closed before market close.
    bar_in_day == 76 means the 15:50 bar (last tradeable exit bar).
    """
    return df.iloc[current_idx]['bar_in_day'] >= 76
```

### 3.4.5 Exit Trigger 5: Regime Change to Disrupted

```python
def check_regime_change(df: pd.DataFrame, entry_regime: int, current_idx: int) -> bool:
    """
    Exit if regime changes to Disrupted (2) while in position.
    Only applies if entry was in Tight-Deep (0) or Wide-Thin (1).
    """
    if entry_regime == 2:
        return False  # Should never enter in Disrupted
    current_regime = df.iloc[current_idx]['f_liquidity_regime']
    return current_regime == 2
```

### 3.4.6 Master Exit Function

```python
def check_exit(df: pd.DataFrame, entry_idx: int, current_idx: int,
               direction: int, entry_price: float, entry_regime: int,
               params: dict) -> Tuple[bool, str]:
    """
    Check all exit conditions.
    
    Returns:
        (should_exit: bool, exit_reason: str)
        exit_reason is one of: 'profit_target', 'stop_loss', 'max_hold', 'end_of_day', 'regime_change', 'none'
    """
    # Priority order: stop_loss first (protect capital), then profit, then time-based
    
    if check_stop_loss(df, entry_idx, current_idx, direction, entry_price, params):
        return True, 'stop_loss'
    
    if check_profit_target(df, entry_idx, current_idx, direction, entry_price, params):
        return True, 'profit_target'
    
    if check_end_of_day(df, current_idx):
        return True, 'end_of_day'
    
    if check_max_hold(entry_idx, current_idx, params):
        return True, 'max_hold'
    
    if check_regime_change(df, entry_regime, current_idx):
        return True, 'regime_change'
    
    return False, 'none'
```

## 3.5 Signal Encoding

The final signal output per bar is:

```python
# Signal columns added to DataFrame
df['sig_direction'] = 0   # {-1, 0, +1}
df['sig_strength'] = 0.0  # [0, 1]
df['sig_regime'] = -1     # {0, 1, 2, -1}
df['sig_action'] = 'none' # {'enter_long', 'enter_short', 'exit', 'hold', 'none'}
```

### Signal Encoding Rules

| sig_action | sig_direction | Meaning |
|-----------|--------------|---------|
| 'enter_long' | +1 | Open long position this bar |
| 'enter_short' | -1 | Open short position this bar |
| 'exit' | 0 | Close position this bar |
| 'hold' | +/-1 | Continue holding position |
| 'none' | 0 | No position, no action |

### Signal Generation Loop

```python
def generate_signals(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    """
    Generate all signals for the dataset.
    
    Iterates bar by bar, tracking position state.
    Returns DataFrame with sig_* columns populated.
    """
    df = df.copy()
    df['sig_direction'] = 0
    df['sig_strength'] = 0.0
    df['sig_regime'] = -1
    df['sig_action'] = 'none'
    
    # Track position state
    in_position = False
    position_direction = 0  # +1 or -1
    entry_idx = -1
    entry_price = 0.0
    entry_regime = -1
    
    for idx in range(len(df)):
        if not in_position:
            # Try to enter
            direction, strength, regime = generate_entry_signal(df, idx, params)
            if direction != 0:
                # Enter position
                in_position = True
                position_direction = direction
                entry_idx = idx
                entry_price = df.iloc[idx]['close']
                entry_regime = regime
                
                df.at[idx, 'sig_direction'] = direction
                df.at[idx, 'sig_strength'] = strength
                df.at[idx, 'sig_regime'] = regime
                df.at[idx, 'sig_action'] = 'enter_long' if direction == 1 else 'enter_short'
            else:
                df.at[idx, 'sig_action'] = 'none'
        else:
            # Check exit conditions
            should_exit, exit_reason = check_exit(
                df, entry_idx, idx, position_direction, entry_price, entry_regime, params
            )
            
            if should_exit:
                # Exit position
                df.at[idx, 'sig_direction'] = 0
                df.at[idx, 'sig_strength'] = 0.0
                df.at[idx, 'sig_regime'] = entry_regime  # Log regime at entry
                df.at[idx, 'sig_action'] = 'exit'
                
                # Reset state
                in_position = False
                position_direction = 0
                entry_idx = -1
                entry_price = 0.0
                entry_regime = -1
            else:
                # Hold position
                df.at[idx, 'sig_direction'] = position_direction
                df.at[idx, 'sig_strength'] = 0.0  # No new strength on hold
                df.at[idx, 'sig_regime'] = entry_regime
                df.at[idx, 'sig_action'] = 'hold'
    
    return df
```

## 3.6 Signal Statistics and Validation

After generating signals, compute and validate:

```python
def validate_signals(df: pd.DataFrame) -> dict:
    """
    Validate generated signals and return statistics.
    """
    stats = {}
    
    # 1. Total entries
    entries = df[df['sig_action'].isin(['enter_long', 'enter_short'])]
    stats['total_entries'] = len(entries)
    
    # 2. Entries per regime
    for regime, name in [(0, 'tight_deep'), (1, 'wide_thin'), (2, 'disrupted')]:
        regime_entries = entries[entries['sig_regime'] == regime]
        stats[f'entries_{name}'] = len(regime_entries)
    
    # 3. Direction split
    stats['long_entries'] = len(entries[entries['sig_action'] == 'enter_long'])
    stats['short_entries'] = len(entries[entries['sig_action'] == 'enter_short'])
    
    # 4. Signal frequency
    total_bars = len(df)
    stats['signal_rate'] = stats['total_entries'] / total_bars
    
    # 5. Average trades per day
    trading_days = df['date'].nunique()
    stats['trades_per_day'] = stats['total_entries'] / trading_days
    
    # 6. Regime distribution
    regime_counts = df['f_liquidity_regime'].value_counts(normalize=True)
    stats['regime_0_pct'] = regime_counts.get(0, 0)
    stats['regime_1_pct'] = regime_counts.get(1, 0)
    stats['regime_2_pct'] = regime_counts.get(2, 0)
    
    # Validations
    assert stats['trades_per_day'] >= 3.0, f"Too few trades: {stats['trades_per_day']:.2f}/day"
    assert stats['entries_disrupted'] == 0, "Entries detected in Disrupted regime!"
    assert stats['signal_rate'] > 0.01, f"Signal rate too low: {stats['signal_rate']:.4f}"
    
    return stats
```

## 3.7 Signal Generation Summary

The signal generation process can be summarized as:

1. **For each bar** in chronological order:
   a. If FLAT: evaluate entry guards, then regime-specific entry logic
   b. If IN POSITION: evaluate exit triggers in priority order (stop → profit → EOD → max hold → regime change)
2. **Entry signals** require: regime != Disrupted, |depletion| > threshold, |toxicity| > threshold, volume > percentile, not first/last bars of day, ATR > 1.0
3. **Tight-Deep entries** trade continuation: go with depletion direction, confirmed by momentum and EMA alignment
4. **Wide-Thin entries** trade breakthrough: go with depletion acceleration, confirmed by range expansion and volume surge
5. **Disrupted entries** are prohibited
6. **Exits** are triggered by: profit target (ATR-based), stop loss (ATR-based), max hold (N bars), end of day (bar 76+), or regime change to Disrupted
7. **Position sizing** scales with depletion magnitude, capped at 2.0x base

---

# SECTION 4: BACKTESTING ENGINE (COMPLETE)

This section defines the complete backtesting engine including transaction cost modeling, position sizing, P&L computation, trade logging, and equity curve generation.

## 4.1 Transaction Cost Model

### Commission
- **Per contract per side**: $2.50 (all-in rate for ES at interactive brokers tier)
- **Per round turn**: $5.00
- **Model**: Fixed dollar amount per trade, deducted from P&L

### Slippage
- **Slippage model**: Fixed tick slippage per side
- **ES tick size**: 0.25 points per tick
- **Slippage per entry**: 1 tick = 0.25 points (adverse fill)
- **Slippage per exit**: 1 tick = 0.25 points (adverse fill)
- **Total slippage per round turn**: 2 ticks = 0.50 points
- **Dollar value per point**: $50 per ES contract
- **Slippage cost per round turn**: 0.50 * $50 = $25.00

### Total Transaction Cost Per Trade
```
total_cost_per_trade = commission_round_turn + slippage_round_turn
total_cost_per_trade = $5.00 + $25.00 = $30.00 per round turn
```

### Implementation
```python
TRANSACTION_COST_PER_TRADE = 30.00  # Dollars per round turn
ES_POINT_VALUE = 50.00  # Dollars per point
ES_TICK_SIZE = 0.25  # Points per tick
SLIPPAGE_TICKS = 1  # Ticks of slippage per side
```

## 4.2 Position Sizing

### Base Position Size
- **Base size**: 1 contract (minimum trade size)
- **Scaling**: Dynamic based on depletion magnitude

### Position Size Formula
```python
def compute_position_size(df: pd.DataFrame, idx: int, base_size: int = 1) -> int:
    """
    Compute position size in contracts.
    
    Position size = round(base_size * f_position_scale)
    Capped at 2 * base_size (2 contracts max)
    Minimum is 1 contract
    """
    scale = df.iloc[idx]['f_position_scale']
    size = max(1, min(2, round(base_size * scale)))
    return int(size)
```

### Dollar Risk Per Trade
```python
def compute_dollar_risk(df: pd.DataFrame, idx: int, params: dict) -> float:
    """
    Compute dollar risk for a trade.
    Risk = stop_distance_in_points * point_value * num_contracts
    """
    atr = df.iloc[idx]['f_atr_20']
    stop_points = params['stop_loss_pct'] * atr
    num_contracts = compute_position_size(df, idx)
    dollar_risk = stop_points * ES_POINT_VALUE * num_contracts
    return dollar_risk
```

## 4.3 P&L Computation

### Per-Bar P&L

For each bar, compute the P&L contribution from holding a position:

```python
def compute_bar_pnl(df: pd.DataFrame, idx: int, position: int, entry_price: float) -> float:
    """
    Compute P&L for a single bar while holding a position.
    
    position: +1 (long) or -1 (short)
    entry_price: price at which position was entered
    
    Returns: Dollar P&L for this bar (unrealized)
    """
    if position == 0:
        return 0.0
    
    close_price = df.iloc[idx]['close']
    
    if position == 1:  # Long
        point_pnl = close_price - entry_price
    elif position == -1:  # Short
        point_pnl = entry_price - close_price
    
    num_contracts = compute_position_size(df, idx)
    dollar_pnl = point_pnl * ES_POINT_VALUE * num_contracts
    
    return dollar_pnl
```

### Exit P&L (Realized)

```python
def compute_exit_pnl(entry_price: float, exit_price: float, position: int, 
                     num_contracts: int) -> float:
    """
    Compute realized P&L when exiting a position.
    Deducts transaction costs.
    """
    if position == 1:  # Long
        point_pnl = exit_price - entry_price
    elif position == -1:  # Short
        point_pnl = entry_price - exit_price
    else:
        return 0.0
    
    gross_pnl = point_pnl * ES_POINT_VALUE * num_contracts
    net_pnl = gross_pnl - TRANSACTION_COST_PER_TRADE
    
    return net_pnl
```

### Slippage-Adjusted Entry/Exit Prices

```python
def apply_slippage(price: float, direction: str, side: str) -> float:
    """
    Apply slippage to price.
    
    direction: 'long' or 'short' (the position being taken)
    side: 'entry' or 'exit'
    
    For long entry: price worse by +1 tick (buy higher)
    For long exit: price worse by -1 tick (sell lower)
    For short entry: price worse by -1 tick (sell lower)
    For short exit: price worse by +1 tick (buy higher)
    """
    slippage = ES_TICK_SIZE * SLIPPAGE_TICKS
    
    if direction == 'long' and side == 'entry':
        return price + slippage
    elif direction == 'long' and side == 'exit':
        return price - slippage
    elif direction == 'short' and side == 'entry':
        return price - slippage
    elif direction == 'short' and side == 'exit':
        return price + slippage
    
    return price
```

## 4.4 Complete Backtest Loop

```python
@dataclass
class Trade:
    """Represents a single completed trade."""
    entry_idx: int
    exit_idx: int
    entry_time: pd.Timestamp
    exit_time: pd.Timestamp
    direction: int  # +1 long, -1 short
    entry_price: float
    exit_price: float
    entry_regime: int
    num_contracts: int
    gross_pnl: float
    net_pnl: float
    bars_held: int
    exit_reason: str
    max_adverse_excursion: float  # Worst intra-trade P&L in points
    max_favorable_excursion: float  # Best intra-trade P&L in points


def run_backtest(df: pd.DataFrame, params: dict) -> Tuple[pd.DataFrame, List[Trade]]:
    """
    Run complete backtest.
    
    Args:
        df: DataFrame with features and signals
        params: Strategy parameters
    
    Returns:
        (df_with_pnl, trades_list)
    """
    df = df.copy()
    df['position'] = 0  # Current position
    df['unrealized_pnl'] = 0.0
    df['realized_pnl'] = 0.0
    df['cumulative_pnl'] = 0.0
    df['equity'] = 0.0
    
    trades: List[Trade] = []
    
    # State variables
    in_position = False
    position_direction = 0
    entry_idx = -1
    entry_price = 0.0  # Slippage-adjusted
    entry_regime = -1
    num_contracts = 0
    trade_max_adverse = 0.0
    trade_max_favorable = 0.0
    cumulative_pnl = 0.0
    
    for idx in range(len(df)):
        action = df.iloc[idx]['sig_action']
        
        if action in ['enter_long', 'enter_short']:
            # Open position
            in_position = True
            position_direction = 1 if action == 'enter_long' else -1
            entry_idx = idx
            entry_regime = int(df.iloc[idx]['sig_regime'])
            num_contracts = compute_position_size(df, idx)
            
            # Apply slippage to entry price
            raw_entry = df.iloc[idx]['close']
            direction_str = 'long' if position_direction == 1 else 'short'
            entry_price = apply_slippage(raw_entry, direction_str, 'entry')
            
            trade_max_adverse = 0.0
            trade_max_favorable = 0.0
            
            df.at[idx, 'position'] = position_direction
            
        elif action == 'exit' and in_position:
            # Close position
            raw_exit = df.iloc[idx]['close']
            direction_str = 'long' if position_direction == 1 else 'short'
            exit_price = apply_slippage(raw_exit, direction_str, 'exit')
            
            # Compute P&L
            gross_pnl = compute_exit_pnl(entry_price, exit_price, position_direction, num_contracts)
            net_pnl = gross_pnl - TRANSACTION_COST_PER_TRADE
            
            # Determine exit reason
            _, exit_reason = check_exit(df, entry_idx, idx, position_direction, 
                                        entry_price, entry_regime, params)
            
            # Record trade
            trade = Trade(
                entry_idx=entry_idx,
                exit_idx=idx,
                entry_time=df.iloc[entry_idx]['ts_event'],
                exit_time=df.iloc[idx]['ts_event'],
                direction=position_direction,
                entry_price=entry_price,
                exit_price=exit_price,
                entry_regime=entry_regime,
                num_contracts=num_contracts,
                gross_pnl=gross_pnl,
                net_pnl=net_pnl,
                bars_held=idx - entry_idx,
                exit_reason=exit_reason,
                max_adverse_excursion=trade_max_adverse,
                max_favorable_excursion=trade_max_favorable
            )
            trades.append(trade)
            
            # Update cumulative P&L
            cumulative_pnl += net_pnl
            df.at[idx, 'realized_pnl'] = net_pnl
            
            # Reset state
            in_position = False
            position_direction = 0
            entry_idx = -1
            entry_price = 0.0
            entry_regime = -1
            num_contracts = 0
            df.at[idx, 'position'] = 0
            
        elif action == 'hold' and in_position:
            # Update unrealized P&L and track MAE/MFE
            current_close = df.iloc[idx]['close']
            if position_direction == 1:
                points_pnl = current_close - entry_price
            else:
                points_pnl = entry_price - current_close
            
            trade_max_favorable = max(trade_max_favorable, points_pnl)
            trade_max_adverse = min(trade_max_adverse, points_pnl)
            
            unrealized = points_pnl * ES_POINT_VALUE * num_contracts
            df.at[idx, 'unrealized_pnl'] = unrealized
            df.at[idx, 'position'] = position_direction
        
        # Update equity curve
        df.at[idx, 'cumulative_pnl'] = cumulative_pnl + df.at[idx, 'unrealized_pnl']
    
    # Set starting equity to $100,000 for percentage-based metrics
    STARTING_EQUITY = 100000.0
    df['equity'] = STARTING_EQUITY + df['cumulative_pnl']
    
    return df, trades
```

## 4.5 Trade Summary Statistics

```python
def compute_trade_statistics(trades: List[Trade], df: pd.DataFrame) -> dict:
    """
    Compute comprehensive trade statistics.
    """
    if not trades:
        return {'error': 'No trades generated'}
    
    stats = {}
    
    # Basic counts
    stats['total_trades'] = len(trades)
    stats['long_trades'] = sum(1 for t in trades if t.direction == 1)
    stats['short_trades'] = sum(1 for t in trades if t.direction == -1)
    
    # P&L statistics
    net_pnls = [t.net_pnl for t in trades]
    stats['total_net_pnl'] = sum(net_pnls)
    stats['total_gross_pnl'] = sum(t.gross_pnl for t in trades)
    stats['total_costs'] = stats['total_gross_pnl'] - stats['total_net_pnl']
    stats['avg_pnl_per_trade'] = np.mean(net_pnls)
    stats['pnl_std'] = np.std(net_pnls)
    stats['median_pnl'] = np.median(net_pnls)
    
    # Win/Loss statistics
    winning_trades = [t for t in trades if t.net_pnl > 0]
    losing_trades = [t for t in trades if t.net_pnl <= 0]
    stats['winning_trades'] = len(winning_trades)
    stats['losing_trades'] = len(losing_trades)
    stats['win_rate'] = len(winning_trades) / len(trades) if trades else 0
    stats['avg_win'] = np.mean([t.net_pnl for t in winning_trades]) if winning_trades else 0
    stats['avg_loss'] = np.mean([t.net_pnl for t in losing_trades]) if losing_trades else 0
    stats['profit_factor'] = (
        sum(t.net_pnl for t in winning_trades) / abs(sum(t.net_pnl for t in losing_trades))
        if losing_trades and sum(t.net_pnl for t in losing_trades) != 0 else float('inf')
    )
    stats['payoff_ratio'] = abs(stats['avg_win'] / stats['avg_loss']) if stats['avg_loss'] != 0 else float('inf')
    
    # Holding period
    stats['avg_bars_held'] = np.mean([t.bars_held for t in trades])
    stats['median_bars_held'] = np.median([t.bars_held for t in trades])
    
    # Exit reason distribution
    exit_reasons = {}
    for t in trades:
        exit_reasons[t.exit_reason] = exit_reasons.get(t.exit_reason, 0) + 1
    stats['exit_reasons'] = exit_reasons
    
    # Regime-specific statistics
    for regime, name in [(0, 'tight_deep'), (1, 'wide_thin')]:
        regime_trades = [t for t in trades if t.entry_regime == regime]
        if regime_trades:
            regime_wins = [t for t in regime_trades if t.net_pnl > 0]
            stats[f'{name}_accuracy'] = len(regime_wins) / len(regime_trades)
            stats[f'{name}_trades'] = len(regime_trades)
            stats[f'{name}_avg_pnl'] = np.mean([t.net_pnl for t in regime_trades])
        else:
            stats[f'{name}_accuracy'] = 0
            stats[f'{name}_trades'] = 0
            stats[f'{name}_avg_pnl'] = 0
    
    # MAE/MFE statistics
    stats['avg_mae'] = np.mean([t.max_adverse_excursion for t in trades])
    stats['avg_mfe'] = np.mean([t.max_favorable_excursion for t in trades])
    
    # Trading frequency
    trading_days = df['date'].nunique()
    stats['trades_per_day'] = stats['total_trades'] / trading_days if trading_days > 0 else 0
    
    return stats
```

## 4.6 Equity Curve and Drawdown Computation

```python
def compute_equity_metrics(df: pd.DataFrame, trades: List[Trade]) -> dict:
    """
    Compute equity curve metrics.
    """
    metrics = {}
    
    equity = df['equity'].values
    
    # Peak equity and drawdown
    peak = np.maximum.accumulate(equity)
    drawdown = (equity - peak) / peak
    drawdown_dollars = equity - peak
    
    metrics['final_equity'] = equity[-1]
    metrics['total_return_pct'] = (equity[-1] / equity[0] - 1) * 100
    metrics['max_drawdown_pct'] = drawdown.min() * 100
    metrics['max_drawdown_dollars'] = drawdown_dollars.min()
    
    # Find max drawdown duration
    max_dd_idx = np.argmin(drawdown)
    peak_before_dd = equity[:max_dd_idx+1].argmax()
    metrics['max_drawdown_duration_bars'] = max_dd_idx - peak_before_dd
    
    # Sharpe ratio (annualized)
    returns = df['equity'].pct_change().dropna()
    if len(returns) > 1 and returns.std() > 0:
        # Annualize: 78 bars/day * 252 days/year
        bars_per_year = 78 * 252
        sharpe = (returns.mean() / returns.std()) * np.sqrt(bars_per_year)
        metrics['sharpe_ratio'] = sharpe
    else:
        metrics['sharpe_ratio'] = 0
    
    # Sortino ratio
    downside_returns = returns[returns < 0]
    if len(downside_returns) > 0 and downside_returns.std() > 0:
        sortino = (returns.mean() / downside_returns.std()) * np.sqrt(bars_per_year)
        metrics['sortino_ratio'] = sortino
    else:
        metrics['sortino_ratio'] = 0
    
    # Calmar ratio
    if abs(metrics['max_drawdown_pct']) > 0:
        metrics['calmar_ratio'] = metrics['total_return_pct'] / abs(metrics['max_drawdown_pct'])
    else:
        metrics['calmar_ratio'] = float('inf')
    
    # Add drawdown series to DataFrame
    df['peak_equity'] = peak
    df['drawdown_pct'] = drawdown * 100
    df['drawdown_dollars'] = drawdown_dollars
    
    return metrics
```

## 4.7 Performance Report

```python
def generate_performance_report(df: pd.DataFrame, trades: List[Trade]) -> str:
    """
    Generate a formatted performance report.
    """
    trade_stats = compute_trade_statistics(trades, df)
    equity_metrics = compute_equity_metrics(df, trades)
    
    report = f"""
{'='*70}
STRATEGY 2 PERFORMANCE REPORT
Queue-Depletion Momentum with Liquidity Regime Filter
{'='*70}

TRADE STATISTICS
----------------
Total Trades:           {trade_stats['total_trades']}
Long Trades:            {trade_stats['long_trades']}
Short Trades:           {trade_stats['short_trades']}
Win Rate:               {trade_stats['win_rate']*100:.2f}%
Profit Factor:          {trade_stats['profit_factor']:.3f}
Payoff Ratio:           {trade_stats['payoff_ratio']:.3f}

P&L SUMMARY
-----------
Total Net P&L:          ${trade_stats['total_net_pnl']:,.2f}
Total Gross P&L:        ${trade_stats['total_gross_pnl']:,.2f}
Total Costs:            ${trade_stats['total_costs']:,.2f}
Avg P&L per Trade:      ${trade_stats['avg_pnl_per_trade']:.2f}
Median P&L:             ${trade_stats['median_pnl']:.2f}

WIN/LOSS BREAKDOWN
------------------
Winning Trades:         {trade_stats['winning_trades']}
Losing Trades:          {trade_stats['losing_trades']}
Avg Win:                ${trade_stats['avg_win']:.2f}
Avg Loss:               ${trade_stats['avg_loss']:.2f}

REGIME PERFORMANCE
------------------
Tight-Deep Accuracy:    {trade_stats.get('tight_deep_accuracy', 0)*100:.2f}% ({trade_stats.get('tight_deep_trades', 0)} trades)
Wide-Thin Accuracy:     {trade_stats.get('wide_thin_accuracy', 0)*100:.2f}% ({trade_stats.get('wide_thin_trades', 0)} trades)

TRADE EXECUTION
---------------
Avg Bars Held:          {trade_stats['avg_bars_held']:.2f}
Trades per Day:         {trade_stats['trades_per_day']:.2f}
Avg MAE (points):       {trade_stats['avg_mae']:.4f}
Avg MFE (points):       {trade_stats['avg_mfe']:.4f}

EQUITY METRICS
--------------
Final Equity:           ${equity_metrics['final_equity']:,.2f}
Total Return:           {equity_metrics['total_return_pct']:.2f}%
Max Drawdown:           {equity_metrics['max_drawdown_pct']:.2f}%
Sharpe Ratio:           {equity_metrics['sharpe_ratio']:.3f}
Sortino Ratio:          {equity_metrics['sortino_ratio']:.3f}
Calmar Ratio:           {equity_metrics['calmar_ratio']:.3f}

EXIT REASONS
------------
{chr(10).join(f"  {k}: {v}" for k, v in trade_stats.get('exit_reasons', {}).items())}
{'='*70}
"""
    return report
```

## 4.8 Same-Bar Signal Handling

The strategy does NOT enter and exit on the same bar. If an exit condition and entry condition both trigger on the same bar, priority is given to the exit (close current position first), then evaluate entry for the next bar. This is naturally handled by the sequential bar-by-bar loop.

## 4.9 End-of-Day Position Handling

- **No overnight positions**: All positions must be closed by bar 76 (15:50 ET)
- **Entry prohibition**: No new entries after bar 74 (15:40 ET)
- **Forced exit**: Bar 76 triggers exit regardless of P&L
- **Rationale**: ES has different overnight dynamics; holding overnight introduces gap risk not captured by the intraday model

## 4.10 Intraday Drawdown Control

```python
def check_intraday_drawdown(df: pd.DataFrame, trades: List[Trade], 
                            max_intraday_dd_pct: float = 3.0) -> bool:
    """
    Check if intraday drawdown exceeds threshold.
    Used as a circuit breaker to stop trading for the day.
    """
    daily_pnl = df.groupby('date')['realized_pnl'].sum()
    daily_cumsum = daily_pnl.cumsum()
    daily_peak = daily_cumsum.cummax()
    daily_dd = (daily_cumsum - daily_peak) / daily_peak * 100
    
    return daily_dd.min() >= -max_intraday_dd_pct
```



---

# SECTION 5: VALIDATION FRAMEWORK

This section defines the complete validation methodology including walk-forward analysis, cross-validation, performance metrics, statistical significance tests, and anti-curve-fit constraints.

## 5.1 Walk-Forward Analysis (WFA)

### 5.1.1 WFA Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| In-sample window size | 15,600 bars | 200 trading days (~9.5 months) of in-sample data |
| Out-of-sample window size | 3,900 bars | 50 trading days (~2.4 months) of OOS data |
| Step size | 3,900 bars | Non-overlapping OOS periods (roll forward by 50 days) |
| Number of folds | 18 | 85,600 dev bars / 3,900 step ≈ 21 folds, but first fold needs 15,600 IS + 3,900 OOS, so 18 complete folds |
| Minimum folds required | 10 | If fewer than 10 folds, expand OOS window |

### 5.1.2 WFA Window Schedule

```python
def generate_wfa_windows(dev_size: int = 85600, is_size: int = 15600, 
                         oos_size: int = 3900) -> List[Tuple[int, int, int, int]]:
    """
    Generate walk-forward analysis windows.
    
    Returns list of (is_start, is_end, oos_start, oos_end) index tuples.
    is_end and oos_start are the same (contiguous).
    """
    windows = []
    
    # First fold: IS = [0, 15600), OOS = [15600, 19500)
    # Subsequent folds roll forward by oos_size
    
    oos_start = is_size
    while oos_start + oos_size <= dev_size:
        is_start = oos_start - is_size
        is_end = oos_start
        oos_end = oos_start + oos_size
        
        windows.append((is_start, is_end, oos_start, oos_end))
        oos_start += oos_size
    
    return windows
```

For 85,600 dev bars, this generates the following windows:

| Fold # | IS Start | IS End | OOS Start | OOS End | IS Days | OOS Days |
|--------|----------|--------|-----------|---------|---------|----------|
| 1 | 0 | 15,600 | 15,600 | 19,500 | 200 | 50 |
| 2 | 3,900 | 19,500 | 19,500 | 23,400 | 200 | 50 |
| 3 | 7,800 | 23,400 | 23,400 | 27,300 | 200 | 50 |
| ... | ... | ... | ... | ... | ... | ... |
| 18 | 66,300 | 81,900 | 81,900 | 85,600 | ~200 | ~50 |

### 5.1.3 WFA Procedure

```python
def run_walk_forward_analysis(df_dev: pd.DataFrame, param_grid: dict) -> dict:
    """
    Run walk-forward analysis with parameter optimization on each IS fold.
    
    Returns WFA results including OOS performance per fold.
    """
    windows = generate_wfa_windows()
    fold_results = []
    
    for fold_num, (is_start, is_end, oos_start, oos_end) in enumerate(windows, 1):
        print(f"WFA Fold {fold_num}/{len(windows)}: IS [{is_start}:{is_end}], OOS [{oos_start}:{oos_end}]")
        
        # Split IS and OOS
        df_is = df_dev.iloc[is_start:is_end].copy()
        df_oos = df_dev.iloc[oos_start:oos_end].copy()
        
        # Step 1: Optimize parameters on IS data
        best_params = optimize_parameters(df_is, param_grid)
        
        # Step 2: Compute features on IS data (for statistics)
        df_is_feat = compute_all_features(df_is)
        df_is_sig = generate_signals(df_is_feat, best_params)
        df_is_bt, is_trades = run_backtest(df_is_sig, best_params)
        is_stats = compute_trade_statistics(is_trades, df_is_bt)
        
        # Step 3: Apply to OOS data (no parameter change!)
        df_oos_feat = compute_all_features(df_oos)
        df_oos_sig = generate_signals(df_oos_feat, best_params)
        df_oos_bt, oos_trades = run_backtest(df_oos_sig, best_params)
        oos_stats = compute_trade_statistics(oos_trades, df_oos_bt)
        oos_equity = compute_equity_metrics(df_oos_bt, oos_trades)
        
        fold_results.append({
            'fold': fold_num,
            'is_start': is_start,
            'is_end': is_end,
            'oos_start': oos_start,
            'oos_end': oos_end,
            'best_params': best_params,
            'is_win_rate': is_stats['win_rate'],
            'is_trades_per_day': is_stats['trades_per_day'],
            'oos_win_rate': oos_stats['win_rate'],
            'oos_trades_per_day': oos_stats['trades_per_day'],
            'oos_sharpe': oos_equity['sharpe_ratio'],
            'oos_max_dd': oos_equity['max_drawdown_pct'],
            'oos_total_pnl': oos_stats['total_net_pnl'],
            'wide_thin_accuracy': oos_stats.get('wide_thin_accuracy', 0),
            'tight_deep_accuracy': oos_stats.get('tight_deep_accuracy', 0),
        })
    
    return {
        'fold_results': fold_results,
        'summary': summarize_wfa_results(fold_results)
    }
```

### 5.1.4 WFA Summary Statistics

```python
def summarize_wfa_results(fold_results: List[dict]) -> dict:
    """
    Summarize walk-forward results across all folds.
    """
    summary = {}
    
    # OOS win rate across folds
    oos_win_rates = [f['oos_win_rate'] for f in fold_results]
    summary['mean_oos_win_rate'] = np.mean(oos_win_rates)
    summary['std_oos_win_rate'] = np.std(oos_win_rates)
    summary['min_oos_win_rate'] = np.min(oos_win_rates)
    summary['pct_folds_above_52.5'] = sum(1 for w in oos_win_rates if w > 0.525) / len(oos_win_rates)
    summary['pct_folds_above_54'] = sum(1 for w in oos_win_rates if w > 0.54) / len(oos_win_rates)
    
    # OOS trades per day
    oos_tpd = [f['oos_trades_per_day'] for f in fold_results]
    summary['mean_oos_trades_per_day'] = np.mean(oos_tpd)
    summary['min_oos_trades_per_day'] = np.min(oos_tpd)
    
    # OOS Sharpe
    oos_sharpes = [f['oos_sharpe'] for f in fold_results]
    summary['mean_oos_sharpe'] = np.mean(oos_sharpes)
    summary['pct_folds_sharpe_positive'] = sum(1 for s in oos_sharpes if s > 0) / len(oos_sharpes)
    
    # Wide-Thin accuracy
    wta = [f['wide_thin_accuracy'] for f in fold_results]
    summary['mean_wide_thin_accuracy'] = np.mean(wta)
    summary['pct_folds_wt_above_54'] = sum(1 for w in wta if w > 0.54) / len(wta)
    summary['pct_folds_wt_above_56'] = sum(1 for w in wta if w > 0.56) / len(wta)
    
    # Consistency score: fraction of folds meeting ALL targets
    meets_targets = []
    for f in fold_results:
        meets = (
            f['oos_win_rate'] > 0.525 and
            f['oos_trades_per_day'] > 4.5 and
            f['wide_thin_accuracy'] > 0.54
        )
        meets_targets.append(meets)
    summary['consistency_score'] = sum(meets_targets) / len(meets_targets)
    
    return summary
```

## 5.2 Parameter Optimization

### 5.2.1 Search Space

```python
PARAM_GRID = {
    'dep_threshold': [0.05, 0.10, 0.15, 0.20, 0.30, 0.50],
    'tox_threshold': [0.05, 0.10, 0.20, 0.40, 0.80],
    'momentum_confirm': [0.0, 0.0001, 0.0002, 0.0005, 0.001],
    'breakthrough_threshold': [0.02, 0.05, 0.10, 0.20, 0.30],
    'exit_bars': [2, 3, 4, 5, 6, 8],
    'profit_target_pct': [0.3, 0.5, 0.8, 1.2, 2.0],
    'stop_loss_pct': [0.2, 0.4, 0.6, 1.0, 1.5],
    'min_volume_pctile': [10.0, 20.0, 30.0, 40.0, 50.0],
}
```

Total combinations: 6 × 5 × 5 × 5 × 6 × 5 × 5 × 5 = **281,250 combinations**

### 5.2.2 Optimization Objective

The objective function combines multiple targets into a single score:

```python
def objective_function(stats: dict, equity: dict) -> float:
    """
    Combined objective for parameter optimization.
    Higher is better.
    
    Penalizes:
    - Low win rate (below 52.5%)
    - Low trade frequency (below 4.5/day)
    - Low Wide-Thin accuracy (below 54%)
    - High drawdown (above 15%)
    - Negative Sharpe
    
    Rewards:
    - High win rate
    - High Sharpe ratio
    - High Wide-Thin accuracy
    - High profit factor
    """
    score = 0.0
    
    # Win rate component (0-40 points)
    wr = stats['win_rate']
    if wr < 0.525:
        score -= 100  # Heavy penalty for below minimum
    else:
        score += 40 * min((wr - 0.50) / 0.10, 1.0)  # Linear up to 60%
    
    # Trade frequency component (0-20 points)
    tpd = stats['trades_per_day']
    if tpd < 4.5:
        score -= 50
    else:
        score += 20 * min(tpd / 10.0, 1.0)
    
    # Wide-Thin accuracy component (0-25 points)
    wt_acc = stats.get('wide_thin_accuracy', 0)
    if wt_acc < 0.54:
        score -= 50
    else:
        score += 25 * min((wt_acc - 0.50) / 0.10, 1.0)
    
    # Sharpe component (0-15 points)
    sharpe = equity.get('sharpe_ratio', 0)
    score += 15 * min(max(sharpe, 0) / 2.0, 1.0)
    
    # Drawdown penalty
    mdd = abs(equity.get('max_drawdown_pct', 0))
    if mdd > 15:
        score -= 50
    elif mdd > 10:
        score -= 20 * (mdd - 10) / 5
    
    return score
```

### 5.2.3 Grid Search with Early Stopping

```python
def optimize_parameters(df_is: pd.DataFrame, param_grid: dict,
                        max_evals: int = 1000) -> dict:
    """
    Grid search parameter optimization with early stopping.
    
    Evaluates at most max_evals combinations.
    Returns best parameters found.
    """
    from itertools import product
    
    best_score = -float('inf')
    best_params = None
    eval_count = 0
    
    # Generate all combinations
    keys = list(param_grid.keys())
    values = [param_grid[k] for k in keys]
    
    for combo in product(*values):
        if eval_count >= max_evals:
            break
        
        params = dict(zip(keys, combo))
        
        # Run backtest with these parameters
        df_feat = compute_all_features(df_is)
        df_sig = generate_signals(df_feat, params)
        df_bt, trades = run_backtest(df_sig, params)
        
        if not trades:
            continue
        
        stats = compute_trade_statistics(trades, df_bt)
        equity = compute_equity_metrics(df_bt, trades)
        
        score = objective_function(stats, equity)
        
        if score > best_score:
            best_score = score
            best_params = params.copy()
        
        eval_count += 1
    
    if best_params is None:
        # Fallback to defaults if no valid combination found
        best_params = DEFAULT_PARAMS.copy()
    
    return best_params
```

### 5.2.4 Default Parameters

```python
DEFAULT_PARAMS = {
    'dep_threshold': 0.15,
    'tox_threshold': 0.20,
    'momentum_confirm': 0.0002,
    'breakthrough_threshold': 0.10,
    'exit_bars': 4,
    'profit_target_pct': 0.8,
    'stop_loss_pct': 0.6,
    'min_volume_pctile': 30.0,
}
```

## 5.3 Performance Metrics

### 5.3.1 Required Metrics

Compute ALL of the following metrics for both development (WFA OOS) and test sets:

| # | Metric | Formula | Target |
|---|--------|---------|--------|
| 1 | Win Rate | winning_trades / total_trades | > 54% |
| 2 | Trades per Day | total_trades / trading_days | > 5 |
| 3 | Wide-Thin Accuracy | winning WT trades / total WT trades | > 56% |
| 4 | Sharpe Ratio | (mean_return / std_return) * sqrt(252*78) | > 1.0 |
| 5 | Max Drawdown % | max(peak - equity) / peak | < 12% |
| 6 | Profit Factor | sum(wins) / abs(sum(losses)) | > 1.15 |
| 7 | Sortino Ratio | (mean_return / downside_std) * sqrt(252*78) | > 1.0 |
| 8 | Calmar Ratio | annualized_return / max_drawdown | > 0.5 |
| 9 | Payoff Ratio | avg_win / abs(avg_loss) | > 1.0 |
| 10 | Total Net P&L | sum(net_pnl across all trades) | > $0 |
| 11 | Average P&L per Trade | total_net_pnl / total_trades | > $0 |
| 12 | Return on Account | total_net_pnl / starting_equity | > 0 |

### 5.3.2 Regime-Specific Metrics

| # | Metric | Target |
|---|--------|--------|
| 13 | Tight-Deep Trade Count | > 100 total |
| 14 | Tight-Deep Win Rate | > 52% |
| 15 | Wide-Thin Trade Count | > 50 total |
| 16 | Wide-Thin Win Rate | > 56% |
| 17 | Disrupted Trade Count | = 0 (no trades in disrupted regime) |

### 5.3.3 Monthly Consistency Metrics

| # | Metric | Target |
|---|--------|--------|
| 18 | % Profitable Months | > 50% |
| 19 | Best Month P&L | Positive |
| 20 | Worst Month P&L | Better than -$5,000 |

## 5.4 Statistical Significance Tests

### 5.4.1 Binomial Test for Win Rate

```python
from scipy import stats

def test_win_rate_significance(num_wins: int, num_trades: int, 
                                null_hypothesis_wr: float = 0.50) -> dict:
    """
    Binomial test: Is the win rate significantly > 50%?
    
    H0: true_win_rate <= 0.50
    H1: true_win_rate > 0.50
    """
    result = stats.binom_test(num_wins, num_trades, null_hypothesis_wr, alternative='greater')
    
    # Also compute confidence interval
    ci_low, ci_high = stats.proportion_confint(num_wins, num_trades, alpha=0.05, method='wilson')
    
    return {
        'p_value': result,
        'significant_at_5pct': result < 0.05,
        'significant_at_1pct': result < 0.01,
        'ci_95_low': ci_low,
        'ci_95_high': ci_high,
    }
```

### 5.4.2 Sharpe Ratio Significance Test

```python
def test_sharpe_significance(sharpe: float, num_obs: int) -> dict:
    """
    Test if Sharpe ratio is significantly > 0.
    
    t-statistic = Sharpe * sqrt(n)
    """
    t_stat = sharpe * np.sqrt(num_obs)
    p_value = 1 - stats.t.cdf(t_stat, df=num_obs - 1)
    
    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'significant_at_5pct': p_value < 0.05,
        'significant_at_1pct': p_value < 0.01,
    }
```

### 5.4.3 Permutation Test

```python
def permutation_test(df: pd.DataFrame, trades: List[Trade], 
                     n_permutations: int = 1000) -> dict:
    """
    Permutation test: Is the strategy's performance better than random?
    
    Shuffle trade directions randomly and recompute P&L distribution.
    """
    actual_pnl = sum(t.net_pnl for t in trades)
    
    # Extract trade durations and entry times (keep these fixed)
    trade_info = [(t.bars_held, t.entry_idx, t.num_contracts) for t in trades]
    
    permuted_pnls = []
    for _ in range(n_permutations):
        perm_pnl = 0
        for bars_held, entry_idx, num_contracts in trade_info:
            # Random direction
            direction = np.random.choice([-1, 1])
            entry_price = df.iloc[entry_idx]['close']
            exit_idx = min(entry_idx + bars_held, len(df) - 1)
            exit_price = df.iloc[exit_idx]['close']
            
            if direction == 1:
                pnl = (exit_price - entry_price) * ES_POINT_VALUE * num_contracts
            else:
                pnl = (entry_price - exit_price) * ES_POINT_VALUE * num_contracts
            
            perm_pnl += pnl - TRANSACTION_COST_PER_TRADE
        
        permuted_pnls.append(perm_pnl)
    
    permuted_pnls = np.array(permuted_pnls)
    p_value = np.mean(permuted_pnls >= actual_pnl)
    
    return {
        'actual_pnl': actual_pnl,
        'perm_mean_pnl': np.mean(permuted_pnls),
        'perm_std_pnl': np.std(permuted_pnls),
        'perm_5pct_pnl': np.percentile(permuted_pnls, 95),
        'p_value': p_value,
        'significant_at_5pct': p_value < 0.05,
    }
```

## 5.5 Anti-Curve-Fit Constraints

### 5.5.1 Parameter Count Limit
- **Maximum optimized parameters**: 10 (strategy uses 8)
- **Justification**: With 8 parameters, the model has moderate complexity. The WFA approach with 18 folds provides sufficient data to validate parameter stability.

### 5.5.2 Degrees of Freedom Budget

```python
def compute_degrees_of_freedom(num_trades: int, num_params: int) -> dict:
    """
    Compute effective degrees of freedom.
    
    Rule of thumb: Need at least 100 trades per optimized parameter.
    """
    trades_per_param = num_trades / num_params
    return {
        'num_trades': num_trades,
        'num_params': num_params,
        'trades_per_param': trades_per_param,
        'sufficient': trades_per_param >= 100,
    }
```

### 5.5.3 WFA Consistency Requirements

For the strategy to pass validation, ALL of the following must be true:

| # | Constraint | Threshold | Rationale |
|---|-----------|-----------|-----------|
| 1 | % folds with WR > 52.5% | >= 60% | Majority of folds profitable |
| 2 | % folds with WR > 54% | >= 40% | Significant portion strong |
| 3 | % folds with positive Sharpe | >= 65% | Most folds make money |
| 4 | Mean OOS WR - Mean IS WR | <= 5% | No severe overfit |
| 5 | Consistency score (all targets) | >= 30% | Reasonable consistency |
| 6 | WT accuracy in test set | >= 54% | Key target metric |

### 5.5.4 Parameter Stability

```python
def check_parameter_stability(fold_results: List[dict]) -> dict:
    """
    Check if optimized parameters are stable across folds.
    
    High variance in parameters indicates overfitting.
    """
    # Extract parameter values across folds
    param_names = ['dep_threshold', 'tox_threshold', 'momentum_confirm',
                   'breakthrough_threshold', 'exit_bars', 'profit_target_pct',
                   'stop_loss_pct', 'min_volume_pctile']
    
    stability = {}
    for pname in param_names:
        values = [f['best_params'][pname] for f in fold_results]
        stability[pname] = {
            'mean': np.mean(values),
            'std': np.std(values),
            'cv': np.std(values) / abs(np.mean(values)) if np.mean(values) != 0 else 0,
            'range': (np.min(values), np.max(values)),
            'stable': np.std(values) < 0.3 * abs(np.mean(values)),  # CV < 30%
        }
    
    # Overall stability: fraction of parameters that are stable
    stability['overall_stable'] = np.mean([
        stability[p]['stable'] for p in param_names
    ])
    
    return stability
```

## 5.6 Final Test Set Evaluation

```python
def evaluate_on_test_set(df_test: pd.DataFrame, best_params: dict) -> dict:
    """
    FINAL evaluation on test set. Run exactly once.
    
    No parameter tuning. No model selection. Use parameters from WFA.
    """
    # Compute features
    df_test_feat = compute_all_features(df_test)
    
    # Generate signals
    df_test_sig = generate_signals(df_test_feat, best_params)
    
    # Run backtest
    df_test_bt, test_trades = run_backtest(df_test_sig, best_params)
    
    # Compute statistics
    test_stats = compute_trade_statistics(test_trades, df_test_bt)
    test_equity = compute_equity_metrics(df_test_bt, test_trades)
    
    # Statistical tests
    binomial_test = test_win_rate_significance(test_stats['winning_trades'], 
                                                test_stats['total_trades'])
    sharpe_test = test_sharpe_significance(test_equity['sharpe_ratio'],
                                           len(df_test_bt))
    perm_test = permutation_test(df_test_bt, test_trades)
    
    results = {
        'trade_stats': test_stats,
        'equity_metrics': test_equity,
        'binomial_test': binomial_test,
        'sharpe_test': sharpe_test,
        'permutation_test': perm_test,
        'passes_targets': check_targets(test_stats, test_equity),
    }
    
    return results


def check_targets(stats: dict, equity: dict) -> dict:
    """
    Check if results meet all targets.
    """
    checks = {
        'overall_accuracy': stats['win_rate'] > 0.54,
        'trades_per_day': stats['trades_per_day'] > 5,
        'wide_thin_accuracy': stats.get('wide_thin_accuracy', 0) > 0.56,
        'sharpe_ratio': equity['sharpe_ratio'] > 1.0,
        'max_drawdown': abs(equity['max_drawdown_pct']) < 12,
        'profit_factor': stats['profit_factor'] > 1.15,
        'win_rate': stats['win_rate'] > 0.54,
    }
    checks['all_pass'] = all(checks.values())
    return checks
```

---

# SECTION 6: CODE ARCHITECTURE

## 6.1 File Structure

```
strategy_02_queue_depletion/
├── __init__.py              # Package init
├── config.py                # All constants, parameters, and configuration
├── data_pipeline.py         # Data loading, cleaning, validation
├── features.py              # Feature engineering (all 30+ features)
├── signals.py               # Signal generation engine
├── backtest.py              # Backtesting engine, trade logging
├── validation.py            # Walk-forward analysis, optimization, metrics
├── reporting.py             # Performance reports, plotting
├── main.py                  # Main execution script
└── tests/
    ├── __init__.py
    ├── test_data.py         # Data pipeline unit tests
    ├── test_features.py     # Feature computation unit tests
    ├── test_signals.py      # Signal generation unit tests
    └── test_backtest.py     # Backtest engine unit tests
```

## 6.2 Module Specifications

### 6.2.1 config.py

```python
"""
Configuration module for Strategy 2.
All constants and tunable parameters in one place.
"""

import numpy as np

# ============================================================================
# DATA CONFIGURATION
# ============================================================================
DATA_PATH = "/mnt/agents/upload/ES_5min_RTH_6year.csv"
OUTPUT_DIR = "/mnt/agents/output"

# Column names (must match CSV exactly)
COL_TIMESTAMP = "ts_event"
COL_SYMBOL = "symbol"
COL_OPEN = "open"
COL_HIGH = "high"
COL_LOW = "low"
COL_CLOSE = "close"
COL_VOLUME = "volume"

# Data parameters
EXPECTED_TOTAL_ROWS = 122295
DEV_SET_SIZE = 85600
TEST_SET_START = 85600
BARS_PER_DAY = 78
RTH_START_TIME = "09:30"
RTH_END_TIME = "16:00"
BAR_FREQUENCY_MINUTES = 5

# ============================================================================
# INSTRUMENT CONFIGURATION
# ============================================================================
ES_TICK_SIZE = 0.25           # Minimum price increment in points
ES_POINT_VALUE = 50.0         # Dollar value of 1 ES point
ES_SYMBOL = "ES"

# ============================================================================
# TRANSACTION COSTS
# ============================================================================
COMMISSION_PER_SIDE = 2.50    # Dollars per contract per side
SLIPPAGE_TICKS = 1            # Ticks of slippage per side
TRANSACTION_COST_PER_TRADE = (COMMISSION_PER_SIDE * 2 + 
                               SLIPPAGE_TICKS * 2 * ES_TICK_SIZE * ES_POINT_VALUE)

# ============================================================================
# STRATEGY PARAMETERS (DEFAULTS)
# ============================================================================
DEFAULT_PARAMS = {
    'dep_threshold': 0.15,
    'tox_threshold': 0.20,
    'momentum_confirm': 0.0002,
    'breakthrough_threshold': 0.10,
    'exit_bars': 4,
    'profit_target_pct': 0.8,
    'stop_loss_pct': 0.6,
    'min_volume_pctile': 30.0,
}

# ============================================================================
# OPTIMIZATION RANGES
# ============================================================================
PARAM_GRID = {
    'dep_threshold': [0.05, 0.10, 0.15, 0.20, 0.30, 0.50],
    'tox_threshold': [0.05, 0.10, 0.20, 0.40, 0.80],
    'momentum_confirm': [0.0, 0.0001, 0.0002, 0.0005, 0.001],
    'breakthrough_threshold': [0.02, 0.05, 0.10, 0.20, 0.30],
    'exit_bars': [2, 3, 4, 5, 6, 8],
    'profit_target_pct': [0.3, 0.5, 0.8, 1.2, 2.0],
    'stop_loss_pct': [0.2, 0.4, 0.6, 1.0, 1.5],
    'min_volume_pctile': [10.0, 20.0, 30.0, 40.0, 50.0],
}

# ============================================================================
# FEATURE PARAMETERS
# ============================================================================
ATR_WINDOW = 20
VOL_WINDOW_SHORT = 20
VOL_WINDOW_LONG = 60
VOLUME_MA_WINDOW = 20
DEPLETION_MA_FAST = 5
DEPLETION_MA_SLOW = 10
LIQUIDITY_QUANTILE_WINDOW = 200
POSITION_SCALE_WINDOW = 100
MOMENTUM_SHORT = 3
MOMENTUM_LONG = 6
EMA_FAST = 12
EMA_SLOW = 26

# ============================================================================
# RISK LIMITS
# ============================================================================
MAX_POSITION_CONTRACTS = 2
MIN_POSITION_CONTRACTS = 1
MAX_HOLDING_BARS = 8
MIN_ATR_FOR_TRADE = 1.0       # Minimum ATR in points
STARTING_EQUITY = 100000.0
MAX_DRAWDOWN_PCT_CIRCUIT = 3.0  # Daily circuit breaker drawdown %

# ============================================================================
# WALK-FORWARD PARAMETERS
# ============================================================================
WFA_IS_SIZE = 15600           # In-sample window size (bars)
WFA_OOS_SIZE = 3900           # Out-of-sample window size (bars)
WFA_STEP_SIZE = 3900          # Step size between folds
WFA_MIN_FOLDS = 10
WFA_MAX_EVALS = 1000          # Max parameter combinations per fold

# ============================================================================
# TARGETS
# ============================================================================
TARGET_WIN_RATE = 0.54
TARGET_TRADES_PER_DAY = 5.0
TARGET_WIDE_THIN_ACCURACY = 0.56
TARGET_SHARPE = 1.0
TARGET_MAX_DRAWDOWN_PCT = 12.0
TARGET_PROFIT_FACTOR = 1.15
```

### 6.2.2 data_pipeline.py

```python
"""
Data loading, cleaning, validation, and splitting.
"""

import pandas as pd
import numpy as np
from typing import Tuple
from strategy_02_queue_depletion.config import *


def load_data(filepath: str = DATA_PATH) -> pd.DataFrame:
    """
    Load ES 5-minute RTH bar data from CSV.
    
    Args:
        filepath: Path to CSV file
    
    Returns:
        Cleaned DataFrame with all required columns
    """
    # Implementation as specified in Section 1.2
    pass


def validate_data(df: pd.DataFrame) -> None:
    """
    Run all data quality checks.
    Raises AssertionError if any check fails.
    
    Implementation as specified in Section 1.4.
    """
    pass


def handle_zero_volume_bars(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle zero-volume bars (circuit breaker halts).
    Forward-fill prices, set volume to minimum.
    """
    pass


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add time-based features: date, time_et, bar_in_day, dow.
    """
    pass


def split_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split data into development and test sets.
    
    Returns:
        (df_dev, df_test): Development and test DataFrames
    """
    pass
```

### 6.2.3 features.py

```python
"""
Complete feature engineering module.
All features defined in Section 2.
"""

import pandas as pd
import numpy as np
from strategy_02_queue_depletion.config import *


def compute_all_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute ALL features in the correct order.
    
    Args:
        df: Cleaned DataFrame with OHLCV columns
    
    Returns:
        DataFrame with all f_* feature columns added
    """
    df = df.copy()
    
    # Group 1: Raw price features
    df = compute_raw_price_features(df)
    
    # Group 2: BVC volume features
    df = compute_bvc_features(df)
    
    # Group 3: Volatility features
    df = compute_volatility_features(df)
    
    # Group 4: Volume features
    df = compute_volume_features(df)
    
    # Group 5: Depletion features
    df = compute_depletion_features(df)
    
    # Group 6: Liquidity regime features
    df = compute_liquidity_regime_features(df)
    
    # Group 7: Toxicity features
    df = compute_toxicity_features(df)
    
    # Group 8: Trend features
    df = compute_trend_features(df)
    
    # Group 9: Composite signal
    df = compute_composite_signal(df)
    
    # Group 10: Position sizing
    df = compute_position_scale(df)
    
    return df


def compute_raw_price_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute Group 1: f_returns, f_log_returns, f_true_range, etc."""
    pass


def compute_bvc_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute Group 2: f_bvc_ratio, f_bvc_buy_vol, etc."""
    pass


def compute_volatility_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute Group 3: f_atr_20, f_vol_realized_20, etc."""
    pass


def compute_volume_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute Group 4: f_volume_sma_20, f_volume_ratio, etc."""
    pass


def compute_depletion_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute Group 5: f_depletion_raw, f_depletion_ma_5, etc."""
    pass


def compute_liquidity_regime_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute Group 6: f_liquidity_score, f_liquidity_regime, etc."""
    pass


def compute_toxicity_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute Group 7: f_toxicity_raw, f_toxicity_ma_5, etc."""
    pass


def compute_trend_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute Group 8: f_ema_12, f_momentum_3, etc."""
    pass


def compute_composite_signal(df: pd.DataFrame) -> pd.DataFrame:
    """Compute Group 9: f_regime_adjusted_signal."""
    pass


def compute_position_scale(df: pd.DataFrame) -> pd.DataFrame:
    """Compute Group 10: f_position_scale."""
    pass


def validate_features(df: pd.DataFrame) -> None:
    """
    Validate all features are correctly computed.
    Raises AssertionError on validation failure.
    """
    pass
```

### 6.2.4 signals.py

```python
"""
Signal generation engine.
Implements the complete state machine described in Section 3.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict
from strategy_02_queue_depletion.config import *


def generate_signals(df: pd.DataFrame, params: Dict) -> pd.DataFrame:
    """
    Generate all signals for the dataset.
    
    Args:
        df: DataFrame with all features computed
        params: Strategy parameters dict
    
    Returns:
        DataFrame with sig_* columns added
    """
    pass


def check_entry_guards(df: pd.DataFrame, idx: int, params: Dict) -> bool:
    """Check universal entry guards."""
    pass


def entry_tight_deep(df: pd.DataFrame, idx: int, params: Dict) -> int:
    """Generate entry signal in Tight-Deep regime."""
    pass


def entry_wide_thin(df: pd.DataFrame, idx: int, params: Dict) -> int:
    """Generate entry signal in Wide-Thin regime."""
    pass


def entry_disrupted(df: pd.DataFrame, idx: int, params: Dict) -> int:
    """No entry in Disrupted regime."""
    pass


def generate_entry_signal(df: pd.DataFrame, idx: int, params: Dict) -> Tuple[int, float, int]:
    """
    Generate entry signal at bar index idx.
    
    Returns:
        (direction, strength, regime)
    """
    pass


def check_exit(df: pd.DataFrame, entry_idx: int, current_idx: int,
               direction: int, entry_price: float, entry_regime: int,
               params: Dict) -> Tuple[bool, str]:
    """
    Check all exit conditions.
    
    Returns:
        (should_exit, exit_reason)
    """
    pass


def check_profit_target(df: pd.DataFrame, entry_idx: int, current_idx: int,
                        direction: int, entry_price: float, params: Dict) -> bool:
    """Check if profit target hit."""
    pass


def check_stop_loss(df: pd.DataFrame, entry_idx: int, current_idx: int,
                    direction: int, entry_price: float, params: Dict) -> bool:
    """Check if stop loss hit."""
    pass


def check_max_hold(entry_idx: int, current_idx: int, params: Dict) -> bool:
    """Check max holding period."""
    pass


def check_end_of_day(df: pd.DataFrame, current_idx: int) -> bool:
    """Check if end of day forced exit."""
    pass


def check_regime_change(df: pd.DataFrame, entry_regime: int, current_idx: int) -> bool:
    """Check if regime changed to Disrupted."""
    pass


def validate_signals(df: pd.DataFrame) -> Dict:
    """Validate generated signals and return statistics."""
    pass
```

### 6.2.5 backtest.py

```python
"""
Complete backtesting engine.
Implements P&L computation, trade logging, and equity curve generation.
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Dict
from strategy_02_queue_depletion.config import *


@dataclass
class Trade:
    """Represents a single completed trade."""
    entry_idx: int
    exit_idx: int
    entry_time: pd.Timestamp
    exit_time: pd.Timestamp
    direction: int
    entry_price: float
    exit_price: float
    entry_regime: int
    num_contracts: int
    gross_pnl: float
    net_pnl: float
    bars_held: int
    exit_reason: str
    max_adverse_excursion: float
    max_favorable_excursion: float


def run_backtest(df: pd.DataFrame, params: Dict) -> Tuple[pd.DataFrame, List[Trade]]:
    """
    Run complete backtest.
    
    Args:
        df: DataFrame with signals
        params: Strategy parameters
    
    Returns:
        (df_with_pnl, trades_list)
    """
    pass


def compute_position_size(df: pd.DataFrame, idx: int, base_size: int = 1) -> int:
    """Compute position size in contracts."""
    pass


def apply_slippage(price: float, direction: str, side: str) -> float:
    """Apply slippage to price."""
    pass


def compute_exit_pnl(entry_price: float, exit_price: float, 
                     position: int, num_contracts: int) -> float:
    """Compute realized P&L."""
    pass


def compute_trade_statistics(trades: List[Trade], df: pd.DataFrame) -> Dict:
    """Compute comprehensive trade statistics."""
    pass


def compute_equity_metrics(df: pd.DataFrame, trades: List[Trade]) -> Dict:
    """Compute equity curve metrics."""
    pass


def generate_performance_report(df: pd.DataFrame, trades: List[Trade]) -> str:
    """Generate formatted performance report."""
    pass
```

### 6.2.6 validation.py

```python
"""
Validation framework: walk-forward analysis, optimization, statistical tests.
"""

import pandas as pd
import numpy as np
from typing import List, Tuple, Dict
from scipy import stats
from itertools import product
from strategy_02_queue_depletion.config import *
from strategy_02_queue_depletion.features import compute_all_features
from strategy_02_queue_depletion.signals import generate_signals
from strategy_02_queue_depletion.backtest import run_backtest, compute_trade_statistics, compute_equity_metrics


def generate_wfa_windows(dev_size: int = DEV_SET_SIZE) -> List[Tuple[int, int, int, int]]:
    """Generate walk-forward analysis windows."""
    pass


def run_walk_forward_analysis(df_dev: pd.DataFrame, param_grid: dict = PARAM_GRID) -> Dict:
    """Run complete walk-forward analysis."""
    pass


def optimize_parameters(df_is: pd.DataFrame, param_grid: dict, 
                        max_evals: int = WFA_MAX_EVALS) -> Dict:
    """Grid search parameter optimization."""
    pass


def objective_function(stats: Dict, equity: Dict) -> float:
    """Combined optimization objective."""
    pass


def summarize_wfa_results(fold_results: List[Dict]) -> Dict:
    """Summarize WFA results."""
    pass


def check_parameter_stability(fold_results: List[Dict]) -> Dict:
    """Check parameter stability across folds."""
    pass


def test_win_rate_significance(num_wins: int, num_trades: int) -> Dict:
    """Binomial test for win rate significance."""
    pass


def test_sharpe_significance(sharpe: float, num_obs: int) -> Dict:
    """Sharpe ratio significance test."""
    pass


def permutation_test(df: pd.DataFrame, trades: List, n_permutations: int = 1000) -> Dict:
    """Permutation test for strategy significance."""
    pass


def evaluate_on_test_set(df_test: pd.DataFrame, best_params: Dict) -> Dict:
    """FINAL evaluation on test set."""
    pass


def check_targets(stats: Dict, equity: Dict) -> Dict:
    """Check if results meet all targets."""
    pass
```

### 6.2.7 reporting.py

```python
"""
Performance reporting and visualization.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict
from strategy_02_queue_depletion.config import *
from strategy_02_queue_depletion.backtest import Trade


def generate_performance_report(df: pd.DataFrame, trades: List[Trade]) -> str:
    """Generate formatted text performance report."""
    pass


def plot_equity_curve(df: pd.DataFrame, output_path: str = None):
    """Plot equity curve with drawdown."""
    pass


def plot_monthly_returns(df: pd.DataFrame, trades: List[Trade], output_path: str = None):
    """Plot monthly return heatmap."""
    pass


def plot_regime_performance(trades: List[Trade], output_path: str = None):
    """Plot performance by liquidity regime."""
    pass


def plot_trade_distribution(trades: List[Trade], output_path: str = None):
    """Plot P&L distribution of trades."""
    pass


def save_all_reports(df: pd.DataFrame, trades: List[Trade], output_dir: str = OUTPUT_DIR):
    """Generate and save all reports and plots."""
    pass
```

### 6.2.8 main.py

```python
"""
Main execution script for Strategy 2.
Run: python -m strategy_02_queue_depletion.main
"""

import sys
import time
from strategy_02_queue_depletion.config import *
from strategy_02_queue_depletion.data_pipeline import load_data, validate_data, split_data
from strategy_02_queue_depletion.features import compute_all_features, validate_features
from strategy_02_queue_depletion.signals import generate_signals, validate_signals
from strategy_02_queue_depletion.backtest import run_backtest, generate_performance_report
from strategy_02_queue_depletion.validation import (
    run_walk_forward_analysis, evaluate_on_test_set
)
from strategy_02_queue_depletion.reporting import save_all_reports


def main():
    """Main execution pipeline."""
    print("="*70)
    print("STRATEGY 2: Queue-Depletion Momentum with Liquidity Regime Filter")
    print("="*70)
    
    # Step 1: Load and validate data
    print("\n[1/7] Loading data...")
    df = load_data(DATA_PATH)
    validate_data(df)
    print(f"  Loaded {len(df):,} rows")
    
    # Step 2: Split data
    print("\n[2/7] Splitting data...")
    df_dev, df_test = split_data(df)
    print(f"  Development: {len(df_dev):,} rows")
    print(f"  Test: {len(df_test):,} rows")
    
    # Step 3: Walk-forward analysis on development set
    print("\n[3/7] Running walk-forward analysis...")
    wfa_results = run_walk_forward_analysis(df_dev)
    wfa_summary = wfa_results['summary']
    
    print(f"  Mean OOS Win Rate: {wfa_summary['mean_oos_win_rate']*100:.2f}%")
    print(f"  Mean OOS Sharpe: {wfa_summary['mean_oos_sharpe']:.3f}")
    print(f"  Consistency Score: {wfa_summary['consistency_score']*100:.1f}%")
    print(f"  WT Accuracy: {wfa_summary['mean_wide_thin_accuracy']*100:.2f}%")
    
    # Use most common parameters across folds as best params
    # (or parameters that maximize the objective)
    # For simplicity, use DEFAULT_PARAMS if WFA doesn't improve
    best_params = DEFAULT_PARAMS.copy()
    
    # Step 4: Evaluate on test set (FINAL — run once)
    print("\n[4/7] Evaluating on test set...")
    test_results = evaluate_on_test_set(df_test, best_params)
    
    test_stats = test_results['trade_stats']
    test_equity = test_results['equity_metrics']
    
    print(f"  Test Win Rate: {test_stats['win_rate']*100:.2f}%")
    print(f"  Test Trades/Day: {test_stats['trades_per_day']:.2f}")
    print(f"  Test WT Accuracy: {test_stats.get('wide_thin_accuracy', 0)*100:.2f}%")
    print(f"  Test Sharpe: {test_equity['sharpe_ratio']:.3f}")
    print(f"  Test Max DD: {test_equity['max_drawdown_pct']:.2f}%")
    
    # Step 5: Check targets
    print("\n[5/7] Checking targets...")
    target_checks = test_results['passes_targets']
    for target, passed in target_checks.items():
        status = "PASS" if passed else "FAIL"
        print(f"  {target}: {status}")
    
    # Step 6: Generate reports
    print("\n[6/7] Generating reports...")
    df_test_feat = compute_all_features(df_test)
    df_test_sig = generate_signals(df_test_feat, best_params)
    df_test_bt, test_trades = run_backtest(df_test_sig, best_params)
    
    report = generate_performance_report(df_test_bt, test_trades)
    print(report)
    
    save_all_reports(df_test_bt, test_trades)
    
    # Step 7: Statistical tests
    print("\n[7/7] Statistical significance tests...")
    print(f"  Binomial p-value: {test_results['binomial_test']['p_value']:.6f}")
    print(f"  Sharpe p-value: {test_results['sharpe_test']['p_value']:.6f}")
    print(f"  Permutation p-value: {test_results['permutation_test']['p_value']:.6f}")
    
    print("\n" + "="*70)
    print("BACKTEST COMPLETE")
    print("="*70)
    
    return test_results


if __name__ == "__main__":
    main()
```

## 6.3 Variable Naming Conventions

| Prefix | Meaning | Examples |
|--------|---------|----------|
| `df_` | DataFrame | `df_dev`, `df_test_bt` |
| `f_` | Feature column | `f_atr_20`, `f_depletion_raw` |
| `sig_` | Signal column | `sig_direction`, `sig_action` |
| `tmp_` | Temporary/intermediate | `tmp_range_expansion` |
| `param_` | Parameter | `param_grid`, `best_params` |
| `is_` | In-sample | `df_is` |
| `oos_` | Out-of-sample | `oos_stats` |
| `wfa_` | Walk-forward analysis | `wfa_results` |
| `es_` | E-mini S&P specific | `ES_POINT_VALUE` |
| `COL_` | Column name constant | `COL_CLOSE` |

## 6.4 Required Python Libraries

```
pandas >= 1.5.0
numpy >= 1.23.0
scipy >= 1.9.0
matplotlib >= 3.5.0
```

No external trading libraries (backtrader, zipline, etc.) are permitted. All code must be implemented from scratch as specified.

---

# SECTION 7: STEP-BY-STEP BUILD ORDER

## Phase 1: Foundation (Steps 1-5)

### Step 1: Create project structure
```bash
mkdir -p /mnt/agents/output/strategy_02_queue_depletion/tests
touch /mnt/agents/output/strategy_02_queue_depletion/__init__.py
touch /mnt/agents/output/strategy_02_queue_depletion/tests/__init__.py
```

### Step 2: Implement config.py
- Write ALL constants from Section 6.2.1
- Include DEFAULT_PARAMS and PARAM_GRID exactly as specified
- Verify all numeric values match this specification

### Step 3: Implement data_pipeline.py
- Implement `load_data()` following Section 1.2 exactly
- Implement `validate_data()` with ALL 10 checks from Section 1.4
- Implement `handle_zero_volume_bars()` for the 7 zero-volume rows
- Implement `add_time_features()` for bar_in_day computation
- Implement `split_data()` with exact split at index 85,600

### Step 4: Test data pipeline
```python
# Run these tests BEFORE proceeding:
df = load_data()
validate_data(df)
assert len(df) == 122295
assert df['ts_event'].is_monotonic_increasing
df_dev, df_test = split_data(df)
assert len(df_dev) == 85600
assert len(df_test) == 36695
print("Data pipeline: PASS")
```

### Step 5: Implement features.py — Group 1 (Raw Price Features)
- Implement `compute_raw_price_features()`:
  - f_returns
  - f_log_returns
  - f_true_range
  - f_bar_range
  - f_body_size
  - f_body_direction
  - f_upper_shadow
  - f_lower_shadow
- Run unit tests: verify ranges, no NaN except expected first values

## Phase 2: Feature Engineering (Steps 6-15)

### Step 6: Implement features.py — Group 2 (BVC Volume Features)
- f_bvc_ratio (handle high==low edge case)
- f_bvc_buy_vol, f_bvc_sell_vol
- f_bvc_imbalance, f_bvc_sign
- Test: verify f_bvc_ratio in [0,1], f_bvc_imbalance in [-1,1]

### Step 7: Implement features.py — Group 3 (Volatility Features)
- f_atr_20 (simple rolling mean, NOT Wilder's)
- f_atr_20_pct
- f_vol_realized_20 (annualized, min_periods=5)
- f_vol_realized_60 (min_periods=20)
- f_vol_ratio
- Test: verify ATR >= 0, vol_ratio > 0

### Step 8: Implement features.py — Group 4 (Volume Features)
- f_volume_sma_20
- f_volume_ratio
- f_volume_zscore_20
- f_relative_volume
- Test: verify ratio >= 0, zscore finite

### Step 9: Implement features.py — Group 5 (Depletion Features)
- f_depletion_raw (SIGNED — critical!)
- f_depletion_abs
- f_depletion_ma_5, f_depletion_ma_10
- f_depletion_diff
- Test: verify sign changes, MA smooths appropriately

### Step 10: Implement features.py — Group 6 (Liquidity Regime)
- f_liquidity_score
- f_liquidity_q33, f_liquidity_q66
- f_liquidity_regime (0, 1, 2)
- Binary indicators: f_regime_tight_deep, f_regime_wide_thin, f_regime_disrupted
- Test: verify regime distribution ~33/33/33%

### Step 11: Implement features.py — Group 7 (Toxicity)
- f_toxicity_raw (signed quadratic / vol)
- f_toxicity_ma_5
- f_toxicity_zscore
- Test: verify capped at +/- 100

### Step 12: Implement features.py — Group 8 (Trend)
- f_ema_12, f_ema_26, f_ema_diff
- f_price_vs_ema20
- f_momentum_3, f_momentum_6
- Test: verify EMA diff crosses zero appropriately

### Step 13: Implement features.py — Group 9 (Composite Signal)
- f_regime_adjusted_signal
- Implement the CASE logic from Section 2.9 exactly
- Test: verify signal is 0 in Disrupted regime

### Step 14: Implement features.py — Group 10 (Position Sizing)
- f_position_scale
- Test: verify range [0.1, 2.0]

### Step 15: Implement validate_features()
- Run ALL feature validation checks from Section 2.12
- Verify no infinite values
- Verify regime distribution balanced
- Print feature count (should be 30+)

## Phase 3: Signal Generation (Steps 16-22)

### Step 16: Implement signals.py — Entry Guards
- `check_entry_guards()` with ALL 8 guards from Section 3.3.1
- Each guard must return False independently
- Log which guard rejects entries for debugging

### Step 17: Implement signals.py — Tight-Deep Entry
- `entry_tight_deep()` with continuation logic
- Require positive depletion + positive momentum + EMA alignment for long
- Require negative depletion + negative momentum + EMA alignment for short

### Step 18: Implement signals.py — Wide-Thin Entry
- `entry_wide_thin()` with breakthrough logic
- Require depletion_diff > threshold + range expansion + volume surge

### Step 19: Implement signals.py — Disrupted Entry
- `entry_disrupted()` — always returns 0

### Step 20: Implement signals.py — Master Entry Function
- `generate_entry_signal()` routes to regime-specific logic
- Computes signal strength as weighted average of dep/tox components

### Step 21: Implement signals.py — Exit Logic
- `check_profit_target()` — ATR-based
- `check_stop_loss()` — uses intraday low/high for realism
- `check_max_hold()` — bar count
- `check_end_of_day()` — bar 76+
- `check_regime_change()` — Disrupted exit
- `check_exit()` — priority ordering

### Step 22: Implement generate_signals() loop
- Bar-by-bar state machine
- Track position state across bars
- Populate sig_direction, sig_strength, sig_regime, sig_action
- Run validate_signals() and verify >3 trades/day, 0 disrupted entries

## Phase 4: Backtesting Engine (Steps 23-28)

### Step 23: Implement backtest.py — Data Structures
- Define Trade dataclass with ALL fields from Section 4.4

### Step 24: Implement backtest.py — Position Sizing
- `compute_position_size()`
- `compute_dollar_risk()`

### Step 25: Implement backtest.py — P&L Functions
- `apply_slippage()` with correct tick adjustment per direction
- `compute_exit_pnl()` with transaction cost deduction

### Step 26: Implement run_backtest()
- Complete bar-by-bar loop from Section 4.4
- Track in_position state
- Record ALL trades with full metadata
- Compute equity curve with $100,000 starting capital

### Step 27: Implement statistics functions
- `compute_trade_statistics()` — ALL metrics from Section 4.5
- `compute_equity_metrics()` — Sharpe, drawdown, etc. from Section 4.6
- `generate_performance_report()` — formatted output from Section 4.7

### Step 28: Test backtest on single fold
- Run backtest on first WFA fold
- Verify trades are generated
- Verify P&L sums correctly
- Verify equity curve monotonic on realized P&L

## Phase 5: Validation (Steps 29-33)

### Step 29: Implement validation.py — WFA Windows
- `generate_wfa_windows()`
- Verify window count >= 10

### Step 30: Implement validation.py — Parameter Optimization
- `objective_function()` with ALL components from Section 5.2.2
- `optimize_parameters()` with grid search and max_evals limit

### Step 31: Implement validation.py — WFA Loop
- `run_walk_forward_analysis()`
- Optimize per fold, evaluate OOS
- Collect all fold results

### Step 32: Implement validation.py — Summary & Stability
- `summarize_wfa_results()`
- `check_parameter_stability()`
- Report consistency score

### Step 33: Implement statistical tests
- `test_win_rate_significance()` — binomial test
- `test_sharpe_significance()` — t-test
- `permutation_test()` — randomization test
- `evaluate_on_test_set()` — FINAL single evaluation
- `check_targets()` — ALL targets from Section 5.3

## Phase 6: Reporting (Steps 34-36)

### Step 34: Implement reporting.py
- `generate_performance_report()` — text report
- `plot_equity_curve()` — equity + drawdown chart
- `plot_regime_performance()` — regime accuracy chart
- `plot_trade_distribution()` — P&L histogram

### Step 35: Implement main.py
- Complete pipeline from Section 6.2.8
- Sequential execution with progress logging

### Step 36: Final Integration Test
```python
# Run complete pipeline on development set
# Verify ALL metrics are computed
# Verify output files are generated
# Verify runtime < 30 minutes for full WFA
```

## Build Order Summary Table

| Phase | Steps | Description | Deliverable |
|-------|-------|-------------|-------------|
| 1 | 1-5 | Foundation | config.py, data_pipeline.py |
| 2 | 6-15 | Feature Engineering | features.py with 30+ features |
| 3 | 16-22 | Signal Generation | signals.py with complete engine |
| 4 | 23-28 | Backtesting | backtest.py with P&L, equity curve |
| 5 | 29-33 | Validation | validation.py with WFA, stats tests |
| 6 | 34-36 | Reporting & Integration | reporting.py, main.py, tests |

---

# SECTION 8: CONSTRAINTS & GUARDRAILS

## 8.1 Forbidden Techniques (Will Cause Immediate Rejection)

The following techniques are STRICTLY PROHIBITED. Their use will be detected and will result in immediate strategy rejection:

| # | Forbidden Technique | Why Forbidden | Detection Method |
|---|-------------------|---------------|-----------------|
| 1 | **Lookahead Bias** | Using future data to make current decisions | Verify no feature uses data from index > current bar |
| 2 | **Future Data in Signals** | Using future prices to generate entry/exit signals | Audit signal generation for any forward references |
| 3 | **End-of-Bar Assumption** | Assuming you know the close before bar completes | All entry signals use prior bar's close or open of current bar |
| 4 | **Repainting** | Changing past signals when new data arrives | Once a signal is generated at bar t, it must never change |
| 5 | **Peek-Ahead in Features** | Features that reference future bars (e.g., centered moving averages) | All rolling windows must end at current bar, not center on it |
| 6 | **Data Snooping on Test Set** | Any parameter tuning, model selection, or decision-making using test set data | Verify test set is used exactly once for final evaluation |
| 7 | **Overnight Position Holding** | Holding positions through market close | Verify all positions closed by bar 76 |
| 8 | **Adaptive Parameters** | Parameters that change based on test set performance | Parameters must be fixed after development phase |
| 9 | **Survivorship Bias** | Only including data for "surviving" instruments | Single instrument (ES), no survivorship issue |
| 10 | **Transaction Cost Omission** | Reporting gross P&L without costs | Verify costs deducted in all P&L calculations |

## 8.2 Anti-Lookahead Verification

Implement and run the following verification function:

```python
def verify_no_lookahead(df: pd.DataFrame) -> bool:
    """
    Verify that no feature or signal uses future data.
    
    Strategy: For each feature column, verify that the value at index i
    depends only on data at indices <= i.
    
    Implementation: This is verified by construction — all features use
    .shift(), .rolling(), .ewm(), or .diff() with non-negative lag.
    """
    # List all feature columns
    feature_cols = [c for c in df.columns if c.startswith('f_')]
    
    # Check that no feature uses .shift(-n) for n > 0
    # (This is checked in code review, not runtime)
    
    # Runtime check: Ensure no NaN propagation that would indicate
    # forward-looking operations
    for col in feature_cols:
        if col in ['f_log_returns', 'f_returns', 'f_momentum_3', 'f_momentum_6']:
            # These legitimately have NaN at the start
            continue
        # After the warm-up period, there should be no NaN
        nan_after_100 = df[col].iloc[100:].isna().sum()
        assert nan_after_100 == 0, f"Feature {col} has {nan_after_100} NaN after bar 100"
    
    return True
```

## 8.3 Maximum Parameter Count Enforcement

```python
def verify_parameter_count(params: dict) -> bool:
    """
    Verify parameter count is within the 10-parameter limit.
    """
    MAX_PARAMS = 10
    num_params = len(params)
    assert num_params <= MAX_PARAMS, (
        f"Strategy has {num_params} optimized parameters, "
        f"maximum allowed is {MAX_PARAMS}"
    )
    return True
```

Strategy 2 has exactly 8 optimized parameters (within limit).

## 8.4 Minimum Trade Count Enforcement

```python
def verify_minimum_trades(trades: list, min_trades: int = 1000) -> bool:
    """
    Verify strategy generates sufficient trades for statistical validity.
    Need at least 1000 trades OR 100 trades per optimized parameter.
    """
    min_by_param = 8 * 100  # 8 parameters * 100 trades/param
    actual_minimum = max(min_trades, min_by_param)
    assert len(trades) >= actual_minimum, (
        f"Only {len(trades)} trades generated, "
        f"minimum required is {actual_minimum}"
    )
    return True
```

## 8.5 Regime Distribution Sanity Check

```python
def verify_regime_distribution(df: pd.DataFrame) -> bool:
    """
    Verify regime classification produces reasonable distribution.
    Each regime should have at least 10% of bars.
    """
    regime_pcts = df['f_liquidity_regime'].value_counts(normalize=True)
    for regime in [0, 1, 2]:
        pct = regime_pcts.get(regime, 0)
        assert 0.10 <= pct <= 0.60, (
            f"Regime {regime} has {pct:.1%} of bars, "
            f"expected [10%, 60%]"
        )
    return True
```

## 8.6 Drawdown Circuit Breaker

```python
def check_drawdown_circuit_breaker(daily_pnl: pd.Series, max_dd_pct: float = 3.0) -> bool:
    """
    Intraday drawdown circuit breaker.
    If daily drawdown exceeds threshold, stop trading for the day.
    This is informational only — the strategy does not implement
    dynamic position reduction based on drawdown.
    """
    cumulative = daily_pnl.cumsum()
    peak = cumulative.cummax()
    dd = (cumulative - peak) / peak.abs() * 100
    return dd.min() >= -max_dd_pct
```

## 8.7 Numerical Stability Guardrails

| Check | Action | Threshold |
|-------|--------|-----------|
| Division by zero | Replace denominator with small epsilon | epsilon = 1e-10 |
| Infinite values | Replace with finite bounds | clip to [-1e6, 1e6] |
| Extreme outliers in features | Winsorize at 1st and 99th percentile | Per feature |
| NaN in critical features | Forward fill or set to default | Within 5 bars |
| ATR = 0 | Set to minimum tradable ATR | 1.0 point |
| Volatility = 0 | Set to small positive value | 0.001 |

## 8.8 Reproducibility Requirements

1. **Random seed**: Set `np.random.seed(42)` at the start of any random process (permutation test)
2. **Deterministic output**: Running the same code on the same data must produce identical results
3. **No stochastic elements in signal generation**: Signal generation must be purely deterministic
4. **Version pinning**: All library versions must be specified in requirements.txt

## 8.9 Failure Handling

### When Data is Insufficient
```python
def handle_insufficient_data(df: pd.DataFrame, min_bars: int = 100) -> pd.DataFrame:
    """
    If dataset has fewer bars than minimum, raise error.
    If a fold has insufficient data, skip that fold with warning.
    """
    if len(df) < min_bars:
        raise ValueError(f"Dataset has {len(df)} bars, minimum {min_bars} required")
    return df
```

### When No Trades Generated
```python
def handle_no_trades(fold_num: int, params: dict) -> dict:
    """
    If a fold generates no trades, return zero stats and continue.
    Log warning for debugging.
    """
    print(f"WARNING: Fold {fold_num} generated 0 trades with params {params}")
    return {
        'total_trades': 0,
        'win_rate': 0,
        'trades_per_day': 0,
        'total_net_pnl': 0,
        'sharpe_ratio': 0,
    }
```

### When All Parameters Fail
```python
def handle_all_params_fail(fold_num: int) -> dict:
    """
    If no parameter combination generates trades in a fold,
    use default parameters and continue.
    """
    print(f"WARNING: All params failed in fold {fold_num}, using defaults")
    return DEFAULT_PARAMS.copy()
```

## 8.10 Code Quality Constraints

- **Maximum function length**: 50 lines (excluding docstrings)
- **Maximum cyclomatic complexity**: 10 per function
- **Type hints**: Required on all function signatures
- **Docstrings**: Required on all public functions
- **No global mutable state**: All state passed through function arguments
- **Pure functions preferred**: Signal generation should be a pure function of (data, params)

---

# SECTION 9: EXPECTED OUTPUTS & ACCEPTANCE CRITERIA

## 9.1 Output Files

The strategy must produce the following output files in `/mnt/agents/output/`:

| # | Filename | Description | Format |
|---|----------|-------------|--------|
| 1 | `strategy_02_performance_report.txt` | Complete performance report | Plain text |
| 2 | `strategy_02_equity_curve.png` | Equity curve with drawdown | PNG, 1200x800 |
| 3 | `strategy_02_regime_performance.png` | Performance by regime | PNG, 800x600 |
| 4 | `strategy_02_trade_distribution.png` | P&L distribution histogram | PNG, 800x600 |
| 5 | `strategy_02_wfa_results.csv` | Per-fold WFA results | CSV |
| 6 | `strategy_02_test_trades.csv` | Complete trade log for test set | CSV |
| 7 | `strategy_02_test_signals.csv` | Signal history for test set | CSV |
| 8 | `strategy_02_summary.json` | Key metrics in JSON format | JSON |

## 9.2 Performance Report Contents

The text report must include ALL of the following sections:

1. **Strategy Header**: Name, description, data range
2. **Parameter Configuration**: All 8 parameter values used
3. **Trade Statistics**: Total trades, long/short split, win rate, profit factor, payoff ratio
4. **P&L Summary**: Total net/gross P&L, avg/median P&L per trade
5. **Win/Loss Breakdown**: Counts, averages, largest win/loss
6. **Regime Performance**: Accuracy and trade count per regime
7. **Trade Execution**: Avg bars held, trades per day, MAE/MFE
8. **Equity Metrics**: Final equity, total return, max drawdown, Sharpe, Sortino, Calmar
9. **Exit Reason Distribution**: Count per exit type
10. **Statistical Tests**: Binomial p-value, Sharpe p-value, permutation p-value
11. **Target Achievement**: PASS/FAIL for each target metric
12. **Walk-Forward Summary**: Mean OOS metrics, consistency score

## 9.3 Acceptance Criteria

### Hard Requirements (ALL Must Pass)

| # | Criterion | Minimum Threshold | Measurement |
|---|-----------|-------------------|-------------|
| 1 | Overall win rate | >= 52.5% | Test set trades |
| 2 | Trades per day | >= 4.5 | Test set / trading days |
| 3 | Wide-Thin accuracy | >= 54% | Test set WT regime trades |
| 4 | Disrupted trades | = 0 | No entries in regime 2 |
| 5 | Sharpe ratio | >= 0.7 | Annualized on test set |
| 6 | Max drawdown | < 15% | Test set equity curve |
| 7 | Profit factor | >= 1.08 | Test set |
| 8 | Binomial test p-value | < 0.05 | Test set win rate |
| 9 | Walk-forward folds | >= 10 | Complete WFA on dev set |
| 10 | WFA consistency | >= 30% | % folds meeting all targets |

### Target Requirements (Strive to Meet All)

| # | Criterion | Target | Stretch |
|---|-----------|--------|---------|
| 1 | Overall win rate | > 54% | > 56% |
| 2 | Trades per day | > 5 | > 7 |
| 3 | Wide-Thin accuracy | > 56% | > 58% |
| 4 | Sharpe ratio | > 1.0 | > 1.5 |
| 5 | Max drawdown | < 12% | < 8% |
| 6 | Profit factor | > 1.15 | > 1.25 |
| 7 | Sortino ratio | > 1.0 | > 1.5 |
| 8 | WFA consistency | > 40% | > 60% |

### Code Quality Requirements

| # | Criterion | Requirement |
|---|-----------|-------------|
| 1 | All functions implemented | No placeholder/stub functions |
| 2 | No lookahead bias | Verified by code review + runtime checks |
| 3 | Transaction costs included | $30/round turn in all P&L |
| 4 | Slippage modeled | 1 tick per side |
| 5 | No overnight positions | All positions closed by bar 76 |
| 6 | Feature validation passes | All 30+ features validated |
| 7 | Deterministic output | Same input produces same output |
| 8 | Error handling | Graceful handling of edge cases |

## 9.4 JSON Summary Format

```json
{
  "strategy": "Queue-Depletion Momentum with Liquidity Regime Filter",
  "strategy_code": "STRAT-02",
  "instrument": "ES",
  "bar_frequency": "5min",
  "data_range": {
    "start": "2020-01-02",
    "end": "2026-03-06",
    "total_bars": 122295
  },
  "train_test_split": {
    "dev_bars": 85600,
    "test_bars": 36695
  },
  "parameters": {
    "dep_threshold": 0.15,
    "tox_threshold": 0.20,
    "momentum_confirm": 0.0002,
    "breakthrough_threshold": 0.10,
    "exit_bars": 4,
    "profit_target_pct": 0.8,
    "stop_loss_pct": 0.6,
    "min_volume_pctile": 30.0
  },
  "test_set_results": {
    "total_trades": 0,
    "win_rate_pct": 0.0,
    "trades_per_day": 0.0,
    "wide_thin_accuracy_pct": 0.0,
    "tight_deep_accuracy_pct": 0.0,
    "sharpe_ratio": 0.0,
    "sortino_ratio": 0.0,
    "max_drawdown_pct": 0.0,
    "profit_factor": 0.0,
    "total_net_pnl": 0.0,
    "avg_pnl_per_trade": 0.0
  },
  "statistical_tests": {
    "binomial_p_value": 0.0,
    "sharpe_p_value": 0.0,
    "permutation_p_value": 0.0
  },
  "walk_forward": {
    "num_folds": 18,
    "mean_oos_win_rate_pct": 0.0,
    "mean_oos_sharpe": 0.0,
    "consistency_score_pct": 0.0
  },
  "targets_met": {
    "overall_accuracy": false,
    "trades_per_day": false,
    "wide_thin_accuracy": false,
    "sharpe_ratio": false,
    "max_drawdown": false,
    "profit_factor": false,
    "all_pass": false
  },
  "timestamp": "2026-01-01T00:00:00Z"
}
```

## 9.5 Rejection Criteria

The strategy implementation will be REJECTED if ANY of the following are true:

1. **Lookahead bias detected**: Any feature, signal, or backtest element uses future data
2. **Test set contamination**: Any parameter tuning or model selection uses test set data
3. **Missing transaction costs**: P&L calculations omit commissions or slippage
4. **Overnight positions**: Strategy holds positions past market close
5. **Hard requirements not met**: Any of the 10 hard acceptance criteria fail
6. **Code does not run**: Implementation raises unhandled exceptions
7. **Non-deterministic output**: Results vary between runs on identical data
8. **Parameter count exceeded**: More than 10 optimized parameters
9. **No statistical testing**: Binomial, Sharpe, or permutation tests omitted
10. **Incomplete implementation**: Any function from the specification is a stub/placeholder

## 9.6 Grading Rubric

| Component | Weight | Evaluation Criteria |
|-----------|--------|-------------------|
| Feature Engineering | 15% | All 30+ features correctly implemented |
| Signal Generation | 20% | Correct regime logic, no lookahead, proper guards |
| Backtesting | 20% | Accurate P&L, costs included, no overnight positions |
| Validation | 20% | WFA completed, statistical tests passed |
| Code Quality | 10% | Clean, documented, tested, no globals |
| Performance | 15% | Meets targets on test set |

---

# APPENDIX A: Complete Feature List

| # | Feature Name | Group | Formula | Dependencies |
|---|-------------|-------|---------|-------------|
| 1 | f_returns | Raw Price | (close - close.shift(1)) / close.shift(1) | close |
| 2 | f_log_returns | Raw Price | log(close / close.shift(1)) | close |
| 3 | f_true_range | Raw Price | max(high-low, |high-close.shift(1)|, |low-close.shift(1)|) | OHLC |
| 4 | f_bar_range | Raw Price | (high - low) / close | OHLC |
| 5 | f_body_size | Raw Price | |close - open| / close | OHLC |
| 6 | f_body_direction | Raw Price | sign(close - open) | OHLC |
| 7 | f_upper_shadow | Raw Price | (high - max(open,close)) / close | OHLC |
| 8 | f_lower_shadow | Raw Price | (min(open,close) - low) / close | OHLC |
| 9 | f_bvc_ratio | BVC | (close - low) / (high - low), or 0.5 if H==L | OHLC |
| 10 | f_bvc_buy_vol | BVC | f_bvc_ratio * volume | f_bvc_ratio, volume |
| 11 | f_bvc_sell_vol | BVC | (1 - f_bvc_ratio) * volume | f_bvc_ratio, volume |
| 12 | f_bvc_imbalance | BVC | 2 * f_bvc_ratio - 1 | f_bvc_ratio |
| 13 | f_bvc_sign | BVC | sign(f_bvc_imbalance) | f_bvc_imbalance |
| 14 | f_atr_20 | Volatility | mean(f_true_range, 20) | f_true_range |
| 15 | f_atr_20_pct | Volatility | f_atr_20 / close | f_atr_20, close |
| 16 | f_vol_realized_20 | Volatility | sqrt(252*78 * var(f_log_returns, 20)) | f_log_returns |
| 17 | f_vol_realized_60 | Volatility | sqrt(252*78 * var(f_log_returns, 60)) | f_log_returns |
| 18 | f_vol_ratio | Volatility | f_vol_realized_20 / f_vol_realized_60 | vol_realized |
| 19 | f_volume_sma_20 | Volume | mean(volume, 20) | volume |
| 20 | f_volume_ratio | Volume | volume / f_volume_sma_20 | volume, f_volume_sma_20 |
| 21 | f_volume_zscore_20 | Volume | (volume - SMA) / std(volume, 20) | volume |
| 22 | f_relative_volume | Volume | alias for f_volume_ratio | same |
| 23 | f_depletion_raw | Depletion | (2*BVC-1) * (range/ATR%) * vol_indicator | BVC, range, ATR, vol |
| 24 | f_depletion_abs | Depletion | abs(f_depletion_raw) | f_depletion_raw |
| 25 | f_depletion_ma_5 | Depletion | mean(f_depletion_raw, 5) | f_depletion_raw |
| 26 | f_depletion_ma_10 | Depletion | mean(f_depletion_raw, 10) | f_depletion_raw |
| 27 | f_depletion_diff | Depletion | f_depletion_ma_5 - f_depletion_ma_10 | depletion MAs |
| 28 | f_liquidity_score | Regime | f_bar_range * (f_relative_volume)^(-0.5) | range, rel_vol |
| 29 | f_liquidity_q33 | Regime | rolling_quantile(f_liquidity_score, 200, 0.33) | f_liquidity_score |
| 30 | f_liquidity_q66 | Regime | rolling_quantile(f_liquidity_score, 200, 0.66) | f_liquidity_score |
| 31 | f_liquidity_regime | Regime | 0/1/2 based on quantile thresholds | f_liquidity_score, quantiles |
| 32 | f_regime_tight_deep | Regime | (f_liquidity_regime == 0).astype(int) | f_liquidity_regime |
| 33 | f_regime_wide_thin | Regime | (f_liquidity_regime == 1).astype(int) | f_liquidity_regime |
| 34 | f_regime_disrupted | Regime | (f_liquidity_regime == 2).astype(int) | f_liquidity_regime |
| 35 | f_toxicity_raw | Toxicity | f_depletion_raw * |f_depletion_raw| / f_vol_realized_20 | depletion, vol |
| 36 | f_toxicity_ma_5 | Toxicity | mean(f_toxicity_raw, 5) | f_toxicity_raw |
| 37 | f_toxicity_zscore | Toxicity | zscore(f_toxicity_raw, 60) | f_toxicity_raw |
| 38 | f_ema_12 | Trend | ewm_mean(close, span=12) | close |
| 39 | f_ema_26 | Trend | ewm_mean(close, span=26) | close |
| 40 | f_ema_diff | Trend | (f_ema_12 - f_ema_26) / close | EMAs, close |
| 41 | f_price_vs_ema20 | Trend | (close - ewm_mean(close,20)) / close | close |
| 42 | f_momentum_3 | Trend | (close - close.shift(3)) / close.shift(3) | close |
| 43 | f_momentum_6 | Trend | (close - close.shift(6)) / close.shift(6) | close |
| 44 | f_regime_adjusted_signal | Composite | regime-dependent formula | All above |
| 45 | f_position_scale | Sizing | min(2.0, |depletion| / mean(|depletion|,100)) | f_depletion_abs |

# APPENDIX B: Signal Encoding Reference

| sig_action | sig_direction | sig_strength | Meaning |
|-----------|--------------|-------------|---------|
| 'enter_long' | +1 | (0, 1] | Open long position |
| 'enter_short' | -1 | (0, 1] | Open short position |
| 'exit' | 0 | 0 | Close position |
| 'hold' | +/-1 | 0 | Continue holding |
| 'none' | 0 | 0 | No position, no action |

# APPENDIX C: Exit Priority Order

1. **Stop Loss** (highest priority — capital protection)
2. **Profit Target** (second priority — capture gains)
3. **End of Day** (bar 76 — hard constraint)
4. **Max Hold** (N bars — time-based exit)
5. **Regime Change** (lowest priority — defensive)

# APPENDIX D: Liquidity Regime Decision Tree

```
                    Start
                      |
              Compute L_t
                      |
            L_t < Q_33? --------YES--> Tight-Deep (0)
                      |                      |
                      NO              Trade Continuation
                      |                      |
            L_t < Q_66? --------YES--> Wide-Thin (1)
                      |                      |
                      NO              Trade Breakthrough
                      |                      |
                 Disrupted (2) <----NO-----
                      |
                 NO TRADE
```

# APPENDIX E: Glossary

| Term | Definition |
|------|-----------|
| BVC | Buy-Volume Classifier — approximates trade direction from OHLCV |
| ATR | Average True Range — volatility measure |
| RTH | Regular Trading Hours (09:30-16:00 ET) |
| ES | E-mini S&P 500 futures contract |
| WFA | Walk-Forward Analysis — rolling in-sample/out-of-sample validation |
| Tight-Deep | Liquidity regime with tight spreads and deep order book |
| Wide-Thin | Liquidity regime with wide spreads and thin order book |
| Disrupted | Liquidity regime with anomalous conditions |
| Queue Depletion | Reduction of resting orders at a price level |
| Toxicity | Measure of informed trading activity |
| MAE | Maximum Adverse Excursion — worst intra-trade loss |
| MFE | Maximum Favorable Excursion — best intra-trade profit |
| Point | 1.0 ES index point = $50 |
| Tick | 0.25 ES index points = $12.50 |

---

## END OF SPECIFICATION

**Total Specification Version**: 1.0.0
**Strategy**: Queue-Depletion Momentum with Liquidity Regime Filter (STRAT-02)
**Author**: Agentic Coding System
**Date**: 2026

---

*This specification is COMPLETE and SELF-CONTAINED. A coding agent should be able to implement the entire strategy from this document without asking clarifying questions. Every constant, formula, threshold, and procedure is specified.*
