# How to check the Pine file in TradingView yourself (generation 47285, NOT CERTIFIED)

1. Open a 15-minute chart of the YM continuous contract with **regular trading hours only** (09:30 to 16:00 Eastern).
2. Paste `gen_047285.pine` into the Pine editor and add it to the chart. Leave every input at its default (execution mode stays `Sim/Paper`).
3. Open the Strategy Tester's list of trades and look for the ten trades below.

Times are US Eastern **bar open times**. Prices are from the research data for 1 contract and include 1 tick of slippage on market and stop fills. TradingView's continuous contract can differ slightly from the supplied data, and its fill model is more optimistic than the research engine's when a stop and a target fall inside one bar, so small price differences are expected. **Exact timing and direction matter more than price.**

| # | Direction | Entry time | Entry price | Exit time (bar open) | Exit price | Exit reason | Net result (ticks) |
|---|---|---|---|---|---|---|---|
| 1 | long | 2023-04-13 09:45 | 33813 | 2023-04-13 15:45 | 34192 | session | +214.8 |
| 2 | long | 2023-05-18 15:45 | 33579 | 2023-05-18 15:45 | 33614 | session | +40.5 |
| 3 | short | 2023-06-23 09:45 | 33983 | 2023-06-23 12:30 | 34079 | stop | -96.5 |
| 4 | long | 2023-06-30 09:45 | 34578 | 2023-06-30 10:30 | 34577 | stop | +22.2 |
| 5 | long | 2023-07-26 09:45 | 35600 | 2023-07-26 10:00 | 35537 | stop | -63.5 |
| 6 | long | 2023-07-26 14:45 | 35775 | 2023-07-26 14:45 | 35701 | stop | -74.5 |
| 7 | long | 2023-08-01 10:00 | 35780 | 2023-08-01 10:15 | 35700 | stop | -80.5 |
| 8 | long | 2023-08-24 10:00 | 34719 | 2023-08-24 10:00 | 34631 | stop | -88.5 |
| 9 | long | 2023-08-31 10:00 | 35063 | 2023-08-31 11:00 | 34983 | stop | -80.5 |
| 10 | short | 2023-09-01 12:00 | 34779 | 2023-09-01 15:15 | 34872 | stop | -93.5 |

If the trades appear at these times and directions, the Pine file is doing what the research engine did. If they do not, do not use the file; report the difference.

The independent replay check (`gen_047285_pine_parity.json`) confirmed that the file's signal logic equals the research engine's on 120 sessions per instrument at two timeframes. It did not execute the order section, which is why this manual check exists.

Reminder: this strategy failed the harness's lowest tier. The check above verifies the translation, not the strategy.
