# Island exchange at generation 22500

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.509 at home, 0.111 away (retention 22%).
- Mean win rate: 73.5% at home, 66.1% away.
- Mean profit factor: 1.50 at home, 0.97 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 4 of 20; 16 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 21055 | A | 5 min | 0.670 / 77.2% / 1.70 | 0.000 / 68.9% / 0.94 / +3.3 / 264 | no | regime: st_gap_direction(g=0.002) |
| 18133 | A | 5 min | 0.636 / 74.7% / 1.72 | 0.000 / 64.8% / 0.82 / +3.0 / 301 | no | regime: st_gap_direction(g=0.002) |
| 17057 | A | 5 min | 0.631 / 75.6% / 1.67 | 0.000 / 67.4% / 0.86 / +3.2 / 334 | no | regime: st_gap_direction(g=0.002) |
| 18999 | A | 5 min | 0.629 / 75.2% / 1.68 | 0.000 / 64.0% / 0.77 / +2.4 / 289 | no | regime: st_gap_direction(g=0.002) |
| 19413 | A | 15 min | 0.605 / 82.0% / 1.97 | 0.289 / 71.7% / 1.07 / +4.1 / 297 | no | regime: st_ichimoku_cloud(s=1) |
| 14407 | A | 15 min | 0.529 / 71.3% / 1.63 | 0.206 / 63.7% / 1.15 / +4.1 / 311 | no | filter: f_signal_bar_not_huge(k=2.0) |
| 14255 | A | 15 min | 0.516 / 77.6% / 1.35 | 0.322 / 72.2% / 1.11 / +2.9 / 309 | yes | regime: st_ichimoku_cloud(s=1) |
| 19087 | A | 15 min | 0.508 / 71.3% / 1.35 | 0.000 / 65.0% / 0.92 / +4.5 / 323 | no | trigger: tr_true_range_spike(k=2.5) |
| 17669 | A | 15 min | 0.490 / 72.4% / 1.34 | 0.000 / 66.9% / 0.92 / +3.7 / 411 | no | trigger: tr_true_range_spike(k=2.5) |
| 20987 | A | 5 min | 0.476 / 73.6% / 1.25 | 0.000 / 68.8% / 0.95 / +3.4 / 778 | no | trigger: tr_trail_flip(f=3.5, n=7) |
| 5480 | B | 30 min | 0.547 / 71.5% / 1.61 | 0.001 / 60.1% / 0.96 / +4.2 / 479 | no | trigger: tr_price_ema_cross(n=34) |
| 21602 | B | 10 min | 0.533 / 72.3% / 1.43 | 0.000 / 60.2% / 0.79 / -0.4 / 347 | no | regime: st_both_vwap_side() |
| 13088 | B | 5 min | 0.513 / 78.1% / 1.55 | 0.258 / 71.0% / 0.99 / +5.4 / 328 | no | regime: st_first_minutes_direction(k=0.5, m=30); st_donchian_mid(n=100) |
| 12506 | B | 30 min | 0.489 / 68.7% / 1.58 | 0.166 / 60.8% / 1.19 / +6.9 / 454 | no | filter: f_companion_confirms() |
| 12820 | B | 10 min | 0.449 / 70.6% / 1.42 | 0.000 / 63.4% / 0.88 / +4.8 / 287 | no | regime: st_both_vwap_side() |
| 9056 | B | 15 min | 0.431 / 72.4% / 1.34 | 0.315 / 69.1% / 1.07 / +2.3 / 430 | yes | filter: f_weekday_block(day=3) |
| 15176 | B | 15 min | 0.385 / 70.6% / 1.23 | 0.129 / 67.1% / 0.97 / +1.8 / 380 | no | regime: st_opening_range_side(m=30) |
| 17714 | B | 5 min | 0.385 / 76.0% / 1.81 | 0.000 / 58.9% / 0.87 / -0.7 / 219 | no | regime: st_both_vwap_side() |
| 19178 | B | 15 min | 0.382 / 71.1% / 1.21 | 0.327 / 71.2% / 1.07 / +3.3 / 872 | yes | filter: f_not_midday() |
| 19590 | B | 15 min | 0.381 / 67.7% / 1.23 | 0.200 / 65.8% / 1.08 / +6.7 / 319 | yes | filter: f_session_segment(seg=1) |
