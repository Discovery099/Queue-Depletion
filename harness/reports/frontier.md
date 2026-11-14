# Frontier report

- Generations completed: 50008
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: see reports/milestones/placebo_latest.md

All figures are research walk-forward out-of-sample results on an island's three home test folds (355 sessions, both instruments pooled, base costs). They are stage 1 screening numbers, the best of many attempts, and none has passed a gate. Win-rate alpha before generation 2,001 used a twin without geometry matching and is overstated for level-based targets.

Genomes evaluated: 47636; with at least 150 out-of-sample trades: 37328.

## Counts by outcome

| Outcome | Generations |
|---|---|
| confirmed | 0 |
| error | 19 |
| stage1_fail | 49969 |
| stage1_pass | 20 |
| void | 0 |

## How many reach each headline level (at least 150 trades)

| Win rate at least | PF at least 1.0 | 1.2 | 1.4 | 1.6 | 1.8 |
|---|---|---|---|---|---|
| 55% | 11868 | 4048 | 1290 | 343 | 55 |
| 60% | 10377 | 3553 | 1139 | 304 | 46 |
| 65% | 7454 | 3077 | 994 | 269 | 42 |
| 70% | 3526 | 2070 | 805 | 243 | 40 |
| 75% | 664 | 632 | 368 | 123 | 31 |
| 80% | 17 | 17 | 17 | 16 | 12 |

## Best profit factor at each win-rate level, by trade frequency

| Trades per year per instrument | Win rate 55-65% | 65-72% | 72-80% | 80%+ |
|---|---|---|---|---|
| 50 to 100 | 2.26 (of 1200) | 1.97 (of 894) | 2.52 (of 411) | 2.12 (of 16) |
| 100 to 150 | 1.96 (of 1294) | 1.72 (of 1171) | 1.77 (of 660) | 1.80 (of 2) |
| 150 to 200 | 1.53 (of 1024) | 1.62 (of 948) | 1.77 (of 406) | none |
| 200 to 400 | 1.45 (of 2899) | 1.53 (of 2400) | 1.47 (of 643) | none |
| 400 to more | 1.28 (of 3215) | 1.30 (of 1959) | 1.32 (of 164) | none |

## Highest geometry-matched win-rate alpha at each frequency level (generation 2,001 onward, profit factor above 1.0)

| Trades per year per instrument | Alpha (points) | Win rate | Profit factor | Trades | Timeframe | Generation | Strategy |
|---|---|---|---|---|---|---|---|
| 50 to 100 | +23.4 | 72.8% | 1.43 | 202 | 5 min | 26056 | tr_keltner_reentry with st_both_vwap_side; r_stop_session_extreme; x_target_location_level, x_partial; limit |
| 100 to 150 | +22.3 | 74.7% | 1.52 | 308 | 5 min | 46803 | tr_roc_thrust with st_donchian_mid, f_inside_prior_day_range; r_stop_swing; x_target_atr, x_invalidate_rsi_mid; stop |
| 150 to 200 | +24.8 | 71.6% | 1.62 | 443 | 5 min | 36239 | tr_band_width_expansion with f_inside_prior_day_range; r_stop_swing; x_partial; limit |
| 200 to 400 | +23.2 | 68.2% | 1.48 | 825 | 5 min | 42379 | tr_band_width_expansion; r_stop_swing; x_partial; limit |
| 400 to more | +17.5 | 49.7% | 1.10 | 1411 | 5 min | 33094 | tr_opening_drive OR tr_roc_thrust; r_stop_swing; x_time_stop; stop |

## Leading candidates by composite score (not certified)

| Generation | Island | Timeframe | Score | Win rate | Alpha | Profit factor | Trades | Per year | Complexity | Strategy |
|---|---|---|---|---|---|---|---|---|---|---|
| 47013 | A | 5 min | 0.734 | 75.3% | +21.6 | 1.77 | 393 | 139 | 17 | tr_roc_thrust with st_donchian_mid, f_inside_prior_day_range, f_stop_before_close; r_stop_swing; x_partial; stop |
| 47771 | A | 5 min | 0.712 | 75.2% | +21.9 | 1.73 | 375 | 133 | 17 | tr_roc_thrust with st_donchian_mid, f_inside_prior_day_range, f_stop_before_close; r_stop_swing; x_partial; stop |
| 45871 | A | 5 min | 0.705 | 73.8% | +20.2 | 1.72 | 432 | 153 | 18 | tr_opening_drive OR tr_roc_thrust with st_donchian_mid, f_inside_prior_day_range; r_stop_swing; x_partial; stop |
| 46211 | A | 5 min | 0.689 | 73.1% | +21.4 | 1.69 | 431 | 153 | 18 | tr_opening_drive OR tr_roc_thrust with st_donchian_mid, f_inside_prior_day_range; r_stop_swing; x_partial; stop |
| 43033 | A | 5 min | 0.686 | 74.3% | +20.5 | 1.70 | 413 | 147 | 17 | tr_roc_thrust with st_donchian_mid, f_inside_prior_day_range, f_stop_before_close; r_stop_swing; x_partial; stop |
| 43093 | A | 5 min | 0.686 | 74.3% | +20.7 | 1.69 | 412 | 146 | 17 | tr_roc_thrust with st_donchian_mid, f_inside_prior_day_range, f_stop_before_close; r_stop_swing; x_partial; stop |
| 47649 | A | 5 min | 0.682 | 72.8% | +22.8 | 1.64 | 423 | 150 | 17 | tr_band_break_failure OR tr_roc_thrust with st_donchian_mid, f_inside_prior_day_range, f_companion_confirms; r_stop_swing; x_partial; stop |
| 47915 | A | 5 min | 0.680 | 72.8% | +22.6 | 1.64 | 423 | 150 | 17 | tr_band_break_failure OR tr_roc_thrust with st_donchian_mid, f_inside_prior_day_range, f_companion_confirms; r_stop_swing; x_partial; stop |
| 42505 | A | 5 min | 0.678 | 73.8% | +20.1 | 1.73 | 401 | 142 | 16 | tr_climax_reversal OR tr_roc_thrust with st_donchian_mid, f_inside_prior_day_range, f_companion_confirms; r_stop_swing; x_partial; stop |
| 48299 | A | 5 min | 0.678 | 73.6% | +17.2 | 1.70 | 432 | 153 | 18 | tr_opening_drive OR tr_roc_thrust with st_donchian_mid, f_inside_prior_day_range; r_stop_swing; x_partial; stop |
| 44793 | A | 5 min | 0.676 | 73.0% | +20.9 | 1.64 | 422 | 150 | 17 | tr_band_break_failure OR tr_roc_thrust with st_donchian_mid, f_inside_prior_day_range, f_companion_confirms; r_stop_swing; x_partial; stop |
| 47973 | A | 5 min | 0.673 | 73.3% | +20.0 | 1.67 | 423 | 150 | 17 | tr_band_break_failure OR tr_roc_thrust with st_donchian_mid, f_inside_prior_day_range, f_companion_confirms; r_stop_swing; x_partial; stop |
| 21335 | A | 5 min | 0.671 | 77.2% | +13.4 | 1.70 | 303 | 108 | 10 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |
| 46795 | A | 5 min | 0.671 | 73.3% | +18.1 | 1.67 | 434 | 154 | 18 | tr_opening_drive OR tr_roc_thrust with st_donchian_mid, f_inside_prior_day_range; r_stop_swing; x_partial; stop |
| 21055 | A | 5 min | 0.670 | 77.2% | +13.2 | 1.70 | 303 | 108 | 10 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |

## Which constraint binds

Among the 15 leading candidates above, gates failed (from each generation's gates.json):

- wf.in_sample_expectancy_costs: 15 of 15
- freq.trades_per_year_per_instrument: 15 of 15
- freq.session_share: 15 of 15
- twin.random_exit_wilson_lower: 13 of 15
- sample.trades_per_instrument: 2 of 15
- freq.max_gap_sessions: 2 of 15
