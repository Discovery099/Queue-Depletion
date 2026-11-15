# Dossier: leading candidate, not certified (generation 44439)

- Generations completed: 100,000 of 100,000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1,000 placebo generations

**This is not a certification.** No strategy reached Bronze, so there is no champion. This dossier describes the leading candidate
at the end of the run, as SPEC 20.3 asks, so the owner can see exactly how far it got and where it fails. It is called "leading
candidate, not certified" throughout.

## 1. What it does and why it might work

On 15-minute bars, when price has moved more than 3 ATR in one direction over the last 8 bars for the first time, and it is on
the same side of the session's VWAP and beyond the cloud, enter in that direction at the next bar's open. Stop 1.5 ATR away.
Take half off at half the risk and move the stop to the entry price; take the rest at 1.5 ATR; be flat by the close. At most six
trades a session, a 10-minute pause after a loss in the same direction, and no more trades after three straight losses.
Long and short rules are mirror images.

The idea: a sharp directional move that is also on the right side of the day's value and of the longer trend tends to continue
for a while on days when the index is trending. The evidence below says that is true to a small degree and only on such days.

## 2. Win-rate statements

Research walk-forward test folds 3 to 8 (711 sessions), ES and YM pooled, base costs, 1 contract:

```
WIN-RATE STATEMENT
Headline win rate (net, flat-to-flat, OOS):   69.3 %   (n = 915 trades)
Wilson 95% interval:                          66.2 % to 72.2 %
Geometry baseline (random-entry twin median): 61.7 %   (200 twins)
Win-rate alpha:                               +7.6 points (twin p99 = 65.0 %)
Random-exit twin win rate:                    56.4 %
Payoff ratio:                                 0.67
Profit factor:                                1.51
Expectancy per trade:                         +9.5 ticks   (+4.1 x round-trip cost)
Largest loss / average win:                   3.5
Trades per year per instrument:               158
Sessions with a trade:                        53 %
```

- Inner holdout (final 15% of research data): **not opened.** Only stage 3 survivors may query it; this candidate failed stage 1.
- Vault-A and Vault-B: **not queried.** It was never eligible.

A note on the headline: about half of all trades end at the stop, yet 69% are winners, because many of those stops are the
break-even stop after the first half was taken at a profit. That is a net win under the flat-to-flat rule, and the twin uses the
same exits, so the alpha is measured fairly; but the headline owes a lot to that exit.

## 3. The Gold vector, item by item

| Requirement | Value | Result |
|---|---|---|
| Win rate at least 80% pooled, 75% on each instrument and timeframe | 69.3% pooled; ES 72.2%, YM 66.5% | FAIL |
| Wilson 95% lower bound at least 76% | 66.2% | FAIL |
| Win-rate alpha at least 12 points | +7.6 | FAIL |
| Profit factor at least 1.8 pooled, 1.4 in every fold | 1.51 pooled; folds 2.04, 1.22, 2.23, 1.53, 1.29, 1.06 | FAIL |
| Payoff ratio at least 0.45 | 0.67 | pass |
| Expectancy at least 3 round-trip costs | 4.1 | pass |
| Largest loss at most 4 average wins; worst 5% of trades lose at most 35% of gross profit | 3.5; 19.5% | pass |
| Trade frequency (120 a year per instrument at 15 minutes) | 158 | pass |
| Participation (40% of sessions at 15 minutes; no gap over the scaled limit) | 53%; longest gap 7 sessions | pass |
| Maximum drawdown at most 20% of net profit; underwater at most 9 months | 7.5%; 92 sessions | pass |
| Profitable in at least 85% of rolling 6-month windows | not evaluated (stage 3 not reached); 94% of rolling 3-month windows | not evaluated |
| At least 4 of 5 core timeframes and 2 of 3 hidden timeframes at Gold floors | 0 of 5 at Gold floors; hidden timeframes not run | FAIL |
| ES and YM with one parameter set at Gold floors | one parameter set, but YM below the floors | FAIL |
| Deflated Sharpe probability at least 0.95; probability of backtest overfitting at most 0.20 | deflated Sharpe not computed (stage 3 not reached); overfitting probability 0.26 over 17 neighbouring configurations | FAIL |
| Zero lookahead, zero repaint, zero canary dependence, red team unbroken | truncation audit clean; Pine replay equal; no canary atoms; red team not run | partly evaluated |
| Vault-A and Vault-B | not attempted | not evaluated |

It also failed the gate that kept it from Bronze: one fold supplies 35.9% of the total profit (limit 35%).

## 4. Results by slice (research data)

| Slice | Trades | Win rate | Profit factor |
|---|---|---|---|
| ES | 446 | 72.2% | 1.80 |
| YM | 469 | 66.5% | 1.21 |
| Long | 495 | 70.3% | 1.65 |
| Short | 420 | 68.1% | 1.36 |
| 2021 | 331 | 71.3% | 1.86 |
| 2022 | 337 | 70.3% | 1.53 |
| 2023 | 226 | 65.0% | 1.14 |
| Sessions where ES and YM diverged | 254 | 63.4% | 1.06 |

| Core timeframe (same parameters) | Win rate | Alpha | Profit factor | Trades a year per instrument |
|---|---|---|---|---|
| 5 minutes | 66.0% | +3.5 | 1.11 | 420 |
| 10 minutes | 67.2% | +5.0 | 1.22 | 229 |
| 15 minutes (selected) | 69.3% | +7.5 | 1.51 | 158 |
| 30 minutes | 63.1% | +3.7 | 1.09 | 88 |
| 60 minutes | 57.5% | +1.1 | 0.96 | 45 |

Hidden off-grid timeframes and the per-regime table belong to stage 3 and were not run. Fifteen-minute bars started 5 or 10
minutes later keep 82 to 84% of the profit factor.

## 5. Against the baseline and the twin

| | Win rate | Profit factor | Trades a year per instrument |
|---|---|---|---|
| Smart Trend V1 as supplied (5 minutes, always in the market, no stop) | 35 to 36% | 0.93 to 1.03 | about 564 |
| Random-entry twin of this candidate (same exits, random entries; median of 200) | 61.7% | 0.95 | about 140 |
| This candidate | 69.3% | 1.51 | 158 |

## 6. Trial count

100,000 generations; 200,156 stage 1 candidate backtests in the ledger; about 120,000 effective independent trials after
clustering; this candidate's lineage had been through thousands of ancestors and siblings. A profit factor of 1.5 on 915 trades
is what the best of that many attempts is expected to look like when the true figure is nearer 1.2. Vault queries used: none.

## 7. Placebo pipeline

This pipeline promoted 0 strategies to Bronze, 0 to Silver and 0 to Gold in 1,000 generations on markets with no edge, on each
of four runs (bootstrap, model, bootstrap, phase-randomised decoys). On those markets selection alone reached a composite score
of 0.21 to 0.34.

## 8. Audits and red team

| Check | Result |
|---|---|
| Static audit (genome, Python, Pine) | clean |
| Truncation audit, 300 bars per instrument | clean: no value depends on later data |
| Intrabar order (stop first against target first) | win rate identical; 9.6% of trades open and close in one bar |
| Selection leak | no data-derived constants |
| Fill at the signal close against the next bar's open | edge survives next-bar fills |
| Pine replay (signal layer executed from the exported text) | equal on 120 sessions per instrument at 5 and 15 minutes; no vanished or late signals |
| Canary atoms | none |
| Decoy markets (30) | median profit factor 0.96; its alpha there is +1.2 points against +7.5 on real data |
| Red team (200-backtest budget) | **not run**: stage 3 was not reached |

## 9. Known weaknesses

- **It earns on trend days only.** With each session's open-to-close drift removed, the expectancy turns negative.
- **It is best exactly where it was selected.** Profit factor 1.51 on 15-minute bars, 1.1 to 1.2 on 5, 10 and 30, below 1.0 on 60.
  One-step parameter neighbours range from 1.13 to 1.50.
- **It is fading.** 1.86 in 2021, 1.53 in 2022, 1.14 in 2023; the most recent fold is 1.06.
- **It is mostly an ES effect.** 1.80 on ES, 1.21 on YM, 1.06 on the days the two disagree.
- **Costs.** Profit factor 1.41 at doubled commission and two ticks of slippage a side. The break-even cost level was not located.
- **Worst-scenario analysis** (SPEC 15.10, recombined bad sessions) was not built, so no figure for a bad month is offered. Largest
  historical drawdown on the six folds: about $6,200 for 1 contract of each instrument, on net profit of $83,100.

## 10. Limits of the evidence

Two highly correlated instruments; regular hours only; 5-minute source bars with unknown intrabar order; about four years of
research data; no live fills; no inner-holdout result; no vault result. Best of about 120,000 effective trials.

## 11. What would count against it further, and a forward plan

It holds no certification to revoke. If the owner chooses to watch it: run it on new bars with no changes (drop them into
`data/forward/`; the forward stage of SPEC 15.12 is not built yet, so this would be a manual run of the default engine), or
paper-trade the Pine file through the existing webhook in paper mode. Evidence against it: a forward profit factor below 1.0 over
100 trades per instrument, or a win rate at or below its twin's 61.7%.

## 12. Pine file

- `reports/candidates/gen_044439.pine` — header states NOT CERTIFIED and lists the failed gate. Defaults stay on paper; no URL.
- `reports/candidates/gen_044439_pine_parity.json` — independent replay result (signal layer; order section not executed).
- `reports/candidates/gen_044439_PINE_CHECK.md` — ten specific trades to look for in TradingView.
- `reports/candidates/gen_044439_stage2.md` — the full informational robustness run.

Nothing here is financial advice, and no backtest result is a promise of live performance.
