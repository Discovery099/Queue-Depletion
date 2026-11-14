# Lessons (distilled from the graveyard)

Built from 56211 failed generations with at least 100 out-of-sample trades. Each line is a description of what failed, with its supporting count; none is a rule. Lessons learned on one timeframe or exit family may be wrong in general and are re-tested every 10,000 generations (SPEC 15.8).

Note: win-rate alpha recorded before generation 2001 used a twin that did not match target-to-stop geometry and is overstated for level-based targets (reports/gate_changes.md).

## Most common failed gates

- floor.profit_factor_pooled: 53039 failures
- sample.min_track_record_sessions: 48429 failures
- wf.median_fold_pf: 43116 failures
- floor.expectancy_in_round_trip_costs: 42536 failures
- floor.win_rate_pooled: 39686 failures
- sample.wilson_lower: 38888 failures
- wf.folds_with_pf_above_1: 38566 failures
- floor.win_rate_each_instrument: 32633 failures
- wf.worst_fold_pf: 13791 failures
- wf.in_sample_expectancy_costs: 13056 failures
- sample.trades_per_instrument: 12207 failures
- sample.trades_per_fold_per_instrument: 8631 failures

## By family

- trend continuation: median win rate 60%, median alpha +4.2 points, median profit factor 1.04, 58% above 1.0; near break-even (13084 failures)
- mean reversion to value: median win rate 50%, median alpha +1.6 points, median profit factor 0.93, 37% above 1.0; no edge after costs (7232 failures)
- breakout failure: median win rate 61%, median alpha +3.7 points, median profit factor 1.03, 56% above 1.0; near break-even (5945 failures)
- opening auction: median win rate 63%, median alpha +4.7 points, median profit factor 1.05, 65% above 1.0; weakly positive, below the gates (5236 failures)
- exhaustion: median win rate 58%, median alpha +2.8 points, median profit factor 0.98, 46% above 1.0; near break-even (4832 failures)
- volatility expansion: median win rate 59%, median alpha +3.9 points, median profit factor 1.02, 57% above 1.0; near break-even (4450 failures)
- liquidity sweep and reversal: median win rate 46%, median alpha +0.6 points, median profit factor 0.87, 24% above 1.0; no edge after costs (4404 failures)
- inter-market lead-lag: median win rate 59%, median alpha +2.7 points, median profit factor 0.98, 44% above 1.0; near break-even (4043 failures)
- volatility contraction: median win rate 60%, median alpha +3.6 points, median profit factor 1.00, 50% above 1.0; near break-even (3895 failures)
- closing auction: median win rate 61%, median alpha +4.9 points, median profit factor 1.07, 64% above 1.0; weakly positive, below the gates (3090 failures)

## By target

- x_target_atr: median win rate 61%, median alpha +3.4 points, median profit factor 1.02, 54% above 1.0; near break-even (20122 failures)
- x_target_r: median win rate 63%, median alpha +3.4 points, median profit factor 1.01, 52% above 1.0; near break-even (15172 failures)
- no target: median win rate 64%, median alpha +7.6 points, median profit factor 1.11, 74% above 1.0; weakly positive, below the gates (6366 failures)
- x_target_location_level: median win rate 51%, median alpha +3.2 points, median profit factor 0.99, 47% above 1.0; near break-even (5382 failures)
- x_target_prior_extreme: median win rate 42%, median alpha +1.8 points, median profit factor 0.95, 40% above 1.0; near break-even (2463 failures)
- x_target_opposite_range_edge: median win rate 40%, median alpha +1.5 points, median profit factor 0.86, 20% above 1.0; no edge after costs (2133 failures)
- x_target_prior_close: median win rate 41%, median alpha +1.9 points, median profit factor 1.00, 51% above 1.0; near break-even (1865 failures)
- x_target_session_mid: median win rate 41%, median alpha +0.7 points, median profit factor 0.79, 9% above 1.0; no edge after costs (1359 failures)
- x_target_vwap: median win rate 42%, median alpha +0.7 points, median profit factor 0.79, 7% above 1.0; no edge after costs (1349 failures)

## By timeframe

- 5: median win rate 61%, median alpha +3.3 points, median profit factor 0.98, 47% above 1.0; near break-even (32188 failures)
- 15: median win rate 60%, median alpha +4.1 points, median profit factor 1.05, 62% above 1.0; weakly positive, below the gates (13712 failures)
- 10: median win rate 51%, median alpha +2.1 points, median profit factor 0.96, 41% above 1.0; near break-even (4191 failures)
- 60: median win rate 50%, median alpha +3.0 points, median profit factor 1.03, 55% above 1.0; near break-even (3452 failures)
- 30: median win rate 50%, median alpha +3.0 points, median profit factor 1.00, 51% above 1.0; near break-even (2668 failures)

## By entry

- market: median win rate 54%, median alpha +3.0 points, median profit factor 1.00, 50% above 1.0; near break-even (30191 failures)
- stop: median win rate 62%, median alpha +4.6 points, median profit factor 1.01, 51% above 1.0; near break-even (13835 failures)
- limit: median win rate 57%, median alpha +3.3 points, median profit factor 1.01, 53% above 1.0; near break-even (12185 failures)

## By trigger

- tr_roc_thrust: median win rate 67%, median alpha +7.2 points, median profit factor 1.13, 78% above 1.0; weakly positive, below the gates (3398 failures)
- tr_false_break_prior_day: median win rate 63%, median alpha +4.3 points, median profit factor 1.04, 60% above 1.0; near break-even (2157 failures)
- tr_opening_drive: median win rate 67%, median alpha +6.6 points, median profit factor 1.11, 79% above 1.0; weakly positive, below the gates (2088 failures)
- tr_companion_leads_break: median win rate 61%, median alpha +3.0 points, median profit factor 0.97, 41% above 1.0; near break-even (1930 failures)
- tr_opening_range_break: median win rate 59%, median alpha +3.1 points, median profit factor 1.01, 54% above 1.0; near break-even (1871 failures)
- tr_climax_reversal: median win rate 66%, median alpha +6.4 points, median profit factor 1.12, 76% above 1.0; weakly positive, below the gates (1808 failures)
- tr_keltner_reentry: median win rate 62%, median alpha +3.8 points, median profit factor 1.06, 64% above 1.0; weakly positive, below the gates (1719 failures)
- tr_cci_breakout: median win rate 62%, median alpha +2.9 points, median profit factor 0.96, 38% above 1.0; near break-even (1717 failures)
- tr_failed_break: median win rate 57%, median alpha +2.8 points, median profit factor 1.01, 51% above 1.0; near break-even (1470 failures)
- tr_bollinger_break: median win rate 60%, median alpha +3.4 points, median profit factor 1.02, 54% above 1.0; near break-even (1287 failures)
- tr_band_width_expansion: median win rate 62%, median alpha +6.4 points, median profit factor 1.13, 80% above 1.0; weakly positive, below the gates (1197 failures)
- tr_band_break_failure: median win rate 67%, median alpha +8.4 points, median profit factor 1.17, 81% above 1.0; weakly positive, below the gates (1169 failures)
- tr_squeeze_release: median win rate 61%, median alpha +3.8 points, median profit factor 1.04, 59% above 1.0; near break-even (1124 failures)
- tr_trail_flip: median win rate 67%, median alpha +6.5 points, median profit factor 1.15, 82% above 1.0; weakly positive, below the gates (1122 failures)
- tr_engulfing: median win rate 54%, median alpha +1.8 points, median profit factor 0.95, 38% above 1.0; no edge after costs (1100 failures)
- tr_internal_bar_strength: median win rate 53%, median alpha +1.9 points, median profit factor 0.93, 36% above 1.0; no edge after costs (1093 failures)
- tr_late_session_extreme: median win rate 64%, median alpha +6.5 points, median profit factor 1.15, 79% above 1.0; weakly positive, below the gates (1090 failures)
- tr_relative_strength_turn: median win rate 62%, median alpha +3.8 points, median profit factor 1.03, 57% above 1.0; near break-even (1085 failures)
- tr_low_volatility_break: median win rate 66%, median alpha +6.9 points, median profit factor 1.12, 72% above 1.0; weakly positive, below the gates (1083 failures)
- tr_ema_cross: median win rate 65%, median alpha +5.8 points, median profit factor 1.15, 76% above 1.0; weakly positive, below the gates (1069 failures)
- tr_close_extreme_fade: median win rate 64%, median alpha +5.9 points, median profit factor 1.08, 73% above 1.0; weakly positive, below the gates (933 failures)
- tr_late_vwap_cross: median win rate 55%, median alpha +2.6 points, median profit factor 0.96, 41% above 1.0; near break-even (918 failures)
- tr_volume_climax_follow: median win rate 59%, median alpha +2.8 points, median profit factor 0.97, 41% above 1.0; near break-even (788 failures)
- tr_htf_extreme_sweep: median win rate 49%, median alpha +0.4 points, median profit factor 0.87, 26% above 1.0; no edge after costs (738 failures)
- tr_coil_break: median win rate 50%, median alpha +1.1 points, median profit factor 0.90, 23% above 1.0; no edge after costs (726 failures)
- tr_price_ema_cross: median win rate 55%, median alpha +3.8 points, median profit factor 1.01, 51% above 1.0; near break-even (703 failures)
- tr_keltner_break: median win rate 55%, median alpha +3.7 points, median profit factor 1.04, 57% above 1.0; near break-even (622 failures)
- tr_inside_bar_break: median win rate 54%, median alpha +2.4 points, median profit factor 0.94, 38% above 1.0; no edge after costs (616 failures)
- tr_rsi2_extreme: median win rate 49%, median alpha -0.4 points, median profit factor 0.84, 11% above 1.0; no edge after costs (562 failures)
- tr_sweep_swing: median win rate 49%, median alpha +1.2 points, median profit factor 0.88, 25% above 1.0; no edge after costs (538 failures)
