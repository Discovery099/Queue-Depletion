# How to check the Pine file in TradingView yourself (generation 82853, NOT CERTIFIED)

1. Open a 15-minute chart of the YM continuous contract with **regular trading hours only** (09:30 to 16:00 Eastern).
2. Paste `gen_082853.pine` into the Pine editor and add it to the chart. Leave every input at its default (execution mode stays `Sim/Paper`).
3. Open the Strategy Tester's list of trades and look for the ten trades below.

Times are US Eastern **bar open times**. Prices are from the research data for 1 contract and include 1 tick of slippage on market and stop fills. TradingView's continuous contract can differ slightly from the supplied data, and its fill model is more optimistic than the research engine's when a stop and a target fall inside one bar, so small price differences are expected. **Exact timing and direction matter more than price.**

| # | Direction | Entry time | Entry price | Exit time (bar open) | Exit price | Exit reason | Net result (ticks) |
|---|---|---|---|---|---|---|---|
| 1 | long | 2023-04-20 10:45 | 33941 | 2023-04-20 11:15 | 33940 | stop | +19.8 |
| 2 | long | 2023-05-10 11:30 | 33554 | 2023-05-10 12:30 | 33442 | stop | -112.5 |
| 3 | long | 2023-06-01 11:45 | 33086 | 2023-06-01 15:30 | 33085 | stop | +25.8 |
| 4 | short | 2023-07-19 10:45 | 35325 | 2023-07-19 11:45 | 35326 | stop | +19.5 |
| 5 | long | 2023-07-20 09:45 | 35388 | 2023-07-20 10:15 | 35387 | stop | +18.0 |
| 6 | long | 2023-07-24 10:45 | 35573 | 2023-07-24 14:30 | 35572 | stop | +16.8 |
| 7 | short | 2023-07-27 14:30 | 35499 | 2023-07-27 14:45 | 35500 | stop | +22.0 |
| 8 | short | 2023-08-03 09:45 | 35243 | 2023-08-03 10:00 | 35332 | stop | -89.5 |
| 9 | short | 2023-08-15 10:15 | 35051 | 2023-08-15 15:45 | 35009 | session | +45.8 |
| 10 | long | 2023-08-28 09:45 | 34672 | 2023-08-28 11:30 | 34529 | stop | -143.5 |

If the trades appear at these times and directions, the Pine file is doing what the research engine did. If they do not, do not use the file; report the difference.

The independent replay check (`gen_082853_pine_parity.json`) confirmed that the file's signal logic equals the research engine's on 120 sessions per instrument at two timeframes. It did not execute the order section, which is why this manual check exists.

Reminder: this strategy failed the harness's lowest tier. The check above verifies the translation, not the strategy.
