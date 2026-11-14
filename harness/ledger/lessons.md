# Lessons (distilled from the graveyard)

Built from 47914 failed generations with at least 100 out-of-sample trades. Each line is a description of what failed, with its supporting count; none is a rule. Lessons learned on one timeframe or exit family may be wrong in general and are re-tested every 10,000 generations (SPEC 15.8).

Note: win-rate alpha recorded before generation 2001 used a twin that did not match target-to-stop geometry and is overstated for level-based targets (reports/gate_changes.md).

## Most common failed gates

- floor.profit_factor_pooled: 45523 failures
- sample.min_track_record_sessions: 42029 failures
- floor.expectancy_in_round_trip_costs: 36920 failures
- wf.median_fold_pf: 36815 failures
- floor.win_rate_pooled: 34792 failures
- sample.wilson_lower: 34183 failures
- wf.folds_with_pf_above_1: 33580 failures
- floor.win_rate_each_instrument: 28834 failures
- wf.worst_fold_pf: 11500 failures
- sample.trades_per_instrument: 10653 failures
- wf.in_sample_expectancy_costs: 9796 failures
- sample.trades_per_fold_per_instrument: 7534 failures

## By family

- trend continuation: median win rate 59%, median alpha +4.1 points, median profit factor 1.03, 56% above 1.0; near break-even (11027 failures)
- mean reversion to value: median win rate 50%, median alpha +1.5 points, median profit factor 0.93, 36% above 1.0; no edge after costs (6443 failures)
- breakout failure: median win rate 60%, median alpha +3.6 points, median profit factor 1.02, 55% above 1.0; near break-even (5134 failures)
- opening auction: median win rate 63%, median alpha +4.5 points, median profit factor 1.05, 65% above 1.0; weakly positive, below the gates (4446 failures)
- exhaustion: median win rate 56%, median alpha +2.4 points, median profit factor 0.95, 42% above 1.0; near break-even (4019 failures)
- liquidity sweep and reversal: median win rate 46%, median alpha +0.5 points, median profit factor 0.86, 23% above 1.0; no edge after costs (3880 failures)
- volatility expansion: median win rate 59%, median alpha +3.7 points, median profit factor 1.01, 54% above 1.0; near break-even (3864 failures)
- volatility contraction: median win rate 58%, median alpha +3.4 points, median profit factor 0.99, 48% above 1.0; near break-even (3355 failures)
- inter-market lead-lag: median win rate 57%, median alpha +2.2 points, median profit factor 0.96, 39% above 1.0; near break-even (3310 failures)
- closing auction: median win rate 61%, median alpha +4.4 points, median profit factor 1.04, 60% above 1.0; near break-even (2436 failures)

## By target

- x_target_atr: median win rate 61%, median alpha +3.3 points, median profit factor 1.01, 52% above 1.0; near break-even (17254 failures)
- x_target_r: median win rate 63%, median alpha +3.3 points, median profit factor 1.00, 51% above 1.0; near break-even (13262 failures)
- x_target_location_level: median win rate 51%, median alpha +3.1 points, median profit factor 0.98, 45% above 1.0; near break-even (4800 failures)
- no target: median win rate 63%, median alpha +6.5 points, median profit factor 1.09, 69% above 1.0; weakly positive, below the gates (4388 failures)
- x_target_prior_extreme: median win rate 43%, median alpha +1.9 points, median profit factor 0.96, 41% above 1.0; near break-even (2165 failures)
- x_target_opposite_range_edge: median win rate 40%, median alpha +1.5 points, median profit factor 0.86, 20% above 1.0; no edge after costs (1919 failures)
- x_target_prior_close: median win rate 41%, median alpha +2.0 points, median profit factor 1.00, 51% above 1.0; near break-even (1675 failures)
- x_target_vwap: median win rate 42%, median alpha +0.7 points, median profit factor 0.79, 7% above 1.0; no edge after costs (1226 failures)
- x_target_session_mid: median win rate 41%, median alpha +0.7 points, median profit factor 0.79, 9% above 1.0; no edge after costs (1225 failures)

## By timeframe

- 5: median win rate 60%, median alpha +2.9 points, median profit factor 0.97, 43% above 1.0; near break-even (26682 failures)
- 15: median win rate 60%, median alpha +4.0 points, median profit factor 1.05, 61% above 1.0; near break-even (12206 failures)
- 10: median win rate 51%, median alpha +2.1 points, median profit factor 0.96, 41% above 1.0; near break-even (3664 failures)
- 60: median win rate 49%, median alpha +3.0 points, median profit factor 1.03, 54% above 1.0; near break-even (3025 failures)
- 30: median win rate 50%, median alpha +3.0 points, median profit factor 1.00, 51% above 1.0; near break-even (2337 failures)

## By entry

- market: median win rate 54%, median alpha +2.9 points, median profit factor 0.99, 49% above 1.0; near break-even (26528 failures)
- stop: median win rate 61%, median alpha +4.0 points, median profit factor 0.98, 47% above 1.0; near break-even (11106 failures)
- limit: median win rate 56%, median alpha +3.1 points, median profit factor 1.00, 50% above 1.0; near break-even (10280 failures)

## By trigger

- tr_roc_thrust: median win rate 67%, median alpha +7.0 points, median profit factor 1.12, 77% above 1.0; weakly positive, below the gates (2389 failures)
- tr_false_break_prior_day: median win rate 63%, median alpha +4.3 points, median profit factor 1.04, 59% above 1.0; near break-even (1980 failures)
- tr_opening_drive: median win rate 67%, median alpha +6.5 points, median profit factor 1.11, 79% above 1.0; weakly positive, below the gates (1798 failures)
- tr_opening_range_break: median win rate 59%, median alpha +3.1 points, median profit factor 1.01, 54% above 1.0; near break-even (1626 failures)
- tr_keltner_reentry: median win rate 62%, median alpha +4.0 points, median profit factor 1.06, 65% above 1.0; weakly positive, below the gates (1547 failures)
- tr_cci_breakout: median win rate 62%, median alpha +2.9 points, median profit factor 0.96, 37% above 1.0; near break-even (1537 failures)
- tr_companion_leads_break: median win rate 59%, median alpha +2.4 points, median profit factor 0.95, 33% above 1.0; no edge after costs (1519 failures)
- tr_climax_reversal: median win rate 66%, median alpha +6.0 points, median profit factor 1.10, 73% above 1.0; weakly positive, below the gates (1324 failures)
- tr_failed_break: median win rate 57%, median alpha +2.8 points, median profit factor 1.00, 51% above 1.0; near break-even (1308 failures)
- tr_bollinger_break: median win rate 60%, median alpha +3.4 points, median profit factor 1.01, 53% above 1.0; near break-even (1158 failures)
- tr_trail_flip: median win rate 67%, median alpha +6.5 points, median profit factor 1.15, 82% above 1.0; weakly positive, below the gates (1061 failures)
- tr_internal_bar_strength: median win rate 52%, median alpha +1.9 points, median profit factor 0.93, 35% above 1.0; no edge after costs (1014 failures)
- tr_ema_cross: median win rate 66%, median alpha +5.8 points, median profit factor 1.15, 76% above 1.0; weakly positive, below the gates (976 failures)
- tr_squeeze_release: median win rate 60%, median alpha +3.7 points, median profit factor 1.03, 57% above 1.0; near break-even (968 failures)
- tr_engulfing: median win rate 53%, median alpha +1.8 points, median profit factor 0.94, 35% above 1.0; no edge after costs (955 failures)
- tr_relative_strength_turn: median win rate 62%, median alpha +3.6 points, median profit factor 1.02, 55% above 1.0; near break-even (934 failures)
- tr_low_volatility_break: median win rate 65%, median alpha +6.8 points, median profit factor 1.12, 71% above 1.0; weakly positive, below the gates (926 failures)
- tr_band_width_expansion: median win rate 62%, median alpha +6.4 points, median profit factor 1.13, 78% above 1.0; weakly positive, below the gates (901 failures)
- tr_late_vwap_cross: median win rate 55%, median alpha +2.6 points, median profit factor 0.96, 40% above 1.0; near break-even (849 failures)
- tr_band_break_failure: median win rate 67%, median alpha +8.1 points, median profit factor 1.17, 79% above 1.0; weakly positive, below the gates (827 failures)
- tr_late_session_extreme: median win rate 64%, median alpha +6.2 points, median profit factor 1.15, 77% above 1.0; weakly positive, below the gates (825 failures)
- tr_volume_climax_follow: median win rate 58%, median alpha +2.7 points, median profit factor 0.97, 40% above 1.0; near break-even (742 failures)
- tr_price_ema_cross: median win rate 56%, median alpha +3.8 points, median profit factor 1.01, 51% above 1.0; near break-even (667 failures)
- tr_htf_extreme_sweep: median win rate 49%, median alpha +0.4 points, median profit factor 0.86, 26% above 1.0; no edge after costs (665 failures)
- tr_coil_break: median win rate 50%, median alpha +0.9 points, median profit factor 0.89, 20% above 1.0; no edge after costs (639 failures)
- tr_close_extreme_fade: median win rate 64%, median alpha +5.3 points, median profit factor 1.06, 69% above 1.0; weakly positive, below the gates (630 failures)
- tr_keltner_break: median win rate 55%, median alpha +3.7 points, median profit factor 1.04, 56% above 1.0; near break-even (541 failures)
- tr_inside_bar_break: median win rate 53%, median alpha +2.3 points, median profit factor 0.93, 35% above 1.0; no edge after costs (520 failures)
- tr_rsi2_extreme: median win rate 49%, median alpha -0.6 points, median profit factor 0.84, 10% above 1.0; no edge after costs (506 failures)
- tr_sweep_swing: median win rate 49%, median alpha +1.1 points, median profit factor 0.88, 25% above 1.0; no edge after costs (500 failures)
