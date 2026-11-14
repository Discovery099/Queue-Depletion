# Island exchange at generation 40000

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.517 at home, 0.392 away (retention 76%).
- Mean win rate: 75.3% at home, 72.4% away.
- Mean profit factor: 1.40 at home, 1.23 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 20 of 20; 0 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 39729 | A | 5 min | 0.669 / 74.3% / 1.67 | 0.415 / 67.7% / 1.43 / +11.3 / 381 | yes | regime: st_donchian_mid(n=100) |
| 39969 | A | 5 min | 0.618 / 73.6% / 1.59 | 0.441 / 68.2% / 1.44 / +13.4 / 415 | yes | regime: st_donchian_mid(n=100) |
| 37429 | A | 5 min | 0.615 / 78.2% / 1.58 | 0.462 / 73.3% / 1.40 / +8.8 / 330 | yes | regime: st_donchian_mid(n=100) |
| 34893 | A | 15 min | 0.534 / 74.2% / 1.53 | 0.322 / 69.0% / 1.23 / +5.9 / 400 | yes | regime: st_vwap_side(); st_gap_direction(g=0.001) |
| 39391 | A | 5 min | 0.531 / 76.1% / 1.41 | 0.395 / 72.1% / 1.30 / +9.5 / 366 | yes | regime: st_donchian_mid(n=100) |
| 30409 | A | 15 min | 0.524 / 76.6% / 1.49 | 0.289 / 71.1% / 1.11 / +3.7 / 301 | yes | location: loc_ema_distance(n=50, k=2.0) |
| 33485 | A | 5 min | 0.522 / 74.7% / 1.34 | 0.308 / 72.3% / 1.08 / +8.4 / 321 | yes | regime: st_gap_direction(g=0.004) |
| 35091 | A | 15 min | 0.519 / 77.2% / 1.30 | 0.350 / 72.5% / 1.13 / +3.2 / 334 | yes | regime: st_ichimoku_cloud(s=1) |
| 38159 | A | 15 min | 0.518 / 75.4% / 1.41 | 0.267 / 69.1% / 1.00 / +3.2 / 766 | yes | trigger: tr_volume_climax_follow(n=10) |
| 39309 | A | 5 min | 0.512 / 75.7% / 1.38 | 0.422 / 74.1% / 1.35 / +8.8 / 441 | yes | regime: st_wave_trend_side(band=5) |
| 37086 | B | 5 min | 0.534 / 76.9% / 1.34 | 0.382 / 73.1% / 1.12 / +6.7 / 468 | yes | filter: f_session_range_developed(k=4.0); f_not_extended_from_vwap(k=3.0) |
| 38672 | B | 5 min | 0.506 / 75.8% / 1.53 | 0.443 / 75.6% / 1.27 / +10.6 / 349 | yes | regime: st_donchian_mid(n=100) |
| 38448 | B | 5 min | 0.502 / 76.5% / 1.34 | 0.338 / 72.5% / 1.08 / +6.5 / 346 | yes | regime: st_donchian_mid(n=100) |
| 33240 | B | 5 min | 0.478 / 74.8% / 1.38 | 0.526 / 77.4% / 1.40 / +13.4 / 328 | yes | regime: st_donchian_mid(n=100) |
| 38992 | B | 5 min | 0.472 / 75.0% / 1.22 | 0.460 / 73.9% / 1.20 / +8.0 / 789 | yes | filter: f_not_extended_from_vwap(k=3.0) |
| 38948 | B | 5 min | 0.468 / 73.4% / 1.35 | 0.309 / 71.8% / 1.05 / +7.2 / 517 | yes | filter: f_inside_prior_day_range(); f_stop_before_close(m=15) |
| 39240 | B | 5 min | 0.467 / 74.4% / 1.40 | 0.529 / 77.0% / 1.43 / +13.2 / 326 | yes | regime: st_donchian_mid(n=100) |
| 38090 | B | 5 min | 0.455 / 74.8% / 1.21 | 0.445 / 73.9% / 1.20 / +7.8 / 833 | yes | filter: f_not_extended_from_vwap(k=3.0) |
| 38984 | B | 5 min | 0.452 / 74.4% / 1.26 | 0.390 / 72.2% / 1.17 / +6.3 / 818 | yes | filter: f_htf_agrees(k=6); f_skip_open(m=30) |
| 38186 | B | 5 min | 0.450 / 74.0% / 1.30 | 0.347 / 70.5% / 1.14 / +5.5 / 779 | yes | filter: f_htf_agrees(k=6); f_skip_open(m=30) |
