# Lessons (distilled from the graveyard)

Built from 80989 failed generations with at least 100 out-of-sample trades. Each line is a description of what failed, with its supporting count; none is a rule. Lessons learned on one timeframe or exit family may be wrong in general and are re-tested every 10,000 generations (SPEC 15.8).

Note: win-rate alpha recorded before generation 2001 used a twin that did not match target-to-stop geometry and is overstated for level-based targets (reports/gate_changes.md).

## Most common failed gates

- floor.profit_factor_pooled: 75006 failures
- sample.min_track_record_sessions: 66321 failures
- wf.median_fold_pf: 61637 failures
- floor.expectancy_in_round_trip_costs: 58727 failures
- floor.win_rate_pooled: 53149 failures
- wf.folds_with_pf_above_1: 52538 failures
- sample.wilson_lower: 51820 failures
- floor.win_rate_each_instrument: 43040 failures
- wf.in_sample_expectancy_costs: 23944 failures
- wf.worst_fold_pf: 20373 failures
- sample.trades_per_instrument: 16774 failures
- twin.random_exit_wilson_lower: 12058 failures

## By family

- trend continuation: median win rate 62%, median alpha +4.7 points, median profit factor 1.06, 63% above 1.0; weakly positive, below the gates (20031 failures)
- mean reversion to value: median win rate 50%, median alpha +1.6 points, median profit factor 0.93, 36% above 1.0; no edge after costs (9417 failures)
- breakout failure: median win rate 62%, median alpha +4.2 points, median profit factor 1.05, 60% above 1.0; near break-even (8396 failures)
- opening auction: median win rate 64%, median alpha +5.1 points, median profit factor 1.07, 68% above 1.0; weakly positive, below the gates (7477 failures)
- exhaustion: median win rate 61%, median alpha +3.7 points, median profit factor 1.02, 53% above 1.0; near break-even (7220 failures)
- volatility expansion: median win rate 60%, median alpha +4.5 points, median profit factor 1.05, 62% above 1.0; weakly positive, below the gates (6195 failures)
- inter-market lead-lag: median win rate 62%, median alpha +3.4 points, median profit factor 1.01, 52% above 1.0; near break-even (6110 failures)
- liquidity sweep and reversal: median win rate 46%, median alpha +0.7 points, median profit factor 0.87, 26% above 1.0; no edge after costs (5671 failures)
- volatility contraction: median win rate 62%, median alpha +4.0 points, median profit factor 1.03, 56% above 1.0; near break-even (5520 failures)
- closing auction: median win rate 64%, median alpha +5.8 points, median profit factor 1.10, 70% above 1.0; weakly positive, below the gates (4952 failures)

## By target

- x_target_atr: median win rate 63%, median alpha +3.8 points, median profit factor 1.04, 58% above 1.0; near break-even (27786 failures)
- x_target_r: median win rate 63%, median alpha +3.6 points, median profit factor 1.02, 55% above 1.0; near break-even (20732 failures)
- no target: median win rate 65%, median alpha +9.8 points, median profit factor 1.15, 80% above 1.0; weakly positive, below the gates (13736 failures)
- x_target_location_level: median win rate 52%, median alpha +3.3 points, median profit factor 0.99, 48% above 1.0; near break-even (6818 failures)
- x_target_prior_extreme: median win rate 42%, median alpha +1.7 points, median profit factor 0.95, 39% above 1.0; no edge after costs (3208 failures)
- x_target_opposite_range_edge: median win rate 40%, median alpha +1.5 points, median profit factor 0.86, 20% above 1.0; no edge after costs (2763 failures)
- x_target_prior_close: median win rate 41%, median alpha +2.0 points, median profit factor 1.00, 50% above 1.0; near break-even (2395 failures)
- x_target_vwap: median win rate 42%, median alpha +0.6 points, median profit factor 0.79, 8% above 1.0; no edge after costs (1778 failures)
- x_target_session_mid: median win rate 42%, median alpha +0.7 points, median profit factor 0.79, 9% above 1.0; no edge after costs (1773 failures)

## By timeframe

- 5: median win rate 64%, median alpha +4.2 points, median profit factor 1.03, 55% above 1.0; near break-even (49728 failures)
- 15: median win rate 59%, median alpha +4.2 points, median profit factor 1.06, 64% above 1.0; weakly positive, below the gates (17720 failures)
- 10: median win rate 51%, median alpha +2.0 points, median profit factor 0.96, 41% above 1.0; near break-even (5352 failures)
- 60: median win rate 50%, median alpha +3.0 points, median profit factor 1.03, 55% above 1.0; near break-even (4641 failures)
- 30: median win rate 50%, median alpha +3.0 points, median profit factor 1.00, 50% above 1.0; near break-even (3548 failures)

## By entry

- market: median win rate 56%, median alpha +3.3 points, median profit factor 1.01, 53% above 1.0; near break-even (41293 failures)
- stop: median win rate 64%, median alpha +5.6 points, median profit factor 1.05, 58% above 1.0; near break-even (21608 failures)
- limit: median win rate 60%, median alpha +3.8 points, median profit factor 1.03, 59% above 1.0; near break-even (18088 failures)

## By trigger

- tr_roc_thrust: median win rate 68%, median alpha +7.8 points, median profit factor 1.16, 82% above 1.0; weakly positive, below the gates (7464 failures)
- tr_climax_reversal: median win rate 67%, median alpha +7.2 points, median profit factor 1.14, 80% above 1.0; weakly positive, below the gates (3301 failures)
- tr_companion_leads_break: median win rate 63%, median alpha +3.7 points, median profit factor 1.00, 51% above 1.0; near break-even (3183 failures)
- tr_opening_drive: median win rate 67%, median alpha +7.3 points, median profit factor 1.13, 80% above 1.0; weakly positive, below the gates (2911 failures)
- tr_false_break_prior_day: median win rate 63%, median alpha +4.4 points, median profit factor 1.05, 60% above 1.0; near break-even (2563 failures)
- tr_opening_range_break: median win rate 59%, median alpha +3.4 points, median profit factor 1.01, 56% above 1.0; near break-even (2490 failures)
- tr_band_break_failure: median win rate 67%, median alpha +8.7 points, median profit factor 1.16, 81% above 1.0; weakly positive, below the gates (2458 failures)
- tr_cci_breakout: median win rate 62%, median alpha +3.0 points, median profit factor 0.96, 39% above 1.0; near break-even (2171 failures)
- tr_band_width_expansion: median win rate 61%, median alpha +6.8 points, median profit factor 1.15, 84% above 1.0; weakly positive, below the gates (2152 failures)
- tr_keltner_reentry: median win rate 62%, median alpha +3.8 points, median profit factor 1.05, 63% above 1.0; weakly positive, below the gates (2085 failures)
- tr_late_session_extreme: median win rate 65%, median alpha +6.8 points, median profit factor 1.15, 80% above 1.0; weakly positive, below the gates (1929 failures)
- tr_failed_break: median win rate 58%, median alpha +2.9 points, median profit factor 1.02, 54% above 1.0; near break-even (1859 failures)
- tr_close_extreme_fade: median win rate 65%, median alpha +7.0 points, median profit factor 1.11, 78% above 1.0; weakly positive, below the gates (1750 failures)
- tr_low_volatility_break: median win rate 67%, median alpha +7.5 points, median profit factor 1.14, 76% above 1.0; weakly positive, below the gates (1592 failures)
- tr_bollinger_break: median win rate 61%, median alpha +3.6 points, median profit factor 1.02, 56% above 1.0; near break-even (1589 failures)
- tr_squeeze_release: median win rate 63%, median alpha +4.0 points, median profit factor 1.05, 61% above 1.0; near break-even (1585 failures)
- tr_engulfing: median win rate 56%, median alpha +2.1 points, median profit factor 0.96, 40% above 1.0; near break-even (1421 failures)
- tr_relative_strength_turn: median win rate 62%, median alpha +3.8 points, median profit factor 1.04, 59% above 1.0; near break-even (1420 failures)
- tr_ema_cross: median win rate 64%, median alpha +5.8 points, median profit factor 1.14, 78% above 1.0; weakly positive, below the gates (1349 failures)
- tr_internal_bar_strength: median win rate 53%, median alpha +1.8 points, median profit factor 0.93, 36% above 1.0; no edge after costs (1328 failures)
- tr_trail_flip: median win rate 67%, median alpha +6.6 points, median profit factor 1.15, 82% above 1.0; weakly positive, below the gates (1273 failures)
- tr_late_vwap_cross: median win rate 56%, median alpha +2.6 points, median profit factor 0.96, 41% above 1.0; near break-even (1052 failures)
- tr_gap_and_go: median win rate 69%, median alpha +8.1 points, median profit factor 1.18, 81% above 1.0; weakly positive, below the gates (1042 failures)
- tr_volume_climax_follow: median win rate 59%, median alpha +2.8 points, median profit factor 0.97, 41% above 1.0; near break-even (921 failures)
- tr_coil_break: median win rate 51%, median alpha +1.5 points, median profit factor 0.92, 29% above 1.0; no edge after costs (910 failures)
- tr_htf_extreme_sweep: median win rate 49%, median alpha +0.5 points, median profit factor 0.87, 25% above 1.0; no edge after costs (857 failures)
- tr_keltner_break: median win rate 54%, median alpha +3.6 points, median profit factor 1.04, 59% above 1.0; near break-even (819 failures)
- tr_inside_bar_break: median win rate 54%, median alpha +2.7 points, median profit factor 0.97, 43% above 1.0; near break-even (814 failures)
- tr_price_ema_cross: median win rate 55%, median alpha +3.9 points, median profit factor 1.00, 51% above 1.0; near break-even (800 failures)
- tr_range_expansion_break: median win rate 63%, median alpha +5.1 points, median profit factor 1.03, 63% above 1.0; near break-even (710 failures)
