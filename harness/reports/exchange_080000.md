# Island exchange at generation 80000

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.703 at home, 0.425 away (retention 60%).
- Mean win rate: 77.1% at home, 70.4% away.
- Mean profit factor: 1.71 at home, 1.30 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 18 of 20; 2 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 79795 | A | 5 min | 0.758 / 75.3% / 1.85 | 0.335 / 65.3% / 1.22 / +11.2 / 366 | no | regime: st_donchian_mid(n=100) |
| 79549 | A | 5 min | 0.742 / 75.4% / 1.73 | 0.424 / 67.9% / 1.34 / +14.1 / 386 | yes | regime: st_donchian_mid(n=100) |
| 47013 | A | 5 min | 0.734 / 75.3% / 1.77 | 0.451 / 68.0% / 1.42 / +14.0 / 372 | yes | regime: st_donchian_mid(n=100) |
| 56425 | A | 5 min | 0.729 / 74.3% / 1.76 | 0.387 / 66.5% / 1.36 / +11.8 / 409 | yes | regime: st_donchian_mid(n=100) |
| 76145 | A | 5 min | 0.727 / 74.3% / 1.75 | 0.385 / 66.3% / 1.34 / +13.1 / 407 | yes | regime: st_donchian_mid(n=100) |
| 54127 | A | 5 min | 0.705 / 73.3% / 1.70 | 0.371 / 65.5% / 1.23 / +15.4 / 409 | yes | regime: st_donchian_mid(n=100) |
| 78335 | A | 5 min | 0.673 / 72.3% / 1.69 | 0.367 / 64.9% / 1.23 / +17.4 / 387 | yes | regime: st_donchian_mid(n=100) |
| 78035 | A | 5 min | 0.658 / 74.5% / 1.62 | 0.390 / 67.1% / 1.27 / +14.5 / 362 | yes | regime: st_ichimoku_cloud(s=1) |
| 79831 | A | 5 min | 0.650 / 73.2% / 1.61 | 0.283 / 63.1% / 1.12 / +10.5 / 388 | no | regime: st_donchian_mid(n=100) |
| 46553 | A | 5 min | 0.629 / 78.6% / 1.61 | 0.441 / 73.2% / 1.36 / +10.2 / 314 | yes | regime: st_donchian_mid(n=100) |
| 73770 | B | 5 min | 0.765 / 80.4% / 1.83 | 0.458 / 74.2% / 1.27 / +7.0 / 484 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
| 75106 | B | 5 min | 0.743 / 81.0% / 1.83 | 0.545 / 76.3% / 1.51 / +9.3 / 363 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
| 78248 | B | 5 min | 0.735 / 80.0% / 1.78 | 0.465 / 74.2% / 1.30 / +7.5 / 504 | yes | regime: st_vwap_side() |
| 63398 | B | 5 min | 0.698 / 79.4% / 1.67 | 0.354 / 71.2% / 1.10 / +5.1 / 386 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 78114 | B | 5 min | 0.691 / 79.2% / 1.65 | 0.410 / 72.5% / 1.16 / +9.5 / 363 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 68278 | B | 5 min | 0.690 / 79.1% / 1.65 | 0.565 / 76.4% / 1.47 / +12.3 / 330 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80) |
| 72844 | B | 5 min | 0.690 / 80.1% / 1.69 | 0.561 / 77.0% / 1.52 / +11.6 / 356 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80) |
| 62402 | B | 5 min | 0.683 / 78.6% / 1.67 | 0.395 / 71.4% / 1.16 / +9.2 / 399 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 66920 | B | 5 min | 0.675 / 79.5% / 1.64 | 0.498 / 74.6% / 1.37 / +9.2 / 339 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
| 79334 | B | 5 min | 0.674 / 78.4% / 1.61 | 0.416 / 72.5% / 1.17 / +9.5 / 397 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
