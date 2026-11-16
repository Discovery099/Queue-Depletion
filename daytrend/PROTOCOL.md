# Daytrend project: protocol, written before any result

Date: 2026-11-16. Third project. The owner's instruction: build something profitable; it need not be based on Smart
Trend. Two earlier searches over indicator rules (200,000 candidates in total) ended at a profit factor of about
1.0 to 1.3 on unseen data, so this project does not search indicator rules again.

## Approach
Test a short list of intraday effects that are documented in published research and have a reason to exist
(trend days, institutional flows near the open and the close), each at its PUBLISHED settings, with no tuning.
Because nothing is fitted here, all 947 search sessions are a fair test of each rule. (Caveat: the papers' own
samples overlap 2020-2023 in part, so publication selection is not removed.)

| ID | Rule | Source settings |
|---|---|---|
| S1 | Noise-area intraday momentum: at each half hour, long if price is above open*(1+avg abs move from the open at this time of day over the last 14 sessions), short if below the mirror level; exit at the half hour when price is back inside the level or the session VWAP, whichever is nearer the trade; flat at the close | Zarattini, Aziz, Barbon (2024): 14 sessions, multiplier 1, 30-minute checks |
| S2 | Last-half-hour momentum: at 15:30 trade in the direction of the move from the prior close to 10:00; exit at the close | Gao, Han, Li, Zhou (2018) |
| S3 | 5-minute opening-range breakout: trade in the direction of the first 5-minute candle at the open of the second; stop at the first candle's other extreme; target 10R; else flat at the close | Zarattini, Aziz (2023) |

Execution and costs: unchanged from harness/ (next bar open + 1 tick, $1.25 a side, stop first, flat at the last bar).
ES and YM, 1 contract.

## What counts as profitable (fixed now)
On the 947 search sessions, at the published settings: pooled profit factor >= 1.30; ES and YM each >= 1.15;
profitable in at least 6 of the 8 folds; profit factor >= 1.15 at doubled costs; the median profit factor of the
one-step parameter neighbours >= 1.20; max drawdown <= 35% of net profit.

## Then
- A rule that passes is frozen and run ONCE on the Holdout (168 sessions from 2023-09-04, never opened). The Holdout
  result is reported as is. Holdout pass = profit factor >= 1.15 and net profit > 0 on both instruments pooled.
- A rule that fails is reported as failed. Its parameters are not then tuned to make it pass.
- One permitted refinement step for a passing rule, on search data only and reported separately from the published
  version: risk controls (a protective stop, a daily trade cap) and a combination of passing rules.
- The vault stays sealed.

## Phase 2 (written after Phase 1: all three published rules failed the bar above; none was tuned)
One machine-learning combiner, one configuration, no hyperparameter search.
- Features at each 5-minute bar: every trigger, state, filter and location technique in the library catalogue at its
  default setting (buy condition minus sell condition), plus 20 plain numeric descriptors (time of day, distance
  from VWAP, moves over 1 to 24 bars in ATR units, the noise-area z-score, volatility and volume ratios, the gap).
- Target: the move from the next bar's open over H bars, in ATR units. Two horizons, each its own model:
  H = 6 bars (30 minutes) and H = to the session close.
- Model: gradient-boosted trees (scikit-learn HistGradientBoostingRegressor, 300 trees, depth 4, learning rate 0.03,
  at least 200 bars per leaf). ES and YM pooled.
- Walk-forward: to predict fold k (3 to 8), train on folds 1..k-1 minus a 2-session embargo. Every prediction used
  is out-of-sample.
- Trade rule: long when the predicted move is at least twice the round-trip cost (in ATR units), short at minus
  that; exit after H bars or at the close; 4 ATR emergency stop.
- Same bar for "profitable" as Phase 1, measured on folds 3 to 8. A threshold sweep is reported for information
  only and is not used to pick a threshold.

## Phase 3: one-time Holdout audit (amendment, written before the Holdout was opened)
Phases 1 and 2 failed the bar, so under the rule above nothing qualifies for the Holdout. This amendment changes
that rule, openly, for this reason: four different approaches (two rule searches of 100,000 candidates each, three
published rules, one machine-learning combiner) have now reached the same ceiling, and the owner's instruction is
to produce something profitable. The only candidates with any measured edge all capture the same effect (moves
that continue on trend days). The remaining useful question is whether that effect survives on data none of them
has seen. The Holdout is the only clean data that can answer it; the vault stays sealed.

Candidates, frozen exactly as they are (no parameter is changed before or after):
| ID | Candidate | Search-data record |
|---|---|---|
| A | Project 1, generation 25968 (5-minute momentum thrust, structure stop, 1 ATR target) | 73.2% wins, profit factor 1.19, 2,281 trades, six folds |
| B | Project 1, generation 44439 (15-minute momentum thrust with VWAP side and cloud) | 69.3% wins, profit factor 1.51, 915 trades, six folds |
| C | S1 noise-area momentum at published settings, ES and YM | profit factor 1.08 pooled (ES 1.21, YM 0.93), 1,497 trades |

Reported for each: trades, win rate, profit factor, net, drawdown, per instrument and pooled, with all three shown
whatever the result. Holdout pass = pooled profit factor >= 1.15 and net profit > 0. With 168 sessions the test is
weak: a strategy with a true profit factor of 1.2 fails it roughly four times in ten, and one with no edge passes
roughly one time in five. An ES-only reading of C is post-hoc and is labelled so.
