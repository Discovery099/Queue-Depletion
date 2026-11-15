# How to check the Pine file in TradingView yourself (generation 87819, NOT CERTIFIED)

1. Open a 15-minute chart of the YM continuous contract with **regular trading hours only** (09:30 to 16:00 Eastern).
2. Paste `gen_087819.pine` into the Pine editor and add it to the chart. Leave every input at its default (execution mode stays `Sim/Paper`).
3. Open the Strategy Tester's list of trades and look for the ten trades below.

Times are US Eastern **bar open times**. Prices are from the research data for 1 contract and include 1 tick of slippage on market and stop fills. TradingView's continuous contract can differ slightly from the supplied data, and its fill model is more optimistic than the research engine's when a stop and a target fall inside one bar, so small price differences are expected. **Exact timing and direction matter more than price.**

| # | Direction | Entry time | Entry price | Exit time (bar open) | Exit price | Exit reason | Net result (ticks) |
|---|---|---|---|---|---|---|---|
| 1 | short | 2023-04-19 09:45 | 33965 | 2023-04-19 14:00 | 34099 | stop | -134.5 |
| 2 | long | 2023-06-14 10:00 | 34411 | 2023-06-14 14:00 | 34257 | stop | -154.5 |
| 3 | long | 2023-07-12 09:45 | 34736 | 2023-07-12 12:15 | 34579 | stop | -157.5 |
| 4 | long | 2023-07-24 10:45 | 35573 | 2023-07-24 14:30 | 35572 | stop | +28.5 |
| 5 | short | 2023-08-02 10:00 | 35586 | 2023-08-02 15:45 | 35396 | session | +125.8 |
| 6 | short | 2023-08-09 12:00 | 35161 | 2023-08-09 13:00 | 35315 | stop | -154.5 |
| 7 | short | 2023-08-16 13:15 | 34912 | 2023-08-16 15:45 | 34819 | session | +83.5 |
| 8 | short | 2023-08-17 15:00 | 34597 | 2023-08-17 15:45 | 34598 | stop | +36.5 |
| 9 | long | 2023-08-25 11:15 | 34188 | 2023-08-25 15:45 | 34379 | session | +127.8 |
| 10 | long | 2023-08-28 09:45 | 34672 | 2023-08-28 15:45 | 34591 | session | -81.5 |

If the trades appear at these times and directions, the Pine file is doing what the research engine did. If they do not, do not use the file; report the difference.

The independent replay check (`gen_087819_pine_parity.json`) confirmed that the file's signal logic equals the research engine's on 120 sessions per instrument at two timeframes. It did not execute the order section, which is why this manual check exists.

Reminder: this strategy failed the harness's lowest tier. The check above verifies the translation, not the strategy.
