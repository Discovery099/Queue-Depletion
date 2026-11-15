# Lessons (distilled from the graveyard)

Built from 64483 failed generations with at least 100 out-of-sample trades. Each line is a description of what failed, with its supporting count; none is a rule. Lessons learned on one timeframe or exit family may be wrong in general and are re-tested every 10,000 generations (SPEC 15.8).

Note: win-rate alpha recorded before generation 2001 used a twin that did not match target-to-stop geometry and is overstated for level-based targets (reports/gate_changes.md).

## Most common failed gates

- floor.profit_factor_pooled: 60456 failures
- sample.min_track_record_sessions: 54577 failures
- wf.median_fold_pf: 49368 failures
- floor.expectancy_in_round_trip_costs: 48083 failures
- floor.win_rate_pooled: 44341 failures
- sample.wilson_lower: 43349 failures
- wf.folds_with_pf_above_1: 43290 failures
- floor.win_rate_each_instrument: 36252 failures
- wf.in_sample_expectancy_costs: 16574 failures
- wf.worst_fold_pf: 15982 failures
- sample.trades_per_instrument: 13739 failures
- sample.trades_per_fold_per_instrument: 9670 failures

## By family

- trend continuation: median win rate 61%, median alpha +4.4 points, median profit factor 1.05, 60% above 1.0; near break-even (15360 failures)
- mean reversion to value: median win rate 50%, median alpha +1.6 points, median profit factor 0.93, 37% above 1.0; no edge after costs (7993 failures)
- breakout failure: median win rate 61%, median alpha +3.9 points, median profit factor 1.03, 58% above 1.0; near break-even (6785 failures)
- opening auction: median win rate 64%, median alpha +4.9 points, median profit factor 1.06, 67% above 1.0; weakly positive, below the gates (6012 failures)
- exhaustion: median win rate 59%, median alpha +3.2 points, median profit factor 0.99, 49% above 1.0; near break-even (5601 failures)
- volatility expansion: median win rate 59%, median alpha +4.1 points, median profit factor 1.03, 59% above 1.0; near break-even (5022 failures)
- liquidity sweep and reversal: median win rate 46%, median alpha +0.7 points, median profit factor 0.87, 25% above 1.0; no edge after costs (4861 failures)
- inter-market lead-lag: median win rate 60%, median alpha +3.0 points, median profit factor 0.99, 47% above 1.0; near break-even (4718 failures)
- volatility contraction: median win rate 60%, median alpha +3.7 points, median profit factor 1.01, 52% above 1.0; near break-even (4390 failures)
- closing auction: median win rate 62%, median alpha +5.3 points, median profit factor 1.08, 67% above 1.0; weakly positive, below the gates (3741 failures)

## By target

- x_target_atr: median win rate 62%, median alpha +3.6 points, median profit factor 1.02, 55% above 1.0; near break-even (22904 failures)
- x_target_r: median win rate 63%, median alpha +3.4 points, median profit factor 1.01, 53% above 1.0; near break-even (17037 failures)
- no target: median win rate 64%, median alpha +8.5 points, median profit factor 1.13, 76% above 1.0; weakly positive, below the gates (8579 failures)
- x_target_location_level: median win rate 52%, median alpha +3.3 points, median profit factor 0.99, 47% above 1.0; near break-even (5874 failures)
- x_target_prior_extreme: median win rate 42%, median alpha +1.7 points, median profit factor 0.95, 39% above 1.0; near break-even (2728 failures)
- x_target_opposite_range_edge: median win rate 40%, median alpha +1.5 points, median profit factor 0.86, 20% above 1.0; no edge after costs (2346 failures)
- x_target_prior_close: median win rate 41%, median alpha +1.9 points, median profit factor 1.00, 50% above 1.0; near break-even (2037 failures)
- x_target_session_mid: median win rate 41%, median alpha +0.8 points, median profit factor 0.79, 9% above 1.0; no edge after costs (1498 failures)
- x_target_vwap: median win rate 42%, median alpha +0.7 points, median profit factor 0.79, 8% above 1.0; no edge after costs (1480 failures)

## By timeframe

- 5: median win rate 62%, median alpha +3.6 points, median profit factor 1.00, 50% above 1.0; near break-even (37885 failures)
- 15: median win rate 60%, median alpha +4.1 points, median profit factor 1.05, 63% above 1.0; weakly positive, below the gates (15096 failures)
- 10: median win rate 51%, median alpha +2.1 points, median profit factor 0.96, 41% above 1.0; near break-even (4650 failures)
- 60: median win rate 50%, median alpha +3.0 points, median profit factor 1.03, 55% above 1.0; near break-even (3867 failures)
- 30: median win rate 50%, median alpha +3.1 points, median profit factor 1.00, 51% above 1.0; near break-even (2985 failures)

## By entry

- market: median win rate 55%, median alpha +3.1 points, median profit factor 1.00, 51% above 1.0; near break-even (33910 failures)
- stop: median win rate 63%, median alpha +4.9 points, median profit factor 1.02, 54% above 1.0; near break-even (16418 failures)
- limit: median win rate 59%, median alpha +3.5 points, median profit factor 1.02, 55% above 1.0; near break-even (14155 failures)

## By trigger

- tr_roc_thrust: median win rate 67%, median alpha +7.4 points, median profit factor 1.14, 80% above 1.0; weakly positive, below the gates (4695 failures)
- tr_opening_drive: median win rate 67%, median alpha +6.9 points, median profit factor 1.12, 79% above 1.0; weakly positive, below the gates (2360 failures)
- tr_companion_leads_break: median win rate 62%, median alpha +3.3 points, median profit factor 0.98, 45% above 1.0; near break-even (2355 failures)
- tr_false_break_prior_day: median win rate 63%, median alpha +4.4 points, median profit factor 1.04, 60% above 1.0; near break-even (2291 failures)
- tr_climax_reversal: median win rate 67%, median alpha +6.6 points, median profit factor 1.12, 77% above 1.0; weakly positive, below the gates (2250 failures)
- tr_opening_range_break: median win rate 59%, median alpha +3.3 points, median profit factor 1.01, 54% above 1.0; near break-even (2085 failures)
- tr_cci_breakout: median win rate 62%, median alpha +2.9 points, median profit factor 0.96, 39% above 1.0; near break-even (1898 failures)
- tr_keltner_reentry: median win rate 62%, median alpha +3.8 points, median profit factor 1.06, 64% above 1.0; weakly positive, below the gates (1855 failures)
- tr_failed_break: median win rate 57%, median alpha +2.8 points, median profit factor 1.01, 52% above 1.0; near break-even (1627 failures)
- tr_band_break_failure: median win rate 67%, median alpha +8.4 points, median profit factor 1.17, 80% above 1.0; weakly positive, below the gates (1595 failures)
- tr_band_width_expansion: median win rate 61%, median alpha +6.4 points, median profit factor 1.14, 82% above 1.0; weakly positive, below the gates (1528 failures)
- tr_bollinger_break: median win rate 61%, median alpha +3.4 points, median profit factor 1.02, 54% above 1.0; near break-even (1390 failures)
- tr_late_session_extreme: median win rate 65%, median alpha +6.7 points, median profit factor 1.15, 80% above 1.0; weakly positive, below the gates (1356 failures)
- tr_squeeze_release: median win rate 62%, median alpha +3.9 points, median profit factor 1.04, 60% above 1.0; near break-even (1283 failures)
- tr_close_extreme_fade: median win rate 65%, median alpha +6.4 points, median profit factor 1.10, 76% above 1.0; weakly positive, below the gates (1257 failures)
- tr_low_volatility_break: median win rate 66%, median alpha +7.0 points, median profit factor 1.13, 73% above 1.0; weakly positive, below the gates (1222 failures)
- tr_engulfing: median win rate 55%, median alpha +2.0 points, median profit factor 0.96, 39% above 1.0; near break-even (1220 failures)
- tr_relative_strength_turn: median win rate 62%, median alpha +3.9 points, median profit factor 1.04, 58% above 1.0; near break-even (1199 failures)
- tr_internal_bar_strength: median win rate 53%, median alpha +1.9 points, median profit factor 0.93, 36% above 1.0; no edge after costs (1176 failures)
- tr_ema_cross: median win rate 65%, median alpha +5.8 points, median profit factor 1.15, 77% above 1.0; weakly positive, below the gates (1174 failures)
- tr_trail_flip: median win rate 67%, median alpha +6.6 points, median profit factor 1.15, 82% above 1.0; weakly positive, below the gates (1168 failures)
- tr_late_vwap_cross: median win rate 56%, median alpha +2.6 points, median profit factor 0.96, 41% above 1.0; near break-even (964 failures)
- tr_volume_climax_follow: median win rate 59%, median alpha +2.8 points, median profit factor 0.97, 40% above 1.0; near break-even (821 failures)
- tr_coil_break: median win rate 50%, median alpha +1.1 points, median profit factor 0.90, 24% above 1.0; no edge after costs (781 failures)
- tr_htf_extreme_sweep: median win rate 49%, median alpha +0.4 points, median profit factor 0.86, 26% above 1.0; no edge after costs (781 failures)
- tr_price_ema_cross: median win rate 55%, median alpha +3.7 points, median profit factor 1.00, 51% above 1.0; near break-even (734 failures)
- tr_keltner_break: median win rate 55%, median alpha +3.7 points, median profit factor 1.05, 59% above 1.0; near break-even (705 failures)
- tr_inside_bar_break: median win rate 54%, median alpha +2.5 points, median profit factor 0.95, 40% above 1.0; near break-even (688 failures)
- tr_gap_and_go: median win rate 68%, median alpha +8.1 points, median profit factor 1.18, 79% above 1.0; weakly positive, below the gates (669 failures)
- tr_rsi2_extreme: median win rate 49%, median alpha -0.6 points, median profit factor 0.84, 11% above 1.0; no edge after costs (589 failures)
