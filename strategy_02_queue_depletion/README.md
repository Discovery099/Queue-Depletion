# STRAT-02 — Queue-Depletion Momentum with Liquidity Regime Filter

A self-contained, from-scratch Python backtesting engine for the **Queue-Depletion
Momentum** strategy on E-mini S&P 500 (ES) 5-minute RTH bars. Implements the full
specification: data pipeline, 45 engineered features, regime-conditioned signal
engine, realistic backtest (costs + slippage), walk-forward analysis, statistical
significance tests, and reporting.

## Layout
```
strategy_02_queue_depletion/
├── config.py          # All constants, DEFAULT_PARAMS, PARAM_GRID
├── data_pipeline.py   # load_data, validate_data (10 checks), split_data
├── features.py        # compute_all_features (45 features), validate_features
├── signals.py         # generate_signals, entry guards/logic, validate_signals
├── backtest.py        # state-machine engine, P&L, equity, statistics
├── validation.py      # WFA, grid-search optimization, stat tests, test-set eval
├── reporting.py       # text report + equity/regime/distribution charts + CSVs
└── main.py            # end-to-end pipeline
```

## Run
```bash
cd /app
python -m strategy_02_queue_depletion.main
```
Outputs are written to `/app/output/`:
`strategy_02_performance_report.txt`, `strategy_02_summary.json`,
`strategy_02_wfa_results.csv`, `strategy_02_test_trades.csv`,
`strategy_02_test_signals.csv`, and three PNG charts.

The data file path and output dir are configurable via env vars
`STRAT02_DATA_PATH` and `STRAT02_OUTPUT_DIR` (defaults: `/app/ES_5min_RTH_6year.csv`,
`/app/output`).

## Tests
```bash
cd /app && python -m pytest strategy_02_queue_depletion/tests -q
```

## Key implementation notes / deviations from the literal spec
These changes keep results correct and the code runnable; numeric semantics are
preserved unless noted.

1. **Paths adapted** to the local environment (`/app/...` instead of `/mnt/agents/...`).
2. **Vectorized features** (NumPy/pandas) instead of per-row `df.apply`; numerically
   identical, ~100x faster.
3. **Single state-machine core** (`backtest._simulate`) drives both `generate_signals`
   and `run_backtest`, guaranteeing the signal log and the backtest are consistent.
   The optimizer reuses this core on pre-extracted arrays (features computed once per
   window, since they are parameter-independent) for tractable full WFA (~3 min).
4. **Transaction cost applied once.** The spec's `compute_exit_pnl` returns a net value
   and `run_backtest` subtracts the cost again (double counting $60 instead of $30).
   We apply the $30/round-turn cost exactly once, matching the stated $30 requirement.
5. **Intraday-gap check** uses a `< 3600s` (within-session) filter. The spec's
   `< 86400s` filter wrongly flags normal overnight/early-close gaps (~17–23h).
6. **WFA folds = 17** (from the spec's own `generate_wfa_windows` loop), not 18 as the
   prose states; still ≥ 10 as required.
7. **Stats**: `scipy.stats.binomtest` (the spec's `binom_test`/`proportion_confint`
   were removed/never in SciPy); the Wilson CI is computed directly.

## Result summary (this dataset)
The engine, validation, and reporting are fully functional and pass all data/feature
integrity checks (45 features, regime split ≈ 35/31/35%, zero Disrupted-regime trades).
With the spec's `DEFAULT_PARAMS`, the strategy **does not meet the aspirational
performance targets** on this data — test win rate ≈ 35.8%, ≈ 0.22 trades/day,
Sharpe ≈ −1.0. Walk-forward OOS win rate averages ≈ 52.2%. This reflects the
strategy hypothesis under-performing on the provided ES history, not an
implementation defect: even loosened parameters remain anti-predictive. All numbers
are written to `strategy_02_summary.json`.
