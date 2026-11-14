# Island exchange at generation 25000

The 10 leading distinct strategies of each island, re-scored on the other island's three test folds (200 geometry-matched twins). Research data only.

- Mean composite score: 0.426 at home, 0.133 away (retention 31%).
- Mean win rate: 71.9% at home, 67.5% away.
- Mean profit factor: 1.28 at home, 0.99 away.
- Survivors (kept at least half their score and a profit factor above 1.0): 7 of 20; 13 removed from the archive.

| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |
|---|---|---|---|---|---|---|
| 14255 | A | 15 min | 0.516 / 77.6% / 1.35 | 0.322 / 72.2% / 1.11 / +2.9 / 309 | yes | regime: st_ichimoku_cloud(s=1) |
| 24561 | A | 5 min | 0.489 / 74.3% / 1.35 | 0.000 / 64.8% / 0.81 / -0.4 / 769 | no | regime: st_other_instrument_trend(n=50) |
| 24597 | A | 5 min | 0.476 / 77.6% / 1.24 | 0.277 / 72.9% / 1.00 / +2.9 / 476 | yes | regime: st_donchian_mid(n=100) |
| 23929 | A | 15 min | 0.463 / 73.0% / 1.31 | 0.000 / 66.9% / 0.92 / +1.6 / 516 | no | filter: f_companion_confirms() |
| 23701 | A | 5 min | 0.461 / 73.5% / 1.23 | 0.389 / 72.9% / 1.14 / +7.1 / 1154 | yes | trigger: tr_opening_drive(k=3.0, m=45) OR tr_roc_thrust(k=3.0, n=8) |
| 17945 | A | 15 min | 0.459 / 75.0% / 1.47 | 0.000 / 66.7% / 0.91 / +3.2 / 237 | no | trigger: tr_gap_and_go(g=0.002, wnd=90) |
| 24765 | A | 5 min | 0.455 / 73.3% / 1.22 | 0.415 / 73.0% / 1.15 / +8.0 / 1094 | yes | trigger: tr_roc_thrust(k=3.0, n=8) |
| 23005 | A | 15 min | 0.451 / 69.6% / 1.33 | 0.000 / 60.1% / 0.97 / +1.2 / 316 | no | trigger: tr_band_width_expansion(m=50, n=20) |
| 12213 | A | 15 min | 0.435 / 67.7% / 1.37 | 0.140 / 64.7% / 1.18 / +6.9 / 343 | no | regime: st_ichimoku_cloud(s=1) |
| 10963 | A | 15 min | 0.424 / 73.8% / 1.18 | 0.000 / 68.0% / 0.91 / +3.8 / 752 | no | regime: st_gap_direction(g=0.001) |
| 9056 | B | 15 min | 0.431 / 72.4% / 1.34 | 0.315 / 69.1% / 1.07 / +2.3 / 430 | yes | filter: f_weekday_block(day=3) |
| 24464 | B | 15 min | 0.422 / 75.2% / 1.23 | 0.000 / 71.9% / 0.96 / +2.9 / 342 | no | trigger: tr_macd_zero_cross(s=1) |
| 24722 | B | 5 min | 0.409 / 69.7% / 1.32 | 0.000 / 61.5% / 0.89 / -2.3 / 382 | no | regime: st_both_vwap_side() |
| 19178 | B | 15 min | 0.382 / 71.1% / 1.21 | 0.327 / 71.2% / 1.07 / +3.3 / 872 | yes | filter: f_not_midday() |
| 19590 | B | 15 min | 0.381 / 67.7% / 1.23 | 0.200 / 65.8% / 1.08 / +6.7 / 319 | yes | filter: f_session_segment(seg=1) |
| 22618 | B | 15 min | 0.376 / 70.8% / 1.17 | 0.000 / 66.9% / 0.88 / -0.4 / 752 | no | filter: f_stop_before_close(m=30) |
| 21484 | B | 60 min | 0.375 / 68.4% / 1.42 | 0.000 / 63.7% / 0.96 / +0.5 / 411 | no | trigger: tr_opening_range_break(m=30) |
| 20784 | B | 15 min | 0.369 / 70.7% / 1.16 | 0.000 / 66.8% / 0.88 / -0.7 / 768 | no | filter: f_stop_before_close(m=30) |
| 23582 | B | 15 min | 0.369 / 71.3% / 1.17 | 0.270 / 69.5% / 0.98 / +0.8 / 541 | no | filter: f_not_midday() |
| 14540 | B | 15 min | 0.368 / 65.1% / 1.30 | 0.000 / 60.7% / 0.94 / +2.8 / 313 | no | regime: st_opening_range_side(m=30) |
