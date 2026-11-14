# Island exchange at generation 57500

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.639 at home, 0.411 away (retention 64%).
- Mean win rate: 76.7% at home, 70.8% away.
- Mean profit factor: 1.63 at home, 1.28 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 19 of 20; 1 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 47013 | A | 5 min | 0.734 / 75.3% / 1.77 | 0.451 / 68.0% / 1.42 / +14.0 / 372 | yes | regime: st_donchian_mid(n=100) |
| 56425 | A | 5 min | 0.729 / 74.3% / 1.76 | 0.387 / 66.5% / 1.36 / +11.8 / 409 | yes | regime: st_donchian_mid(n=100) |
| 52413 | A | 5 min | 0.717 / 74.1% / 1.74 | 0.369 / 65.7% / 1.27 / +13.1 / 408 | yes | regime: st_donchian_mid(n=100) |
| 51909 | A | 5 min | 0.712 / 73.8% / 1.72 | 0.398 / 66.5% / 1.40 / +12.5 / 418 | yes | regime: st_donchian_mid(n=100) |
| 54127 | A | 5 min | 0.705 / 73.3% / 1.70 | 0.371 / 65.5% / 1.23 / +15.4 / 409 | yes | regime: st_donchian_mid(n=100) |
| 55323 | A | 5 min | 0.631 / 78.7% / 1.62 | 0.433 / 73.1% / 1.35 / +9.4 / 316 | yes | regime: st_donchian_mid(n=100) |
| 46553 | A | 5 min | 0.629 / 78.6% / 1.61 | 0.441 / 73.2% / 1.36 / +10.2 / 314 | yes | regime: st_donchian_mid(n=100) |
| 56955 | A | 5 min | 0.620 / 74.6% / 1.71 | 0.000 / 64.8% / 0.82 / +1.8 / 301 | no | regime: st_gap_direction(g=0.002) |
| 47097 | A | 15 min | 0.619 / 74.5% / 1.71 | 0.317 / 66.1% / 1.30 / +4.2 / 454 | yes | regime: st_vwap_side(); st_ichimoku_cloud(s=1) |
| 49267 | A | 5 min | 0.614 / 78.5% / 1.61 | 0.414 / 71.8% / 1.33 / +9.2 / 330 | yes | regime: st_donchian_mid(n=100) |
| 57412 | B | 5 min | 0.679 / 79.2% / 1.64 | 0.398 / 72.3% / 1.15 / +8.2 / 365 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 57094 | B | 5 min | 0.655 / 79.1% / 1.63 | 0.484 / 74.7% / 1.35 / +10.2 / 474 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 55510 | B | 5 min | 0.643 / 77.8% / 1.53 | 0.437 / 72.8% / 1.22 / +10.0 / 342 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=390, q=80) |
| 55762 | B | 5 min | 0.616 / 79.2% / 1.58 | 0.485 / 74.5% / 1.35 / +9.1 / 419 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 54166 | B | 5 min | 0.616 / 78.4% / 1.59 | 0.429 / 72.8% / 1.23 / +5.5 / 416 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 55722 | B | 5 min | 0.598 / 78.0% / 1.58 | 0.529 / 74.9% / 1.33 / +11.8 / 442 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 53200 | B | 5 min | 0.587 / 76.8% / 1.55 | 0.461 / 72.8% / 1.26 / +9.7 / 430 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 57178 | B | 5 min | 0.577 / 77.9% / 1.56 | 0.486 / 74.1% / 1.37 / +9.6 / 437 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
| 55372 | B | 5 min | 0.548 / 76.3% / 1.44 | 0.441 / 72.0% / 1.30 / +8.6 / 418 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=80) |
| 52378 | B | 5 min | 0.545 / 76.5% / 1.47 | 0.494 / 73.9% / 1.28 / +11.5 / 429 | yes | filter: f_htf_agrees(k=6); f_atr_rank_high(n=200, q=70) |
