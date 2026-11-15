# Island exchange at generation 100000

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.716 at home, 0.404 away (retention 56%).
- Mean win rate: 77.1% at home, 69.6% away.
- Mean profit factor: 1.77 at home, 1.27 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 18 of 20; 2 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 92947 | A | 5 min | 0.758 / 75.9% / 1.81 | 0.409 / 67.9% / 1.36 / +13.8 / 361 | yes | regime: st_donchian_mid(n=100) |
| 84825 | A | 5 min | 0.757 / 75.7% / 1.78 | 0.430 / 67.9% / 1.39 / +14.2 / 361 | yes | regime: st_donchian_mid(n=100) |
| 86829 | A | 5 min | 0.756 / 76.2% / 1.81 | 0.396 / 67.5% / 1.36 / +13.2 / 372 | yes | regime: st_donchian_mid(n=100) |
| 79549 | A | 5 min | 0.742 / 75.4% / 1.73 | 0.424 / 67.9% / 1.34 / +14.1 / 386 | yes | regime: st_donchian_mid(n=100) |
| 99589 | A | 5 min | 0.736 / 74.1% / 1.77 | 0.340 / 65.1% / 1.18 / +14.8 / 367 | no | regime: st_donchian_mid(n=100) |
| 54127 | A | 5 min | 0.705 / 73.3% / 1.70 | 0.371 / 65.5% / 1.23 / +15.4 / 409 | yes | regime: st_donchian_mid(n=100) |
| 98335 | A | 5 min | 0.685 / 75.1% / 1.67 | 0.316 / 65.6% / 1.14 / +12.8 / 331 | no | regime: st_ichimoku_cloud(s=1) |
| 99929 | A | 5 min | 0.677 / 71.3% / 1.80 | 0.348 / 62.8% / 1.22 / +22.7 / 374 | yes | regime: st_donchian_mid(n=100) |
| 78335 | A | 5 min | 0.673 / 72.3% / 1.69 | 0.367 / 64.9% / 1.23 / +17.4 / 387 | yes | regime: st_donchian_mid(n=100) |
| 98245 | A | 5 min | 0.657 / 70.8% / 1.76 | 0.359 / 62.5% / 1.25 / +23.2 / 384 | yes | regime: st_donchian_mid(n=100) |
| 88594 | B | 5 min | 0.788 / 81.9% / 2.02 | 0.416 / 73.6% / 1.22 / +6.7 / 435 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80); f_noise_ratio_ok(n=5, thr=40) |
| 89092 | B | 5 min | 0.757 / 82.6% / 1.98 | 0.502 / 75.3% / 1.42 / +8.6 / 336 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80); f_noise_ratio_ok(n=5, thr=40) |
| 93086 | B | 5 min | 0.749 / 80.4% / 1.81 | 0.419 / 73.5% / 1.25 / +6.4 / 517 | yes | regime: st_vwap_side() |
| 99272 | B | 5 min | 0.728 / 80.5% / 1.88 | 0.375 / 72.9% / 1.25 / +7.2 / 351 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80); f_noise_ratio_ok(n=3, thr=40) |
| 85308 | B | 5 min | 0.705 / 79.5% / 1.71 | 0.547 / 75.8% / 1.44 / +12.4 / 330 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80) |
| 98022 | B | 5 min | 0.697 / 80.5% / 1.74 | 0.498 / 76.1% / 1.49 / +10.4 / 335 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80); f_noise_ratio_ok(n=5, thr=40) |
| 78114 | B | 5 min | 0.691 / 79.2% / 1.65 | 0.410 / 72.5% / 1.16 / +9.5 / 363 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 97724 | B | 5 min | 0.691 / 79.5% / 1.70 | 0.400 / 72.8% / 1.21 / +7.3 / 349 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80); f_noise_ratio_ok(n=5, thr=40) |
| 62402 | B | 5 min | 0.683 / 78.6% / 1.67 | 0.395 / 71.4% / 1.16 / +9.2 / 399 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 99106 | B | 5 min | 0.680 / 79.0% / 1.77 | 0.363 / 71.6% / 1.11 / +8.3 / 352 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70); f_signal_bar_not_huge(k=2.0) |
