# Lessons (distilled from the graveyard)

Built from 15919 failed generations with at least 100 out-of-sample trades. Each line is a description of what failed, with its supporting count; none is a rule. Lessons learned on one timeframe or exit family may be wrong in general and are re-tested every 10,000 generations (SPEC 15.8).

Note: win-rate alpha recorded before generation 2001 used a twin that did not match target-to-stop geometry and is overstated for level-based targets (reports/gate_changes.md).

## Most common failed gates

- floor.profit_factor_pooled: 15290 failures
- sample.min_track_record_sessions: 14523 failures
- floor.win_rate_pooled: 13069 failures
- sample.wilson_lower: 13058 failures
- floor.expectancy_in_round_trip_costs: 12507 failures
- wf.median_fold_pf: 11797 failures
- wf.folds_with_pf_above_1: 11649 failures
- floor.win_rate_each_instrument: 11532 failures
- sample.trades_per_instrument: 4197 failures
- sample.trades_per_fold_per_instrument: 2949 failures
- wf.worst_fold_pf: 2929 failures
- sample.trades_per_complexity_point: 1711 failures

## By family

- trend continuation: median win rate 53%, median alpha +3.8 points, median profit factor 1.00, 51% above 1.0; near break-even (3535 failures)
- mean reversion to value: median win rate 48%, median alpha +1.3 points, median profit factor 0.92, 34% above 1.0; no edge after costs (2559 failures)
- breakout failure: median win rate 56%, median alpha +3.0 points, median profit factor 0.99, 47% above 1.0; near break-even (1842 failures)
- liquidity sweep and reversal: median win rate 44%, median alpha +0.4 points, median profit factor 0.85, 20% above 1.0; no edge after costs (1698 failures)
- volatility expansion: median win rate 56%, median alpha +3.5 points, median profit factor 1.00, 50% above 1.0; near break-even (1284 failures)
- volatility contraction: median win rate 53%, median alpha +2.9 points, median profit factor 0.97, 43% above 1.0; near break-even (1233 failures)
- opening auction: median win rate 56%, median alpha +3.5 points, median profit factor 1.02, 57% above 1.0; near break-even (1132 failures)
- exhaustion: median win rate 46%, median alpha +0.4 points, median profit factor 0.86, 15% above 1.0; no edge after costs (1085 failures)
- inter-market lead-lag: median win rate 50%, median alpha +1.3 points, median profit factor 0.91, 26% above 1.0; no edge after costs (870 failures)
- closing auction: median win rate 56%, median alpha +3.5 points, median profit factor 1.01, 53% above 1.0; near break-even (681 failures)

## By target

- x_target_atr: median win rate 57%, median alpha +2.7 points, median profit factor 0.98, 47% above 1.0; near break-even (5540 failures)
- x_target_r: median win rate 61%, median alpha +2.6 points, median profit factor 0.97, 45% above 1.0; near break-even (4572 failures)
- x_target_location_level: median win rate 50%, median alpha +2.6 points, median profit factor 0.95, 39% above 1.0; near break-even (1764 failures)
- x_target_prior_extreme: median win rate 42%, median alpha +1.9 points, median profit factor 0.96, 41% above 1.0; near break-even (935 failures)
- x_target_opposite_range_edge: median win rate 40%, median alpha +1.5 points, median profit factor 0.86, 20% above 1.0; no edge after costs (893 failures)
- x_target_prior_close: median win rate 40%, median alpha +1.9 points, median profit factor 0.99, 47% above 1.0; near break-even (744 failures)
- x_target_vwap: median win rate 41%, median alpha +0.7 points, median profit factor 0.79, 6% above 1.0; no edge after costs (617 failures)
- x_target_session_mid: median win rate 41%, median alpha +1.3 points, median profit factor 0.80, 9% above 1.0; no edge after costs (567 failures)
- no target: median win rate 47%, median alpha +3.0 points, median profit factor 0.99, 48% above 1.0; near break-even (287 failures)

## By timeframe

- 5: median win rate 50%, median alpha +1.7 points, median profit factor 0.90, 28% above 1.0; no edge after costs (7464 failures)
- 15: median win rate 59%, median alpha +3.6 points, median profit factor 1.03, 56% above 1.0; near break-even (4651 failures)
- 10: median win rate 49%, median alpha +1.9 points, median profit factor 0.94, 35% above 1.0; no edge after costs (1560 failures)
- 60: median win rate 49%, median alpha +2.9 points, median profit factor 1.02, 53% above 1.0; near break-even (1149 failures)
- 30: median win rate 50%, median alpha +3.2 points, median profit factor 1.01, 52% above 1.0; near break-even (1095 failures)

## By entry

- market: median win rate 51%, median alpha +2.6 points, median profit factor 0.97, 44% above 1.0; near break-even (10912 failures)
- limit: median win rate 51%, median alpha +2.0 points, median profit factor 0.95, 39% above 1.0; near break-even (2783 failures)
- stop: median win rate 53%, median alpha +2.1 points, median profit factor 0.88, 28% above 1.0; no edge after costs (2224 failures)

## By trigger

- tr_false_break_prior_day: median win rate 62%, median alpha +4.1 points, median profit factor 1.03, 56% above 1.0; near break-even (875 failures)
- tr_keltner_reentry: median win rate 62%, median alpha +4.3 points, median profit factor 1.09, 68% above 1.0; weakly positive, below the gates (626 failures)
- tr_trail_flip: median win rate 67%, median alpha +6.6 points, median profit factor 1.16, 84% above 1.0; weakly positive, below the gates (577 failures)
- tr_opening_range_break: median win rate 55%, median alpha +2.9 points, median profit factor 1.00, 52% above 1.0; near break-even (560 failures)
- tr_cci_breakout: median win rate 58%, median alpha +3.1 points, median profit factor 0.96, 40% above 1.0; near break-even (558 failures)
- tr_failed_break: median win rate 55%, median alpha +2.8 points, median profit factor 1.00, 50% above 1.0; near break-even (496 failures)
- tr_internal_bar_strength: median win rate 49%, median alpha +1.2 points, median profit factor 0.92, 26% above 1.0; no edge after costs (436 failures)
- tr_companion_leads_break: median win rate 51%, median alpha +1.6 points, median profit factor 0.91, 21% above 1.0; no edge after costs (403 failures)
- tr_price_ema_cross: median win rate 56%, median alpha +5.0 points, median profit factor 1.05, 56% above 1.0; near break-even (386 failures)
- tr_late_vwap_cross: median win rate 54%, median alpha +2.3 points, median profit factor 0.93, 36% above 1.0; no edge after costs (341 failures)
- tr_low_volatility_break: median win rate 64%, median alpha +7.2 points, median profit factor 1.14, 74% above 1.0; weakly positive, below the gates (336 failures)
- tr_bollinger_break: median win rate 58%, median alpha +3.3 points, median profit factor 1.01, 54% above 1.0; near break-even (330 failures)
- tr_coil_break: median win rate 50%, median alpha +1.3 points, median profit factor 0.93, 23% above 1.0; no edge after costs (313 failures)
- tr_ema_cross: median win rate 62%, median alpha +5.6 points, median profit factor 1.11, 66% above 1.0; weakly positive, below the gates (277 failures)
- tr_sweep_swing: median win rate 48%, median alpha +1.2 points, median profit factor 0.88, 26% above 1.0; no edge after costs (272 failures)
- tr_squeeze_release: median win rate 55%, median alpha +3.2 points, median profit factor 1.01, 51% above 1.0; near break-even (267 failures)
- tr_engulfing: median win rate 47%, median alpha +0.6 points, median profit factor 0.87, 16% above 1.0; no edge after costs (264 failures)
- tr_true_range_spike: median win rate 57%, median alpha +4.6 points, median profit factor 1.02, 56% above 1.0; near break-even (264 failures)
- tr_late_session_extreme: median win rate 59%, median alpha +5.9 points, median profit factor 1.25, 78% above 1.0; weakly positive, below the gates (256 failures)
- tr_htf_extreme_sweep: median win rate 49%, median alpha +0.6 points, median profit factor 0.86, 28% above 1.0; no edge after costs (253 failures)
- tr_volume_climax_follow: median win rate 53%, median alpha +2.5 points, median profit factor 0.96, 35% above 1.0; near break-even (250 failures)
- tr_macd_zero_cross: median win rate 56%, median alpha +3.6 points, median profit factor 0.99, 48% above 1.0; near break-even (228 failures)
- tr_relative_strength_turn: median win rate 51%, median alpha +1.7 points, median profit factor 0.97, 42% above 1.0; near break-even (227 failures)
- tr_pin_bar: median win rate 46%, median alpha -0.4 points, median profit factor 0.85, 8% above 1.0; no edge after costs (225 failures)
- tr_band_width_expansion: median win rate 60%, median alpha +5.0 points, median profit factor 1.10, 71% above 1.0; weakly positive, below the gates (223 failures)
- tr_swing_break_failure: median win rate 48%, median alpha +1.1 points, median profit factor 0.89, 18% above 1.0; no edge after costs (221 failures)
- tr_initial_balance_extension: median win rate 60%, median alpha +5.4 points, median profit factor 1.10, 74% above 1.0; weakly positive, below the gates (216 failures)
- tr_double_tap: median win rate 37%, median alpha -0.1 points, median profit factor 0.85, 13% above 1.0; no edge after costs (193 failures)
- tr_inside_bar_break: median win rate 48%, median alpha +1.6 points, median profit factor 0.90, 23% above 1.0; no edge after costs (184 failures)
- tr_rsi2_extreme: median win rate 46%, median alpha -1.1 points, median profit factor 0.81, 5% above 1.0; no edge after costs (180 failures)
