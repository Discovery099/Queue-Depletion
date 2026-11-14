# Island exchange at generation 37500

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.495 at home, 0.294 away (retention 59%).
- Mean win rate: 75.5% at home, 71.6% away.
- Mean profit factor: 1.38 at home, 1.12 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 16 of 20; 4 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 37429 | A | 5 min | 0.615 / 78.2% / 1.58 | 0.462 / 73.3% / 1.40 / +8.8 / 330 | yes | regime: st_donchian_mid(n=100) |
| 34893 | A | 15 min | 0.534 / 74.2% / 1.53 | 0.322 / 69.0% / 1.23 / +5.9 / 400 | yes | regime: st_vwap_side(); st_gap_direction(g=0.001) |
| 30409 | A | 15 min | 0.524 / 76.6% / 1.49 | 0.289 / 71.1% / 1.11 / +3.7 / 301 | yes | location: loc_ema_distance(n=50, k=2.0) |
| 33485 | A | 5 min | 0.522 / 74.7% / 1.34 | 0.308 / 72.3% / 1.08 / +8.4 / 321 | yes | regime: st_gap_direction(g=0.004) |
| 35091 | A | 15 min | 0.519 / 77.2% / 1.30 | 0.350 / 72.5% / 1.13 / +3.2 / 334 | yes | regime: st_ichimoku_cloud(s=1) |
| 32251 | A | 15 min | 0.514 / 75.3% / 1.41 | 0.280 / 69.2% / 1.01 / +4.0 / 773 | yes | trigger: tr_volume_climax_follow(n=10) |
| 35645 | A | 15 min | 0.512 / 75.7% / 1.50 | 0.000 / 66.7% / 0.93 / +0.2 / 499 | no | regime: st_wave_trend_side(band=0) |
| 36351 | A | 15 min | 0.505 / 76.2% / 1.42 | 0.000 / 66.7% / 0.88 / -0.5 / 403 | no | regime: st_both_vwap_side() |
| 37285 | A | 15 min | 0.494 / 75.7% / 1.31 | 0.000 / 68.1% / 0.88 / +2.0 / 407 | no | regime: st_both_vwap_side() |
| 33989 | A | 5 min | 0.485 / 74.2% / 1.27 | 0.319 / 71.1% / 1.04 / +5.8 / 955 | yes | regime: st_macd_side(s=2) |
| 37086 | B | 5 min | 0.534 / 76.9% / 1.34 | 0.382 / 73.1% / 1.12 / +6.7 / 468 | yes | filter: f_session_range_developed(k=4.0); f_not_extended_from_vwap(k=3.0) |
| 36910 | B | 5 min | 0.501 / 74.8% / 1.38 | 0.370 / 73.2% / 1.11 / +8.2 / 456 | yes | filter: f_inside_prior_day_range(); f_stop_before_close(m=15) |
| 33240 | B | 5 min | 0.478 / 74.8% / 1.38 | 0.526 / 77.4% / 1.40 / +13.4 / 328 | yes | regime: st_donchian_mid(n=100) |
| 36184 | B | 5 min | 0.468 / 78.9% / 1.75 | 0.282 / 73.3% / 1.16 / +6.4 / 262 | yes | filter: f_session_range_developed(k=6.0); f_not_extended_from_vwap(k=3.0) |
| 36930 | B | 5 min | 0.467 / 75.1% / 1.22 | 0.458 / 73.8% / 1.20 / +8.6 / 800 | yes | filter: f_not_extended_from_vwap(k=3.0) |
| 34248 | B | 5 min | 0.459 / 75.8% / 1.29 | 0.000 / 70.7% / 0.96 / +4.2 / 386 | no | regime: st_first_minutes_direction(k=0.5, m=30); st_donchian_mid(n=100) |
| 36848 | B | 5 min | 0.457 / 74.9% / 1.46 | 0.403 / 74.7% / 1.24 / +9.3 / 359 | yes | regime: st_donchian_mid(n=100) |
| 37384 | B | 5 min | 0.451 / 74.8% / 1.21 | 0.454 / 74.0% / 1.21 / +8.2 / 835 | yes | filter: f_not_extended_from_vwap(k=3.0) |
| 33766 | B | 5 min | 0.437 / 73.3% / 1.25 | 0.340 / 70.7% / 1.15 / +5.4 / 825 | yes | filter: f_htf_agrees(k=4); f_skip_open(m=30) |
| 35232 | B | 5 min | 0.435 / 73.2% / 1.25 | 0.337 / 70.7% / 1.15 / +5.3 / 832 | yes | filter: f_htf_agrees(k=4); f_skip_open(m=30) |
