# Island exchange at generation 47500

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.572 at home, 0.320 away (retention 56%).
- Mean win rate: 76.0% at home, 70.1% away.
- Mean profit factor: 1.54 at home, 1.17 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 17 of 20; 3 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 47013 | A | 5 min | 0.734 / 75.3% / 1.77 | 0.451 / 68.0% / 1.42 / +14.0 / 372 | yes | regime: st_donchian_mid(n=100) |
| 45871 | A | 5 min | 0.705 / 73.8% / 1.72 | 0.393 / 66.5% / 1.40 / +11.7 / 418 | yes | regime: st_donchian_mid(n=100) |
| 44793 | A | 5 min | 0.676 / 73.0% / 1.64 | 0.381 / 66.1% / 1.25 / +14.7 / 413 | yes | regime: st_donchian_mid(n=100) |
| 43623 | A | 5 min | 0.659 / 72.6% / 1.64 | 0.375 / 66.0% / 1.27 / +14.8 / 421 | yes | regime: st_donchian_mid(n=100) |
| 46553 | A | 5 min | 0.629 / 78.6% / 1.61 | 0.441 / 73.2% / 1.36 / +10.2 / 314 | yes | regime: st_donchian_mid(n=100) |
| 47097 | A | 15 min | 0.619 / 74.5% / 1.71 | 0.317 / 66.1% / 1.30 / +4.2 / 454 | yes | regime: st_vwap_side(); st_ichimoku_cloud(s=1) |
| 47081 | A | 5 min | 0.609 / 78.4% / 1.59 | 0.420 / 72.9% / 1.32 / +9.7 / 321 | yes | regime: st_donchian_mid(n=100) |
| 45429 | A | 15 min | 0.576 / 77.6% / 1.46 | 0.000 / 68.8% / 0.90 / +1.0 / 336 | no | regime: st_donchian_mid(n=100) |
| 42799 | A | 15 min | 0.567 / 77.8% / 1.47 | 0.000 / 69.2% / 0.93 / +3.4 / 341 | no | regime: st_donchian_mid(n=100) |
| 30409 | A | 15 min | 0.524 / 76.6% / 1.49 | 0.289 / 71.1% / 1.11 / +3.7 / 301 | yes | location: loc_ema_distance(n=50, k=2.0) |
| 46692 | B | 5 min | 0.541 / 76.5% / 1.39 | 0.343 / 71.2% / 1.09 / +5.8 / 510 | yes | filter: f_session_range_developed(k=4.0); f_not_extended_from_vwap(k=3.0) |
| 45920 | B | 5 min | 0.536 / 77.2% / 1.61 | 0.296 / 69.0% / 1.12 / +4.3 / 329 | yes | regime: st_market_tide(band=5) |
| 37086 | B | 5 min | 0.534 / 76.9% / 1.34 | 0.382 / 73.1% / 1.12 / +6.7 / 468 | yes | filter: f_session_range_developed(k=4.0); f_not_extended_from_vwap(k=3.0) |
| 42402 | B | 5 min | 0.523 / 77.0% / 1.38 | 0.352 / 73.2% / 1.11 / +7.4 / 328 | yes | regime: st_donchian_mid(n=100) |
| 45242 | B | 5 min | 0.518 / 77.4% / 1.60 | 0.285 / 68.5% / 1.10 / +4.0 / 337 | yes | regime: st_market_tide(band=5) |
| 46712 | B | 5 min | 0.515 / 74.9% / 1.39 | 0.399 / 72.6% / 1.25 / +7.8 / 613 | yes | regime: st_donchian_mid(n=100) |
| 47170 | B | 5 min | 0.504 / 78.1% / 1.84 | 0.246 / 69.7% / 1.07 / +4.8 / 284 | no | filter: f_session_range_developed(k=6.0); f_not_extended_from_vwap(k=3.0) |
| 45102 | B | 5 min | 0.499 / 75.2% / 1.38 | 0.351 / 72.0% / 1.13 / +6.2 / 600 | yes | regime: st_donchian_mid(n=100) |
| 41400 | B | 5 min | 0.486 / 75.0% / 1.34 | 0.358 / 71.6% / 1.13 / +5.0 / 764 | yes | filter: f_htf_agrees(k=6); f_skip_open(m=45) |
| 44562 | B | 5 min | 0.484 / 74.5% / 1.35 | 0.316 / 72.4% / 1.05 / +7.1 / 474 | yes | filter: f_inside_prior_day_range(); f_stop_before_close(m=30) |
