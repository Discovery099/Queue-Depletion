# Island exchange at generation 45000

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.569 at home, 0.365 away (retention 64%).
- Mean win rate: 75.2% at home, 70.4% away.
- Mean profit factor: 1.53 at home, 1.24 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 17 of 20; 3 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 43033 | A | 5 min | 0.686 / 74.3% / 1.70 | 0.450 / 67.7% / 1.47 / +14.2 / 387 | yes | regime: st_donchian_mid(n=100) |
| 42505 | A | 5 min | 0.678 / 73.8% / 1.73 | 0.305 / 64.2% / 1.23 / +11.0 / 388 | no | regime: st_donchian_mid(n=100) |
| 44793 | A | 5 min | 0.676 / 73.0% / 1.64 | 0.381 / 66.1% / 1.25 / +14.7 / 413 | yes | regime: st_donchian_mid(n=100) |
| 43623 | A | 5 min | 0.659 / 72.6% / 1.64 | 0.375 / 66.0% / 1.27 / +14.8 / 421 | yes | regime: st_donchian_mid(n=100) |
| 43987 | A | 5 min | 0.650 / 73.3% / 1.68 | 0.366 / 65.7% / 1.39 / +9.6 / 435 | yes | regime: st_donchian_mid(n=100) |
| 37429 | A | 5 min | 0.615 / 78.2% / 1.58 | 0.462 / 73.3% / 1.40 / +8.8 / 330 | yes | regime: st_donchian_mid(n=100) |
| 43417 | A | 15 min | 0.609 / 74.5% / 1.66 | 0.320 / 66.1% / 1.28 / +4.8 / 454 | yes | regime: st_vwap_side(); st_ichimoku_cloud(s=1) |
| 43991 | A | 5 min | 0.607 / 75.0% / 1.55 | 0.000 / 63.8% / 1.00 / +4.3 / 431 | no | regime: st_donchian_mid(n=100) |
| 44149 | A | 5 min | 0.605 / 78.0% / 1.53 | 0.408 / 72.4% / 1.30 / +9.8 / 344 | yes | regime: st_donchian_mid(n=100) |
| 43849 | A | 15 min | 0.575 / 74.6% / 1.60 | 0.246 / 65.4% / 1.07 / +2.4 / 381 | no | regime: st_both_vwap_side(); st_ichimoku_cloud(s=1) |
| 42672 | B | 5 min | 0.537 / 77.0% / 1.39 | 0.339 / 71.9% / 1.08 / +4.9 / 501 | yes | filter: f_session_range_developed(k=4.0); f_not_extended_from_vwap(k=3.0) |
| 37086 | B | 5 min | 0.534 / 76.9% / 1.34 | 0.382 / 73.1% / 1.12 / +6.7 / 468 | yes | filter: f_session_range_developed(k=4.0); f_not_extended_from_vwap(k=3.0) |
| 42402 | B | 5 min | 0.523 / 77.0% / 1.38 | 0.352 / 73.2% / 1.11 / +7.4 / 328 | yes | regime: st_donchian_mid(n=100) |
| 40946 | B | 5 min | 0.509 / 76.2% / 1.73 | 0.455 / 74.7% / 1.48 / +10.1 / 292 | yes | regime: st_wave_trend_side(band=5) |
| 41334 | B | 5 min | 0.508 / 75.7% / 1.54 | 0.456 / 75.6% / 1.31 / +10.6 / 349 | yes | regime: st_donchian_mid(n=100) |
| 43830 | B | 5 min | 0.494 / 75.4% / 1.37 | 0.286 / 70.5% / 1.05 / +3.7 / 332 | yes | regime: st_donchian_mid(n=100) |
| 41400 | B | 5 min | 0.486 / 75.0% / 1.34 | 0.358 / 71.6% / 1.13 / +5.0 / 764 | yes | filter: f_htf_agrees(k=6); f_skip_open(m=45) |
| 44562 | B | 5 min | 0.484 / 74.5% / 1.35 | 0.316 / 72.4% / 1.05 / +7.1 / 474 | yes | filter: f_inside_prior_day_range(); f_stop_before_close(m=30) |
| 33240 | B | 5 min | 0.478 / 74.8% / 1.38 | 0.526 / 77.4% / 1.40 / +13.4 / 328 | yes | regime: st_donchian_mid(n=100) |
| 43082 | B | 5 min | 0.473 / 74.5% / 1.43 | 0.527 / 77.5% / 1.43 / +13.0 / 324 | yes | regime: st_donchian_mid(n=100) |
