# Island exchange at generation 35000

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.469 at home, 0.269 away (retention 57%).
- Mean win rate: 74.0% at home, 70.3% away.
- Mean profit factor: 1.35 at home, 1.12 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 15 of 20; 5 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 34893 | A | 15 min | 0.534 / 74.2% / 1.53 | 0.322 / 69.0% / 1.23 / +5.9 / 400 | yes | regime: st_vwap_side(); st_gap_direction(g=0.001) |
| 30409 | A | 15 min | 0.524 / 76.6% / 1.49 | 0.289 / 71.1% / 1.11 / +3.7 / 301 | yes | location: loc_ema_distance(n=50, k=2.0) |
| 33485 | A | 5 min | 0.522 / 74.7% / 1.34 | 0.308 / 72.3% / 1.08 / +8.4 / 321 | yes | regime: st_gap_direction(g=0.004) |
| 14255 | A | 15 min | 0.516 / 77.6% / 1.35 | 0.322 / 72.2% / 1.11 / +2.9 / 309 | yes | regime: st_ichimoku_cloud(s=1) |
| 32251 | A | 15 min | 0.514 / 75.3% / 1.41 | 0.280 / 69.2% / 1.01 / +4.0 / 773 | yes | trigger: tr_volume_climax_follow(n=10) |
| 31539 | A | 15 min | 0.494 / 75.2% / 1.48 | 0.267 / 68.9% / 1.07 / +4.3 / 470 | yes | regime: st_late_session_trend(start=300) |
| 33989 | A | 5 min | 0.485 / 74.2% / 1.27 | 0.319 / 71.1% / 1.04 / +5.8 / 955 | yes | regime: st_macd_side(s=2) |
| 32693 | A | 15 min | 0.469 / 75.4% / 1.30 | 0.000 / 68.8% / 0.92 / +2.1 / 1207 | no | trigger: tr_volume_climax_follow(n=10) |
| 33729 | A | 5 min | 0.448 / 68.8% / 1.41 | 0.000 / 62.2% / 0.97 / +2.6 / 397 | no | regime: st_vwap_side() |
| 34425 | A | 5 min | 0.441 / 69.7% / 1.29 | 0.029 / 64.7% / 1.22 / +6.3 / 354 | no | regime: st_gap_direction(g=0.004) |
| 33240 | B | 5 min | 0.478 / 74.8% / 1.38 | 0.526 / 77.4% / 1.40 / +13.4 / 328 | yes | regime: st_donchian_mid(n=100) |
| 33818 | B | 5 min | 0.470 / 78.2% / 1.49 | 0.000 / 70.5% / 0.94 / +5.3 / 312 | no | regime: st_first_minutes_direction(k=0.5, m=30); st_donchian_mid(n=100) |
| 34872 | B | 5 min | 0.462 / 75.2% / 1.44 | 0.584 / 78.6% / 1.51 / +15.2 / 304 | yes | regime: st_donchian_mid(n=100) |
| 34326 | B | 5 min | 0.455 / 74.0% / 1.24 | 0.373 / 71.6% / 1.12 / +5.3 / 872 | yes | filter: f_signal_bar_not_huge(k=1.5) |
| 33766 | B | 5 min | 0.437 / 73.3% / 1.25 | 0.340 / 70.7% / 1.15 / +5.4 / 825 | yes | filter: f_htf_agrees(k=4); f_skip_open(m=30) |
| 9056 | B | 15 min | 0.431 / 72.4% / 1.34 | 0.315 / 69.1% / 1.07 / +2.3 / 430 | yes | filter: f_weekday_block(day=3) |
| 31088 | B | 5 min | 0.427 / 73.8% / 1.20 | 0.390 / 72.7% / 1.21 / +6.3 / 971 | yes | filter: f_htf_agrees(k=4); f_skip_open(m=15) |
| 33464 | B | 5 min | 0.426 / 74.0% / 1.22 | 0.353 / 71.2% / 1.11 / +5.0 / 770 | yes | filter: f_signal_bar_not_huge(k=1.5); f_skip_open(m=15) |
| 34230 | B | 10 min | 0.424 / 69.4% / 1.25 | 0.000 / 62.9% / 0.86 / +3.1 / 498 | no | regime: st_both_vwap_side() |
| 33982 | B | 5 min | 0.416 / 73.2% / 1.22 | 0.361 / 71.9% / 1.16 / +5.8 / 634 | yes | filter: f_session_range_developed(k=6.0) |
