# How to check the Pine file in TradingView yourself (generation 65921, NOT CERTIFIED)

1. Open a 15-minute chart of the YM continuous contract with **regular trading hours only** (09:30 to 16:00 Eastern).
2. Paste `gen_065921.pine` into the Pine editor and add it to the chart. Leave every input at its default (execution mode stays `Sim/Paper`).
3. Open the Strategy Tester's list of trades and look for the ten trades below.

Times are US Eastern **bar open times**. Prices are from the research data for 1 contract and include 1 tick of slippage on market and stop fills. TradingView's continuous contract can differ slightly from the supplied data, and its fill model is more optimistic than the research engine's when a stop and a target fall inside one bar, so small price differences are expected. **Exact timing and direction matter more than price.**

| # | Direction | Entry time | Entry price | Exit time (bar open) | Exit price | Exit reason | Net result (ticks) |
|---|---|---|---|---|---|---|---|
| 1 | long | 2023-04-06 12:15 | 33652 | 2023-04-06 12:45 | 33651 | stop | +20.5 |
| 2 | short | 2023-04-20 15:30 | 33815 | 2023-04-20 15:45 | 33892 | stop | -77.5 |
| 3 | short | 2023-05-04 09:45 | 33230 | 2023-05-04 11:00 | 33231 | stop | +40.2 |
| 4 | short | 2023-05-12 14:15 | 33186 | 2023-05-12 15:30 | 33279 | stop | -93.5 |
| 5 | long | 2023-05-15 13:00 | 33400 | 2023-05-15 13:15 | 33399 | stop | +18.8 |
| 6 | long | 2023-05-26 09:45 | 33059 | 2023-05-26 11:15 | 33058 | stop | +28.8 |
| 7 | short | 2023-05-31 10:30 | 32834 | 2023-05-31 13:30 | 32935 | stop | -101.5 |
| 8 | long | 2023-06-01 11:45 | 33086 | 2023-06-01 15:30 | 33085 | stop | +25.8 |
| 9 | long | 2023-07-18 10:00 | 34962 | 2023-07-18 15:45 | 35139 | session | +107.8 |
| 10 | short | 2023-08-15 09:45 | 35167 | 2023-08-15 15:45 | 35009 | session | +102.0 |

If the trades appear at these times and directions, the Pine file is doing what the research engine did. If they do not, do not use the file; report the difference.

The independent replay check (`gen_065921_pine_parity.json`) confirmed that the file's signal logic equals the research engine's on 120 sessions per instrument at two timeframes. It did not execute the order section, which is why this manual check exists.

Reminder: this strategy failed the harness's lowest tier. The check above verifies the translation, not the strategy.
