# Island exchange at generation 90000

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.707 at home, 0.411 away (retention 58%).
- Mean win rate: 77.2% at home, 70.0% away.
- Mean profit factor: 1.72 at home, 1.26 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 17 of 20; 3 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 84825 | A | 5 min | 0.757 / 75.7% / 1.78 | 0.430 / 67.9% / 1.39 / +14.2 / 361 | yes | regime: st_donchian_mid(n=100) |
| 86829 | A | 5 min | 0.756 / 76.2% / 1.81 | 0.396 / 67.5% / 1.36 / +13.2 / 372 | yes | regime: st_donchian_mid(n=100) |
| 84695 | A | 5 min | 0.744 / 75.1% / 1.78 | 0.418 / 68.0% / 1.37 / +14.5 / 369 | yes | regime: st_donchian_mid(n=100) |
| 79549 | A | 5 min | 0.742 / 75.4% / 1.73 | 0.424 / 67.9% / 1.34 / +14.1 / 386 | yes | regime: st_donchian_mid(n=100) |
| 54127 | A | 5 min | 0.705 / 73.3% / 1.70 | 0.371 / 65.5% / 1.23 / +15.4 / 409 | yes | regime: st_donchian_mid(n=100) |
| 89579 | A | 5 min | 0.687 / 75.0% / 1.66 | 0.320 / 65.9% / 1.15 / +12.7 / 328 | no | regime: st_ichimoku_cloud(s=1) |
| 78335 | A | 5 min | 0.673 / 72.3% / 1.69 | 0.367 / 64.9% / 1.23 / +17.4 / 387 | yes | regime: st_donchian_mid(n=100) |
| 88515 | A | 5 min | 0.661 / 73.9% / 1.62 | 0.313 / 65.5% / 1.11 / +14.1 / 330 | no | regime: st_ichimoku_cloud(s=1) |
| 88747 | A | 5 min | 0.658 / 74.7% / 1.62 | 0.329 / 66.0% / 1.15 / +13.5 / 350 | yes | regime: st_ichimoku_cloud(s=1) |
| 89663 | A | 5 min | 0.657 / 72.6% / 1.65 | 0.295 / 63.9% / 1.10 / +13.8 / 421 | no | regime: st_donchian_mid(n=100) |
| 88594 | B | 5 min | 0.788 / 81.9% / 2.02 | 0.416 / 73.6% / 1.22 / +6.7 / 435 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80); f_noise_ratio_ok(n=5, thr=40) |
| 89092 | B | 5 min | 0.757 / 82.6% / 1.98 | 0.502 / 75.3% / 1.42 / +8.6 / 336 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80); f_noise_ratio_ok(n=5, thr=40) |
| 78248 | B | 5 min | 0.735 / 80.0% / 1.78 | 0.465 / 74.2% / 1.30 / +7.5 / 504 | yes | regime: st_vwap_side() |
| 85308 | B | 5 min | 0.705 / 79.5% / 1.71 | 0.547 / 75.8% / 1.44 / +12.4 / 330 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80) |
| 81204 | B | 5 min | 0.701 / 79.3% / 1.67 | 0.351 / 70.7% / 1.09 / +7.3 / 389 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 78114 | B | 5 min | 0.691 / 79.2% / 1.65 | 0.410 / 72.5% / 1.16 / +9.5 / 363 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 72844 | B | 5 min | 0.690 / 80.1% / 1.69 | 0.561 / 77.0% / 1.52 / +11.6 / 356 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80) |
| 62402 | B | 5 min | 0.683 / 78.6% / 1.67 | 0.395 / 71.4% / 1.16 / +9.2 / 399 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 66920 | B | 5 min | 0.675 / 79.5% / 1.64 | 0.498 / 74.6% / 1.37 / +9.2 / 339 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
| 79334 | B | 5 min | 0.674 / 78.4% / 1.61 | 0.416 / 72.5% / 1.17 / +9.5 / 397 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
