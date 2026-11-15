# How to check the Pine file in TradingView yourself (generation 50391, NOT CERTIFIED)

1. Open a 15-minute chart of the YM continuous contract with **regular trading hours only** (09:30 to 16:00 Eastern).
2. Paste `gen_050391.pine` into the Pine editor and add it to the chart. Leave every input at its default (execution mode stays `Sim/Paper`).
3. Open the Strategy Tester's list of trades and look for the ten trades below.

Times are US Eastern **bar open times**. Prices are from the research data for 1 contract and include 1 tick of slippage on market and stop fills. TradingView's continuous contract can differ slightly from the supplied data, and its fill model is more optimistic than the research engine's when a stop and a target fall inside one bar, so small price differences are expected. **Exact timing and direction matter more than price.**

| # | Direction | Entry time | Entry price | Exit time (bar open) | Exit price | Exit reason | Net result (ticks) |
|---|---|---|---|---|---|---|---|
| 1 | long | 2023-04-13 10:30 | 33930 | 2023-04-13 15:45 | 34192 | session | +156.5 |
| 2 | short | 2023-04-17 14:15 | 33975 | 2023-04-17 14:45 | 34053 | stop | -78.5 |
| 3 | long | 2023-04-24 10:15 | 33990 | 2023-04-24 11:30 | 33909 | stop | -81.5 |
| 4 | long | 2023-04-24 14:00 | 33959 | 2023-04-24 15:45 | 34007 | session | +40.0 |
| 5 | short | 2023-05-02 10:15 | 33832 | 2023-05-02 13:00 | 33672.5 | stop | +104.5 |
| 6 | long | 2023-06-01 11:45 | 33086 | 2023-06-01 15:30 | 33085 | stop | +25.8 |
| 7 | short | 2023-06-28 11:00 | 34003 | 2023-06-28 11:30 | 34076 | stop | -73.5 |
| 8 | short | 2023-07-27 14:30 | 35499 | 2023-07-27 14:45 | 35500 | stop | +22.0 |
| 9 | short | 2023-08-04 14:45 | 35206 | 2023-08-04 15:00 | 35207 | stop | +25.2 |
| 10 | short | 2023-08-24 11:45 | 34332 | 2023-08-24 15:45 | 34131 | session | +124.2 |

If the trades appear at these times and directions, the Pine file is doing what the research engine did. If they do not, do not use the file; report the difference.

The independent replay check (`gen_050391_pine_parity.json`) confirmed that the file's signal logic equals the research engine's on 120 sessions per instrument at two timeframes. It did not execute the order section, which is why this manual check exists.

Reminder: this strategy failed the harness's lowest tier. The check above verifies the translation, not the strategy.
