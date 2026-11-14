# Frontier report

- Generations completed: 20008
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: see reports/milestones/placebo_latest.md

All figures are research walk-forward out-of-sample results on an island's three home test folds (355 sessions, both instruments pooled, base costs). They are stage 1 screening numbers, the best of many attempts, and none has passed a gate. Win-rate alpha before generation 2,001 used a twin without geometry matching and is overstated for level-based targets.

Genomes evaluated: 18916; with at least 150 out-of-sample trades: 14041.

## Counts by outcome

| Outcome | Generations |
|---|---|
| confirmed | 0 |
| error | 0 |
| stage1_fail | 20007 |
| stage1_pass | 1 |
| void | 0 |

## How many reach each headline level (at least 150 trades)

| Win rate at least | PF at least 1.0 | 1.2 | 1.4 | 1.6 | 1.8 |
|---|---|---|---|---|---|
| 55% | 3322 | 1243 | 416 | 110 | 28 |
| 60% | 2737 | 1018 | 339 | 86 | 23 |
| 65% | 1873 | 815 | 266 | 68 | 21 |
| 70% | 833 | 508 | 204 | 60 | 21 |
| 75% | 129 | 119 | 65 | 28 | 14 |
| 80% | 10 | 10 | 10 | 10 | 9 |

## Best profit factor at each win-rate level, by trade frequency

| Trades per year per instrument | Win rate 55-65% | 65-72% | 72-80% | 80%+ |
|---|---|---|---|---|
| 50 to 100 | 2.26 (of 486) | 1.81 (of 329) | 2.06 (of 103) | 2.12 (of 9) |
| 100 to 150 | 1.96 (of 528) | 1.63 (of 384) | 1.74 (of 139) | 1.80 (of 1) |
| 150 to 200 | 1.47 (of 368) | 1.48 (of 235) | 1.52 (of 85) | none |
| 200 to 400 | 1.34 (of 947) | 1.47 (of 624) | 1.37 (of 138) | none |
| 400 to more | 1.28 (of 847) | 1.22 (of 440) | 1.21 (of 29) | none |

## Highest geometry-matched win-rate alpha at each frequency level (generation 2,001 onward, profit factor above 1.0)

| Trades per year per instrument | Alpha (points) | Win rate | Profit factor | Trades | Timeframe | Generation | Strategy |
|---|---|---|---|---|---|---|---|
| 50 to 100 | +20.4 | 72.6% | 1.43 | 201 | 5 min | 15980 | tr_keltner_reentry with st_both_vwap_side; r_stop_swing; x_target_location_level, x_partial; limit |
| 100 to 150 | +20.6 | 50.6% | 1.72 | 308 | 5 min | 4375 | tr_late_session_extreme with st_efficiency_trend, f_companion_confirms; r_stop_signal_bar; x_target_r; market |
| 150 to 200 | +14.5 | 57.2% | 1.45 | 486 | 15 min | 18809 | tr_bollinger_break with f_adx_low; r_stop_signal_bar; x_target_r; market |
| 200 to 400 | +13.6 | 72.1% | 1.03 | 1119 | 5 min | 15903 | tr_opening_drive OR tr_roc_thrust; r_stop_atr; x_target_atr, x_invalidate_macd; market |
| 400 to more | +10.5 | 68.8% | 1.12 | 1467 | 15 min | 15957 | tr_cci_breakout OR tr_roc_thrust; r_stop_atr; x_target_atr, x_invalidate_rsi_mid; market |

## Leading candidates by composite score (not certified)

| Generation | Island | Timeframe | Score | Win rate | Alpha | Profit factor | Trades | Per year | Complexity | Strategy |
|---|---|---|---|---|---|---|---|---|---|---|
| 18133 | A | 5 min | 0.636 | 74.7% | +13.5 | 1.72 | 340 | 121 | 12 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; limit |
| 18119 | A | 5 min | 0.632 | 74.7% | +12.9 | 1.72 | 340 | 121 | 12 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; limit |
| 17057 | A | 5 min | 0.631 | 75.6% | +10.7 | 1.67 | 365 | 130 | 10 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |
| 18999 | A | 5 min | 0.629 | 75.2% | +12.9 | 1.68 | 314 | 111 | 12 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; limit |
| 17681 | A | 5 min | 0.628 | 75.6% | +13.6 | 1.74 | 299 | 106 | 12 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; limit |
| 17339 | A | 5 min | 0.627 | 75.5% | +10.4 | 1.67 | 364 | 129 | 10 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |
| 19659 | A | 5 min | 0.627 | 75.2% | +12.6 | 1.68 | 314 | 111 | 12 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; limit |
| 17123 | A | 5 min | 0.627 | 75.1% | +11.5 | 1.66 | 377 | 134 | 10 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |
| 18529 | A | 5 min | 0.626 | 75.6% | +13.3 | 1.74 | 299 | 106 | 12 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; limit |
| 19109 | A | 5 min | 0.623 | 74.6% | +12.3 | 1.71 | 338 | 120 | 12 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; limit |
| 17939 | A | 5 min | 0.619 | 75.5% | +12.5 | 1.73 | 298 | 106 | 12 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; limit |
| 18231 | A | 5 min | 0.618 | 77.3% | +14.3 | 1.73 | 277 | 98 | 16 | tr_trail_flip with st_gap_direction, f_stop_before_close; r_stop_swing; x_target_atr; limit |
| 19413 | A | 15 min | 0.605 | 82.0% | +12.2 | 1.97 | 267 | 95 | 8 | tr_false_break_prior_day with st_ichimoku_cloud; r_stop_atr; x_target_r; market |
| 15525 | A | 15 min | 0.597 | 81.3% | +12.0 | 1.92 | 273 | 97 | 8 | tr_false_break_prior_day with st_ichimoku_cloud; r_stop_atr; x_target_r; market |
| 15905 | A | 15 min | 0.595 | 81.3% | +11.7 | 1.92 | 273 | 97 | 8 | tr_false_break_prior_day with st_ichimoku_cloud; r_stop_atr; x_target_r; market |

## Which constraint binds

Among the 15 leading candidates above, gates failed (from each generation's gates.json):

- freq.trades_per_year_per_instrument: 15 of 15
- freq.session_share: 15 of 15
- sample.trades_per_instrument: 7 of 15
- freq.max_gap_sessions: 6 of 15
- wf.in_sample_expectancy_costs: 3 of 15
- wr.skew: 3 of 15
- freq.worst_regime_cell_share: 3 of 15
- twin.random_exit_wilson_lower: 3 of 15
- sample.trades_per_complexity_point: 1 of 15
