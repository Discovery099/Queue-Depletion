# Informational stage 2 run: generation 44439

This candidate did not pass stage 1, so nothing here promotes it. The run measures how it behaves outside the conditions it was selected on. Research data only; base costs unless stated; both instruments pooled over the six walk-forward test folds.

```
direction: both_mirrored; holding: INTRADAY_FLAT; complexity: 12
regime: st_vwap_side(); st_ichimoku_cloud(s=1)
trigger: tr_roc_thrust(k=3.0, n=8)
entry: market
stop: r_stop_atr(k=1.5)
exit: x_partial(r=0.5); x_target_atr(k=1.5)
sequencing: cool-down 10 min, max 6 trades per session, stand down after 3 straight losses
```

## Gates

| Gate | Value | Needs | Pass |
|---|---|---|---|
| s2.no_canary_atoms | 1.0 | >= 1 | yes |
| s2.truncation_audit_clean | 1.0 | >= 1 | yes |
| s2.intrabar_win_rate_gap_pts | 0.0 | <= 6 | yes |
| s2.selection_leak_constants | 0.0 | <= 0 | yes |
| s2.edge_survives_next_bar_fill | 4.132459 | > 0 | yes |
| s2.core_timeframes_passing | 4.0 | >= 2 | yes |
| s2.worst_timeframe_pf | 0.959198 | >= 1.15 | NO |
| s2.timeframe_win_rate_spread_pts | 11.76066 | <= 8 | NO |
| s2.alpha_positive_every_timeframe | 1.097422 | > 0 | yes |
| s2.alpha_above_twin_p95_every_timeframe | 0.0 | >= 1 | NO |
| s2.timeframe_pf_cv | 0.156083 | <= 0.3 | yes |
| s2.alignment_pf_ratio | 0.742998 | >= 0.75 | NO |
| s2.alignment_win_rate_gap_pts | 7.075853 | <= 5 | NO |
| s2.stress_cost_pf | 1.409789 | >= 1.3 | yes |
| s2.weaker_side_pf | 1.363104 | >= 1.2 | yes |
| s2.long_short_win_rate_gap_pts | 2.207792 | <= 10 | yes |
| s2.drift_neutral_expectancy_retention | -2.562881 | >= 0.7 | NO |
| s2.inverted_market_pf | 1.301983 | > 1.0 | yes |
| s2.inverted_market_expectancy_retention | 0.594914 | >= 0.5 | yes |
| s2.each_instrument_win_rate | 0.665245 | >= 0.6 | yes |
| s2.each_instrument_pf | 1.210531 | >= 1.0 | yes |
| s2.zero_shot_transfer_retention | 0.842704 | >= 0.7 | yes |
| s2.synthetic_relatives_profitable | 16440.0 | > 0 | yes |
| s2.plateau_one_step_pass_share | 0.111111 | >= 0.8 | NO |
| s2.plateau_two_step_pass_share | 0.0 | >= 0.6 | NO |
| s2.peak_excess_over_neighbourhood | 0.006496 | <= 0.25 | yes |
| s2.median_decoy_pf | 0.964189 | < 1.1 | yes |
| s2.alpha_gap_real_minus_decoy_pts | 6.252467 | >= 8 | NO |

## Core timeframes (one parameter set)

| Timeframe | Win rate | Alpha | Profit factor | Trades | Per year per instrument | Expectancy (round-trip costs) |
|---|---|---|---|---|---|---|
| 5 min | 66.0% | +3.5 | 1.11 | 2453 | 420 | +0.78 |
| 10 min | 67.2% | +5.0 | 1.22 | 1306 | 229 | +2.11 |
| 15 min | 69.3% | +7.5 | 1.51 | 915 | 158 | +4.13 |
| 30 min | 63.1% | +3.7 | 1.09 | 510 | 88 | +1.09 |
| 60 min | 57.5% | +1.1 | 0.96 | 259 | 45 | -1.50 |

## intrabar

```
{
 "pessimistic_win_rate": 0.692896174863388,
 "optimistic_win_rate": 0.692896174863388,
 "gap_pts": 0.0,
 "same_bar_share": 0.09617486338797815
}
```

## parity mode

```
{
 "default_expectancy_costs": 4.132459016393442,
 "signal_close_expectancy_costs": 3.9373095688539284
}
```

## stress costs

```
{
 "profit_factor": 1.4097890626134169,
 "net_usd": 70568.75,
 "win_rate": 0.6835164835164835
}
```

## long short

```
{
 "long": {
  "n": 495,
  "win_rate": 0.703030303030303,
  "profit_factor": 1.6528589541392213
 },
 "short": {
  "n": 420,
  "win_rate": 0.680952380952381,
  "profit_factor": 1.3631042818971777
 }
}
```

## drift neutral

```
{
 "expectancy_costs": -10.591000214408234,
 "retention": -2.5628808833660046,
 "win_rate": 0.4858490566037736
}
```

## inverted market

```
{
 "profit_factor": 1.3019831057321494,
 "win_rate": 0.6688382193268186,
 "expectancy_costs": 2.4584591846806827
}
```

## transfer

```
{
 "ES_to_YM": 0.8969217047342509,
 "YM_to_ES": 0.8427038147549065
}
```

## divergence days

```
{
 "sessions": 257,
 "n": 254,
 "win_rate": 0.6338582677165354,
 "profit_factor": 1.0550891425337232,
 "note": "ES and YM are highly correlated; these are the sessions where they give partly independent evidence."
}
```

## synthetic relatives

```
{
 "blended_returns": {
  "profit_factor": 1.4727506211227461,
  "net_usd": 77539.375,
  "win_rate": 0.6902356902356902
 },
 "regime_shuffle": {
  "profit_factor": 1.0941810005299113,
  "net_usd": 16440.0,
  "win_rate": 0.6442641946697567
 },
 "note": "Derived from ES and YM; these are not new markets."
}
```

## decoys

```
{
 "n": 30,
 "median_pf": 0.9641892623215809,
 "median_alpha_pts": 1.2088761727090447,
 "max_pf": 1.1369863304646284,
 "real_alpha_pts": 7.461342981920904
}
```

## cpcv

```
{
 "combinations": 44,
 "pf_p5": 1.1672441427106177,
 "pf_median": 1.4823946457562587,
 "share_pf_above_1": 1.0
}
```

## pbo

```
{
 "pbo": 0.263,
 "slope": 0.6693935091104272,
 "configs": 17,
 "combos": 2000
}
```

## Parameter neighbours

One-step neighbours: 9; their profit factors: 1.41, 1.37, 1.47, 1.50, 1.36, 1.13, 1.18, 1.48, 1.39. Fog 25th-percentile score 0.103 (retention 70% of the nominal score, 200 variants).
