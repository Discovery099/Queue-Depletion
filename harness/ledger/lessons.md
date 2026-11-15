# Lessons (distilled from the graveyard)

Built from 72743 failed generations with at least 100 out-of-sample trades. Each line is a description of what failed, with its supporting count; none is a rule. Lessons learned on one timeframe or exit family may be wrong in general and are re-tested every 10,000 generations (SPEC 15.8).

Note: win-rate alpha recorded before generation 2001 used a twin that did not match target-to-stop geometry and is overstated for level-based targets (reports/gate_changes.md).

## Most common failed gates

- floor.profit_factor_pooled: 67787 failures
- sample.min_track_record_sessions: 60581 failures
- wf.median_fold_pf: 55527 failures
- floor.expectancy_in_round_trip_costs: 53485 failures
- floor.win_rate_pooled: 48832 failures
- wf.folds_with_pf_above_1: 47941 failures
- sample.wilson_lower: 47689 failures
- floor.win_rate_each_instrument: 39719 failures
- wf.in_sample_expectancy_costs: 20174 failures
- wf.worst_fold_pf: 18143 failures
- sample.trades_per_instrument: 15266 failures
- sample.trades_per_fold_per_instrument: 10691 failures

## By family

- trend continuation: median win rate 62%, median alpha +4.5 points, median profit factor 1.06, 61% above 1.0; weakly positive, below the gates (17654 failures)
- mean reversion to value: median win rate 50%, median alpha +1.6 points, median profit factor 0.93, 36% above 1.0; no edge after costs (8747 failures)
- breakout failure: median win rate 62%, median alpha +4.0 points, median profit factor 1.04, 59% above 1.0; near break-even (7614 failures)
- opening auction: median win rate 64%, median alpha +5.0 points, median profit factor 1.07, 67% above 1.0; weakly positive, below the gates (6792 failures)
- exhaustion: median win rate 60%, median alpha +3.4 points, median profit factor 1.00, 51% above 1.0; near break-even (6372 failures)
- volatility expansion: median win rate 60%, median alpha +4.3 points, median profit factor 1.04, 61% above 1.0; near break-even (5603 failures)
- inter-market lead-lag: median win rate 61%, median alpha +3.2 points, median profit factor 1.00, 49% above 1.0; near break-even (5398 failures)
- liquidity sweep and reversal: median win rate 47%, median alpha +0.7 points, median profit factor 0.87, 26% above 1.0; no edge after costs (5257 failures)
- volatility contraction: median win rate 61%, median alpha +3.9 points, median profit factor 1.02, 54% above 1.0; near break-even (4934 failures)
- closing auction: median win rate 63%, median alpha +5.6 points, median profit factor 1.09, 69% above 1.0; weakly positive, below the gates (4372 failures)

## By target

- x_target_atr: median win rate 62%, median alpha +3.7 points, median profit factor 1.03, 57% above 1.0; near break-even (25489 failures)
- x_target_r: median win rate 63%, median alpha +3.5 points, median profit factor 1.02, 54% above 1.0; near break-even (18858 failures)
- no target: median win rate 65%, median alpha +9.2 points, median profit factor 1.14, 78% above 1.0; weakly positive, below the gates (11028 failures)
- x_target_location_level: median win rate 52%, median alpha +3.3 points, median profit factor 0.99, 48% above 1.0; near break-even (6354 failures)
- x_target_prior_extreme: median win rate 42%, median alpha +1.7 points, median profit factor 0.95, 39% above 1.0; near break-even (2956 failures)
- x_target_opposite_range_edge: median win rate 40%, median alpha +1.5 points, median profit factor 0.86, 20% above 1.0; no edge after costs (2582 failures)
- x_target_prior_close: median win rate 41%, median alpha +1.9 points, median profit factor 1.00, 50% above 1.0; near break-even (2218 failures)
- x_target_session_mid: median win rate 41%, median alpha +0.7 points, median profit factor 0.79, 9% above 1.0; no edge after costs (1629 failures)
- x_target_vwap: median win rate 42%, median alpha +0.7 points, median profit factor 0.79, 8% above 1.0; no edge after costs (1629 failures)

## By timeframe

- 5: median win rate 63%, median alpha +3.9 points, median profit factor 1.01, 52% above 1.0; near break-even (43774 failures)
- 15: median win rate 59%, median alpha +4.1 points, median profit factor 1.06, 63% above 1.0; weakly positive, below the gates (16396 failures)
- 10: median win rate 51%, median alpha +2.1 points, median profit factor 0.96, 41% above 1.0; near break-even (5030 failures)
- 60: median win rate 50%, median alpha +3.0 points, median profit factor 1.03, 55% above 1.0; near break-even (4264 failures)
- 30: median win rate 50%, median alpha +3.0 points, median profit factor 1.00, 50% above 1.0; near break-even (3279 failures)

## By entry

- market: median win rate 55%, median alpha +3.2 points, median profit factor 1.01, 52% above 1.0; near break-even (37560 failures)
- stop: median win rate 63%, median alpha +5.3 points, median profit factor 1.04, 56% above 1.0; near break-even (19075 failures)
- limit: median win rate 59%, median alpha +3.6 points, median profit factor 1.03, 57% above 1.0; near break-even (16108 failures)

## By trigger

- tr_roc_thrust: median win rate 68%, median alpha +7.5 points, median profit factor 1.15, 81% above 1.0; weakly positive, below the gates (6042 failures)
- tr_companion_leads_break: median win rate 63%, median alpha +3.4 points, median profit factor 0.99, 48% above 1.0; near break-even (2742 failures)
- tr_climax_reversal: median win rate 67%, median alpha +6.8 points, median profit factor 1.13, 79% above 1.0; weakly positive, below the gates (2738 failures)
- tr_opening_drive: median win rate 67%, median alpha +7.2 points, median profit factor 1.12, 80% above 1.0; weakly positive, below the gates (2675 failures)
- tr_false_break_prior_day: median win rate 63%, median alpha +4.4 points, median profit factor 1.04, 60% above 1.0; near break-even (2433 failures)
- tr_opening_range_break: median win rate 59%, median alpha +3.3 points, median profit factor 1.01, 55% above 1.0; near break-even (2301 failures)
- tr_cci_breakout: median win rate 62%, median alpha +2.9 points, median profit factor 0.96, 39% above 1.0; near break-even (2061 failures)
- tr_band_break_failure: median win rate 67%, median alpha +8.6 points, median profit factor 1.17, 81% above 1.0; weakly positive, below the gates (2043 failures)
- tr_keltner_reentry: median win rate 62%, median alpha +3.8 points, median profit factor 1.05, 64% above 1.0; weakly positive, below the gates (1984 failures)
- tr_band_width_expansion: median win rate 62%, median alpha +6.6 points, median profit factor 1.14, 83% above 1.0; weakly positive, below the gates (1830 failures)
- tr_failed_break: median win rate 58%, median alpha +2.9 points, median profit factor 1.01, 53% above 1.0; near break-even (1737 failures)
- tr_late_session_extreme: median win rate 65%, median alpha +6.8 points, median profit factor 1.15, 80% above 1.0; weakly positive, below the gates (1656 failures)
- tr_close_extreme_fade: median win rate 65%, median alpha +6.7 points, median profit factor 1.11, 78% above 1.0; weakly positive, below the gates (1521 failures)
- tr_bollinger_break: median win rate 61%, median alpha +3.6 points, median profit factor 1.02, 56% above 1.0; near break-even (1509 failures)
- tr_squeeze_release: median win rate 63%, median alpha +4.0 points, median profit factor 1.04, 61% above 1.0; near break-even (1430 failures)
- tr_low_volatility_break: median win rate 67%, median alpha +7.2 points, median profit factor 1.13, 75% above 1.0; weakly positive, below the gates (1415 failures)
- tr_engulfing: median win rate 55%, median alpha +2.1 points, median profit factor 0.96, 40% above 1.0; near break-even (1324 failures)
- tr_relative_strength_turn: median win rate 62%, median alpha +3.8 points, median profit factor 1.04, 58% above 1.0; near break-even (1318 failures)
- tr_ema_cross: median win rate 64%, median alpha +5.8 points, median profit factor 1.14, 78% above 1.0; weakly positive, below the gates (1263 failures)
- tr_internal_bar_strength: median win rate 53%, median alpha +1.8 points, median profit factor 0.93, 36% above 1.0; no edge after costs (1251 failures)
- tr_trail_flip: median win rate 67%, median alpha +6.6 points, median profit factor 1.15, 82% above 1.0; weakly positive, below the gates (1224 failures)
- tr_late_vwap_cross: median win rate 56%, median alpha +2.6 points, median profit factor 0.96, 41% above 1.0; near break-even (1006 failures)
- tr_volume_climax_follow: median win rate 59%, median alpha +2.8 points, median profit factor 0.97, 41% above 1.0; near break-even (872 failures)
- tr_gap_and_go: median win rate 68%, median alpha +8.1 points, median profit factor 1.17, 79% above 1.0; weakly positive, below the gates (849 failures)
- tr_coil_break: median win rate 50%, median alpha +1.3 points, median profit factor 0.91, 27% above 1.0; no edge after costs (830 failures)
- tr_htf_extreme_sweep: median win rate 49%, median alpha +0.4 points, median profit factor 0.87, 26% above 1.0; no edge after costs (807 failures)
- tr_price_ema_cross: median win rate 55%, median alpha +3.9 points, median profit factor 1.01, 51% above 1.0; near break-even (772 failures)
- tr_keltner_break: median win rate 54%, median alpha +3.6 points, median profit factor 1.05, 59% above 1.0; near break-even (765 failures)
- tr_inside_bar_break: median win rate 54%, median alpha +2.6 points, median profit factor 0.96, 41% above 1.0; near break-even (753 failures)
- tr_sweep_prior_close: median win rate 58%, median alpha +3.3 points, median profit factor 1.00, 50% above 1.0; near break-even (624 failures)
