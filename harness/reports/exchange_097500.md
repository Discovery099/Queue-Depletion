# Island exchange at generation 97500

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.713 at home, 0.411 away (retention 58%).
- Mean win rate: 77.3% at home, 70.0% away.
- Mean profit factor: 1.75 at home, 1.28 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 18 of 20; 2 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 92947 | A | 5 min | 0.758 / 75.9% / 1.81 | 0.409 / 67.9% / 1.36 / +13.8 / 361 | yes | regime: st_donchian_mid(n=100) |
| 84825 | A | 5 min | 0.757 / 75.7% / 1.78 | 0.430 / 67.9% / 1.39 / +14.2 / 361 | yes | regime: st_donchian_mid(n=100) |
| 86829 | A | 5 min | 0.756 / 76.2% / 1.81 | 0.396 / 67.5% / 1.36 / +13.2 / 372 | yes | regime: st_donchian_mid(n=100) |
| 79549 | A | 5 min | 0.742 / 75.4% / 1.73 | 0.424 / 67.9% / 1.34 / +14.1 / 386 | yes | regime: st_donchian_mid(n=100) |
| 95797 | A | 5 min | 0.728 / 74.0% / 1.75 | 0.355 / 64.9% / 1.21 / +14.9 / 385 | no | regime: st_donchian_mid(n=100) |
| 54127 | A | 5 min | 0.705 / 73.3% / 1.70 | 0.371 / 65.5% / 1.23 / +15.4 / 409 | yes | regime: st_donchian_mid(n=100) |
| 78335 | A | 5 min | 0.673 / 72.3% / 1.69 | 0.367 / 64.9% / 1.23 / +17.4 / 387 | yes | regime: st_donchian_mid(n=100) |
| 94495 | A | 5 min | 0.658 / 71.0% / 1.77 | 0.358 / 62.5% / 1.24 / +23.5 / 392 | yes | regime: st_donchian_mid(n=100) |
| 94161 | A | 5 min | 0.656 / 75.2% / 1.59 | 0.402 / 68.5% / 1.29 / +13.8 / 321 | yes | regime: st_ichimoku_cloud(s=1) |
| 92223 | A | 5 min | 0.653 / 73.5% / 1.59 | 0.337 / 65.8% / 1.13 / +15.4 / 342 | yes | regime: st_ichimoku_cloud(s=1) |
| 88594 | B | 5 min | 0.788 / 81.9% / 2.02 | 0.416 / 73.6% / 1.22 / +6.7 / 435 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80); f_noise_ratio_ok(n=5, thr=40) |
| 89092 | B | 5 min | 0.757 / 82.6% / 1.98 | 0.502 / 75.3% / 1.42 / +8.6 / 336 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80); f_noise_ratio_ok(n=5, thr=40) |
| 93086 | B | 5 min | 0.749 / 80.4% / 1.81 | 0.419 / 73.5% / 1.25 / +6.4 / 517 | yes | regime: st_vwap_side() |
| 95022 | B | 5 min | 0.719 / 81.1% / 1.82 | 0.388 / 73.5% / 1.27 / +6.1 / 351 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80); f_noise_ratio_ok(n=3, thr=40) |
| 96980 | B | 5 min | 0.707 / 79.3% / 1.67 | 0.349 / 70.7% / 1.09 / +6.6 / 386 | no | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 85308 | B | 5 min | 0.705 / 79.5% / 1.71 | 0.547 / 75.8% / 1.44 / +12.4 / 330 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80) |
| 78114 | B | 5 min | 0.691 / 79.2% / 1.65 | 0.410 / 72.5% / 1.16 / +9.5 / 363 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 72844 | B | 5 min | 0.690 / 80.1% / 1.69 | 0.561 / 77.0% / 1.52 / +11.6 / 356 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80) |
| 97324 | B | 5 min | 0.689 / 79.9% / 1.71 | 0.384 / 72.6% / 1.21 / +5.2 / 347 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80); f_noise_ratio_ok(n=5, thr=40) |
| 62402 | B | 5 min | 0.683 / 78.6% / 1.67 | 0.395 / 71.4% / 1.16 / +9.2 / 399 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
