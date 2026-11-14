# Lessons (distilled from the graveyard)

Built from 1267 failed generations with at least 100 out-of-sample trades. Each line is a description of what failed, with its supporting count; none is a rule. Lessons learned on one timeframe or exit family may be wrong in general and are re-tested every 10,000 generations (SPEC 15.8).

Note: win-rate alpha recorded before generation 2001 used a twin that did not match target-to-stop geometry and is overstated for level-based targets (reports/gate_changes.md).

## Most common failed gates

- floor.profit_factor_pooled: 1249 failures
- sample.wilson_lower: 1248 failures
- floor.win_rate_pooled: 1247 failures
- sample.min_track_record_sessions: 1226 failures
- floor.win_rate_each_instrument: 1221 failures
- floor.expectancy_in_round_trip_costs: 1030 failures
- wf.folds_with_pf_above_1: 941 failures
- wf.median_fold_pf: 867 failures
- sample.trades_per_instrument: 428 failures
- sample.trades_per_fold_per_instrument: 283 failures
- sample.trades_per_complexity_point: 113 failures
- wf.worst_fold_pf: 58 failures

## By family

- trend continuation: median win rate 48%, median alpha +6.5 points, median profit factor 0.97, 40% above 1.0; near break-even (312 failures)
- mean reversion to value: median win rate 41%, median alpha +0.2 points, median profit factor 0.86, 21% above 1.0; no edge after costs (258 failures)
- liquidity sweep and reversal: median win rate 40%, median alpha +1.4 points, median profit factor 0.85, 18% above 1.0; no edge after costs (200 failures)
- exhaustion: median win rate 39%, median alpha +1.3 points, median profit factor 0.84, 11% above 1.0; no edge after costs (105 failures)
- breakout failure: median win rate 44%, median alpha +4.7 points, median profit factor 0.91, 24% above 1.0; no edge after costs (100 failures)
- inter-market lead-lag: median win rate 45%, median alpha +1.9 points, median profit factor 0.88, 19% above 1.0; no edge after costs (80 failures)
- volatility contraction: median win rate 47%, median alpha +5.1 points, median profit factor 0.95, 42% above 1.0; near break-even (71 failures)
- volatility expansion: median win rate 50%, median alpha +4.0 points, median profit factor 0.98, 39% above 1.0; near break-even (69 failures)
- opening auction: median win rate 50%, median alpha +6.3 points, median profit factor 0.98, 45% above 1.0; near break-even (44 failures)
- closing auction: median win rate 49%, median alpha +4.2 points, median profit factor 0.96, 46% above 1.0; near break-even (28 failures)

## By target

- x_target_atr: median win rate 47%, median alpha +3.7 points, median profit factor 0.94, 35% above 1.0; no edge after costs (235 failures)
- x_target_r: median win rate 49%, median alpha +1.2 points, median profit factor 0.92, 28% above 1.0; no edge after costs (218 failures)
- x_target_location_level: median win rate 50%, median alpha +2.0 points, median profit factor 0.93, 33% above 1.0; no edge after costs (171 failures)
- x_target_prior_extreme: median win rate 41%, median alpha +4.0 points, median profit factor 0.94, 39% above 1.0; no edge after costs (155 failures)
- x_target_prior_close: median win rate 38%, median alpha +5.9 points, median profit factor 0.98, 47% above 1.0; near break-even (143 failures)
- x_target_opposite_range_edge: median win rate 39%, median alpha +3.0 points, median profit factor 0.83, 13% above 1.0; no edge after costs (137 failures)
- x_target_session_mid: median win rate 42%, median alpha +5.1 points, median profit factor 0.81, 10% above 1.0; no edge after costs (105 failures)
- x_target_vwap: median win rate 43%, median alpha +3.1 points, median profit factor 0.79, 5% above 1.0; no edge after costs (101 failures)

## By timeframe

- 5: median win rate 44%, median alpha +2.8 points, median profit factor 0.87, 18% above 1.0; no edge after costs (493 failures)
- 15: median win rate 46%, median alpha +3.2 points, median profit factor 0.94, 37% above 1.0; no edge after costs (270 failures)
- 10: median win rate 44%, median alpha +2.7 points, median profit factor 0.91, 20% above 1.0; no edge after costs (206 failures)
- 30: median win rate 47%, median alpha +2.7 points, median profit factor 0.94, 38% above 1.0; no edge after costs (175 failures)
- 60: median win rate 46%, median alpha +3.0 points, median profit factor 1.00, 50% above 1.0; near break-even (123 failures)

## By entry

- market: median win rate 45%, median alpha +2.9 points, median profit factor 0.90, 28% above 1.0; no edge after costs (1267 failures)

## By trigger

- tr_sweep_swing: median win rate 43%, median alpha +1.6 points, median profit factor 0.90, 32% above 1.0; no edge after costs (31 failures)
- tr_internal_bar_strength: median win rate 40%, median alpha -4.0 points, median profit factor 0.83, 11% above 1.0; no edge after costs (28 failures)
- tr_false_break_prior_day: median win rate 45%, median alpha +5.6 points, median profit factor 0.94, 31% above 1.0; no edge after costs (26 failures)
- tr_price_ema_cross: median win rate 48%, median alpha +10.0 points, median profit factor 0.91, 35% above 1.0; no edge after costs (26 failures)
- tr_relative_strength_turn: median win rate 43%, median alpha +0.7 points, median profit factor 0.93, 20% above 1.0; no edge after costs (25 failures)
- tr_di_cross: median win rate 45%, median alpha +4.7 points, median profit factor 0.94, 38% above 1.0; no edge after costs (24 failures)
- tr_failed_break: median win rate 38%, median alpha +1.2 points, median profit factor 0.85, 13% above 1.0; no edge after costs (23 failures)
- tr_cmo_hook: median win rate 47%, median alpha +3.1 points, median profit factor 0.95, 45% above 1.0; no edge after costs (22 failures)
- tr_companion_reclaim: median win rate 45%, median alpha +1.7 points, median profit factor 0.83, 9% above 1.0; no edge after costs (22 failures)
- tr_engulfing: median win rate 45%, median alpha +1.9 points, median profit factor 0.84, 5% above 1.0; no edge after costs (22 failures)
- tr_rsi2_extreme: median win rate 29%, median alpha -8.0 points, median profit factor 0.79, 14% above 1.0; no edge after costs (22 failures)
- tr_stochastic_hook: median win rate 50%, median alpha +5.2 points, median profit factor 0.94, 32% above 1.0; no edge after costs (22 failures)
- tr_cycle_phase_hook: median win rate 41%, median alpha +0.2 points, median profit factor 0.78, 15% above 1.0; no edge after costs (20 failures)
- tr_squeeze_release: median win rate 52%, median alpha +5.2 points, median profit factor 1.05, 60% above 1.0; near break-even (20 failures)
- tr_vwap_cross: median win rate 50%, median alpha +6.0 points, median profit factor 0.94, 35% above 1.0; no edge after costs (20 failures)
- tr_double_tap: median win rate 39%, median alpha +3.2 points, median profit factor 0.88, 20% above 1.0; no edge after costs (20 failures)
- tr_true_range_spike: median win rate 51%, median alpha +5.1 points, median profit factor 1.01, 53% above 1.0; near break-even (19 failures)
- tr_htf_extreme_sweep: median win rate 45%, median alpha +0.6 points, median profit factor 0.84, 17% above 1.0; no edge after costs (18 failures)
- tr_sweep_prior_close: median win rate 41%, median alpha +4.6 points, median profit factor 0.82, 17% above 1.0; no edge after costs (18 failures)
- tr_two_bar_reversal: median win rate 48%, median alpha +10.0 points, median profit factor 0.90, 44% above 1.0; no edge after costs (18 failures)
- tr_divergence_at_session_extreme: median win rate 42%, median alpha +1.5 points, median profit factor 0.87, 18% above 1.0; no edge after costs (17 failures)
- tr_round_number_reject: median win rate 45%, median alpha +0.6 points, median profit factor 0.86, 12% above 1.0; no edge after costs (17 failures)
- tr_rsi_midline_cross: median win rate 49%, median alpha +7.0 points, median profit factor 0.99, 47% above 1.0; near break-even (17 failures)
- tr_stochastic_cross: median win rate 46%, median alpha +2.0 points, median profit factor 0.91, 18% above 1.0; no edge after costs (17 failures)
- tr_sweep_opening_range: median win rate 44%, median alpha +6.0 points, median profit factor 0.98, 41% above 1.0; near break-even (17 failures)
- tr_companion_leads_break: median win rate 49%, median alpha +6.8 points, median profit factor 0.93, 31% above 1.0; no edge after costs (16 failures)
- tr_hma_turn: median win rate 49%, median alpha +4.8 points, median profit factor 0.95, 44% above 1.0; near break-even (16 failures)
- tr_pin_bar: median win rate 41%, median alpha +2.2 points, median profit factor 0.92, 12% above 1.0; no edge after costs (16 failures)
- tr_three_bar_run: median win rate 50%, median alpha +3.8 points, median profit factor 0.96, 31% above 1.0; near break-even (16 failures)
- tr_trail_flip: median win rate 51%, median alpha +13.5 points, median profit factor 1.09, 81% above 1.0; weakly positive, below the gates (16 failures)
