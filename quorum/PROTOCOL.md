# Quorum project: protocol, written before any result was looked at

Date: 2026-11-15. This is a new project. It reuses the data partition, cost model and order simulator of `harness/`
(all frozen there) and nothing else from that run's results.

## Owner's goal
At least 5 trades a day, win rate 60% or more, profit factor 2.0 or more, low drawdown; Smart Trend V1 is the base
strategy; other strategies from the 16k library are merged with it so that a trade is taken only when two or three
strategies of different origin agree on the same candle or within 1 to 4 candles; day and overnight; not tied to one
timeframe; no curve fitting, no repainting.

## The owner's hypothesis, stated so it can fail
H1. A Smart Trend arrow that is matched by an arrow of a second, independent strategy on the same bar or within 1 to 4
bars is followed by a better move in the arrow's direction than a Smart Trend arrow alone.
H2. That improvement is large enough to pay costs and reach the goal.

## Data and what it cannot test
- ES and YM, 5-minute, regular hours only (09:30 to 16:00 New York), 2020-01-02 to 2024-04-29 in the research block.
- Overnight holding CANNOT be tested: the overnight path is not in the data. Everything is flat at the session close.
  Rules are written in bars and ATR units, with no session-anchored inputs, so they can run on a 24-hour chart, but
  that behaviour is untested here.
- Timeframes below 5 minutes cannot be tested. 10, 15 and 30 minutes are built from the 5-minute bars.

## Splits (fixed now)
| Block | Sessions | Use |
|---|---|---|
| Discover | walk-forward folds 1, 3, 5, 7 of the 947 search sessions | all searching and selection |
| Confirm | folds 2, 4, 6, 8 | checked only for the shortlist the search hands over; never used as a fitness |
| Holdout | the 168 sessions from 2023-09-04 (never opened by the previous project) | opened ONCE, for at most 3 frozen finalists |
| Vault | 473 sessions after 2024-04-29 | stays sealed; not used by this project |

## Execution model (unchanged from harness/)
Signals on a closed bar; market entry at the next bar's open plus 1 tick slippage; commission $1.25 a side; stop before
target inside a bar; target needs a 1-tick trade-through; flat at the session's last bar. TradingView's
"process orders on close" fills are more optimistic and are shown only for comparison.

## Phases
1. Owner's hypothesis exactly as written: Smart Trend V1 defaults, the Lorentzian script's defaults, sync window 0 to 4,
   the three exits in the owner's merged script. No tuning. Event study (exit-free) plus backtests, against each
   strategy alone and against random entries with the same exits.
2. Voter census: every portable trigger technique in the library catalogue, as a stream of buy/sell events.
   Forward-move statistics for each voter alone and for every pair that agrees within the window, on Discover,
   replicated on Confirm. Multiple-testing control by Benjamini-Hochberg.
3. Quorum search, up to 100,000 evaluations, on Discover only. A candidate = Smart Trend base (as arrow or as regime)
   + a panel of voters + quorum size + window + one exit from a small fixed menu.
4. Shortlist to Confirm; timeframe check (5, 10, 15, 30 minutes with the same bar-count parameters); both instruments;
   random-entry twin; neighbouring parameters; doubled costs.
5. At most 3 finalists frozen, then the Holdout, once. Reported whatever it shows.

## Acceptance (the owner's goal, per instrument, after costs, on Confirm and on Holdout)
trades/day >= 5, win rate >= 60%, profit factor >= 2.0, max drawdown <= 20% of net profit, win rate at least 5 points
above the random-entry twin. A candidate that misses is reported as a miss. Thresholds are not relaxed after results.

## Anti-repaint rules
Closed bars only; no `lookahead_on`; no higher-timeframe request (higher-timeframe context is built by counting bars);
every signal series passes a truncation test (recomputing on a shortened history must not change past values beyond the
warm-up).

## Shortlist and finalist rule (written while the search was running, before any Confirm result of a search candidate was seen)
- Shortlist from Discover: the top 300 by search fitness plus the top 100 among candidates with at least 3 trades a day
  per instrument, thinned so that no two share more than half of their ES entries; at most 60.
- Confirm is computed for the shortlist only. Finalists (at most 3): shortlist members with Confirm profit factor
  above 1.0 on ES and on YM separately, ranked by the same fitness formula evaluated on the Confirm folds, again thinned
  by entry overlap. Picking by Confirm biases the Confirm figure upward; the Holdout is the unbiased number.
- Finalist checks on all eight search folds: 10, 15 and 30 minute bars with unchanged bar-count parameters; random-entry
  twin (60 twins); doubled costs ("stress"); every one-step parameter neighbour.
- Holdout: run once for the finalists, with frozen parameters, and reported as is.
