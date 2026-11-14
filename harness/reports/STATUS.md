# Status at generation 20,008

- Generations completed: 20,008 of 100,000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B). The vault has not been read.
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1,000 placebo generations

`OUTCOME so far: NONE` — no strategy has met Bronze. The closest approach is described below. The owner can rely on the harness
and on the negative findings; the owner cannot rely on any strategy found so far.

## What exists

The harness of the specification is built and tested (131 tests): data partition and sealed vault, pessimistic order simulator,
baseline reproduction, 196 library-derived atoms across 11 mechanism families plus 12 canaries and a honeypot, genome and search
operators, stage 1 screen with random-entry and random-exit twins, stages 2 to 4, Vault Keeper, decoy markets, placebo mode,
Pine v6 exporter with the owner's webhook layer, an independent Pine replay check, trial ledger, archive, epoch reports.
`reports/milestones/bootstrap.md` lists each Generation 0 item with its evidence and what is not built yet.

## What the search found

| Measure | Value |
|---|---|
| Generations | 20,008 (survey to 2,000, then assembly and early refinement) |
| Stage 1 passes on home folds | 1 (generation 17196) |
| Confirmed on all six test folds | 0 |
| Reached stage 2 or beyond | 0 |
| Raw stage 1 trials in the ledger | 40,148 candidate rows (includes the dry run and recounts); effective independent trials about 24,000 |
| Canary adoption among stage 1 passes | 0% |
| Honeypot genome voided at every epoch | yes |
| Ledger hash chain | intact, 120,804 rows |
| Reproducibility | 20 of 20 past generations re-run from their folders give identical metrics |

**Closest approach (not certified).** Generation 17196, 30-minute bars: enter when price crosses its 34-bar average, stop 0.3% of
price, target at the level supplied by the trigger, half off at 0.5 of the risk. On all six walk-forward test folds, both instruments,
base costs:

```
Headline win rate (net, flat-to-flat, OOS):   63.8 %   (n = 1,025 trades)
Geometry baseline (random-entry twin median): 57.3 %   (200 twins)
Win-rate alpha:                               +6.5 points
Profit factor:                                1.30   (per fold: 1.49, 1.49, 1.15, 1.58, 1.01, 1.33)
Expectancy per trade:                         +3.4 x round-trip cost
```

It misses Bronze on three gates: win rate 63.8% against 65%, profit factor 1.30 against 1.40, Wilson lower bound 60.8% against 61%.
It is the best of about 24,000 effective attempts, so by itself it is not evidence of an edge; it has not been through stage 2
(other timeframes, decoys, cost stress, parameter neighbours).

**The leaders are fitted to the folds they were selected on.** At generation 20,008 the 20 highest-scoring distinct strategies
average 75.6% wins and profit factor 1.63 on their island's folds. On the other island's folds, which never influenced them:
66.3% wins, profit factor 0.91, and they keep 18% of their composite score (43% at generation 15,008). The gap is widening as the
search continues, which is what overfitting looks like. Details: `reports/exchange_015008.md`, `reports/exchange_020008.md`.

**The placebo sets the yardstick.** On a decoy market with no edge, selection alone reached a composite score of 0.34 in 1,000
generations. The real leaders' score on unseen folds (0.10 to 0.22) is below that.

**Frontier** (`reports/frontier.md`; home-fold screening numbers, best of many attempts):

- 80% win rate with profit factor above 1.0 and at least 150 out-of-sample trades: reached by 10 genomes on their home folds, all
  trading fewer than 150 times a year per instrument. None passed the stage 1 screen, and none was among the leaders re-scored on
  unseen folds, so their win rate there is not known.
- At 200 or more trades a year per instrument, the best profit factor at 65 to 80% wins is about 1.4 to 1.5 on home folds, and no
  genome reaches 80% wins.
- Profit factors above 1.8 occur only below about 100 trades a year per instrument.
- The binding constraints are win rate and profit factor together on unseen folds, then trade frequency and participation.

**What carried any signal:** trend-continuation entries on 15- and 30-minute bars (average crosses, ATR-trail flips) with structure
or percentage stops. **What did not:** oscillator hooks, candle patterns, sweep-and-reclaim triggers, and companion-instrument
triggers used alone (median profit factor 0.84 to 0.88 after costs). `ledger/lessons.md` has the counts.

## Checks that fired, and what was changed

- The random-entry twin was tightened to match target-to-stop geometry after the survey showed level-based targets inflating alpha.
- A gate was added requiring a profitable record before each test fold, after leaders appeared that lost before their home folds and
  won inside them.
- Both are in `reports/gate_changes.md`. Ten deviations and fixes are in `reports/ERRATA.md`, including the six vault bars seen once
  before the specification had been read.

## Honest reading

After 20,008 generations there is no certifiable strategy, and the evidence so far says the 80% target with a high profit factor
and 200 trades a year is not within reach of single-idea strategies built from these techniques on this data. What exists is a weak,
consistent residual in slow trend-following entries (a few points of win-rate alpha, profit factor 1.0 to 1.3 on unseen folds).
Whether combining such entries can clear Bronze is what the next phase tests. It may not.

## Next steps

1. Continue the loop (`python3 -m orchestrator.loop --generations N`). It resumes from `state/checkpoint.json`.
2. Curb home-fold fitting before spending more generations: enforce behavioural deduplication, and weight parent selection by
   the exchange result instead of the home score alone (a tightening).
3. Build the ENSEMBLE operator, the one remaining route in SPEC 9.6 that has not been tried.
4. The single most valuable extra evidence remains what the specification says: a less correlated instrument (NQ, RTY, CL or GC)
   held as pure out-of-sample data, and forward paper trading once anything is certified.

## Limits of everything above

Two highly correlated instruments; regular hours only; 5-minute bars with unknown intrabar order; about four years of research data;
no live fills; no vault result. Timeframes below 5 minutes cannot be tested with this data. Nothing here is financial advice.

## Housekeeping

- Disk: `runs/` holds 20,008 generation folders, 3.6 GB; 25 GB free. Old folders have not been packed yet.
- `runs/` and `library/raw/` are not in version control (size). Everything else is committed locally.
- **The commits have not reached GitHub.** The connection to `Discovery099/Queue-Depletion` is read-only for this session, so every
  push is refused. Until that is fixed the work exists only in this session's container.
