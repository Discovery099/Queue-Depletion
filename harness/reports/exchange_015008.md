# Island exchange at generation 15008

The 10 highest-scoring distinct strategies of each island, re-scored on the other island's three test folds (data that never influenced their design; 200 geometry-matched twins). Research data only.

- Mean composite score: 0.515 at home, 0.220 away (retention 43%).
- Mean win rate: 74.4% at home, 68.5% away.
- Mean profit factor: 1.48 at home, 1.06 away; 13 of 20 stay above 1.0 away.
- Leaders passing the stage 1 screen on the away folds: 0 of 20.

| Generation | Home | Timeframe | Home: score / win rate / PF / alpha | Away: score / win rate / PF / alpha / trades | Strategy |
|---|---|---|---|---|---|
| 14703 | A | 15 min | 0.535 / 73.6% / 1.44 / +9.9 | 0.310 / 68.6% / 1.17 / +4.1 / 344 | tr_false_break_prior_day with st_ichimoku_cloud; r_stop_atr; x_target_r; market |
| 14887 | A | 5 min | 0.535 / 73.7% / 1.49 / +9.4 | 0.000 / 69.1% / 0.94 / +3.5 / 417 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |
| 13159 | A | 15 min | 0.534 / 74.1% / 1.43 / +9.3 | 0.349 / 70.7% / 1.23 / +5.6 / 392 | tr_false_break_prior_day with st_ichimoku_cloud; r_stop_atr; x_target_r; market |
| 14407 | A | 15 min | 0.529 / 71.3% / 1.63 / +10.8 | 0.123 / 63.7% / 1.15 / +4.1 / 311 | tr_ema_cross with f_signal_bar_not_huge; r_stop_swing; x_target_r; market |
| 12233 | A | 15 min | 0.526 / 73.9% / 1.41 / +8.4 | 0.333 / 70.6% / 1.19 / +5.8 / 367 | tr_false_break_prior_day with st_ichimoku_cloud; r_stop_atr; x_target_r; market |
| 13539 | A | 5 min | 0.524 / 73.7% / 1.44 / +8.0 | 0.000 / 69.3% / 0.94 / +3.9 / 460 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |
| 13469 | A | 5 min | 0.524 / 73.6% / 1.44 / +8.8 | 0.000 / 69.3% / 0.94 / +3.6 / 460 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |
| 14935 | A | 15 min | 0.517 / 70.6% / 1.54 / +9.9 | 0.213 / 64.8% / 1.18 / +3.8 / 318 | tr_ema_cross with f_signal_bar_not_huge; r_stop_swing; x_target_r; market |
| 14255 | A | 15 min | 0.516 / 77.6% / 1.35 / +8.3 | 0.322 / 72.2% / 1.11 / +2.9 / 309 | tr_false_break_prior_day with st_ichimoku_cloud; r_stop_atr; x_target_r; market |
| 8403 | A | 15 min | 0.516 / 73.7% / 1.42 / +8.8 | 0.251 / 69.5% / 1.14 / +5.5 / 466 | tr_false_break_prior_day OR tr_rsi_divergence with st_ichimoku_cloud; r_stop_atr; x_target_r; market |
| 5480 | B | 30 min | 0.547 / 71.5% / 1.61 / +15.0 | 0.188 / 60.1% / 0.96 / +4.2 / 479 | tr_price_ema_cross; r_stop_percent; x_target_atr; market |
| 9866 | B | 30 min | 0.523 / 71.2% / 1.59 / +14.0 | 0.157 / 60.1% / 0.95 / +3.9 / 481 | tr_price_ema_cross; r_stop_percent; x_target_atr, x_trail_r; market |
| 13088 | B | 5 min | 0.513 / 78.1% / 1.55 / +12.9 | 0.258 / 71.0% / 0.99 / +5.4 / 328 | tr_low_volatility_break with st_first_minutes_direction, st_donchian_mid, f_weekday_block; r_stop_percent; x_target_atr; market |
| 13742 | B | 5 min | 0.512 / 78.1% / 1.54 / +13.4 | 0.253 / 70.9% / 0.99 / +5.1 / 327 | tr_low_volatility_break with st_first_minutes_direction, st_donchian_mid, f_weekday_block; r_stop_percent; x_target_atr; market |
| 14970 | B | 5 min | 0.510 / 78.1% / 1.56 / +13.1 | 0.259 / 71.2% / 1.00 / +6.1 / 316 | tr_low_volatility_break with st_first_minutes_direction, st_donchian_mid, f_weekday_block; r_stop_percent; x_target_atr; market |
| 12756 | B | 5 min | 0.509 / 77.8% / 1.52 / +12.9 | 0.269 / 71.4% / 1.02 / +5.1 / 343 | tr_low_volatility_break with st_first_minutes_direction, st_other_instrument_trend, f_weekday_block; r_stop_percent; x_target_atr; market |
| 9850 | B | 5 min | 0.490 / 78.4% / 1.47 / +12.9 | 0.261 / 74.1% / 1.13 / +7.6 / 297 | tr_low_volatility_break with st_first_minutes_direction, st_other_instrument_trend, f_weekday_block; r_stop_percent; x_target_atr; market |
| 12506 | B | 30 min | 0.489 / 68.7% / 1.58 / +13.9 | 0.251 / 60.8% / 1.19 / +6.9 / 454 | tr_price_ema_cross with f_companion_confirms; r_stop_percent; x_target_atr; market |
| 13116 | B | 5 min | 0.484 / 75.4% / 1.32 / +10.5 | 0.298 / 71.2% / 1.00 / +6.4 / 400 | tr_low_volatility_break with st_first_minutes_direction, st_donchian_mid; r_stop_percent; x_target_atr; market |
| 13126 | B | 5 min | 0.476 / 75.0% / 1.31 / +10.1 | 0.298 / 71.3% / 1.01 / +6.3 / 404 | tr_low_volatility_break with st_first_minutes_direction, st_donchian_mid; r_stop_percent; x_target_atr; market |
