"""
Configuration: all constants and tunable parameters in one place.
Paths adapted to the local environment (data file at /app, outputs at /app/output).
"""

import os

# ============================================================================
# DATA CONFIGURATION
# ============================================================================
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_APP_ROOT = os.path.abspath(os.path.join(_THIS_DIR, ".."))

DATA_PATH = os.environ.get("STRAT02_DATA_PATH", os.path.join(_APP_ROOT, "ES_5min_RTH_6year.csv"))
OUTPUT_DIR = os.environ.get("STRAT02_OUTPUT_DIR", os.path.join(_APP_ROOT, "output"))

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
TEST_SET_SIZE = 36695
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
# $5 commission round-turn + $25 slippage round-turn = $30 / round turn
TRANSACTION_COST_PER_TRADE = (COMMISSION_PER_SIDE * 2 +
                               SLIPPAGE_TICKS * 2 * ES_TICK_SIZE * ES_POINT_VALUE)

STARTING_EQUITY = 100000.0

# ============================================================================
# STRATEGY PARAMETERS (DEFAULTS) — exactly 8 optimized parameters
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
ANNUALIZATION = 252 * 78  # bars per year for annualizing 5-min returns

# ============================================================================
# WALK-FORWARD ANALYSIS
# ============================================================================
WFA_IS_SIZE = 15600
WFA_OOS_SIZE = 3900
WFA_MAX_EVALS = 1000

# ============================================================================
# RANDOM SEED (reproducibility)
# ============================================================================
RANDOM_SEED = 42

# Exit reason codes (internal engine) -> labels
EXIT_REASON_LABELS = {
    0: 'none',
    1: 'stop_loss',
    2: 'profit_target',
    3: 'end_of_day',
    4: 'max_hold',
    5: 'regime_change',
}
