# Island exchange at generation 42500

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.545 at home, 0.359 away (retention 66%).
- Mean win rate: 75.7% at home, 71.6% away.
- Mean profit factor: 1.49 at home, 1.21 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 18 of 20; 2 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 39729 | A | 5 min | 0.669 / 74.3% / 1.67 | 0.415 / 67.7% / 1.43 / +11.3 / 381 | yes | regime: st_donchian_mid(n=100) |
| 41949 | A | 5 min | 0.649 / 73.6% / 1.61 | 0.459 / 67.9% / 1.46 / +13.6 / 424 | yes | regime: st_donchian_mid(n=100) |
| 42435 | A | 5 min | 0.622 / 74.3% / 1.68 | 0.000 / 65.6% / 0.85 / +3.2 / 311 | no | regime: st_gap_direction(g=0.002) |
| 37429 | A | 5 min | 0.615 / 78.2% / 1.58 | 0.462 / 73.3% / 1.40 / +8.8 / 330 | yes | regime: st_donchian_mid(n=100) |
| 42207 | A | 5 min | 0.605 / 74.2% / 1.65 | 0.000 / 65.3% / 0.85 / +3.5 / 317 | no | regime: st_gap_direction(g=0.002) |
| 40377 | A | 5 min | 0.603 / 79.5% / 1.68 | 0.317 / 71.2% / 1.22 / +8.6 / 288 | yes | regime: st_donchian_mid(n=100) |
| 41529 | A | 5 min | 0.596 / 78.1% / 1.53 | 0.457 / 73.4% / 1.38 / +10.6 / 331 | yes | regime: st_donchian_mid(n=100) |
| 40905 | A | 15 min | 0.567 / 74.1% / 1.59 | 0.286 / 66.9% / 1.12 / +4.0 / 505 | yes | regime: st_vwap_side(); st_ichimoku_cloud(s=1) |
| 39391 | A | 5 min | 0.531 / 76.1% / 1.41 | 0.395 / 72.1% / 1.30 / +9.5 / 366 | yes | regime: st_donchian_mid(n=100) |
| 30409 | A | 15 min | 0.524 / 76.6% / 1.49 | 0.289 / 71.1% / 1.11 / +3.7 / 301 | yes | location: loc_ema_distance(n=50, k=2.0) |
| 37086 | B | 5 min | 0.534 / 76.9% / 1.34 | 0.382 / 73.1% / 1.12 / +6.7 / 468 | yes | filter: f_session_range_developed(k=4.0); f_not_extended_from_vwap(k=3.0) |
| 42402 | B | 5 min | 0.523 / 77.0% / 1.38 | 0.352 / 73.2% / 1.11 / +7.4 / 328 | yes | regime: st_donchian_mid(n=100) |
| 40946 | B | 5 min | 0.509 / 76.2% / 1.73 | 0.455 / 74.7% / 1.48 / +10.1 / 292 | yes | regime: st_wave_trend_side(band=5) |
| 41334 | B | 5 min | 0.508 / 75.7% / 1.54 | 0.456 / 75.6% / 1.31 / +10.6 / 349 | yes | regime: st_donchian_mid(n=100) |
| 41400 | B | 5 min | 0.486 / 75.0% / 1.34 | 0.358 / 71.6% / 1.13 / +5.0 / 764 | yes | filter: f_htf_agrees(k=6); f_skip_open(m=45) |
| 41482 | B | 5 min | 0.479 / 75.1% / 1.34 | 0.359 / 71.8% / 1.13 / +4.8 / 760 | yes | filter: f_htf_agrees(k=6); f_skip_open(m=45) |
| 33240 | B | 5 min | 0.478 / 74.8% / 1.38 | 0.526 / 77.4% / 1.40 / +13.4 / 328 | yes | regime: st_donchian_mid(n=100) |
| 40438 | B | 5 min | 0.476 / 73.5% / 1.36 | 0.311 / 71.8% / 1.05 / +7.5 / 517 | yes | filter: f_inside_prior_day_range(); f_stop_before_close(m=15) |
| 38992 | B | 5 min | 0.472 / 75.0% / 1.22 | 0.460 / 73.9% / 1.20 / +8.0 / 789 | yes | filter: f_not_extended_from_vwap(k=3.0) |
| 41532 | B | 5 min | 0.458 / 75.1% / 1.22 | 0.443 / 73.6% / 1.19 / +8.2 / 784 | yes | regime: st_other_instrument_trend(n=20) |
