# Island exchange at generation 30000

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.436 at home, 0.197 away (retention 45%).
- Mean win rate: 72.8% at home, 67.6% away.
- Mean profit factor: 1.33 at home, 1.01 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 11 of 20; 9 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 14255 | A | 15 min | 0.516 / 77.6% / 1.35 | 0.322 / 72.2% / 1.11 / +2.9 / 309 | yes | regime: st_ichimoku_cloud(s=1) |
| 26847 | A | 15 min | 0.514 / 75.2% / 1.41 | 0.277 / 69.2% / 1.01 / +3.5 / 773 | yes | trigger: tr_volume_climax_follow(n=10) |
| 29997 | A | 5 min | 0.512 / 74.4% / 1.36 | 0.313 / 72.1% / 1.08 / +7.7 / 330 | yes | regime: st_gap_direction(g=0.004) |
| 29719 | A | 5 min | 0.505 / 76.6% / 1.88 | 0.000 / 66.0% / 0.91 / +6.2 / 197 | no | regime: st_gap_direction(g=0.004) |
| 29867 | A | 15 min | 0.478 / 70.1% / 1.44 | 0.000 / 60.6% / 0.91 / +4.7 / 264 | no | trigger: tr_band_width_expansion(m=50, n=20) |
| 26643 | A | 5 min | 0.461 / 73.4% / 1.24 | 0.384 / 72.7% / 1.13 / +7.4 / 1168 | yes | trigger: tr_opening_drive(k=3.0, m=45) OR tr_roc_thrust(k=3.0, n=8) |
| 29957 | A | 5 min | 0.455 / 74.0% / 1.43 | 0.000 / 62.8% / 0.77 / -1.4 / 352 | no | regime: st_session_open_side(); st_gap_direction(g=0.001) |
| 29089 | A | 15 min | 0.432 / 69.7% / 1.36 | 0.195 / 61.4% / 1.06 / +5.0 / 264 | no | trigger: tr_band_width_expansion(m=50, n=20) |
| 28353 | A | 5 min | 0.426 / 73.3% / 1.17 | 0.301 / 70.4% / 1.02 / +5.4 / 793 | yes | trigger: tr_opening_drive(k=3.0, m=45) OR tr_roc_thrust(k=3.0, n=5) |
| 11757 | A | 5 min | 0.421 / 71.0% / 1.25 | 0.000 / 66.3% / 0.90 / +3.8 / 762 | no | trigger: tr_trail_flip(f=3.0, n=14) |
| 29872 | B | 5 min | 0.492 / 72.3% / 1.40 | 0.000 / 64.9% / 0.95 / +0.9 / 538 | no | filter: f_entropy_low(n=5, thr=40); f_weekday_block(day=3) |
| 9056 | B | 15 min | 0.431 / 72.4% / 1.34 | 0.315 / 69.1% / 1.07 / +2.3 / 430 | yes | filter: f_weekday_block(day=3) |
| 25968 | B | 5 min | 0.415 / 73.0% / 1.15 | 0.460 / 73.3% / 1.23 / +7.8 / 1189 | yes | trigger: tr_roc_thrust(k=3.0, n=8) |
| 29574 | B | 5 min | 0.400 / 72.7% / 1.27 | 0.000 / 60.8% / 0.76 / -0.2 / 309 | no | regime: st_both_vwap_side() |
| 26228 | B | 5 min | 0.390 / 72.8% / 1.13 | 0.459 / 73.6% / 1.24 / +7.5 / 1222 | yes | trigger: tr_opening_drive(k=3.0, m=45) OR tr_roc_thrust(k=3.0, n=8) |
| 29404 | B | 5 min | 0.384 / 72.2% / 1.15 | 0.392 / 71.8% / 1.16 / +7.4 / 987 | yes | regime: st_donchian_mid(n=100) |
| 19178 | B | 15 min | 0.382 / 71.1% / 1.21 | 0.327 / 71.2% / 1.07 / +3.3 / 872 | yes | filter: f_not_midday() |
| 19590 | B | 15 min | 0.381 / 67.7% / 1.23 | 0.200 / 65.8% / 1.08 / +6.7 / 319 | yes | filter: f_session_segment(seg=1) |
| 26588 | B | 5 min | 0.368 / 71.0% / 1.24 | 0.000 / 64.5% / 0.87 / +1.6 / 313 | no | regime: st_first_minutes_direction(k=0.5, m=30) |
| 19924 | B | 5 min | 0.363 / 74.4% / 1.64 | 0.000 / 62.5% / 0.90 / -0.8 / 232 | no | regime: st_both_vwap_side() |
