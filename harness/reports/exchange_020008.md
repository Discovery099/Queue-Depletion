# Island exchange at generation 20008

The 10 highest-scoring distinct strategies of each island, re-scored on the other island's three test folds (data that never influenced their design; 200 geometry-matched twins). Research data only.

- Mean composite score: 0.567 at home, 0.100 away (retention 18%).
- Mean win rate: 75.6% at home, 66.3% away.
- Mean profit factor: 1.63 at home, 0.91 away; 5 of 20 stay above 1.0 away.
- Leaders passing the stage 1 screen on the away folds: 0 of 20.

| Generation | Home | Timeframe | Home: score / win rate / PF / alpha | Away: score / win rate / PF / alpha / trades | Strategy |
|---|---|---|---|---|---|
| 18133 | A | 5 min | 0.636 / 74.7% / 1.72 / +13.5 | 0.000 / 64.8% / 0.82 / +3.0 / 301 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; limit |
| 17057 | A | 5 min | 0.631 / 75.6% / 1.67 / +10.7 | 0.000 / 67.4% / 0.86 / +3.2 / 334 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |
| 18999 | A | 5 min | 0.629 / 75.2% / 1.68 / +12.9 | 0.000 / 64.0% / 0.77 / +2.4 / 289 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; limit |
| 17681 | A | 5 min | 0.628 / 75.6% / 1.74 / +13.6 | 0.000 / 62.4% / 0.73 / -0.2 / 266 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; limit |
| 17339 | A | 5 min | 0.627 / 75.5% / 1.67 / +10.4 | 0.000 / 67.1% / 0.84 / +1.1 / 331 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |
| 17123 | A | 5 min | 0.627 / 75.1% / 1.66 / +11.5 | 0.000 / 66.9% / 0.85 / +2.3 / 356 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; market |
| 19109 | A | 5 min | 0.623 / 74.6% / 1.71 / +12.3 | 0.000 / 65.0% / 0.82 / +1.4 / 297 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; limit |
| 17939 | A | 5 min | 0.619 / 75.5% / 1.73 / +12.5 | 0.000 / 62.3% / 0.72 / +1.1 / 265 | tr_trail_flip with st_gap_direction; r_stop_swing; x_target_atr; limit |
| 18231 | A | 5 min | 0.618 / 77.3% / 1.73 / +14.3 | 0.000 / 64.1% / 0.75 / +0.6 / 270 | tr_trail_flip with st_gap_direction, f_stop_before_close; r_stop_swing; x_target_atr; limit |
| 19413 | A | 15 min | 0.605 / 82.0% / 1.97 / +12.2 | 0.106 / 71.7% / 1.07 / +4.1 / 297 | tr_false_break_prior_day with st_ichimoku_cloud; r_stop_atr; x_target_r; market |
| 5480 | B | 30 min | 0.547 / 71.5% / 1.61 / +15.0 | 0.188 / 60.1% / 0.96 / +4.2 / 479 | tr_price_ema_cross; r_stop_percent; x_target_atr; market |
| 9866 | B | 30 min | 0.523 / 71.2% / 1.59 / +14.0 | 0.157 / 60.1% / 0.95 / +3.9 / 481 | tr_price_ema_cross; r_stop_percent; x_target_atr, x_trail_r; market |
| 13088 | B | 5 min | 0.513 / 78.1% / 1.55 / +12.9 | 0.258 / 71.0% / 0.99 / +5.4 / 328 | tr_low_volatility_break with st_first_minutes_direction, st_donchian_mid, f_weekday_block; r_stop_percent; x_target_atr; market |
| 13742 | B | 5 min | 0.512 / 78.1% / 1.54 / +13.4 | 0.253 / 70.9% / 0.99 / +5.1 / 327 | tr_low_volatility_break with st_first_minutes_direction, st_donchian_mid, f_weekday_block; r_stop_percent; x_target_atr; market |
| 14970 | B | 5 min | 0.510 / 78.1% / 1.56 / +13.1 | 0.259 / 71.2% / 1.00 / +6.1 / 316 | tr_low_volatility_break with st_first_minutes_direction, st_donchian_mid, f_weekday_block; r_stop_percent; x_target_atr; market |
| 12756 | B | 5 min | 0.509 / 77.8% / 1.52 / +12.9 | 0.269 / 71.4% / 1.02 / +5.1 / 343 | tr_low_volatility_break with st_first_minutes_direction, st_other_instrument_trend, f_weekday_block; r_stop_percent; x_target_atr; market |
| 15662 | B | 5 min | 0.504 / 77.6% / 1.52 / +13.7 | 0.000 / 69.9% / 0.97 / +6.3 / 329 | tr_low_volatility_break with st_first_minutes_direction, st_donchian_mid, f_weekday_block; r_stop_percent; x_target_atr, x_breakeven; market |
| 19770 | B | 10 min | 0.502 / 71.8% / 1.37 / +12.6 | 0.000 / 60.2% / 0.79 / -0.9 / 337 | tr_keltner_reentry with st_both_vwap_side; r_stop_swing; x_target_atr; market |
| 9850 | B | 5 min | 0.490 / 78.4% / 1.47 / +12.9 | 0.261 / 74.1% / 1.13 / +7.6 / 297 | tr_low_volatility_break with st_first_minutes_direction, st_other_instrument_trend, f_weekday_block; r_stop_percent; x_target_atr; market |
| 12506 | B | 30 min | 0.489 / 68.7% / 1.58 / +13.9 | 0.251 / 60.8% / 1.19 / +6.9 / 454 | tr_price_ema_cross with f_companion_confirms; r_stop_percent; x_target_atr; market |
