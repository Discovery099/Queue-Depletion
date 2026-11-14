# Lessons (distilled from the graveyard)

Built from 11148 failed generations with at least 100 out-of-sample trades. Each line is a description of what failed, with its supporting count; none is a rule. Lessons learned on one timeframe or exit family may be wrong in general and are re-tested every 10,000 generations (SPEC 15.8).

Note: win-rate alpha recorded before generation 2001 used a twin that did not match target-to-stop geometry and is overstated for level-based targets (reports/gate_changes.md).

## Most common failed gates

- floor.profit_factor_pooled: 10753 failures
- sample.min_track_record_sessions: 10240 failures
- sample.wilson_lower: 9430 failures
- floor.win_rate_pooled: 9414 failures
- floor.expectancy_in_round_trip_costs: 8784 failures
- floor.win_rate_each_instrument: 8453 failures
- wf.median_fold_pf: 8196 failures
- wf.folds_with_pf_above_1: 8164 failures
- sample.trades_per_instrument: 2997 failures
- sample.trades_per_fold_per_instrument: 2148 failures
- wf.worst_fold_pf: 1848 failures
- sample.trades_per_complexity_point: 1185 failures

## By family

- trend continuation: median win rate 53%, median alpha +3.8 points, median profit factor 1.00, 49% above 1.0; near break-even (2476 failures)
- mean reversion to value: median win rate 47%, median alpha +1.0 points, median profit factor 0.91, 32% above 1.0; no edge after costs (1815 failures)
- breakout failure: median win rate 55%, median alpha +3.0 points, median profit factor 0.98, 47% above 1.0; near break-even (1270 failures)
- liquidity sweep and reversal: median win rate 44%, median alpha +0.3 points, median profit factor 0.85, 19% above 1.0; no edge after costs (1255 failures)
- volatility expansion: median win rate 54%, median alpha +3.5 points, median profit factor 1.00, 51% above 1.0; near break-even (899 failures)
- volatility contraction: median win rate 53%, median alpha +2.8 points, median profit factor 0.96, 42% above 1.0; near break-even (858 failures)
- opening auction: median win rate 54%, median alpha +3.4 points, median profit factor 1.01, 56% above 1.0; near break-even (771 failures)
- exhaustion: median win rate 45%, median alpha +0.2 points, median profit factor 0.86, 13% above 1.0; no edge after costs (758 failures)
- inter-market lead-lag: median win rate 49%, median alpha +1.4 points, median profit factor 0.91, 26% above 1.0; no edge after costs (584 failures)
- closing auction: median win rate 55%, median alpha +3.9 points, median profit factor 1.03, 56% above 1.0; near break-even (462 failures)

## By target

- x_target_atr: median win rate 57%, median alpha +2.7 points, median profit factor 0.98, 46% above 1.0; near break-even (3849 failures)
- x_target_r: median win rate 59%, median alpha +2.5 points, median profit factor 0.97, 44% above 1.0; near break-even (2993 failures)
- x_target_location_level: median win rate 50%, median alpha +2.6 points, median profit factor 0.95, 38% above 1.0; near break-even (1238 failures)
- x_target_prior_extreme: median win rate 42%, median alpha +2.1 points, median profit factor 0.96, 41% above 1.0; near break-even (729 failures)
- x_target_opposite_range_edge: median win rate 40%, median alpha +1.5 points, median profit factor 0.85, 20% above 1.0; no edge after costs (694 failures)
- x_target_prior_close: median win rate 39%, median alpha +2.1 points, median profit factor 0.98, 46% above 1.0; near break-even (578 failures)
- x_target_vwap: median win rate 40%, median alpha +0.8 points, median profit factor 0.80, 6% above 1.0; no edge after costs (479 failures)
- x_target_session_mid: median win rate 41%, median alpha +1.4 points, median profit factor 0.80, 8% above 1.0; no edge after costs (452 failures)
- no target: median win rate 47%, median alpha +3.1 points, median profit factor 1.01, 54% above 1.0; near break-even (136 failures)

## By timeframe

- 5: median win rate 49%, median alpha +1.6 points, median profit factor 0.90, 27% above 1.0; no edge after costs (5100 failures)
- 15: median win rate 58%, median alpha +3.5 points, median profit factor 1.02, 55% above 1.0; near break-even (3206 failures)
- 10: median win rate 49%, median alpha +1.9 points, median profit factor 0.93, 34% above 1.0; no edge after costs (1136 failures)
- 60: median win rate 49%, median alpha +3.1 points, median profit factor 1.02, 53% above 1.0; near break-even (856 failures)
- 30: median win rate 50%, median alpha +3.0 points, median profit factor 1.00, 51% above 1.0; near break-even (850 failures)

## By entry

- market: median win rate 50%, median alpha +2.5 points, median profit factor 0.96, 42% above 1.0; near break-even (8221 failures)
- limit: median win rate 49%, median alpha +1.8 points, median profit factor 0.94, 35% above 1.0; no edge after costs (1698 failures)
- stop: median win rate 53%, median alpha +2.2 points, median profit factor 0.88, 29% above 1.0; no edge after costs (1229 failures)

## By trigger

- tr_false_break_prior_day: median win rate 61%, median alpha +4.4 points, median profit factor 1.04, 58% above 1.0; near break-even (620 failures)
- tr_keltner_reentry: median win rate 60%, median alpha +4.0 points, median profit factor 1.08, 67% above 1.0; weakly positive, below the gates (398 failures)
- tr_cci_breakout: median win rate 58%, median alpha +3.5 points, median profit factor 0.98, 46% above 1.0; near break-even (397 failures)
- tr_opening_range_break: median win rate 53%, median alpha +3.0 points, median profit factor 1.01, 54% above 1.0; near break-even (385 failures)
- tr_trail_flip: median win rate 63%, median alpha +6.2 points, median profit factor 1.14, 83% above 1.0; weakly positive, below the gates (309 failures)
- tr_internal_bar_strength: median win rate 48%, median alpha +0.7 points, median profit factor 0.90, 26% above 1.0; no edge after costs (304 failures)
- tr_failed_break: median win rate 54%, median alpha +2.7 points, median profit factor 0.99, 48% above 1.0; near break-even (296 failures)
- tr_price_ema_cross: median win rate 55%, median alpha +5.0 points, median profit factor 1.04, 55% above 1.0; near break-even (287 failures)
- tr_companion_leads_break: median win rate 50%, median alpha +1.7 points, median profit factor 0.91, 24% above 1.0; no edge after costs (263 failures)
- tr_coil_break: median win rate 50%, median alpha +1.5 points, median profit factor 0.94, 27% above 1.0; no edge after costs (232 failures)
- tr_sweep_swing: median win rate 47%, median alpha +1.1 points, median profit factor 0.88, 25% above 1.0; no edge after costs (221 failures)
- tr_bollinger_break: median win rate 57%, median alpha +3.5 points, median profit factor 1.03, 57% above 1.0; near break-even (220 failures)
- tr_low_volatility_break: median win rate 66%, median alpha +7.1 points, median profit factor 1.14, 75% above 1.0; weakly positive, below the gates (209 failures)
- tr_late_vwap_cross: median win rate 52%, median alpha +2.4 points, median profit factor 0.92, 35% above 1.0; no edge after costs (207 failures)
- tr_late_session_extreme: median win rate 58%, median alpha +6.1 points, median profit factor 1.27, 80% above 1.0; weakly positive, below the gates (205 failures)
- tr_ema_cross: median win rate 62%, median alpha +5.7 points, median profit factor 1.11, 66% above 1.0; weakly positive, below the gates (198 failures)
- tr_squeeze_release: median win rate 55%, median alpha +3.2 points, median profit factor 1.00, 50% above 1.0; near break-even (187 failures)
- tr_volume_climax_follow: median win rate 53%, median alpha +2.7 points, median profit factor 0.98, 39% above 1.0; near break-even (184 failures)
- tr_true_range_spike: median win rate 54%, median alpha +3.6 points, median profit factor 1.00, 50% above 1.0; near break-even (180 failures)
- tr_macd_zero_cross: median win rate 55%, median alpha +4.0 points, median profit factor 1.00, 51% above 1.0; near break-even (171 failures)
- tr_htf_extreme_sweep: median win rate 48%, median alpha +0.8 points, median profit factor 0.87, 31% above 1.0; no edge after costs (168 failures)
- tr_pin_bar: median win rate 44%, median alpha -0.6 points, median profit factor 0.84, 7% above 1.0; no edge after costs (163 failures)
- tr_swing_break_failure: median win rate 47%, median alpha +1.3 points, median profit factor 0.89, 19% above 1.0; no edge after costs (160 failures)
- tr_band_width_expansion: median win rate 59%, median alpha +5.2 points, median profit factor 1.11, 72% above 1.0; weakly positive, below the gates (160 failures)
- tr_engulfing: median win rate 45%, median alpha +0.6 points, median profit factor 0.86, 8% above 1.0; no edge after costs (159 failures)
- tr_initial_balance_extension: median win rate 60%, median alpha +5.3 points, median profit factor 1.10, 76% above 1.0; weakly positive, below the gates (156 failures)
- tr_double_tap: median win rate 36%, median alpha -0.2 points, median profit factor 0.85, 13% above 1.0; no edge after costs (151 failures)
- tr_relative_strength_turn: median win rate 49%, median alpha +1.7 points, median profit factor 0.97, 41% above 1.0; near break-even (148 failures)
- tr_inside_bar_break: median win rate 48%, median alpha +1.3 points, median profit factor 0.89, 24% above 1.0; no edge after costs (134 failures)
- tr_rsi_divergence: median win rate 44%, median alpha +1.2 points, median profit factor 0.90, 18% above 1.0; no edge after costs (131 failures)
