# Informational stage 2 run: generation 25968

This candidate did not pass stage 1, so nothing here promotes it. The run measures how it behaves outside the conditions it was selected on. Research data only; base costs unless stated; both instruments pooled over the six walk-forward test folds.

```
direction: both_mirrored; holding: INTRADAY_FLAT; complexity: 8
trigger: tr_roc_thrust(k=3.0, n=8)
entry: market
stop: r_stop_swing(buf=0.05, n=12)
exit: x_target_atr(k=1.0)
sequencing: cool-down 15 min, max 6 trades per session, stand down after 3 straight losses
```

## Gates

| Gate | Value | Needs | Pass |
|---|---|---|---|
| s2.no_canary_atoms | 1.0 | >= 1 | yes |
| s2.truncation_audit_clean | 1.0 | >= 1 | yes |
| s2.intrabar_win_rate_gap_pts | 0.210373 | <= 6 | yes |
| s2.selection_leak_constants | 0.0 | <= 0 | yes |
| s2.edge_survives_next_bar_fill | 2.020693 | > 0 | yes |
| s2.core_timeframes_passing | 3.0 | >= 2 | yes |
| s2.worst_timeframe_pf | 0.95022 | >= 1.15 | NO |
| s2.timeframe_win_rate_spread_pts | 22.915855 | <= 8 | NO |
| s2.alpha_positive_every_timeframe | 1.514311 | > 0 | yes |
| s2.alpha_above_twin_p95_every_timeframe | 0.0 | >= 1 | NO |
| s2.timeframe_pf_cv | 0.074088 | <= 0.3 | yes |
| s2.alignment_pf_ratio | 0.904236 | >= 0.75 | yes |
| s2.alignment_win_rate_gap_pts | 7.688027 | <= 5 | NO |
| s2.stress_cost_pf | 1.108532 | >= 1.3 | NO |
| s2.weaker_side_pf | 1.157873 | >= 1.2 | NO |
| s2.long_short_win_rate_gap_pts | 1.619423 | <= 10 | yes |
| s2.drift_neutral_expectancy_retention | -0.729716 | >= 0.7 | NO |
| s2.inverted_market_pf | 1.068862 | > 1.0 | yes |
| s2.inverted_market_expectancy_retention | 0.467674 | >= 0.5 | NO |
| s2.each_instrument_win_rate | 0.72007 | >= 0.6 | yes |
| s2.each_instrument_pf | 1.143349 | >= 1.0 | yes |
| s2.zero_shot_transfer_retention | 1.0 | >= 0.7 | yes |
| s2.synthetic_relatives_profitable | 28915.0 | > 0 | yes |
| s2.plateau_one_step_pass_share | 0.0 | >= 0.8 | NO |
| s2.plateau_two_step_pass_share | 0.0 | >= 0.6 | NO |
| s2.peak_excess_over_neighbourhood | 2.209215 | <= 0.25 | NO |
| s2.median_decoy_pf | 0.919966 | < 1.1 | yes |
| s2.alpha_gap_real_minus_decoy_pts | 4.478049 | >= 8 | NO |

## Core timeframes (one parameter set)

| Timeframe | Win rate | Alpha | Profit factor | Trades | Per year per instrument | Expectancy (round-trip costs) |
|---|---|---|---|---|---|---|
| 5 min | 73.2% | +7.2 | 1.19 | 2281 | 403 | +2.02 |
| 10 min | 67.8% | +5.8 | 1.10 | 1374 | 234 | +0.89 |
| 15 min | 65.5% | +6.6 | 1.14 | 1055 | 184 | +1.60 |
| 30 min | 56.9% | +3.6 | 1.07 | 691 | 119 | +0.80 |
| 60 min | 50.3% | +1.5 | 0.95 | 394 | 67 | -0.69 |

## intrabar

```
{
 "pessimistic_win_rate": 0.7316966242875932,
 "optimistic_win_rate": 0.7338003502626971,
 "gap_pts": 0.21037259751038873,
 "same_bar_share": 0.17580008768084174
}
```

## parity mode

```
{
 "default_expectancy_costs": 2.020692678649715,
 "signal_close_expectancy_costs": 2.082308397433343
}
```

## stress costs

```
{
 "profit_factor": 1.1085322764002827,
 "net_usd": 44155.0,
 "win_rate": 0.7297060114085125
}
```

## long short

```
{
 "long": {
  "n": 1162,
  "win_rate": 0.7237521514629949,
  "profit_factor": 1.1578731138887506
 },
 "short": {
  "n": 1119,
  "win_rate": 0.739946380697051,
  "profit_factor": 1.2290617494382894
 }
}
```

## drift neutral

```
{
 "expectancy_costs": -1.4745324983804795,
 "retention": -0.729716356158525,
 "win_rate": 0.6769596199524941
}
```

## inverted market

```
{
 "profit_factor": 1.0688622437640884,
 "win_rate": 0.6921022510492179,
 "expectancy_costs": 0.9450244528458949
}
```

## transfer

```
{
 "ES_to_YM": 1.0,
 "YM_to_ES": 1.0
}
```

## divergence days

```
{
 "sessions": 257,
 "n": 679,
 "win_rate": 0.7304860088365243,
 "profit_factor": 1.1480748684262594,
 "note": "ES and YM are highly correlated; these are the sessions where they give partly independent evidence."
}
```

## synthetic relatives

```
{
 "blended_returns": {
  "profit_factor": 1.0715965928787203,
  "net_usd": 28915.0,
  "win_rate": 0.7148097203117836
 },
 "regime_shuffle": {
  "profit_factor": 1.0686676937362822,
  "net_usd": 32537.5,
  "win_rate": 0.7150170648464164
 },
 "note": "Derived from ES and YM; these are not new markets."
}
```

## decoys

```
{
 "n": 30,
 "median_pf": 0.9199662653944805,
 "median_alpha_pts": 2.727862692831712,
 "max_pf": 1.0277898435313082,
 "real_alpha_pts": 7.20591128074769
}
```

## cpcv

```
{
 "combinations": 44,
 "pf_p5": 1.0838834220635454,
 "pf_median": 1.213799694395048,
 "share_pf_above_1": 1.0
}
```

## pbo

```
{
 "pbo": 0.049,
 "slope": 0.8714571716347732,
 "configs": 14,
 "combos": 2000
}
```

## Parameter neighbours

One-step neighbours: 7; their profit factors: 1.18, 1.10, 1.09, 1.09, 0.92, 1.19, 1.19. Fog 25th-percentile score 0.000 (retention 0% of the nominal score, 200 variants).
