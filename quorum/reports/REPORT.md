OUTCOME: the agreement idea was tested and does not reach the goal. Trades taken only when Smart Trend and other
strategies agree within 0 to 4 candles win 46 to 55% with a profit factor of about 1.0 to 1.1 on data the search
never saw. Nothing reached 5 trades a day with 60% wins and a profit factor of 2, even on the data it was selected on.

# Quorum project report (2026-11-15)

Data: ES and YM, 5-minute, regular hours, 947 sessions (2020-01-02 to 2023-09-01). After costs ($1.25 a side, 1 tick
slippage a side), entry at the next candle's open, flat at 16:00, 1 contract. "Discover" is half of those sessions
(walk-forward folds 1, 3, 5, 7); "Confirm" is the other half and was never used to pick anything except the final
ranking of a 9-member shortlist. The rules were written down in `PROTOCOL.md` before any result was seen.

## 1. Your idea exactly as you wrote it (Smart Trend V1 arrows + Lorentzian signals, defaults)

5-minute chart, all 947 sessions, exit after 4 candles (the Lorentzian script's own exit):

| Signal | Trades a day (ES / YM) | Win rate (ES / YM) | Profit factor (ES / YM) |
|---|---|---|---|
| Smart Trend arrows alone | 1.73 / 1.72 | 46% / 48% | 0.98 / 1.02 |
| Lorentzian signals alone | 1.64 / 1.70 | 46% / 48% | 0.94 / 0.91 |
| Both on the same candle | 0.55 / 0.59 | 50% / 52% | 1.07 / 1.06 |
| Both within 2 candles | 0.89 / 0.91 | 46% / 50% | 1.00 / 0.99 |
| Both within 4 candles | 1.03 / 1.03 | 47% / 49% | 0.94 / 0.97 |
| Random entries, same exit | | 43 to 47% | 0.83 to 0.92 |

With a 1 ATR stop and a 2R target the agreed trades win 35 to 38% (profit factor 1.04 to 1.13); held until the opposite
agreement, 42 to 50% (0.97 to 1.16). Same-candle agreement is slightly better than either script alone, by an amount
that could be chance (t about 1.5), and it trades about once every two days. Full table for 5, 10, 15 and 30 minutes:
`phase1.json`. The pictures you sent are real examples of it working; the table counts the ones where it did not.

## 2. Does agreement between ANY two library techniques help?

157 "voters" (59 portable trigger techniques from the 16k library at up to three settings each, plus the Lorentzian
signal and the kernel turn). For every voter and every pair of different techniques agreeing within 2 candles, the
average move over the next 30 minutes in the signal's direction, after costs, in ATR units:

| | Discover | Confirm |
|---|---|---|
| A single voter's signal (average) | -0.085 | -0.113 |
| Same, but only in the Smart Trail's direction | -0.050 | -0.080 |
| Two voters agreeing within 2 candles (8,320 pairs) | -0.047 | -0.107 |
| Pairs with a strong result on Discover (t > 2) | 217 (about 190 expected by luck alone) | none repeated |
| Pairs that pass a false-discovery test at 10% | 0 | |

Agreement improves the average move by about 0.04 ATR on the half used to look and by nothing on the other half.
Round-trip costs are about 0.11 ATR on ES and 0.07 on YM at 5 minutes, larger than any average move found.

## 3. The 100,000-candidate merge search

Each candidate = Smart Trend base (as an arrow or as the trail's direction, factor 1 to 3) + 1 to 4 voters + how many
must agree + window 0 to 4 + one exit (ATR stop and target with optional half-off and break-even, fixed bars, Smart
Trail stop, or opposite agreement). 99,993 candidates were evaluated on Discover only.

| Trades a day per instrument (Discover) | Candidates | Median profit factor | Best profit factor | Meeting 60% wins and profit factor 2 |
|---|---|---|---|---|
| under 1 | 33,254 | 1.22 | 3.00 | 299 |
| 1 to 3 | 33,764 | 1.08 | 1.63 | 0 |
| 3 to 5 | 10,953 | 1.00 | 1.25 | 0 |
| 5 or more | 4,460 | 0.97 | 1.17 | 0 |

So even on the data used for selection, the goal is met only by candidates that trade less than once a day, where a
small sample makes a lucky result easy.

On the unseen half:

| Group | Profit factor on Discover | Profit factor on Confirm |
|---|---|---|
| 300 candidates picked at random | 1.08 | 0.93 |
| The 9 best distinct candidates | 1.50 | 0.98 (1 of 9 above 1.0) |
| Best high-frequency candidate (5.0 trades a day, 64% wins) | 1.12 | 0.98 (62% wins) |

## 4. The one candidate that stayed above 1.0 (the default of the delivered script)

Smart Trend arrow (factor 2), then within 3 candles one of: squeeze release, wick rejection at a 5-bar extreme, Hull
average (49) turn, low-volume new extreme reversal. Stop 3 ATR, half off at 1.5 ATR then stop to entry, rest at
2.25 ATR, out after 12 candles.

| Measure | Value |
|---|---|
| Discover | 1.42 trades a day, 61% wins, profit factor 1.50 |
| Confirm | 1.40 trades a day, 55% wins, profit factor 1.06 (ES 1.05, YM 1.07); drawdown larger than the net profit |
| All 947 sessions | 58% wins, profit factor 1.28; random entries with the same exits: 53%, 0.91 |
| Doubled costs | profit factor 1.17 |
| Other timeframes, same settings | 10 min 1.07; 15 min 0.94; 30 min 1.34 |
| 21 one-step parameter neighbours | profit factor 0.83 to 1.40, median 1.19 |

It has a real but small edge over random entries (about 5 points of win rate) and it is not a strategy that meets
any part of the goal on unseen data.

## 5. Why the goal is out of reach here

A profit factor of 2 at 60% wins means the average win is 1.33 times the average loss: about 0.4 of the risk earned
per trade, five times a day. Across 157 techniques and 8,320 agreements the average move after a signal is 0.0 to
0.1 ATR before costs, and costs are 0.07 to 0.11 ATR. Agreement between indicators built from the same candles mostly
repeats the same information; it removes trades but does not add foresight. The previous project (100,000 generations)
reached the same ceiling by a different route: about 1.2 to 1.3 on unseen data.

## 6. What was not tested, and deviations from the protocol

- Overnight holding: the data has regular hours only. NQ and 1-minute bars (your screenshots): no data here.
- The Holdout (168 sessions from 2023-09-04) was NOT opened. Nothing met the acceptance levels on Confirm, so opening
  it could not change the verdict; it stays clean. The vault stays sealed.
- The shortlist came out at 9 instead of up to 60: the best 400 candidates were near-copies of each other.
- Confirm was also computed for 300 randomly chosen candidates, to report the overall picture (not used for selection).
- The delivered Pine file has not been compiled in TradingView. Its voter formulas are generated by the emitter that
  was checked against an independent interpreter in the previous project; its agreement logic was checked in Python
  against the research engine (identical on 1,501 signals); the order section and the Lorentzian block are unverified.
- The Lorentzian signal scales two of its inputs by their all-time high and low, so its arrows depend on how much
  history the chart has loaded. They do not repaint on a fixed history.

## 7. Options

1. Send NQ data (and 1-minute, 24-hour data if you have it). The whole pipeline now runs in about 15 minutes, so the
   same test on the market and timeframe you actually watch is cheap. This is the most useful next step.
2. Lower the frequency target. Results look better on slower charts (30-minute agreement trades: profit factor 1.2 to 1.5 on ES and
   0.9 to 1.3 on YM, on 120 to 230 trades each), at well under one trade a day and on samples too small to trust yet.
3. Paper-trade the delivered script on NQ 1-minute and compare with the check sheet logic; it is a test bench, and its
   inputs let you switch voters on and off without code.

Nothing here is financial advice, and no backtest result is a promise of live performance.
