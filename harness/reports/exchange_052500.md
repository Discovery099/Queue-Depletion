# Island exchange at generation 52500

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.606 at home, 0.390 away (retention 64%).
- Mean win rate: 75.6% at home, 69.9% away.
- Mean profit factor: 1.56 at home, 1.25 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 20 of 20; 0 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 47013 | A | 5 min | 0.734 / 75.3% / 1.77 | 0.451 / 68.0% / 1.42 / +14.0 / 372 | yes | regime: st_donchian_mid(n=100) |
| 52413 | A | 5 min | 0.717 / 74.1% / 1.74 | 0.369 / 65.7% / 1.27 / +13.1 / 408 | yes | regime: st_donchian_mid(n=100) |
| 51909 | A | 5 min | 0.712 / 73.8% / 1.72 | 0.398 / 66.5% / 1.40 / +12.5 / 418 | yes | regime: st_donchian_mid(n=100) |
| 50503 | A | 5 min | 0.692 / 73.5% / 1.69 | 0.412 / 66.7% / 1.42 / +12.8 / 421 | yes | regime: st_donchian_mid(n=100) |
| 47649 | A | 5 min | 0.682 / 72.8% / 1.64 | 0.383 / 65.9% / 1.25 / +15.7 / 413 | yes | regime: st_donchian_mid(n=100) |
| 46553 | A | 5 min | 0.629 / 78.6% / 1.61 | 0.441 / 73.2% / 1.36 / +10.2 / 314 | yes | regime: st_donchian_mid(n=100) |
| 52189 | A | 5 min | 0.628 / 71.5% / 1.60 | 0.322 / 64.5% / 1.16 / +15.7 / 422 | yes | regime: st_donchian_mid(n=100) |
| 51943 | A | 5 min | 0.621 / 72.1% / 1.62 | 0.384 / 66.0% / 1.38 / +13.3 / 438 | yes | regime: st_donchian_mid(n=100) |
| 47097 | A | 15 min | 0.619 / 74.5% / 1.71 | 0.317 / 66.1% / 1.30 / +4.2 / 454 | yes | regime: st_vwap_side(); st_ichimoku_cloud(s=1) |
| 49267 | A | 5 min | 0.614 / 78.5% / 1.61 | 0.414 / 71.8% / 1.33 / +9.2 / 330 | yes | regime: st_donchian_mid(n=100) |
| 52420 | B | 5 min | 0.602 / 78.2% / 1.59 | 0.438 / 73.2% / 1.25 / +6.0 / 411 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 48034 | B | 5 min | 0.574 / 78.4% / 1.69 | 0.306 / 70.0% / 1.15 / +5.5 / 297 | yes | regime: st_market_tide(band=10) |
| 52434 | B | 5 min | 0.572 / 76.6% / 1.46 | 0.419 / 71.9% / 1.17 / +9.0 / 467 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 52308 | B | 5 min | 0.571 / 76.7% / 1.54 | 0.465 / 73.0% / 1.28 / +9.6 / 433 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 52378 | B | 5 min | 0.545 / 76.5% / 1.47 | 0.494 / 73.9% / 1.28 / +11.5 / 429 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 48736 | B | 5 min | 0.543 / 76.5% / 1.39 | 0.343 / 71.2% / 1.09 / +5.6 / 510 | yes | filter: f_session_range_developed(k=4.0); f_not_extended_from_vwap(k=3.0) |
| 37086 | B | 5 min | 0.534 / 76.9% / 1.34 | 0.382 / 73.1% / 1.12 / +6.7 / 468 | yes | filter: f_session_range_developed(k=4.0); f_not_extended_from_vwap(k=3.0) |
| 42402 | B | 5 min | 0.523 / 77.0% / 1.38 | 0.352 / 73.2% / 1.11 / +7.4 / 328 | yes | regime: st_donchian_mid(n=100) |
| 48466 | B | 5 min | 0.506 / 76.1% / 1.33 | 0.355 / 72.7% / 1.11 / +6.0 / 487 | yes | filter: f_session_range_developed(k=4.0); f_not_extended_from_vwap(k=3.0) |
| 45102 | B | 5 min | 0.499 / 75.2% / 1.38 | 0.351 / 72.0% / 1.13 / +6.2 / 600 | yes | regime: st_donchian_mid(n=100) |
