# Frontier report

- Generations completed: 15008
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: see reports/milestones/placebo_latest.md

All figures are research walk-forward out-of-sample results on an island's three home test folds (355 sessions, both instruments pooled, base costs). They are stage 1 screening numbers, the best of many attempts, and none has passed a gate. Win-rate alpha before generation 2,001 used a twin without geometry matching and is overstated for level-based targets.

Genomes evaluated: 14155; with at least 150 out-of-sample trades: 10329.

## Counts by outcome

| Outcome | Generations |
|---|---|
| confirmed | 0 |
| error | 0 |
| stage1_fail | 15008 |
| stage1_pass | 0 |
| void | 0 |

## How many reach each headline level (at least 150 trades)

| Win rate at least | PF at least 1.0 | 1.2 | 1.4 | 1.6 | 1.8 |
|---|---|---|---|---|---|
| 55% | 2291 | 812 | 252 | 62 | 10 |
| 60% | 1844 | 640 | 191 | 43 | 6 |
| 65% | 1224 | 493 | 137 | 27 | 4 |
| 70% | 503 | 282 | 97 | 23 | 4 |
| 75% | 68 | 60 | 19 | 5 | 0 |
| 80% | 1 | 1 | 1 | 1 | 0 |

## Best profit factor at each win-rate level, by trade frequency

| Trades per year per instrument | Win rate 55-65% | 65-72% | 72-80% | 80%+ |
|---|---|---|---|---|
| 50 to 100 | 2.26 (of 346) | 1.81 (of 216) | 2.00 (of 44) | 1.76 (of 1) |
| 100 to 150 | 1.96 (of 370) | 1.63 (of 247) | 1.56 (of 88) | none |
| 150 to 200 | 1.47 (of 273) | 1.48 (of 158) | 1.49 (of 59) | none |
| 200 to 400 | 1.33 (of 646) | 1.30 (of 416) | 1.37 (of 93) | none |
| 400 to more | 1.28 (of 587) | 1.22 (of 292) | 1.21 (of 22) | none |

## Highest geometry-matched win-rate alpha at each frequency level (generation 2,001 onward, profit factor above 1.0)

| Trades per year per instrument | Alpha (points) | Win rate | Profit factor | Trades | Timeframe | Generation | Strategy |
|---|---|---|---|---|---|---|---|
| 50 to 100 | +19.4 | 55.7% | 1.78 | 271 | 5 min | 4133 | tr_late_session_extreme with st_efficiency_trend, f_companion_confirms; r_stop_swing; x_time_stop; market |
| 100 to 150 | +20.6 | 50.6% | 1.72 | 308 | 5 min | 4375 | tr_late_session_extreme with st_efficiency_trend, f_companion_confirms; r_stop_signal_bar; x_target_r; market |
| 150 to 200 | +14.2 | 72.6% | 1.12 | 438 | 15 min | 13153 | tr_roc_thrust with f_not_extended_from_vwap; r_stop_atr; x_target_atr, x_invalidate_macd; market |
| 200 to 400 | +11.5 | 49.6% | 1.15 | 704 | 60 min | 6287 | tr_internal_bar_strength[inv]; r_stop_signal_bar; x_target_r; market |
| 400 to more | +9.1 | 60.7% | 1.09 | 1594 | 5 min | 9106 | tr_engulfing OR tr_companion_leads_break with st_both_vwap_side; r_stop_swing; x_target_location_level, x_partial; limit |

## Leading candidates by composite score (not certified)

| Generation | Island | Timeframe | Score | Win rate | Alpha | Profit factor | Trades | Per year | Complexity | Strategy |
|---|---|---|---|---|---|---|---|---|---|---|
| 5480 | B | 30 min | 0.547 | 71.5% | +15.0 | 1.61 | 340 | 121 | 6 | tr_price_ema_cross; r_stop_percent; x_target_atr; market |
| 5444 | B | 30 min | 0.545 | 71.5% | +14.6 | 1.61 | 340 | 121 | 6 | tr_price_ema_cross; r_stop_percent; x_target_atr; market |
| 6892 | B | 30 min | 0.544 | 71.5% | +14.6 | 1.61 | 340 | 121 | 6 | tr_price_ema_cross; r_stop_percent; x_target_atr; market |
| 6362 | B | 30 min | 0.544 | 71.5% | +14.5 | 1.61 | 340 | 121 | 6 | tr_price_ema_cross; r_stop_percent; x_target_atr; market |
| 14703 | A | 15 min | 0.535 | 73.6% | +9.9 | 1.44 | 330 | 117 | 8 | tr_false_break_prior_day with st_ichimoku_cloud; r_stop_atr; x_target_r; market |
| 14887 | A | 5 min | 0.535 | 73.7% | +9.4 | 1.49 | 457 | 162 | 10 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |
| 13159 | A | 15 min | 0.534 | 74.1% | +9.3 | 1.43 | 359 | 127 | 8 | tr_false_break_prior_day with st_ichimoku_cloud; r_stop_atr; x_target_r; market |
| 7160 | B | 30 min | 0.532 | 71.5% | +14.1 | 1.59 | 340 | 121 | 8 | tr_price_ema_cross; r_stop_percent; x_target_atr, x_partial; market |
| 14407 | A | 15 min | 0.529 | 71.3% | +10.8 | 1.63 | 327 | 116 | 10 | tr_ema_cross with f_signal_bar_not_huge; r_stop_swing; x_target_r; market |
| 12147 | A | 15 min | 0.529 | 74.1% | +8.6 | 1.43 | 359 | 127 | 8 | tr_false_break_prior_day with st_ichimoku_cloud; r_stop_atr; x_target_r; market |
| 8637 | A | 15 min | 0.529 | 74.1% | +8.6 | 1.43 | 359 | 127 | 8 | tr_false_break_prior_day with st_ichimoku_cloud; r_stop_atr; x_target_r; market |
| 14583 | A | 15 min | 0.527 | 71.3% | +10.4 | 1.63 | 327 | 116 | 10 | tr_ema_cross with f_signal_bar_not_huge; r_stop_swing; x_target_r; market |
| 12233 | A | 15 min | 0.526 | 73.9% | +8.4 | 1.41 | 341 | 121 | 8 | tr_false_break_prior_day with st_ichimoku_cloud; r_stop_atr; x_target_r; market |
| 13539 | A | 5 min | 0.524 | 73.7% | +8.0 | 1.44 | 495 | 176 | 10 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |
| 13469 | A | 5 min | 0.524 | 73.6% | +8.8 | 1.44 | 497 | 176 | 10 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |

## Which constraint binds

Among the 15 leading candidates above, gates failed (from each generation's gates.json):

- freq.worst_regime_cell_share: 9 of 15
- freq.session_share: 8 of 15
- sample.trades_per_fold_per_instrument: 5 of 15
- wf.worst_fold_win_rate_gap_pts: 5 of 15
- wf.median_fold_pf: 5 of 15
- freq.max_gap_sessions: 5 of 15
- twin.random_exit_wilson_lower: 5 of 15
