# Status at generation 50,008

- Generations completed: 50,008 of 100,000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B). The vault has not been read.
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1,000 placebo generations (three runs, three decoy types)

`OUTCOME so far: NONE` — no strategy has met Bronze. Two leading candidates are described below; neither is certified. The owner
can rely on the harness and on the negative findings; the owner cannot yet rely on any strategy.

## Where the search stands

| Measure | Value |
|---|---|
| Generations | 50,008 |
| Passed the stage 1 screen on their island's folds | 20 |
| Confirmed on all six test folds | 0 |
| Reached stage 2 or beyond | 0 |
| Stage 1 candidate rows in the ledger | 100,172 (includes the dry run, re-runs and recounts); effective independent trials about 60,000 |
| Canary adoption among stage 1 passes | 0% |
| Honeypot genome voided at every epoch | yes |
| Ledger hash chain | intact, 301,790 rows |
| Reproducibility | 60 of 60 past generations re-run from their folders give identical metrics (checks at 20,008, 30,008, 50,008) |
| Placebo | 0 promotions in 1,000 generations on each of a bootstrap, a model and a second bootstrap decoy |

## Leading candidates (not certified)

**Generation 44439, 15-minute bars: one gate short of the Bronze screen.** Enter when the net move over 8 bars first exceeds 3 ATR,
with price on the trade side of session VWAP and beyond the cloud; stop 1.5 ATR; half off at half the risk; target 1.5 ATR.
On all six walk-forward test folds, both instruments, base costs:

```
Headline win rate (net, flat-to-flat, OOS):   69.3 %   (n = 915 trades)
Wilson 95% lower bound:                       66.2 %
Geometry baseline (random-entry twin median): 61.7 %   (200 twins)
Win-rate alpha:                               +7.6 points (twin p99 = 65.0 %)
Random-exit twin win rate:                    56.4 %
Payoff ratio:                                 0.67
Profit factor:                                1.51   (per fold: 2.04, 1.22, 2.23, 1.53, 1.29, 1.06)
Expectancy per trade:                         +4.1 x round-trip cost
Trades per year per instrument:               158
```

It fails one confirmation gate: one fold supplies 35.9% of the profit and the limit is 35%. The gate stands, so it is not promoted.
An informational robustness run (`reports/candidates/gen_044439_stage2.md`) shows why caution is right:

- For it: no lookahead; no dependence on intrabar ordering; profit factor 1.41 at doubled costs; long and short both profitable;
  1.30 on the inverted market; no edge on decoy markets.
- Against it: it is best exactly where it was selected. Profit factor is 1.51 on 15-minute bars but 1.11 on 5, 1.22 on 10, 1.09
  on 30 and 0.96 on 60; shifting the 15-minute bar boundaries by 5 or 10 minutes cuts it to about 1.1; the two most recent folds
  are the weakest (1.29, 1.06); profit disappears when each session's net drift is removed.

**Generation 25968, 5-minute bars: the most consistent.** The same momentum-thrust entry with a structure stop and a 1 ATR target.
On all six folds: 73.2% wins over 2,281 trades, twin 66.0%, profit factor 1.19 (1.11 at doubled costs), about 400 trades a year per
instrument, every fold and both instruments profitable. It scores the same on folds it was not selected on. It fails Bronze on
profit factor. A Pine export marked NOT CERTIFIED, its parity result and a TradingView check sheet are in `reports/candidates/`.

**Honest reading of both.** There is a real, small edge in momentum-thrust entries on trend days: about +4 to +7 points of win rate
beyond what the exits alone give, worth a profit factor of roughly 1.1 to 1.2 once the choice of timeframe and bar alignment is
taken out. The 1.5 of generation 44439 is the top of a noisy landscape around that level, found after about 60,000 effective
attempts. Nothing found so far supports 80% wins with a profit factor of 1.8.

## What changed the search (all tightenings; `reports/gate_changes.md`)

After 20,008 generations the leaders kept only 18% of their score on folds that had not influenced them. Since then: a symmetric
overfit penalty in the score, a profitable-record requirement before each test fold, behavioural de-duplication, and an automatic
island exchange every 2,500 generations that removes leaders which do not hold up. Retention on unseen folds rose to about 60 to
75%, and the leaders' profit factor on unseen folds from 0.91 to about 1.2 (`reports/exchange_*.md`).

## Frontier (`reports/frontier.md`; home-fold screening numbers, best of many attempts)

- 80% wins with at least 150 out-of-sample trades: 17 genomes on their home folds, all below 150 trades a year per instrument;
  none passed the screen.
- 70% wins with profit factor at least 1.4: 805 genomes on home folds; on all six folds the best robust figures are those above.
- The binding constraint is profit factor on unseen data at any useful trade frequency. Win rate near 70% is reachable; a payoff
  ratio high enough to turn it into a profit factor of 1.4 on every fold is not, so far.

## What carried signal, and what did not

Carried a little: momentum thrusts and average crosses in the direction of the session (VWAP side, cloud, trail regime), on 5- to
30-minute bars. Did not: oscillator hooks, candle patterns, sweep-and-reclaim triggers, companion-instrument triggers alone, and
ensembles of weak entries (the union takes the weaker member's quality). `ledger/lessons.md` has the counts.

## Next steps

1. Continue the loop to 100,000 (`python3 -m orchestrator.loop --generations N`). A Bronze pass in the momentum-thrust family is
   possible; the stage 2 results above say it would be a narrow one.
2. Decide what a Bronze would be worth to you. It means walk-forward evidence only, and the informational runs already show the
   timeframe and alignment weaknesses that would cap this family below Silver.
3. The most valuable extra evidence is unchanged: a less correlated instrument (NQ, RTY, CL or GC) held as pure out-of-sample data.

## Limits of everything above

Two highly correlated instruments; regular hours only; 5-minute bars with unknown intrabar order; about four years of research data;
no live fills; no vault result. Timeframes below 5 minutes cannot be tested with this data. Nothing here is financial advice.

## Housekeeping

- Disk: `runs/` holds 50,008 generation folders, 9.4 GB; 18 GB free. Older stage 1 failures are being packed into one archive per
  1,000 generations (`tools/pack_runs.py`).
- The branch `claude/dazzling-rubin-wc3b48` is pushed to GitHub. Ledgers are stored as compressed snapshots; `runs/` and
  `library/raw/` are not in the repository.
- Deviations and fixes: `reports/ERRATA.md` (14 items). Not yet built: `reports/milestones/bootstrap.md`.
