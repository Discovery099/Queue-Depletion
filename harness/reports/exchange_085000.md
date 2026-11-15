# Island exchange at generation 85000

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.696 at home, 0.433 away (retention 62%).
- Mean win rate: 77.4% at home, 71.1% away.
- Mean profit factor: 1.70 at home, 1.31 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 20 of 20; 0 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 84825 | A | 5 min | 0.757 / 75.7% / 1.78 | 0.430 / 67.9% / 1.39 / +14.2 / 361 | yes | regime: st_donchian_mid(n=100) |
| 84827 | A | 5 min | 0.755 / 75.8% / 1.79 | 0.416 / 68.2% / 1.36 / +14.1 / 365 | yes | regime: st_donchian_mid(n=100) |
| 84695 | A | 5 min | 0.744 / 75.1% / 1.78 | 0.418 / 68.0% / 1.37 / +14.5 / 369 | yes | regime: st_donchian_mid(n=100) |
| 79549 | A | 5 min | 0.742 / 75.4% / 1.73 | 0.424 / 67.9% / 1.34 / +14.1 / 386 | yes | regime: st_donchian_mid(n=100) |
| 54127 | A | 5 min | 0.705 / 73.3% / 1.70 | 0.371 / 65.5% / 1.23 / +15.4 / 409 | yes | regime: st_donchian_mid(n=100) |
| 78335 | A | 5 min | 0.673 / 72.3% / 1.69 | 0.367 / 64.9% / 1.23 / +17.4 / 387 | yes | regime: st_donchian_mid(n=100) |
| 46553 | A | 5 min | 0.629 / 78.6% / 1.61 | 0.441 / 73.2% / 1.36 / +10.2 / 314 | yes | regime: st_donchian_mid(n=100) |
| 77607 | A | 5 min | 0.628 / 78.0% / 1.58 | 0.391 / 72.2% / 1.31 / +8.0 / 349 | yes | regime: st_donchian_mid(n=100) |
| 83811 | A | 5 min | 0.620 / 72.7% / 1.63 | 0.447 / 68.3% / 1.39 / +14.2 / 438 | yes | regime: st_donchian_mid(n=100) |
| 47097 | A | 15 min | 0.619 / 74.5% / 1.71 | 0.317 / 66.1% / 1.30 / +4.2 / 454 | yes | regime: st_vwap_side(); st_ichimoku_cloud(s=1) |
| 80566 | B | 5 min | 0.766 / 80.6% / 1.86 | 0.451 / 74.0% / 1.24 / +7.0 / 480 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
| 75106 | B | 5 min | 0.743 / 81.0% / 1.83 | 0.545 / 76.3% / 1.51 / +9.3 / 363 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
| 78248 | B | 5 min | 0.735 / 80.0% / 1.78 | 0.465 / 74.2% / 1.30 / +7.5 / 504 | yes | regime: st_vwap_side() |
| 81204 | B | 5 min | 0.701 / 79.3% / 1.67 | 0.351 / 70.7% / 1.09 / +7.3 / 389 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 83610 | B | 5 min | 0.697 / 79.5% / 1.69 | 0.550 / 76.1% / 1.45 / +12.4 / 327 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80) |
| 78114 | B | 5 min | 0.691 / 79.2% / 1.65 | 0.410 / 72.5% / 1.16 / +9.5 / 363 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 72844 | B | 5 min | 0.690 / 80.1% / 1.69 | 0.561 / 77.0% / 1.52 / +11.6 / 356 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80) |
| 62402 | B | 5 min | 0.683 / 78.6% / 1.67 | 0.395 / 71.4% / 1.16 / +9.2 / 399 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 66920 | B | 5 min | 0.675 / 79.5% / 1.64 | 0.498 / 74.6% / 1.37 / +9.2 / 339 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
| 79334 | B | 5 min | 0.674 / 78.4% / 1.61 | 0.416 / 72.5% / 1.17 / +9.5 / 397 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
