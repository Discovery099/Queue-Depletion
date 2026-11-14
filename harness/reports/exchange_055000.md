# Island exchange at generation 55000

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.626 at home, 0.394 away (retention 63%).
- Mean win rate: 75.9% at home, 69.7% away.
- Mean profit factor: 1.59 at home, 1.24 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 17 of 20; 3 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 53323 | A | 5 min | 0.761 / 75.2% / 1.85 | 0.302 / 64.2% / 1.17 / +11.2 / 363 | no | regime: st_donchian_mid(n=100) |
| 54251 | A | 5 min | 0.736 / 74.7% / 1.80 | 0.352 / 65.2% / 1.26 / +12.8 / 385 | no | regime: st_donchian_mid(n=100) |
| 47013 | A | 5 min | 0.734 / 75.3% / 1.77 | 0.451 / 68.0% / 1.42 / +14.0 / 372 | yes | regime: st_donchian_mid(n=100) |
| 52413 | A | 5 min | 0.717 / 74.1% / 1.74 | 0.369 / 65.7% / 1.27 / +13.1 / 408 | yes | regime: st_donchian_mid(n=100) |
| 54127 | A | 5 min | 0.705 / 73.3% / 1.70 | 0.371 / 65.5% / 1.23 / +15.4 / 409 | yes | regime: st_donchian_mid(n=100) |
| 50503 | A | 5 min | 0.692 / 73.5% / 1.69 | 0.412 / 66.7% / 1.42 / +12.8 / 421 | yes | regime: st_donchian_mid(n=100) |
| 54777 | A | 5 min | 0.645 / 75.9% / 1.61 | 0.228 / 64.0% / 1.04 / +4.1 / 425 | no | regime: st_donchian_mid(n=100) |
| 46553 | A | 5 min | 0.629 / 78.6% / 1.61 | 0.441 / 73.2% / 1.36 / +10.2 / 314 | yes | regime: st_donchian_mid(n=100) |
| 52189 | A | 5 min | 0.628 / 71.5% / 1.60 | 0.322 / 64.5% / 1.16 / +15.7 / 422 | yes | regime: st_donchian_mid(n=100) |
| 47097 | A | 15 min | 0.619 / 74.5% / 1.71 | 0.317 / 66.1% / 1.30 / +4.2 / 454 | yes | regime: st_vwap_side(); st_ichimoku_cloud(s=1) |
| 52964 | B | 5 min | 0.628 / 77.6% / 1.52 | 0.431 / 72.8% / 1.22 / +9.0 / 342 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80) |
| 54166 | B | 5 min | 0.616 / 78.4% / 1.59 | 0.429 / 72.8% / 1.23 / +5.5 / 416 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 53224 | B | 5 min | 0.605 / 78.4% / 1.58 | 0.506 / 74.4% / 1.30 / +10.7 / 387 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 53200 | B | 5 min | 0.587 / 76.8% / 1.55 | 0.461 / 72.8% / 1.26 / +9.7 / 430 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 52378 | B | 5 min | 0.545 / 76.5% / 1.47 | 0.494 / 73.9% / 1.28 / +11.5 / 429 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 54778 | B | 5 min | 0.543 / 76.8% / 1.45 | 0.464 / 73.9% / 1.31 / +9.0 / 459 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 48736 | B | 5 min | 0.543 / 76.5% / 1.39 | 0.343 / 71.2% / 1.09 / +5.6 / 510 | yes | filter: f_session_range_developed(k=4.0); f_not_extended_from_vwap(k=3.0) |
| 37086 | B | 5 min | 0.534 / 76.9% / 1.34 | 0.382 / 73.1% / 1.12 / +6.7 / 468 | yes | filter: f_session_range_developed(k=4.0); f_not_extended_from_vwap(k=3.0) |
| 42402 | B | 5 min | 0.523 / 77.0% / 1.38 | 0.352 / 73.2% / 1.11 / +7.4 / 328 | yes | regime: st_donchian_mid(n=100) |
| 54756 | B | 5 min | 0.522 / 76.5% / 1.38 | 0.449 / 72.9% / 1.23 / +8.7 / 628 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
