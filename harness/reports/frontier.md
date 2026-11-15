# Frontier report

- Generations completed: 100000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: see reports/milestones/placebo_latest.md

All figures are research walk-forward out-of-sample results on an island's three home test folds (355 sessions, both instruments pooled, base costs). They are stage 1 screening numbers, the best of many attempts, and none has passed a gate. Win-rate alpha before generation 2,001 used a twin without geometry matching and is overstated for level-based targets.

Genomes evaluated: 95626; with at least 150 out-of-sample trades: 76875.

## Counts by outcome

| Outcome | Generations |
|---|---|
| confirmed | 0 |
| error | 19 |
| stage1_fail | 99915 |
| stage1_pass | 66 |
| void | 0 |

## How many reach each headline level (at least 150 trades)

| Win rate at least | PF at least 1.0 | 1.2 | 1.4 | 1.6 | 1.8 |
|---|---|---|---|---|---|
| 55% | 32925 | 13464 | 5178 | 1778 | 264 |
| 60% | 29804 | 12491 | 4933 | 1713 | 250 |
| 65% | 22850 | 11437 | 4684 | 1665 | 244 |
| 70% | 11210 | 7421 | 4018 | 1602 | 239 |
| 75% | 2773 | 2714 | 1966 | 859 | 179 |
| 80% | 173 | 173 | 173 | 167 | 89 |

## Best profit factor at each win-rate level, by trade frequency

| Trades per year per instrument | Win rate 55-65% | 65-72% | 72-80% | 80%+ |
|---|---|---|---|---|
| 50 to 100 | 2.26 (of 2294) | 2.23 (of 1761) | 2.52 (of 1102) | 2.60 (of 62) |
| 100 to 150 | 1.97 (of 2484) | 1.80 (of 2795) | 2.07 (of 2797) | 2.12 (of 92) |
| 150 to 200 | 1.58 (of 2014) | 1.72 (of 2726) | 1.96 (of 1251) | 1.87 (of 22) |
| 200 to 400 | 1.50 (of 5818) | 1.58 (of 6489) | 1.74 (of 1533) | none |
| 400 to more | 1.28 (of 6940) | 1.36 (of 5988) | 1.32 (of 548) | none |

## Highest geometry-matched win-rate alpha at each frequency level (generation 2,001 onward, profit factor above 1.0)

| Trades per year per instrument | Alpha (points) | Win rate | Profit factor | Trades | Timeframe | Generation | Strategy |
|---|---|---|---|---|---|---|---|
| 50 to 100 | +31.8 | 71.8% | 1.92 | 273 | 5 min | 99115 | tr_climax_reversal[inv] OR tr_roc_thrust with st_donchian_mid, f_inside_prior_day_range, f_companion_confirms, f_skip_open; r_stop_swing; x_partial, x_invalidate_ema; stop |
| 100 to 150 | +31.2 | 71.0% | 1.79 | 390 | 5 min | 94693 | tr_climax_reversal[inv] OR tr_roc_thrust with st_donchian_mid, f_inside_prior_day_range, f_companion_confirms; r_stop_swing; x_partial, x_breakeven, x_invalidate_ema; stop |
| 150 to 200 | +30.9 | 66.3% | 1.35 | 478 | 5 min | 97005 | tr_low_volatility_break OR tr_roc_thrust with st_donchian_mid, f_inside_prior_day_range, f_stop_before_close; r_stop_swing; x_partial, x_breakeven; limit |
| 200 to 400 | +28.6 | 64.3% | 1.14 | 762 | 5 min | 96035 | tr_close_extreme_fade OR tr_roc_thrust with f_htf_agrees; r_stop_swing; x_partial, x_breakeven; limit |
| 400 to more | +26.1 | 61.1% | 1.12 | 1866 | 15 min | 92803 | tr_internal_bar_strength[inv]; r_stop_signal_bar; x_partial, x_breakeven; limit |

## Leading candidates by composite score (not certified)

| Generation | Island | Timeframe | Score | Win rate | Alpha | Profit factor | Trades | Per year | Complexity | Strategy |
|---|---|---|---|---|---|---|---|---|---|---|
| 88594 | B | 5 min | 0.788 | 81.9% | +15.1 | 2.02 | 409 | 145 | 18 | tr_williams_hook OR tr_roc_thrust with f_htf_agrees, f_atr_rank_high, f_noise_ratio_ok; r_stop_atr; x_target_atr; market |
| 88840 | B | 5 min | 0.776 | 81.7% | +13.8 | 2.00 | 405 | 144 | 18 | tr_williams_hook OR tr_roc_thrust with f_htf_agrees, f_atr_rank_high, f_noise_ratio_ok; r_stop_atr; x_target_atr; market |
| 96760 | B | 5 min | 0.774 | 81.9% | +14.2 | 2.02 | 409 | 145 | 21 | tr_williams_hook OR tr_roc_thrust with f_htf_agrees, f_atr_rank_high, f_noise_ratio_ok; r_stop_atr; x_target_atr, x_trail_r; market |
| 94412 | B | 5 min | 0.772 | 81.8% | +13.2 | 1.98 | 411 | 146 | 18 | tr_williams_hook OR tr_roc_thrust with f_htf_agrees, f_atr_rank_high, f_noise_ratio_ok; r_stop_atr; x_target_atr; market |
| 94770 | B | 5 min | 0.770 | 81.9% | +13.7 | 2.02 | 409 | 145 | 21 | tr_williams_hook OR tr_roc_thrust with f_htf_agrees, f_atr_rank_high, f_noise_ratio_ok; r_stop_atr; x_target_atr, x_trail_r; market |
| 94216 | B | 5 min | 0.770 | 81.9% | +13.4 | 2.02 | 409 | 145 | 20 | tr_williams_hook OR tr_roc_thrust with f_htf_agrees, f_atr_rank_high, f_noise_ratio_ok; r_stop_atr; x_target_atr, x_breakeven; market |
| 80566 | B | 5 min | 0.766 | 80.6% | +12.7 | 1.86 | 453 | 161 | 15 | tr_williams_hook OR tr_roc_thrust with f_htf_agrees, f_atr_rank_high; r_stop_atr; x_target_atr; market |
| 73770 | B | 5 min | 0.765 | 80.4% | +12.8 | 1.83 | 455 | 161 | 15 | tr_williams_hook OR tr_roc_thrust with f_htf_agrees, f_atr_rank_high; r_stop_atr; x_target_atr; market |
| 93372 | B | 5 min | 0.765 | 81.0% | +13.3 | 1.89 | 399 | 142 | 18 | tr_williams_hook OR tr_roc_thrust with f_htf_agrees, f_atr_rank_high, f_noise_ratio_ok; r_stop_atr; x_target_atr; market |
| 98020 | B | 5 min | 0.764 | 81.3% | +13.9 | 1.91 | 402 | 143 | 18 | tr_williams_hook OR tr_roc_thrust with f_htf_agrees, f_atr_rank_high, f_noise_ratio_ok; r_stop_atr; x_target_atr; market |
| 77812 | B | 5 min | 0.764 | 80.4% | +12.7 | 1.83 | 455 | 161 | 15 | tr_williams_hook OR tr_roc_thrust with f_htf_agrees, f_atr_rank_high; r_stop_atr; x_target_atr; market |
| 86275 | A | 5 min | 0.764 | 76.1% | +22.0 | 1.88 | 339 | 120 | 22 | tr_band_break_failure OR tr_roc_thrust with st_donchian_mid, st_other_instrument_trend, f_inside_prior_day_range, f_stop_before_close; r_stop_swing; x_partial; stop |
| 86886 | B | 5 min | 0.764 | 80.4% | +12.7 | 1.83 | 454 | 161 | 15 | tr_williams_hook OR tr_roc_thrust with f_htf_agrees, f_atr_rank_high; r_stop_atr; x_target_atr; market |
| 78936 | B | 5 min | 0.763 | 80.4% | +12.6 | 1.83 | 454 | 161 | 15 | tr_williams_hook OR tr_roc_thrust with f_htf_agrees, f_atr_rank_high; r_stop_atr; x_target_atr; market |
| 97422 | B | 5 min | 0.763 | 81.4% | +12.9 | 1.91 | 409 | 145 | 18 | tr_williams_hook OR tr_roc_thrust with f_htf_agrees, f_atr_rank_high, f_noise_ratio_ok; r_stop_atr; x_target_atr; market |

## Which constraint binds

Among the 15 leading candidates above, gates failed (from each generation's gates.json):

- wf.in_sample_expectancy_costs: 12 of 15
- freq.session_share: 12 of 15
- freq.trades_per_year_per_instrument: 10 of 15
- sample.trades_per_complexity_point: 3 of 15
- twin.random_exit_wilson_lower: 1 of 15
