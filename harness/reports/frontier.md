# Frontier report

- Generations completed: 30008
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: see reports/milestones/placebo_latest.md

All figures are research walk-forward out-of-sample results on an island's three home test folds (355 sessions, both instruments pooled, base costs). They are stage 1 screening numbers, the best of many attempts, and none has passed a gate. Win-rate alpha before generation 2,001 used a twin without geometry matching and is overstated for level-based targets.

Genomes evaluated: 28484; with at least 150 out-of-sample trades: 21790.

## Counts by outcome

| Outcome | Generations |
|---|---|
| confirmed | 0 |
| error | 19 |
| stage1_fail | 29985 |
| stage1_pass | 4 |
| void | 0 |

## How many reach each headline level (at least 150 trades)

| Win rate at least | PF at least 1.0 | 1.2 | 1.4 | 1.6 | 1.8 |
|---|---|---|---|---|---|
| 55% | 5696 | 1955 | 626 | 163 | 36 |
| 60% | 4822 | 1640 | 521 | 133 | 29 |
| 65% | 3353 | 1348 | 419 | 107 | 26 |
| 70% | 1433 | 810 | 305 | 94 | 26 |
| 75% | 212 | 196 | 112 | 53 | 19 |
| 80% | 14 | 14 | 14 | 13 | 11 |

## Best profit factor at each win-rate level, by trade frequency

| Trades per year per instrument | Win rate 55-65% | 65-72% | 72-80% | 80%+ |
|---|---|---|---|---|
| 50 to 100 | 2.26 (of 750) | 1.81 (of 547) | 2.06 (of 200) | 2.12 (of 14) |
| 100 to 150 | 1.96 (of 833) | 1.63 (of 659) | 1.74 (of 202) | 1.80 (of 1) |
| 150 to 200 | 1.47 (of 587) | 1.56 (of 444) | 1.52 (of 116) | none |
| 200 to 400 | 1.39 (of 1617) | 1.47 (of 1134) | 1.41 (of 235) | none |
| 400 to more | 1.28 (of 1567) | 1.25 (of 909) | 1.29 (of 78) | none |

## Highest geometry-matched win-rate alpha at each frequency level (generation 2,001 onward, profit factor above 1.0)

| Trades per year per instrument | Alpha (points) | Win rate | Profit factor | Trades | Timeframe | Generation | Strategy |
|---|---|---|---|---|---|---|---|
| 50 to 100 | +23.4 | 72.8% | 1.43 | 202 | 5 min | 26056 | tr_keltner_reentry with st_both_vwap_side; r_stop_session_extreme; x_target_location_level, x_partial; limit |
| 100 to 150 | +20.6 | 50.6% | 1.72 | 308 | 5 min | 4375 | tr_late_session_extreme with st_efficiency_trend, f_companion_confirms; r_stop_signal_bar; x_target_r; market |
| 150 to 200 | +16.9 | 68.9% | 1.54 | 450 | 5 min | 20173 | tr_trail_flip with st_gap_direction; r_stop_swing; x_partial; limit |
| 200 to 400 | +15.5 | 63.5% | 1.08 | 1045 | 5 min | 29791 | tr_mfi_hook[inv] with f_stop_before_close; r_stop_swing; x_partial; limit |
| 400 to more | +12.6 | 47.0% | 1.05 | 1842 | 5 min | 25264 | tr_price_ema_cross; r_stop_swing; x_time_stop; stop |

## Leading candidates by composite score (not certified)

| Generation | Island | Timeframe | Score | Win rate | Alpha | Profit factor | Trades | Per year | Complexity | Strategy |
|---|---|---|---|---|---|---|---|---|---|---|
| 21335 | A | 5 min | 0.671 | 77.2% | +13.4 | 1.70 | 303 | 108 | 10 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |
| 21055 | A | 5 min | 0.670 | 77.2% | +13.2 | 1.70 | 303 | 108 | 10 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |
| 21129 | A | 5 min | 0.665 | 77.2% | +12.6 | 1.70 | 303 | 108 | 10 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |
| 22279 | A | 5 min | 0.665 | 77.2% | +12.5 | 1.70 | 303 | 108 | 10 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |
| 22469 | A | 5 min | 0.656 | 76.8% | +13.1 | 1.66 | 302 | 107 | 10 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |
| 18133 | A | 5 min | 0.636 | 74.7% | +13.5 | 1.72 | 340 | 121 | 12 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; limit |
| 18119 | A | 5 min | 0.632 | 74.7% | +12.9 | 1.72 | 340 | 121 | 12 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; limit |
| 17057 | A | 5 min | 0.631 | 75.6% | +10.7 | 1.67 | 365 | 130 | 10 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |
| 22361 | A | 5 min | 0.630 | 74.8% | +13.6 | 1.73 | 330 | 117 | 12 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; limit |
| 18999 | A | 5 min | 0.629 | 75.2% | +12.9 | 1.68 | 314 | 111 | 12 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; limit |
| 20711 | A | 5 min | 0.628 | 76.8% | +12.2 | 1.61 | 306 | 109 | 10 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |
| 17681 | A | 5 min | 0.628 | 75.6% | +13.6 | 1.74 | 299 | 106 | 12 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; limit |
| 17339 | A | 5 min | 0.627 | 75.5% | +10.4 | 1.67 | 364 | 129 | 10 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |
| 19659 | A | 5 min | 0.627 | 75.2% | +12.6 | 1.68 | 314 | 111 | 12 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; limit |
| 17123 | A | 5 min | 0.627 | 75.1% | +11.5 | 1.66 | 377 | 134 | 10 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |

## Which constraint binds

Among the 15 leading candidates above, gates failed (from each generation's gates.json):

- freq.trades_per_year_per_instrument: 15 of 15
- freq.session_share: 15 of 15
- wf.in_sample_expectancy_costs: 9 of 15
- sample.trades_per_instrument: 7 of 15
- freq.max_gap_sessions: 6 of 15
