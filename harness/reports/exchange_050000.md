# Island exchange at generation 50000

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.572 at home, 0.366 away (retention 64%).
- Mean win rate: 75.5% at home, 69.9% away.
- Mean profit factor: 1.52 at home, 1.22 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 19 of 20; 1 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 47013 | A | 5 min | 0.734 / 75.3% / 1.77 | 0.451 / 68.0% / 1.42 / +14.0 / 372 | yes | regime: st_donchian_mid(n=100) |
| 45871 | A | 5 min | 0.705 / 73.8% / 1.72 | 0.393 / 66.5% / 1.40 / +11.7 / 418 | yes | regime: st_donchian_mid(n=100) |
| 47649 | A | 5 min | 0.682 / 72.8% / 1.64 | 0.383 / 65.9% / 1.25 / +15.7 / 413 | yes | regime: st_donchian_mid(n=100) |
| 47973 | A | 5 min | 0.673 / 73.3% / 1.67 | 0.372 / 65.8% / 1.29 / +12.4 / 412 | yes | regime: st_donchian_mid(n=100) |
| 46553 | A | 5 min | 0.629 / 78.6% / 1.61 | 0.441 / 73.2% / 1.36 / +10.2 / 314 | yes | regime: st_donchian_mid(n=100) |
| 47097 | A | 15 min | 0.619 / 74.5% / 1.71 | 0.317 / 66.1% / 1.30 / +4.2 / 454 | yes | regime: st_vwap_side(); st_ichimoku_cloud(s=1) |
| 49267 | A | 5 min | 0.614 / 78.5% / 1.61 | 0.414 / 71.8% / 1.33 / +9.2 / 330 | yes | regime: st_donchian_mid(n=100) |
| 48981 | A | 5 min | 0.524 / 71.9% / 1.46 | 0.436 / 67.8% / 1.35 / +15.6 / 456 | yes | regime: st_donchian_mid(n=100) |
| 30409 | A | 15 min | 0.524 / 76.6% / 1.49 | 0.289 / 71.1% / 1.11 / +3.7 / 301 | yes | location: loc_ema_distance(n=50, k=2.0) |
| 47823 | A | 5 min | 0.524 / 71.1% / 1.40 | 0.451 / 68.3% / 1.37 / +16.1 / 461 | yes | regime: st_donchian_mid(n=100) |
| 48034 | B | 5 min | 0.574 / 78.4% / 1.69 | 0.306 / 70.0% / 1.15 / +5.5 / 297 | yes | regime: st_market_tide(band=10) |
| 48736 | B | 5 min | 0.543 / 76.5% / 1.39 | 0.343 / 71.2% / 1.09 / +5.6 / 510 | yes | filter: f_session_range_developed(k=4.0); f_not_extended_from_vwap(k=3.0) |
| 37086 | B | 5 min | 0.534 / 76.9% / 1.34 | 0.382 / 73.1% / 1.12 / +6.7 / 468 | yes | filter: f_session_range_developed(k=4.0); f_not_extended_from_vwap(k=3.0) |
| 42402 | B | 5 min | 0.523 / 77.0% / 1.38 | 0.352 / 73.2% / 1.11 / +7.4 / 328 | yes | regime: st_donchian_mid(n=100) |
| 49626 | B | 5 min | 0.521 / 75.5% / 1.42 | 0.251 / 69.1% / 0.99 / +5.5 / 346 | no | filter: f_inside_prior_day_range(); f_not_extended_from_vwap(k=3.0) |
| 45242 | B | 5 min | 0.518 / 77.4% / 1.60 | 0.285 / 68.5% / 1.10 / +4.0 / 337 | yes | regime: st_market_tide(band=5) |
| 46712 | B | 5 min | 0.515 / 74.9% / 1.39 | 0.399 / 72.6% / 1.25 / +7.8 / 613 | yes | regime: st_donchian_mid(n=100) |
| 48466 | B | 5 min | 0.506 / 76.1% / 1.33 | 0.355 / 72.7% / 1.11 / +6.0 / 487 | yes | filter: f_session_range_developed(k=4.0); f_not_extended_from_vwap(k=3.0) |
| 45102 | B | 5 min | 0.499 / 75.2% / 1.38 | 0.351 / 72.0% / 1.13 / +6.2 / 600 | yes | regime: st_donchian_mid(n=100) |
| 41400 | B | 5 min | 0.486 / 75.0% / 1.34 | 0.358 / 71.6% / 1.13 / +5.0 / 764 | yes | filter: f_htf_agrees(k=6); f_skip_open(m=45) |
