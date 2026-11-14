# Island exchange at generation 62500

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.671 at home, 0.408 away (retention 61%).
- Mean win rate: 76.9% at home, 70.4% away.
- Mean profit factor: 1.66 at home, 1.29 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 17 of 20; 3 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 47013 | A | 5 min | 0.734 / 75.3% / 1.77 | 0.451 / 68.0% / 1.42 / +14.0 / 372 | yes | regime: st_donchian_mid(n=100) |
| 56425 | A | 5 min | 0.729 / 74.3% / 1.76 | 0.387 / 66.5% / 1.36 / +11.8 / 409 | yes | regime: st_donchian_mid(n=100) |
| 57709 | A | 5 min | 0.727 / 75.5% / 1.77 | 0.431 / 67.5% / 1.41 / +13.6 / 385 | yes | regime: st_donchian_mid(n=100) |
| 52413 | A | 5 min | 0.717 / 74.1% / 1.74 | 0.369 / 65.7% / 1.27 / +13.1 / 408 | yes | regime: st_donchian_mid(n=100) |
| 61909 | A | 5 min | 0.709 / 73.5% / 1.71 | 0.329 / 64.2% / 1.18 / +13.5 / 383 | no | regime: st_donchian_mid(n=100) |
| 54127 | A | 5 min | 0.705 / 73.3% / 1.70 | 0.371 / 65.5% / 1.23 / +15.4 / 409 | yes | regime: st_donchian_mid(n=100) |
| 62303 | A | 5 min | 0.661 / 76.5% / 1.69 | 0.000 / 67.4% / 0.91 / +1.7 / 276 | no | regime: st_gap_direction(g=0.002) |
| 61493 | A | 15 min | 0.631 / 75.3% / 1.78 | 0.257 / 63.9% / 1.21 / +2.5 / 415 | no | regime: st_vwap_side(); st_ichimoku_cloud(s=1) |
| 60021 | A | 5 min | 0.629 / 73.9% / 1.61 | 0.404 / 67.4% / 1.29 / +15.0 / 371 | yes | regime: st_ichimoku_cloud(s=1) |
| 46553 | A | 5 min | 0.629 / 78.6% / 1.61 | 0.441 / 73.2% / 1.36 / +10.2 / 314 | yes | regime: st_donchian_mid(n=100) |
| 62036 | B | 5 min | 0.689 / 79.1% / 1.67 | 0.556 / 76.0% / 1.46 / +12.5 / 333 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80) |
| 61032 | B | 5 min | 0.689 / 79.6% / 1.68 | 0.543 / 76.5% / 1.53 / +11.3 / 366 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
| 62402 | B | 5 min | 0.683 / 78.6% / 1.67 | 0.395 / 71.4% / 1.16 / +9.2 / 399 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 57412 | B | 5 min | 0.679 / 79.2% / 1.64 | 0.398 / 72.3% / 1.15 / +8.2 / 365 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 61950 | B | 5 min | 0.663 / 79.7% / 1.64 | 0.556 / 75.8% / 1.45 / +10.2 / 335 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
| 59610 | B | 5 min | 0.662 / 78.9% / 1.63 | 0.338 / 70.9% / 1.10 / +4.5 / 364 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 55510 | B | 5 min | 0.643 / 77.8% / 1.53 | 0.437 / 72.8% / 1.22 / +10.0 / 342 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80) |
| 60898 | B | 5 min | 0.622 / 77.9% / 1.54 | 0.532 / 74.7% / 1.35 / +11.1 / 430 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
| 60770 | B | 5 min | 0.609 / 78.7% / 1.55 | 0.444 / 73.8% / 1.31 / +6.5 / 439 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 62426 | B | 5 min | 0.605 / 77.9% / 1.48 | 0.526 / 74.9% / 1.37 / +10.1 / 470 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
