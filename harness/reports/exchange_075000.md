# Island exchange at generation 75000

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.690 at home, 0.424 away (retention 61%).
- Mean win rate: 76.7% at home, 70.2% away.
- Mean profit factor: 1.69 at home, 1.30 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 19 of 20; 1 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 47013 | A | 5 min | 0.734 / 75.3% / 1.77 | 0.451 / 68.0% / 1.42 / +14.0 / 372 | yes | regime: st_donchian_mid(n=100) |
| 56425 | A | 5 min | 0.729 / 74.3% / 1.76 | 0.387 / 66.5% / 1.36 / +11.8 / 409 | yes | regime: st_donchian_mid(n=100) |
| 57709 | A | 5 min | 0.727 / 75.5% / 1.77 | 0.431 / 67.5% / 1.41 / +13.6 / 385 | yes | regime: st_donchian_mid(n=100) |
| 54127 | A | 5 min | 0.705 / 73.3% / 1.70 | 0.371 / 65.5% / 1.23 / +15.4 / 409 | yes | regime: st_donchian_mid(n=100) |
| 73083 | A | 5 min | 0.703 / 74.1% / 1.74 | 0.363 / 65.7% / 1.27 / +12.0 / 408 | yes | regime: st_donchian_mid(n=100) |
| 69351 | A | 5 min | 0.673 / 72.6% / 1.68 | 0.357 / 64.9% / 1.23 / +14.8 / 387 | yes | regime: st_donchian_mid(n=100) |
| 73395 | A | 5 min | 0.671 / 73.4% / 1.69 | 0.361 / 65.5% / 1.32 / +11.8 / 432 | yes | regime: st_donchian_mid(n=100) |
| 73309 | A | 5 min | 0.653 / 72.6% / 1.63 | 0.320 / 64.7% / 1.12 / +15.8 / 380 | no | regime: st_donchian_mid(n=100) |
| 67443 | A | 5 min | 0.648 / 74.2% / 1.60 | 0.396 / 67.4% / 1.28 / +14.1 / 359 | yes | regime: st_ichimoku_cloud(s=1) |
| 47097 | A | 15 min | 0.619 / 74.5% / 1.71 | 0.317 / 66.1% / 1.30 / +4.2 / 454 | yes | regime: st_vwap_side(); st_ichimoku_cloud(s=1) |
| 73770 | B | 5 min | 0.765 / 80.4% / 1.83 | 0.458 / 74.2% / 1.27 / +7.0 / 484 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
| 74526 | B | 5 min | 0.730 / 80.7% / 1.75 | 0.509 / 76.1% / 1.48 / +8.3 / 352 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
| 63398 | B | 5 min | 0.698 / 79.4% / 1.67 | 0.354 / 71.2% / 1.10 / +5.1 / 386 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 68278 | B | 5 min | 0.690 / 79.1% / 1.65 | 0.565 / 76.4% / 1.47 / +12.3 / 330 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80) |
| 72844 | B | 5 min | 0.690 / 80.1% / 1.69 | 0.561 / 77.0% / 1.52 / +11.6 / 356 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80) |
| 62402 | B | 5 min | 0.683 / 78.6% / 1.67 | 0.395 / 71.4% / 1.16 / +9.2 / 399 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 57412 | B | 5 min | 0.679 / 79.2% / 1.64 | 0.398 / 72.3% / 1.15 / +8.2 / 365 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 66920 | B | 5 min | 0.675 / 79.5% / 1.64 | 0.498 / 74.6% / 1.37 / +9.2 / 339 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
| 63408 | B | 5 min | 0.672 / 78.2% / 1.60 | 0.427 / 72.6% / 1.17 / +10.8 / 398 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 61950 | B | 5 min | 0.663 / 79.7% / 1.64 | 0.556 / 75.8% / 1.45 / +10.2 / 335 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
