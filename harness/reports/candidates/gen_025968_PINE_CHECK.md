# How to check the Pine file in TradingView yourself (generation 25968, NOT CERTIFIED)

1. Open a 5-minute chart of the YM continuous contract with **regular trading hours only** (09:30 to 16:00 Eastern).
2. Paste `gen_025968.pine` into the Pine editor and add it to the chart. Leave every input at its default (execution mode stays `Sim/Paper`).
3. Open the Strategy Tester's list of trades and look for the ten trades below.

Times are US Eastern and are **bar open times**; an entry at 10:35 means the order filled at the open of the 10:35 bar. Prices are from the research data, 1 contract, and include 1 tick of slippage on market and stop fills. TradingView's continuous contract can differ slightly from the supplied data, and its fill model is more optimistic than the research engine's when a stop and a target fall inside one bar, so small price differences are expected. **Exact timing and direction matter more than price.**

| # | Direction | Entry time | Entry price | Exit time (bar open) | Exit price | Exit reason | Net result (ticks) |
|---|---|---|---|---|---|---|---|
| 1 | short | 2023-04-06 09:45 | 33538 | 2023-04-06 10:40 | 33505 | target | +32.5 |
| 2 | long | 2023-04-10 10:15 | 33659 | 2023-04-10 12:35 | 33694 | target | +34.5 |
| 3 | short | 2023-04-18 10:05 | 33998 | 2023-04-18 10:25 | 33969 | target | +28.5 |
| 4 | short | 2023-05-10 13:25 | 33351 | 2023-05-10 13:25 | 33316 | target | +34.5 |
| 5 | long | 2023-06-23 15:45 | 34021 | 2023-06-23 15:55 | 33984 | session | -37.5 |
| 6 | long | 2023-07-11 09:35 | 34300 | 2023-07-11 10:00 | 34219 | stop | -81.5 |
| 7 | short | 2023-07-12 11:45 | 34646 | 2023-07-12 11:55 | 34613 | target | +32.5 |
| 8 | short | 2023-07-20 14:30 | 35372 | 2023-07-20 14:35 | 35440 | stop | -68.5 |
| 9 | short | 2023-08-04 13:55 | 35502 | 2023-08-04 13:55 | 35479 | target | +22.5 |
| 10 | long | 2023-08-30 09:35 | 34982 | 2023-08-30 09:45 | 35014 | target | +31.5 |

If the trades appear at these times and directions, the Pine file is doing what the research engine did. If they do not, do not use the file; report the difference.

The independent replay check (`gen_025968_pine_parity.json`) already confirmed that the file's signal logic equals the research engine's on 120 sessions per instrument at 5 and 15 minutes. It did not execute the order section, which is why this manual check exists.

Reminder: this strategy failed the harness's lowest tier. The check above verifies the translation, not the strategy.
