"""
Data loading, validation, zero-volume handling, time features, and train/test split.
Implements Section 1 of the specification.
"""

from typing import Tuple
import pandas as pd
import numpy as np

from strategy_02_queue_depletion.config import (
    DATA_PATH, DEV_SET_SIZE, EXPECTED_TOTAL_ROWS, TEST_SET_SIZE,
)

EXPECTED_COLS = ['ts_event', 'symbol', 'open', 'high', 'low', 'close', 'volume']


def load_data(filepath: str = DATA_PATH) -> pd.DataFrame:
    """Load ES 5-minute RTH bar data from CSV (Section 1.2)."""
    df = pd.read_csv(filepath)

    assert list(df.columns) == EXPECTED_COLS, \
        f"Expected columns {EXPECTED_COLS}, got {list(df.columns)}"

    df['ts_event'] = pd.to_datetime(df['ts_event'], utc=True)
    df = df.sort_values('ts_event').reset_index(drop=True)

    assert df['ts_event'].is_unique, "Duplicate timestamps found in data"

    # Intraday consecutive bars are 300s apart. Overnight/weekend/holiday gaps are
    # much larger (>1h); early-close days produce sub-24h overnight gaps, so filter
    # to within-session diffs (< 1 hour) before asserting the 5-minute cadence.
    time_diffs = df['ts_event'].diff().dt.total_seconds().dropna()
    intraday_diffs = time_diffs[time_diffs < 3600]
    bad = intraday_diffs[intraday_diffs != 300.0].unique()
    assert (intraday_diffs == 300.0).all(), f"Non-5-minute intraday gaps detected: {bad}"

    df = handle_zero_volume_bars(df)

    price_vol_cols = ['open', 'high', 'low', 'close', 'volume']
    assert df[price_vol_cols].notna().all().all(), "Missing values in price/volume columns"

    assert (df['high'] >= df['low']).all(), "Rows found where high < low"
    assert (df['high'] >= df['open']).all(), "Rows found where high < open"
    assert (df['high'] >= df['close']).all(), "Rows found where high < close"
    assert (df['low'] <= df['open']).all(), "Rows found where low > open"
    assert (df['low'] <= df['close']).all(), "Rows found where low > close"

    df = add_time_features(df)
    return df


def handle_zero_volume_bars(df: pd.DataFrame) -> pd.DataFrame:
    """Forward-fill prices on zero-volume bars; set volume to 1 (Section 1.2 step 10)."""
    zero_vol_mask = df['volume'] == 0
    if zero_vol_mask.any():
        df.loc[zero_vol_mask, ['open', 'high', 'low', 'close']] = \
            df[['open', 'high', 'low', 'close']].ffill()
        df.loc[zero_vol_mask, 'volume'] = 1
    return df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add date, ET time, bar_in_day, and day-of-week columns (Section 1.5)."""
    et = df['ts_event'].dt.tz_convert('America/New_York')
    df['date'] = et.dt.date
    df['time_et'] = et.dt.time
    df['bar_in_day'] = df.groupby('date').cumcount()
    df['dow'] = df['ts_event'].dt.dayofweek
    return df


def validate_data(df: pd.DataFrame) -> None:
    """Run all 10 data-quality checks (Section 1.4)."""
    assert len(df) == EXPECTED_TOTAL_ROWS, f"Expected {EXPECTED_TOTAL_ROWS} rows, got {len(df)}"
    assert df.index[0] == 0, "Index does not start at 0"
    assert list(df.columns[:7]) == EXPECTED_COLS, "Columns do not match schema"
    assert df[['open', 'high', 'low', 'close', 'volume']].isnull().sum().sum() == 0, \
        "Missing values in price columns"
    assert (df['high'] >= df['low']).all(), "high < low detected"
    assert (df['volume'] >= 0).all(), "Negative volume detected"
    assert df['ts_event'].is_unique, "Timestamps not unique"
    assert df['ts_event'].is_monotonic_increasing, "Timestamps not chronological"

    et = df['ts_event'].dt.tz_convert('America/New_York')
    minutes = et.dt.hour * 60 + et.dt.minute
    assert (minutes >= 9 * 60 + 30).all() and (minutes <= 16 * 60).all(), \
        "Timestamps outside RTH 09:30-16:00 ET"
    assert df['ts_event'].dt.dayofweek.isin([0, 1, 2, 3, 4]).all(), "Weekend timestamps detected"

    print(f"  Data validation passed ({len(df):,} rows, {df['date'].nunique():,} trading days).")


def split_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Fixed development/test split at index 85,600 (Section 1.3)."""
    df_dev = df.iloc[:DEV_SET_SIZE].copy()
    df_test = df.iloc[DEV_SET_SIZE:].copy()

    assert len(df_dev) == DEV_SET_SIZE, f"Expected {DEV_SET_SIZE} dev bars, got {len(df_dev)}"
    assert len(df_test) == TEST_SET_SIZE, f"Expected {TEST_SET_SIZE} test bars, got {len(df_test)}"
    assert len(df_dev) + len(df_test) == len(df), "Split does not cover full dataset"
    return df_dev, df_test
