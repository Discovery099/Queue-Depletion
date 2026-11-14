# Lessons (distilled from the graveyard)

Built from 5727 failed generations with at least 100 out-of-sample trades. Each line is a description of what failed, with its supporting count; none is a rule. Lessons learned on one timeframe or exit family may be wrong in general and are re-tested every 10,000 generations (SPEC 15.8).

Note: win-rate alpha recorded before generation 2001 used a twin that did not match target-to-stop geometry and is overstated for level-based targets (reports/gate_changes.md).

## Most common failed gates

- floor.profit_factor_pooled: 5552 failures
- sample.min_track_record_sessions: 5333 failures
- sample.wilson_lower: 5077 failures
- floor.win_rate_pooled: 5067 failures
- floor.win_rate_each_instrument: 4679 failures
- floor.expectancy_in_round_trip_costs: 4560 failures
- wf.folds_with_pf_above_1: 4245 failures
- wf.median_fold_pf: 4148 failures
- sample.trades_per_instrument: 1575 failures
- sample.trades_per_fold_per_instrument: 1108 failures
- wf.worst_fold_pf: 759 failures
- sample.trades_per_complexity_point: 571 failures

## By family

- trend continuation: median win rate 51%, median alpha +3.7 points, median profit factor 0.99, 47% above 1.0; near break-even (1306 failures)
- mean reversion to value: median win rate 45%, median alpha +0.6 points, median profit factor 0.90, 29% above 1.0; no edge after costs (987 failures)
- liquidity sweep and reversal: median win rate 42%, median alpha +0.4 points, median profit factor 0.85, 19% above 1.0; no edge after costs (705 failures)
- breakout failure: median win rate 50%, median alpha +2.7 points, median profit factor 0.96, 42% above 1.0; near break-even (545 failures)
- volatility contraction: median win rate 51%, median alpha +2.6 points, median profit factor 0.95, 40% above 1.0; near break-even (465 failures)
- volatility expansion: median win rate 53%, median alpha +3.6 points, median profit factor 1.00, 51% above 1.0; near break-even (458 failures)
- opening auction: median win rate 52%, median alpha +3.3 points, median profit factor 1.01, 53% above 1.0; near break-even (396 failures)
- exhaustion: median win rate 43%, median alpha +0.3 points, median profit factor 0.86, 12% above 1.0; no edge after costs (372 failures)
- inter-market lead-lag: median win rate 48%, median alpha +1.2 points, median profit factor 0.90, 19% above 1.0; no edge after costs (290 failures)
- closing auction: median win rate 56%, median alpha +5.1 points, median profit factor 1.12, 67% above 1.0; weakly positive, below the gates (203 failures)

## By target

- x_target_atr: median win rate 55%, median alpha +2.6 points, median profit factor 0.98, 45% above 1.0; near break-even (1801 failures)
- x_target_r: median win rate 53%, median alpha +2.2 points, median profit factor 0.96, 42% above 1.0; near break-even (1441 failures)
- x_target_location_level: median win rate 50%, median alpha +2.4 points, median profit factor 0.95, 36% above 1.0; no edge after costs (676 failures)
- x_target_prior_extreme: median win rate 42%, median alpha +2.3 points, median profit factor 0.96, 41% above 1.0; near break-even (468 failures)
- x_target_opposite_range_edge: median win rate 39%, median alpha +1.7 points, median profit factor 0.85, 18% above 1.0; no edge after costs (392 failures)
- x_target_prior_close: median win rate 38%, median alpha +2.4 points, median profit factor 0.97, 43% above 1.0; near break-even (357 failures)
- x_target_vwap: median win rate 41%, median alpha +1.3 points, median profit factor 0.79, 5% above 1.0; no edge after costs (286 failures)
- x_target_session_mid: median win rate 42%, median alpha +2.1 points, median profit factor 0.80, 9% above 1.0; no edge after costs (280 failures)
- no target: median win rate 46%, median alpha +2.5 points, median profit factor 1.00, 50% above 1.0; near break-even (26 failures)

## By timeframe

- 5: median win rate 47%, median alpha +1.5 points, median profit factor 0.89, 24% above 1.0; no edge after costs (2539 failures)
- 15: median win rate 54%, median alpha +3.3 points, median profit factor 1.01, 52% above 1.0; near break-even (1577 failures)
- 10: median win rate 48%, median alpha +2.0 points, median profit factor 0.93, 31% above 1.0; no edge after costs (638 failures)
- 30: median win rate 49%, median alpha +3.0 points, median profit factor 0.99, 48% above 1.0; near break-even (529 failures)
- 60: median win rate 48%, median alpha +3.2 points, median profit factor 1.03, 55% above 1.0; near break-even (444 failures)

## By entry

- market: median win rate 49%, median alpha +2.3 points, median profit factor 0.94, 38% above 1.0; no edge after costs (4817 failures)
- limit: median win rate 48%, median alpha +1.6 points, median profit factor 0.94, 31% above 1.0; no edge after costs (593 failures)
- stop: median win rate 52%, median alpha +2.8 points, median profit factor 0.91, 38% above 1.0; no edge after costs (317 failures)

## By trigger

- tr_false_break_prior_day: median win rate 57%, median alpha +4.5 points, median profit factor 1.05, 59% above 1.0; weakly positive, below the gates (230 failures)
- tr_cci_breakout: median win rate 58%, median alpha +3.6 points, median profit factor 1.00, 50% above 1.0; near break-even (189 failures)
- tr_keltner_reentry: median win rate 56%, median alpha +3.7 points, median profit factor 1.06, 63% above 1.0; weakly positive, below the gates (166 failures)
- tr_opening_range_break: median win rate 51%, median alpha +3.2 points, median profit factor 1.01, 60% above 1.0; near break-even (161 failures)
- tr_internal_bar_strength: median win rate 46%, median alpha +0.2 points, median profit factor 0.90, 24% above 1.0; no edge after costs (159 failures)
- tr_price_ema_cross: median win rate 54%, median alpha +5.7 points, median profit factor 1.05, 58% above 1.0; weakly positive, below the gates (144 failures)
- tr_sweep_swing: median win rate 45%, median alpha +1.2 points, median profit factor 0.90, 28% above 1.0; no edge after costs (132 failures)
- tr_coil_break: median win rate 50%, median alpha +1.8 points, median profit factor 0.95, 32% above 1.0; near break-even (130 failures)
- tr_companion_leads_break: median win rate 50%, median alpha +2.3 points, median profit factor 0.92, 21% above 1.0; no edge after costs (124 failures)
- tr_ema_cross: median win rate 61%, median alpha +5.6 points, median profit factor 1.11, 67% above 1.0; weakly positive, below the gates (118 failures)
- tr_late_session_extreme: median win rate 59%, median alpha +6.2 points, median profit factor 1.28, 85% above 1.0; weakly positive, below the gates (116 failures)
- tr_failed_break: median win rate 47%, median alpha +1.8 points, median profit factor 0.94, 34% above 1.0; no edge after costs (114 failures)
- tr_squeeze_release: median win rate 55%, median alpha +3.2 points, median profit factor 1.01, 52% above 1.0; near break-even (111 failures)
- tr_true_range_spike: median win rate 52%, median alpha +3.3 points, median profit factor 0.99, 44% above 1.0; near break-even (108 failures)
- tr_bollinger_break: median win rate 56%, median alpha +3.8 points, median profit factor 1.06, 63% above 1.0; weakly positive, below the gates (105 failures)
- tr_macd_zero_cross: median win rate 54%, median alpha +4.7 points, median profit factor 1.00, 51% above 1.0; near break-even (96 failures)
- tr_volume_climax_follow: median win rate 51%, median alpha +2.9 points, median profit factor 0.99, 44% above 1.0; near break-even (90 failures)
- tr_low_volatility_break: median win rate 63%, median alpha +6.8 points, median profit factor 1.10, 70% above 1.0; weakly positive, below the gates (87 failures)
- tr_engulfing: median win rate 45%, median alpha +1.1 points, median profit factor 0.86, 5% above 1.0; no edge after costs (86 failures)
- tr_double_tap: median win rate 36%, median alpha -0.1 points, median profit factor 0.85, 15% above 1.0; no edge after costs (86 failures)
- tr_inside_bar_break: median win rate 49%, median alpha +1.2 points, median profit factor 0.90, 24% above 1.0; no edge after costs (85 failures)
- tr_band_width_expansion: median win rate 61%, median alpha +5.5 points, median profit factor 1.11, 71% above 1.0; weakly positive, below the gates (84 failures)
- tr_initial_balance_extension: median win rate 58%, median alpha +5.3 points, median profit factor 1.10, 72% above 1.0; weakly positive, below the gates (83 failures)
- tr_cmo_hook: median win rate 48%, median alpha +1.6 points, median profit factor 0.95, 38% above 1.0; near break-even (82 failures)
- tr_trail_flip: median win rate 58%, median alpha +5.9 points, median profit factor 1.09, 77% above 1.0; weakly positive, below the gates (79 failures)
- tr_htf_extreme_sweep: median win rate 44%, median alpha +0.1 points, median profit factor 0.85, 22% above 1.0; no edge after costs (77 failures)
- tr_swing_break_failure: median win rate 45%, median alpha +0.8 points, median profit factor 0.88, 17% above 1.0; no edge after costs (72 failures)
- tr_late_vwap_cross: median win rate 54%, median alpha +3.1 points, median profit factor 0.97, 44% above 1.0; near break-even (71 failures)
- tr_pin_bar: median win rate 42%, median alpha -0.6 points, median profit factor 0.87, 7% above 1.0; no edge after costs (70 failures)
- tr_sweep_prior_close: median win rate 47%, median alpha +2.4 points, median profit factor 0.88, 19% above 1.0; no edge after costs (69 failures)
