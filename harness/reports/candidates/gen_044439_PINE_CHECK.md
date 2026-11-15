# How to check the Pine file in TradingView yourself (generation 44439, NOT CERTIFIED)

1. Open a 15-minute chart of the YM continuous contract with **regular trading hours only** (09:30 to 16:00 Eastern).
2. Paste `gen_044439.pine` into the Pine editor and add it to the chart. Leave every input at its default (execution mode stays `Sim/Paper`).
3. Open the Strategy Tester's list of trades and look for the ten trades below.

Times are US Eastern **bar open times**. Prices are from the research data for 1 contract and include 1 tick of slippage on market and stop fills. TradingView's continuous contract can differ slightly from the supplied data, and its fill model is more optimistic than the research engine's when a stop and a target fall inside one bar, so small price differences are expected. **Exact timing and direction matter more than price.**

| # | Direction | Entry time | Entry price | Exit time (bar open) | Exit price | Exit reason | Net result (ticks) |
|---|---|---|---|---|---|---|---|
| 1 | long | 2023-04-06 12:45 | 33690 | 2023-04-06 15:45 | 33657 | session | -33.5 |
| 2 | short | 2023-04-25 13:15 | 33731 | 2023-04-25 15:45 | 33655 | target | +57.5 |
| 3 | long | 2023-06-02 12:00 | 33718 | 2023-06-02 14:30 | 33830 | target | +84.0 |
| 4 | long | 2023-06-13 11:15 | 34264 | 2023-06-13 14:30 | 34165 | stop | -99.5 |
| 5 | short | 2023-07-06 09:45 | 34125 | 2023-07-06 10:15 | 34042 | target | +62.2 |
| 6 | long | 2023-07-11 11:00 | 34269 | 2023-07-11 11:45 | 34343 | target | +55.5 |
| 7 | short | 2023-08-02 10:00 | 35586 | 2023-08-02 10:15 | 35511 | target | +55.8 |
| 8 | short | 2023-08-15 10:15 | 35051 | 2023-08-15 15:45 | 35009 | session | +45.8 |
| 9 | long | 2023-08-24 10:00 | 34719 | 2023-08-24 10:00 | 34631 | stop | -88.5 |
| 10 | short | 2023-08-24 11:45 | 34332 | 2023-08-24 14:30 | 34237 | target | +71.2 |

If the trades appear at these times and directions, the Pine file is doing what the research engine did. If they do not, do not use the file; report the difference.

The independent replay check (`gen_044439_pine_parity.json`) confirmed that the file's signal logic equals the research engine's on 120 sessions per instrument at two timeframes. It did not execute the order section, which is why this manual check exists.

Reminder: this strategy failed the harness's lowest tier. The check above verifies the translation, not the strategy.
