# Holdout candidates: Pine scripts for your own backtest

None of these is a validated strategy. All five were tested and none passed (see the table). They are here so you
can see for yourself how they behave, including on the data after April 2024 that the research never touched.

| File | Chart | 2020 to Sep 2023 | Sep 2023 to Apr 2024 (never seen) |
|---|---|---|---|
| `A_gen25968_momentum_thrust_5min.pine` | 5 min | 73% wins, PF 1.19, about 1.6 trades a day per instrument | 69% wins, PF 0.91, net -$7,290 |
| `B_gen44439_momentum_thrust_15min.pine` | 15 min | 69% wins, PF 1.51, about 0.6 a day | 61% wins, PF 0.80, net -$9,642 |
| `C_noise_area_momentum.pine` | 5 min (works on 10, 15, 30) | 37% wins, PF 1.08 (ES 1.21, YM 0.93), 0.8 a day | 35% wins, PF 0.95 (ES 1.10, YM 0.78), net -$3,060 |
| `S2_last_half_hour_momentum.pine` | 5 min | 44% wins, PF 0.81 | not run (failed earlier) |
| `S3_opening_range_breakout_5min.pine` | 5 min | 21% wins, PF 0.92 | not run (failed earlier) |

ES and YM pooled, 1 contract, after $1.25 a side commission and 1 tick slippage a side, entry at the next candle's open.

## How to backtest
1. Open ES1! or YM1! at the chart timeframe in the table. A, B: use a regular-hours chart. C, S2, S3: either a
   regular-hours or a 24-hour chart; they trade only 09:30 to 16:00 New York (input "Trading session").
2. Pine Editor, paste the file, "Add to chart". Leave the defaults (paper mode, no webhook URL, 1 contract).
3. Strategy Tester: compare the trades against `CHECK_SHEETS.md`, ten trades per instrument from the end of the
   research data. Same times and sides mean the script behaves as it did in research.
4. Then look at November 2025 onward (or whatever your history reaches): that is data none of this work ever saw.

## What was checked, and what was not
- None of these files has been compiled in TradingView (it cannot run here). If one shows an error, send it to me.
- A and B: signal logic checked against the research engine by an independent interpreter (identical); the order
  section was not executed.
- C: its noise boundaries, VWAP, entry and exit signals were reproduced bar by bar in Python from the Pine logic and
  matched the research engine exactly on all 947 sessions for ES and YM. S2 and S3 are simple enough that I checked
  them by reading only.
- TradingView fills stops and targets more favourably than the research engine (which assumes the stop is hit first
  when both are inside one candle), so its results for A and B will look better than the research figures.
- A and B carry your "06 Webhook / Live Gates" group with paper defaults; stop and target exits send CLOSE_LONG /
  CLOSE_SHORT. Verify your server handles those in paper mode before anything else.

Nothing here is financial advice, and no backtest result is a promise of live performance.
