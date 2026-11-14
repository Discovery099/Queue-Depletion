# Island exchange at generation 60000

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.654 at home, 0.411 away (retention 63%).
- Mean win rate: 76.5% at home, 70.0% away.
- Mean profit factor: 1.64 at home, 1.27 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 18 of 20; 2 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 47013 | A | 5 min | 0.734 / 75.3% / 1.77 | 0.451 / 68.0% / 1.42 / +14.0 / 372 | yes | regime: st_donchian_mid(n=100) |
| 56425 | A | 5 min | 0.729 / 74.3% / 1.76 | 0.387 / 66.5% / 1.36 / +11.8 / 409 | yes | regime: st_donchian_mid(n=100) |
| 57709 | A | 5 min | 0.727 / 75.5% / 1.77 | 0.431 / 67.5% / 1.41 / +13.6 / 385 | yes | regime: st_donchian_mid(n=100) |
| 52413 | A | 5 min | 0.717 / 74.1% / 1.74 | 0.369 / 65.7% / 1.27 / +13.1 / 408 | yes | regime: st_donchian_mid(n=100) |
| 54127 | A | 5 min | 0.705 / 73.3% / 1.70 | 0.371 / 65.5% / 1.23 / +15.4 / 409 | yes | regime: st_donchian_mid(n=100) |
| 58669 | A | 5 min | 0.643 / 72.1% / 1.64 | 0.306 / 64.3% / 1.11 / +14.2 / 417 | no | regime: st_donchian_mid(n=100) |
| 58575 | A | 5 min | 0.630 / 72.1% / 1.59 | 0.293 / 63.1% / 1.10 / +14.9 / 442 | no | regime: st_donchian_mid(n=100) |
| 46553 | A | 5 min | 0.629 / 78.6% / 1.61 | 0.441 / 73.2% / 1.36 / +10.2 / 314 | yes | regime: st_donchian_mid(n=100) |
| 59673 | A | 5 min | 0.620 / 74.7% / 1.58 | 0.411 / 68.5% / 1.30 / +14.8 / 327 | yes | regime: st_ichimoku_cloud(s=1) |
| 47097 | A | 15 min | 0.619 / 74.5% / 1.71 | 0.317 / 66.1% / 1.30 / +4.2 / 454 | yes | regime: st_vwap_side(); st_ichimoku_cloud(s=1) |
| 57412 | B | 5 min | 0.679 / 79.2% / 1.64 | 0.398 / 72.3% / 1.15 / +8.2 / 365 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 58850 | B | 5 min | 0.679 / 78.8% / 1.67 | 0.404 / 71.7% / 1.17 / +10.1 / 396 | yes | regime: st_trail_regime(f=2.5, n=14) |
| 59610 | B | 5 min | 0.662 / 78.9% / 1.63 | 0.338 / 70.9% / 1.10 / +4.5 / 364 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 57094 | B | 5 min | 0.655 / 79.1% / 1.63 | 0.484 / 74.7% / 1.35 / +10.2 / 474 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 55510 | B | 5 min | 0.643 / 77.8% / 1.53 | 0.437 / 72.8% / 1.22 / +10.0 / 342 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80) |
| 59506 | B | 5 min | 0.631 / 79.1% / 1.59 | 0.480 / 73.9% / 1.29 / +8.6 / 445 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 58744 | B | 5 min | 0.606 / 78.8% / 1.56 | 0.442 / 73.8% / 1.31 / +6.5 / 442 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 58482 | B | 5 min | 0.606 / 78.1% / 1.52 | 0.450 / 73.6% / 1.21 / +10.5 / 409 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 58662 | B | 5 min | 0.597 / 77.7% / 1.51 | 0.528 / 74.7% / 1.35 / +10.4 / 434 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
| 57178 | B | 5 min | 0.577 / 77.9% / 1.56 | 0.486 / 74.1% / 1.37 / +9.6 / 437 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
