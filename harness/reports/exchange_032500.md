# Island exchange at generation 32500

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.451 at home, 0.241 away (retention 53%).
- Mean win rate: 73.3% at home, 68.8% away.
- Mean profit factor: 1.33 at home, 1.05 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 14 of 20; 6 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 30409 | A | 15 min | 0.524 / 76.6% / 1.49 | 0.289 / 71.1% / 1.11 / +3.7 / 301 | yes | location: loc_ema_distance(n=50, k=2.0) |
| 14255 | A | 15 min | 0.516 / 77.6% / 1.35 | 0.322 / 72.2% / 1.11 / +2.9 / 309 | yes | regime: st_ichimoku_cloud(s=1) |
| 32251 | A | 15 min | 0.514 / 75.3% / 1.41 | 0.280 / 69.2% / 1.01 / +4.0 / 773 | yes | trigger: tr_volume_climax_follow(n=10) |
| 32189 | A | 5 min | 0.513 / 69.5% / 1.62 | 0.000 / 60.7% / 0.90 / +11.1 / 458 | no | regime: st_session_range_position(thr=0.6) |
| 30471 | A | 5 min | 0.513 / 74.5% / 1.34 | 0.311 / 72.4% / 1.09 / +8.5 / 323 | yes | regime: st_gap_direction(g=0.004) |
| 31539 | A | 15 min | 0.494 / 75.2% / 1.48 | 0.267 / 68.9% / 1.07 / +4.3 / 470 | yes | regime: st_late_session_trend(start=300) |
| 31269 | A | 5 min | 0.471 / 74.0% / 1.29 | 0.362 / 72.0% / 1.09 / +6.6 / 901 | yes | regime: st_ichimoku_cloud(s=1) |
| 31575 | A | 15 min | 0.464 / 69.3% / 1.41 | 0.000 / 58.9% / 0.94 / +4.3 / 263 | no | trigger: tr_band_width_expansion(m=50, n=20) |
| 31735 | A | 15 min | 0.430 / 74.4% / 1.26 | 0.000 / 69.1% / 0.92 / +2.3 / 1157 | no | trigger: tr_volume_climax_follow(n=10) |
| 28353 | A | 5 min | 0.426 / 73.3% / 1.17 | 0.301 / 70.4% / 1.02 / +5.4 / 793 | yes | trigger: tr_opening_drive(k=3.0, m=45) OR tr_roc_thrust(k=3.0, n=5) |
| 30340 | B | 5 min | 0.444 / 70.7% / 1.29 | 0.239 / 65.0% / 0.96 / +0.7 / 649 | no | filter: f_entropy_low(n=5, thr=40) |
| 30916 | B | 5 min | 0.440 / 73.9% / 1.21 | 0.390 / 72.3% / 1.20 / +5.9 / 936 | yes | filter: f_htf_agrees(k=4); f_skip_open(m=15) |
| 9056 | B | 15 min | 0.431 / 72.4% / 1.34 | 0.315 / 69.1% / 1.07 / +2.3 / 430 | yes | filter: f_weekday_block(day=3) |
| 31088 | B | 5 min | 0.427 / 73.8% / 1.20 | 0.390 / 72.7% / 1.21 / +6.3 / 971 | yes | filter: f_htf_agrees(k=4); f_skip_open(m=15) |
| 31726 | B | 5 min | 0.424 / 74.4% / 1.38 | 0.374 / 74.2% / 1.17 / +9.3 / 365 | yes | regime: st_donchian_mid(n=100) |
| 32456 | B | 5 min | 0.415 / 73.2% / 1.24 | 0.361 / 71.7% / 1.16 / +5.1 / 621 | yes | filter: f_session_range_developed(k=6.0); f_skip_open(m=30) |
| 31352 | B | 15 min | 0.410 / 73.3% / 1.36 | 0.296 / 70.1% / 1.17 / +5.0 / 251 | yes | regime: st_opening_range_side(m=30); st_ichimoku_cloud(s=2) |
| 32250 | B | 5 min | 0.396 / 72.9% / 1.21 | 0.317 / 70.5% / 1.11 / +5.8 / 921 | yes | filter: f_htf_agrees(k=4); f_skip_open(m=15) |
| 32454 | B | 5 min | 0.387 / 73.0% / 1.27 | 0.000 / 60.1% / 0.73 / -0.2 / 303 | no | regime: st_both_vwap_side() |
| 30438 | B | 5 min | 0.384 / 69.5% / 1.19 | 0.000 / 65.6% / 0.97 / +1.1 / 1002 | no | filter: f_entropy_low(n=5, thr=40) |
