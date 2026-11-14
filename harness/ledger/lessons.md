# Lessons (distilled from the graveyard)

Built from 23286 failed generations with at least 100 out-of-sample trades. Each line is a description of what failed, with its supporting count; none is a rule. Lessons learned on one timeframe or exit family may be wrong in general and are re-tested every 10,000 generations (SPEC 15.8).

Note: win-rate alpha recorded before generation 2001 used a twin that did not match target-to-stop geometry and is overstated for level-based targets (reports/gate_changes.md).

## Most common failed gates

- floor.profit_factor_pooled: 22395 failures
- sample.min_track_record_sessions: 21228 failures
- floor.win_rate_pooled: 18558 failures
- floor.expectancy_in_round_trip_costs: 18472 failures
- sample.wilson_lower: 18463 failures
- wf.median_fold_pf: 17571 failures
- wf.folds_with_pf_above_1: 17091 failures
- floor.win_rate_each_instrument: 16030 failures
- sample.trades_per_instrument: 5819 failures
- wf.worst_fold_pf: 4821 failures
- sample.trades_per_fold_per_instrument: 4110 failures
- sample.trades_per_complexity_point: 2499 failures

## By family

- trend continuation: median win rate 54%, median alpha +3.7 points, median profit factor 1.00, 51% above 1.0; near break-even (5079 failures)
- mean reversion to value: median win rate 49%, median alpha +1.4 points, median profit factor 0.93, 35% above 1.0; no edge after costs (3562 failures)
- breakout failure: median win rate 57%, median alpha +3.0 points, median profit factor 0.99, 48% above 1.0; near break-even (2569 failures)
- liquidity sweep and reversal: median win rate 45%, median alpha +0.4 points, median profit factor 0.85, 21% above 1.0; no edge after costs (2314 failures)
- volatility expansion: median win rate 58%, median alpha +3.6 points, median profit factor 1.01, 52% above 1.0; near break-even (1996 failures)
- opening auction: median win rate 59%, median alpha +3.7 points, median profit factor 1.02, 57% above 1.0; near break-even (1867 failures)
- volatility contraction: median win rate 54%, median alpha +3.0 points, median profit factor 0.97, 43% above 1.0; near break-even (1786 failures)
- exhaustion: median win rate 47%, median alpha +0.7 points, median profit factor 0.88, 19% above 1.0; no edge after costs (1621 failures)
- inter-market lead-lag: median win rate 52%, median alpha +1.6 points, median profit factor 0.93, 30% above 1.0; no edge after costs (1450 failures)
- closing auction: median win rate 57%, median alpha +3.4 points, median profit factor 1.01, 52% above 1.0; near break-even (1042 failures)

## By target

- x_target_atr: median win rate 58%, median alpha +2.7 points, median profit factor 0.98, 46% above 1.0; near break-even (8019 failures)
- x_target_r: median win rate 62%, median alpha +2.8 points, median profit factor 0.98, 46% above 1.0; near break-even (6929 failures)
- x_target_location_level: median win rate 50%, median alpha +2.8 points, median profit factor 0.96, 40% above 1.0; near break-even (2580 failures)
- x_target_prior_extreme: median win rate 42%, median alpha +1.9 points, median profit factor 0.96, 41% above 1.0; near break-even (1259 failures)
- x_target_opposite_range_edge: median win rate 40%, median alpha +1.6 points, median profit factor 0.87, 21% above 1.0; no edge after costs (1143 failures)
- x_target_prior_close: median win rate 40%, median alpha +1.9 points, median profit factor 1.00, 50% above 1.0; near break-even (1007 failures)
- no target: median win rate 50%, median alpha +3.3 points, median profit factor 1.01, 52% above 1.0; near break-even (827 failures)
- x_target_vwap: median win rate 41%, median alpha +0.8 points, median profit factor 0.80, 7% above 1.0; no edge after costs (786 failures)
- x_target_session_mid: median win rate 41%, median alpha +1.0 points, median profit factor 0.80, 9% above 1.0; no edge after costs (736 failures)

## By timeframe

- 5: median win rate 52%, median alpha +1.9 points, median profit factor 0.92, 31% above 1.0; no edge after costs (11493 failures)
- 15: median win rate 60%, median alpha +3.6 points, median profit factor 1.03, 57% above 1.0; near break-even (6659 failures)
- 10: median win rate 50%, median alpha +2.0 points, median profit factor 0.95, 36% above 1.0; no edge after costs (2085 failures)
- 60: median win rate 49%, median alpha +2.9 points, median profit factor 1.02, 53% above 1.0; near break-even (1667 failures)
- 30: median win rate 50%, median alpha +3.1 points, median profit factor 1.01, 52% above 1.0; near break-even (1382 failures)

## By entry

- market: median win rate 52%, median alpha +2.7 points, median profit factor 0.98, 45% above 1.0; near break-even (14786 failures)
- limit: median win rate 52%, median alpha +2.3 points, median profit factor 0.96, 41% above 1.0; near break-even (4608 failures)
- stop: median win rate 55%, median alpha +2.3 points, median profit factor 0.89, 30% above 1.0; no edge after costs (3892 failures)

## By trigger

- tr_false_break_prior_day: median win rate 62%, median alpha +4.2 points, median profit factor 1.03, 56% above 1.0; near break-even (1201 failures)
- tr_keltner_reentry: median win rate 62%, median alpha +4.2 points, median profit factor 1.08, 68% above 1.0; weakly positive, below the gates (931 failures)
- tr_opening_range_break: median win rate 58%, median alpha +2.9 points, median profit factor 1.00, 52% above 1.0; near break-even (928 failures)
- tr_trail_flip: median win rate 67%, median alpha +6.6 points, median profit factor 1.16, 82% above 1.0; weakly positive, below the gates (830 failures)
- tr_cci_breakout: median win rate 60%, median alpha +2.9 points, median profit factor 0.95, 37% above 1.0; no edge after costs (780 failures)
- tr_failed_break: median win rate 56%, median alpha +2.9 points, median profit factor 1.00, 49% above 1.0; near break-even (724 failures)
- tr_companion_leads_break: median win rate 52%, median alpha +1.6 points, median profit factor 0.92, 20% above 1.0; no edge after costs (661 failures)
- tr_internal_bar_strength: median win rate 50%, median alpha +1.4 points, median profit factor 0.92, 30% above 1.0; no edge after costs (589 failures)
- tr_low_volatility_break: median win rate 64%, median alpha +6.8 points, median profit factor 1.12, 71% above 1.0; weakly positive, below the gates (531 failures)
- tr_late_vwap_cross: median win rate 55%, median alpha +2.4 points, median profit factor 0.94, 37% above 1.0; no edge after costs (524 failures)
- tr_bollinger_break: median win rate 59%, median alpha +3.2 points, median profit factor 1.00, 52% above 1.0; near break-even (522 failures)
- tr_price_ema_cross: median win rate 56%, median alpha +4.3 points, median profit factor 1.03, 53% above 1.0; near break-even (497 failures)
- tr_engulfing: median win rate 49%, median alpha +1.1 points, median profit factor 0.89, 23% above 1.0; no edge after costs (487 failures)
- tr_coil_break: median win rate 49%, median alpha +0.9 points, median profit factor 0.91, 21% above 1.0; no edge after costs (427 failures)
- tr_relative_strength_turn: median win rate 55%, median alpha +2.6 points, median profit factor 1.00, 49% above 1.0; near break-even (409 failures)
- tr_band_width_expansion: median win rate 63%, median alpha +5.8 points, median profit factor 1.11, 74% above 1.0; weakly positive, below the gates (403 failures)
- tr_volume_climax_follow: median win rate 56%, median alpha +2.8 points, median profit factor 0.98, 41% above 1.0; near break-even (400 failures)
- tr_squeeze_release: median win rate 55%, median alpha +3.3 points, median profit factor 1.03, 54% above 1.0; near break-even (388 failures)
- tr_htf_extreme_sweep: median win rate 49%, median alpha +0.4 points, median profit factor 0.86, 27% above 1.0; no edge after costs (374 failures)
- tr_ema_cross: median win rate 64%, median alpha +5.7 points, median profit factor 1.10, 68% above 1.0; weakly positive, below the gates (365 failures)
- tr_sweep_swing: median win rate 48%, median alpha +1.2 points, median profit factor 0.88, 27% above 1.0; no edge after costs (347 failures)
- tr_opening_drive: median win rate 66%, median alpha +5.4 points, median profit factor 1.08, 75% above 1.0; weakly positive, below the gates (340 failures)
- tr_late_session_extreme: median win rate 60%, median alpha +5.9 points, median profit factor 1.25, 78% above 1.0; weakly positive, below the gates (311 failures)
- tr_true_range_spike: median win rate 59%, median alpha +4.6 points, median profit factor 1.02, 57% above 1.0; near break-even (310 failures)
- tr_macd_zero_cross: median win rate 56%, median alpha +3.6 points, median profit factor 0.99, 47% above 1.0; near break-even (297 failures)
- tr_swing_break_failure: median win rate 49%, median alpha +1.3 points, median profit factor 0.91, 22% above 1.0; no edge after costs (290 failures)
- tr_pin_bar: median win rate 46%, median alpha -0.2 points, median profit factor 0.85, 9% above 1.0; no edge after costs (287 failures)
- tr_initial_balance_extension: median win rate 60%, median alpha +5.3 points, median profit factor 1.08, 72% above 1.0; weakly positive, below the gates (284 failures)
- tr_rsi2_extreme: median win rate 48%, median alpha -0.7 points, median profit factor 0.83, 4% above 1.0; no edge after costs (269 failures)
- tr_inside_bar_break: median win rate 49%, median alpha +1.8 points, median profit factor 0.90, 24% above 1.0; no edge after costs (258 failures)
