# Island exchange at generation 65000

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.677 at home, 0.429 away (retention 63%).
- Mean win rate: 76.7% at home, 70.4% away.
- Mean profit factor: 1.67 at home, 1.31 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 20 of 20; 0 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 47013 | A | 5 min | 0.734 / 75.3% / 1.77 | 0.451 / 68.0% / 1.42 / +14.0 / 372 | yes | regime: st_donchian_mid(n=100) |
| 56425 | A | 5 min | 0.729 / 74.3% / 1.76 | 0.387 / 66.5% / 1.36 / +11.8 / 409 | yes | regime: st_donchian_mid(n=100) |
| 57709 | A | 5 min | 0.727 / 75.5% / 1.77 | 0.431 / 67.5% / 1.41 / +13.6 / 385 | yes | regime: st_donchian_mid(n=100) |
| 62957 | A | 5 min | 0.719 / 74.2% / 1.74 | 0.366 / 65.6% / 1.27 / +12.9 / 407 | yes | regime: st_donchian_mid(n=100) |
| 54127 | A | 5 min | 0.705 / 73.3% / 1.70 | 0.371 / 65.5% / 1.23 / +15.4 / 409 | yes | regime: st_donchian_mid(n=100) |
| 64139 | A | 5 min | 0.699 / 73.7% / 1.70 | 0.366 / 65.8% / 1.33 / +11.7 / 415 | yes | regime: st_donchian_mid(n=100) |
| 63377 | A | 5 min | 0.665 / 72.5% / 1.68 | 0.362 / 64.9% / 1.23 / +15.6 / 388 | yes | regime: st_donchian_mid(n=100) |
| 64739 | A | 5 min | 0.642 / 74.3% / 1.61 | 0.394 / 67.5% / 1.29 / +13.4 / 357 | yes | regime: st_ichimoku_cloud(s=1) |
| 46553 | A | 5 min | 0.629 / 78.6% / 1.61 | 0.441 / 73.2% / 1.36 / +10.2 / 314 | yes | regime: st_donchian_mid(n=100) |
| 47097 | A | 15 min | 0.619 / 74.5% / 1.71 | 0.317 / 66.1% / 1.30 / +4.2 / 454 | yes | regime: st_vwap_side(); st_ichimoku_cloud(s=1) |
| 63398 | B | 5 min | 0.698 / 79.4% / 1.67 | 0.354 / 71.2% / 1.10 / +5.1 / 386 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 62036 | B | 5 min | 0.689 / 79.1% / 1.67 | 0.556 / 76.0% / 1.46 / +12.5 / 333 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80) |
| 61032 | B | 5 min | 0.689 / 79.6% / 1.68 | 0.543 / 76.5% / 1.53 / +11.3 / 366 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
| 62402 | B | 5 min | 0.683 / 78.6% / 1.67 | 0.395 / 71.4% / 1.16 / +9.2 / 399 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 57412 | B | 5 min | 0.679 / 79.2% / 1.64 | 0.398 / 72.3% / 1.15 / +8.2 / 365 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 63408 | B | 5 min | 0.672 / 78.2% / 1.60 | 0.427 / 72.6% / 1.17 / +10.8 / 398 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 61950 | B | 5 min | 0.663 / 79.7% / 1.64 | 0.556 / 75.8% / 1.45 / +10.2 / 335 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
| 64446 | B | 5 min | 0.657 / 78.2% / 1.57 | 0.418 / 72.6% / 1.21 / +8.8 / 340 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80) |
| 64588 | B | 5 min | 0.622 / 78.5% / 1.65 | 0.509 / 74.6% / 1.36 / +10.7 / 303 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
| 60898 | B | 5 min | 0.622 / 77.9% / 1.54 | 0.532 / 74.7% / 1.35 / +11.1 / 430 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
