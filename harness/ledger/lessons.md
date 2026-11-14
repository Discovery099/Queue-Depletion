# Lessons (distilled from the graveyard)

Built from 39628 failed generations with at least 100 out-of-sample trades. Each line is a description of what failed, with its supporting count; none is a rule. Lessons learned on one timeframe or exit family may be wrong in general and are re-tested every 10,000 generations (SPEC 15.8).

Note: win-rate alpha recorded before generation 2001 used a twin that did not match target-to-stop geometry and is overstated for level-based targets (reports/gate_changes.md).

## Most common failed gates

- floor.profit_factor_pooled: 37928 failures
- sample.min_track_record_sessions: 35379 failures
- floor.expectancy_in_round_trip_costs: 31010 failures
- wf.median_fold_pf: 30449 failures
- floor.win_rate_pooled: 29649 failures
- sample.wilson_lower: 29235 failures
- wf.folds_with_pf_above_1: 28345 failures
- floor.win_rate_each_instrument: 24809 failures
- wf.worst_fold_pf: 9254 failures
- sample.trades_per_instrument: 9144 failures
- wf.in_sample_expectancy_costs: 6856 failures
- sample.trades_per_fold_per_instrument: 6461 failures

## By family

- trend continuation: median win rate 58%, median alpha +3.9 points, median profit factor 1.03, 54% above 1.0; near break-even (8900 failures)
- mean reversion to value: median win rate 50%, median alpha +1.5 points, median profit factor 0.93, 36% above 1.0; no edge after costs (5537 failures)
- breakout failure: median win rate 59%, median alpha +3.3 points, median profit factor 1.01, 52% above 1.0; near break-even (4253 failures)
- opening auction: median win rate 62%, median alpha +4.3 points, median profit factor 1.04, 63% above 1.0; near break-even (3678 failures)
- liquidity sweep and reversal: median win rate 46%, median alpha +0.5 points, median profit factor 0.86, 23% above 1.0; no edge after costs (3379 failures)
- volatility expansion: median win rate 59%, median alpha +3.7 points, median profit factor 1.01, 53% above 1.0; near break-even (3276 failures)
- exhaustion: median win rate 53%, median alpha +2.0 points, median profit factor 0.93, 36% above 1.0; no edge after costs (3206 failures)
- volatility contraction: median win rate 57%, median alpha +3.3 points, median profit factor 0.98, 46% above 1.0; near break-even (2815 failures)
- inter-market lead-lag: median win rate 54%, median alpha +1.9 points, median profit factor 0.95, 35% above 1.0; no edge after costs (2672 failures)
- closing auction: median win rate 60%, median alpha +3.9 points, median profit factor 1.02, 57% above 1.0; near break-even (1912 failures)

## By target

- x_target_atr: median win rate 60%, median alpha +3.1 points, median profit factor 1.00, 50% above 1.0; near break-even (14219 failures)
- x_target_r: median win rate 63%, median alpha +3.2 points, median profit factor 1.00, 50% above 1.0; near break-even (11339 failures)
- x_target_location_level: median win rate 51%, median alpha +3.1 points, median profit factor 0.98, 44% above 1.0; near break-even (4137 failures)
- no target: median win rate 60%, median alpha +5.2 points, median profit factor 1.06, 62% above 1.0; weakly positive, below the gates (2735 failures)
- x_target_prior_extreme: median win rate 43%, median alpha +1.9 points, median profit factor 0.96, 41% above 1.0; near break-even (1876 failures)
- x_target_opposite_range_edge: median win rate 40%, median alpha +1.5 points, median profit factor 0.86, 20% above 1.0; no edge after costs (1680 failures)
- x_target_prior_close: median win rate 41%, median alpha +2.0 points, median profit factor 1.00, 51% above 1.0; near break-even (1477 failures)
- x_target_vwap: median win rate 42%, median alpha +0.7 points, median profit factor 0.80, 7% above 1.0; no edge after costs (1091 failures)
- x_target_session_mid: median win rate 41%, median alpha +0.8 points, median profit factor 0.79, 9% above 1.0; no edge after costs (1074 failures)

## By timeframe

- 5: median win rate 57%, median alpha +2.5 points, median profit factor 0.95, 39% above 1.0; no edge after costs (21272 failures)
- 15: median win rate 61%, median alpha +3.9 points, median profit factor 1.04, 60% above 1.0; near break-even (10617 failures)
- 10: median win rate 51%, median alpha +2.1 points, median profit factor 0.96, 40% above 1.0; near break-even (3111 failures)
- 60: median win rate 49%, median alpha +2.9 points, median profit factor 1.02, 54% above 1.0; near break-even (2613 failures)
- 30: median win rate 50%, median alpha +3.0 points, median profit factor 1.00, 51% above 1.0; near break-even (2015 failures)

## By entry

- market: median win rate 54%, median alpha +2.8 points, median profit factor 0.99, 48% above 1.0; near break-even (22875 failures)
- stop: median win rate 60%, median alpha +3.3 points, median profit factor 0.95, 41% above 1.0; near break-even (8400 failures)
- limit: median win rate 55%, median alpha +2.8 points, median profit factor 0.99, 47% above 1.0; near break-even (8353 failures)

## By trigger

- tr_false_break_prior_day: median win rate 63%, median alpha +4.3 points, median profit factor 1.04, 58% above 1.0; near break-even (1786 failures)
- tr_opening_range_break: median win rate 58%, median alpha +3.0 points, median profit factor 1.01, 53% above 1.0; near break-even (1435 failures)
- tr_roc_thrust: median win rate 66%, median alpha +6.3 points, median profit factor 1.10, 74% above 1.0; weakly positive, below the gates (1421 failures)
- tr_opening_drive: median win rate 67%, median alpha +6.3 points, median profit factor 1.11, 78% above 1.0; weakly positive, below the gates (1381 failures)
- tr_keltner_reentry: median win rate 62%, median alpha +3.9 points, median profit factor 1.06, 65% above 1.0; weakly positive, below the gates (1351 failures)
- tr_cci_breakout: median win rate 61%, median alpha +2.9 points, median profit factor 0.95, 36% above 1.0; near break-even (1290 failures)
- tr_companion_leads_break: median win rate 57%, median alpha +1.9 points, median profit factor 0.94, 26% above 1.0; no edge after costs (1178 failures)
- tr_failed_break: median win rate 57%, median alpha +2.8 points, median profit factor 1.00, 49% above 1.0; near break-even (1132 failures)
- tr_trail_flip: median win rate 67%, median alpha +6.5 points, median profit factor 1.15, 82% above 1.0; weakly positive, below the gates (976 failures)
- tr_bollinger_break: median win rate 60%, median alpha +3.4 points, median profit factor 1.01, 53% above 1.0; near break-even (967 failures)
- tr_internal_bar_strength: median win rate 52%, median alpha +1.9 points, median profit factor 0.93, 34% above 1.0; no edge after costs (910 failures)
- tr_climax_reversal: median win rate 65%, median alpha +5.7 points, median profit factor 1.08, 70% above 1.0; weakly positive, below the gates (863 failures)
- tr_ema_cross: median win rate 66%, median alpha +5.9 points, median profit factor 1.15, 75% above 1.0; weakly positive, below the gates (857 failures)
- tr_engulfing: median win rate 52%, median alpha +1.7 points, median profit factor 0.92, 32% above 1.0; no edge after costs (811 failures)
- tr_low_volatility_break: median win rate 65%, median alpha +6.8 points, median profit factor 1.11, 70% above 1.0; weakly positive, below the gates (810 failures)
- tr_late_vwap_cross: median win rate 55%, median alpha +2.5 points, median profit factor 0.95, 39% above 1.0; near break-even (778 failures)
- tr_relative_strength_turn: median win rate 60%, median alpha +3.3 points, median profit factor 1.01, 53% above 1.0; near break-even (768 failures)
- tr_squeeze_release: median win rate 59%, median alpha +3.6 points, median profit factor 1.02, 55% above 1.0; near break-even (765 failures)
- tr_band_width_expansion: median win rate 63%, median alpha +6.2 points, median profit factor 1.12, 76% above 1.0; weakly positive, below the gates (678 failures)
- tr_volume_climax_follow: median win rate 58%, median alpha +2.7 points, median profit factor 0.97, 40% above 1.0; near break-even (674 failures)
- tr_price_ema_cross: median win rate 56%, median alpha +3.9 points, median profit factor 1.02, 52% above 1.0; near break-even (620 failures)
- tr_late_session_extreme: median win rate 63%, median alpha +6.0 points, median profit factor 1.15, 76% above 1.0; weakly positive, below the gates (589 failures)
- tr_htf_extreme_sweep: median win rate 49%, median alpha +0.3 points, median profit factor 0.86, 26% above 1.0; no edge after costs (583 failures)
- tr_coil_break: median win rate 50%, median alpha +0.9 points, median profit factor 0.89, 21% above 1.0; no edge after costs (574 failures)
- tr_keltner_break: median win rate 55%, median alpha +3.8 points, median profit factor 1.05, 57% above 1.0; near break-even (455 failures)
- tr_band_break_failure: median win rate 67%, median alpha +7.5 points, median profit factor 1.16, 77% above 1.0; weakly positive, below the gates (451 failures)
- tr_sweep_swing: median win rate 50%, median alpha +1.2 points, median profit factor 0.87, 25% above 1.0; no edge after costs (444 failures)
- tr_close_extreme_fade: median win rate 63%, median alpha +5.0 points, median profit factor 1.04, 66% above 1.0; near break-even (432 failures)
- tr_rsi2_extreme: median win rate 49%, median alpha -0.4 points, median profit factor 0.84, 9% above 1.0; no edge after costs (426 failures)
- tr_companion_reclaim: median win rate 48%, median alpha +0.3 points, median profit factor 0.88, 24% above 1.0; no edge after costs (422 failures)
