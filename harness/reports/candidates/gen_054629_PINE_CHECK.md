# How to check the Pine file in TradingView yourself (generation 54629, NOT CERTIFIED)

1. Open a 15-minute chart of the YM continuous contract with **regular trading hours only** (09:30 to 16:00 Eastern).
2. Paste `gen_054629.pine` into the Pine editor and add it to the chart. Leave every input at its default (execution mode stays `Sim/Paper`).
3. Open the Strategy Tester's list of trades and look for the ten trades below.

Times are US Eastern **bar open times**. Prices are from the research data for 1 contract and include 1 tick of slippage on market and stop fills. TradingView's continuous contract can differ slightly from the supplied data, and its fill model is more optimistic than the research engine's when a stop and a target fall inside one bar, so small price differences are expected. **Exact timing and direction matter more than price.**

| # | Direction | Entry time | Entry price | Exit time (bar open) | Exit price | Exit reason | Net result (ticks) |
|---|---|---|---|---|---|---|---|
| 1 | short | 2023-05-10 13:30 | 33327 | 2023-05-10 14:00 | 33430 | stop | -103.5 |
| 2 | long | 2023-06-02 12:00 | 33718 | 2023-06-02 15:45 | 33819 | session | +78.5 |
| 3 | long | 2023-06-29 10:15 | 34272 | 2023-06-29 10:30 | 34271 | stop | +20.5 |
| 4 | long | 2023-07-20 09:45 | 35388 | 2023-07-20 10:15 | 35387 | stop | +18.0 |
| 5 | short | 2023-08-04 14:30 | 35248 | 2023-08-04 15:45 | 35167 | session | +65.5 |
| 6 | short | 2023-08-08 09:45 | 35250 | 2023-08-08 12:15 | 35234.5 | stop | +33.5 |
| 7 | short | 2023-08-15 10:15 | 35051 | 2023-08-15 15:45 | 35009 | session | +45.8 |
| 8 | short | 2023-08-22 11:15 | 34386 | 2023-08-22 12:30 | 34387 | stop | +20.5 |
| 9 | long | 2023-08-24 10:00 | 34719 | 2023-08-24 10:00 | 34631 | stop | -88.5 |
| 10 | short | 2023-09-01 12:00 | 34779 | 2023-09-01 15:15 | 34872 | stop | -93.5 |

If the trades appear at these times and directions, the Pine file is doing what the research engine did. If they do not, do not use the file; report the difference.

The independent replay check (`gen_054629_pine_parity.json`) confirmed that the file's signal logic equals the research engine's on 120 sessions per instrument at two timeframes. It did not execute the order section, which is why this manual check exists.

Reminder: this strategy failed the harness's lowest tier. The check above verifies the translation, not the strategy.
