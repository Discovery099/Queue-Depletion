# How to check the Pine file in TradingView yourself (generation 54507, NOT CERTIFIED)

1. Open a 15-minute chart of the YM continuous contract with **regular trading hours only** (09:30 to 16:00 Eastern).
2. Paste `gen_054507.pine` into the Pine editor and add it to the chart. Leave every input at its default (execution mode stays `Sim/Paper`).
3. Open the Strategy Tester's list of trades and look for the ten trades below.

Times are US Eastern **bar open times**. Prices are from the research data for 1 contract and include 1 tick of slippage on market and stop fills. TradingView's continuous contract can differ slightly from the supplied data, and its fill model is more optimistic than the research engine's when a stop and a target fall inside one bar, so small price differences are expected. **Exact timing and direction matter more than price.**

| # | Direction | Entry time | Entry price | Exit time (bar open) | Exit price | Exit reason | Net result (ticks) |
|---|---|---|---|---|---|---|---|
| 1 | long | 2023-03-31 15:30 | 33436 | 2023-03-31 15:45 | 33457 | session | +27.5 |
| 2 | short | 2023-04-20 15:15 | 33818 | 2023-04-20 15:45 | 33896 | stop | -78.5 |
| 3 | short | 2023-05-12 11:45 | 33268 | 2023-05-12 13:15 | 33269 | stop | +21.5 |
| 4 | long | 2023-06-13 11:15 | 34264 | 2023-06-13 14:30 | 34165 | stop | -99.5 |
| 5 | long | 2023-06-15 10:00 | 34464 | 2023-06-15 10:30 | 34463 | stop | +31.8 |
| 6 | long | 2023-06-29 11:15 | 34266 | 2023-06-29 14:00 | 34265 | stop | +21.5 |
| 7 | long | 2023-08-07 10:30 | 35472 | 2023-08-07 15:45 | 35557 | session | +71.2 |
| 8 | long | 2023-08-10 10:15 | 35640 | 2023-08-10 10:30 | 35523 | stop | -117.5 |
| 9 | short | 2023-08-16 13:15 | 34912 | 2023-08-16 13:45 | 35004 | stop | -92.5 |
| 10 | long | 2023-08-24 10:00 | 34719 | 2023-08-24 10:00 | 34631 | stop | -88.5 |

If the trades appear at these times and directions, the Pine file is doing what the research engine did. If they do not, do not use the file; report the difference.

The independent replay check (`gen_054507_pine_parity.json`) confirmed that the file's signal logic equals the research engine's on 120 sessions per instrument at two timeframes. It did not execute the order section, which is why this manual check exists.

Reminder: this strategy failed the harness's lowest tier. The check above verifies the translation, not the strategy.
