# PRD — STRAT-02: Queue-Depletion Momentum with Liquidity Regime Filter

## Problem statement
Build, from a complete specification (`coding_spec_strategy_02.md`), a self-contained
Python backtesting engine for the "Queue-Depletion Momentum with Liquidity Regime
Filter" strategy on ES 5-minute RTH bars (`ES_5min_RTH_6year.csv`, 122,295 bars,
2020–2026). Standalone Python package only (no web app).

## User choices (gathered)
- Delivery: Standalone Python package only.
- WFA: Run the FULL walk-forward analysis as specified.
- Paths: Adapt hardcoded `/mnt/agents/...` paths to local `/app`.
- Performance: Vectorize math for speed (numerically identical).

## Architecture (delivered)
Package `strategy_02_queue_depletion/`:
- config.py, data_pipeline.py, features.py (45 features, vectorized),
  signals.py, backtest.py (single state-machine core + stats/equity),
  validation.py (17-fold WFA, grid-search optimizer, binomial/Sharpe/permutation
  tests, test-set eval), reporting.py (text report + 3 charts + CSVs), main.py.
- tests/test_strategy.py (11 pytest tests, all pass).
- Data at /app/ES_5min_RTH_6year.csv; outputs to /app/output/.

## What's been implemented (2026-06-20)
- Full Section 1–9 spec: data load + 10 validations, 45 features (validated,
  regime split ~35/31/35%), regime-conditioned signals (0 Disrupted entries),
  backtest with $30/round-turn cost + 1-tick/side slippage, equity/Sharpe/Sortino/
  Calmar/drawdown, 17-fold WFA with per-fold grid-search optimization (~3 min),
  statistical significance tests, full reporting (8 output files), JSON summary.
- Verified end-to-end: `python -m strategy_02_queue_depletion.main` runs in ~171s.
- All 11 unit/integration tests pass. Equity chart renders correctly.

## Deviations from literal spec (documented in README)
1. Transaction cost applied ONCE ($30), spec double-counted it ($60). 
2. Intraday-gap check uses <3600s filter (spec's <86400s wrongly flags overnight gaps).
3. 17 WFA folds (per spec's own window-generator loop), not the prose's "18".
4. scipy.stats.binomtest + manual Wilson CI (spec's binom_test/proportion_confint
   are not available in current SciPy).
5. Vectorized features + shared numpy engine + feature caching in optimizer (faster,
   identical numbers).

## Result (honest)
Engine/validation/reporting fully functional and integrity-clean. With the spec's
DEFAULT_PARAMS the strategy does NOT meet aspirational targets on this data:
test win rate ~35.8%, ~0.22 trades/day, Sharpe ~-1.0, profit factor 0.67;
WFA mean OOS win rate ~52.2%, consistency 0%. This reflects the strategy hypothesis
under-performing on the provided ES history (anti-predictive even with loosened
params), not an implementation defect. All metrics in strategy_02_summary.json.

## Updates (2026-06-20, iteration 2)
- Final test evaluation now uses WFA-SELECTED params (per-parameter modal vote across
  the 17 folds via `select_wfa_best_params`), not DEFAULT_PARAMS. Dev-set only; no
  test-set tuning. Chosen modal params still fail targets (30 trades, 50% WR) — edge
  absent, as expected.
- Added monthly-returns heatmap (`strategy_02_monthly_returns.png`) and
  parameter-stability CSV (`strategy_02_param_stability.csv`, mean/std/cv/mode +
  per-fold values). Now 10 output files. Pipeline still ~170s.

## Updates (2026-06-20, iteration 3)
- WFA final-param selection now **OOS-objective weighted** (softmax over each fold's
  OOS objective; `select_wfa_best_params(method='weighted'|'best_fold'|'modal')`).
- Added `diagnostics.py` (sign-inversion + threshold sweep). FINDING: no profitable
  variant exists — both directions lose on dev & test (WR 35-43%, PF<1, neg test
  Sharpe). The strategy has no edge on this ES data. Writes strategy_02_diagnostics.json.
- Added `invert_signal` flag to the engine (diagnostic only).
- Added complete **TradingView Pine Script v5** `strategy_02.pine` (full port: features,
  regime logic, guards, ATR exits, $30 RT costs). Copied to /app/output/.
- 12 output artifacts; tests still 11/11 pass.

## Backlog / Next action items
- P1: Optionally use WFA-selected (rather than default) params for final test eval.
- P2: Add monthly-returns heatmap + Sortino test; parameter-stability report to CSV.
- P2: Explore signal sign/feature variants (research) if the goal is to hit targets —
  would be a strategy redesign, beyond the literal spec.
