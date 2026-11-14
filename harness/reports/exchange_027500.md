# Island exchange at generation 27500

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.431 at home, 0.198 away (retention 46%).
- Mean win rate: 73.1% at home, 68.6% away.
- Mean profit factor: 1.30 at home, 1.01 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 10 of 20; 10 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 14255 | A | 15 min | 0.516 / 77.6% / 1.35 | 0.322 / 72.2% / 1.11 / +2.9 / 309 | yes | regime: st_ichimoku_cloud(s=1) |
| 26847 | A | 15 min | 0.514 / 75.2% / 1.41 | 0.277 / 69.2% / 1.01 / +3.5 / 773 | yes | trigger: tr_volume_climax_follow(n=10) |
| 26269 | A | 5 min | 0.488 / 77.8% / 1.33 | 0.000 / 71.8% / 0.91 / +1.8 / 603 | no | regime: st_donchian_mid(n=55) |
| 26643 | A | 5 min | 0.461 / 73.4% / 1.24 | 0.384 / 72.7% / 1.13 / +7.4 / 1168 | yes | trigger: tr_opening_drive(k=3.0, m=45) OR tr_roc_thrust(k=3.0, n=8) |
| 24765 | A | 5 min | 0.455 / 73.3% / 1.22 | 0.415 / 73.0% / 1.15 / +8.0 / 1094 | yes | trigger: tr_roc_thrust(k=3.0, n=8) |
| 23327 | A | 15 min | 0.450 / 73.4% / 1.28 | 0.000 / 67.4% / 0.94 / +2.9 / 586 | no | trigger: tr_volume_climax_follow(n=10) |
| 26099 | A | 15 min | 0.433 / 70.0% / 1.38 | 0.183 / 61.4% / 1.06 / +1.6 / 264 | no | trigger: tr_band_width_expansion(m=50, n=20) |
| 25821 | A | 5 min | 0.432 / 76.1% / 1.22 | 0.000 / 70.7% / 0.86 / +0.6 / 860 | no | trigger: tr_trail_flip(f=3.0, n=14) |
| 27205 | A | 5 min | 0.429 / 72.3% / 1.25 | 0.291 / 70.1% / 0.99 / +5.2 / 683 | no | regime: st_donchian_mid(n=55) |
| 24721 | A | 15 min | 0.423 / 74.6% / 1.25 | 0.000 / 71.0% / 0.95 / +4.0 / 618 | no | regime: st_vwap_side() |
| 27072 | B | 5 min | 0.455 / 75.6% / 1.28 | 0.000 / 70.9% / 0.97 / +5.7 / 388 | no | regime: st_first_minutes_direction(k=0.5, m=30); st_donchian_mid(n=100) |
| 9056 | B | 15 min | 0.431 / 72.4% / 1.34 | 0.315 / 69.1% / 1.07 / +2.3 / 430 | yes | filter: f_weekday_block(day=3) |
| 27500 | B | 10 min | 0.422 / 69.6% / 1.24 | 0.000 / 58.8% / 0.73 / -0.6 / 357 | no | regime: st_both_vwap_side() |
| 25968 | B | 5 min | 0.415 / 73.0% / 1.15 | 0.460 / 73.3% / 1.23 / +7.8 / 1189 | yes | trigger: tr_roc_thrust(k=3.0, n=8) |
| 27426 | B | 5 min | 0.396 / 69.1% / 1.21 | 0.335 / 67.5% / 1.10 / +4.1 / 550 | yes | filter: f_inside_prior_day_range() |
| 26228 | B | 5 min | 0.390 / 72.8% / 1.13 | 0.459 / 73.6% / 1.24 / +7.5 / 1222 | yes | trigger: tr_opening_drive(k=3.0, m=45) OR tr_roc_thrust(k=3.0, n=8) |
| 19178 | B | 15 min | 0.382 / 71.1% / 1.21 | 0.327 / 71.2% / 1.07 / +3.3 / 872 | yes | filter: f_not_midday() |
| 19590 | B | 15 min | 0.381 / 67.7% / 1.23 | 0.200 / 65.8% / 1.08 / +6.7 / 319 | yes | filter: f_session_segment(seg=1) |
| 27434 | B | 5 min | 0.377 / 72.3% / 1.55 | 0.000 / 59.6% / 0.70 / +5.0 / 235 | no | regime: st_both_vwap_side() |
| 26752 | B | 5 min | 0.374 / 75.3% / 1.74 | 0.000 / 62.9% / 0.92 / +1.9 / 229 | no | regime: st_both_vwap_side() |
