# Smart Trend + HMA + RSI — enhancement research

All 13 proposed enhancements are built, tested and reported here. The research uses 6 years of
5-minute regular-trading-hours (RTH) data for ES, MES, MNQ, YM and MGC, from 2020-01 to 2026-03.

| File | What it is |
|---|---|
| `pine/SmartTrend_Enhanced.pine` | The enhanced TradingView strategy (Pine v6). The original signal engine is unchanged, and every enhancement is an input. |
| `st/` | Python research engine: indicators, signal logic, a bar-by-bar simulator with TradingView fill rules, filters, meta-model, portfolio |
| `run_baseline.py` | Original strategy on the 6-year data, reconciled against your TradingView exports |
| `run_final.py` | End-to-end evaluation: walk-forward model, stacked enhancements, portfolio, model export |
| `make_charts.py` | Equity-curve chart |
| `tests/` | Look-ahead (causality) tests and logic checks |
| `results/` | Metrics CSVs, trade lists, the exported model (`meta_model.json`), `equity_curve.png`, run log |

## Headline (out of sample, realistic fills)

Portfolio: 6 MES + 5 MNQ + 1 YM, about $200k notional per market, 2022-01 to 2026-03.
Fills: 1 tick slippage, limit orders must trade 1 tick through, $2.50 round-turn commission per contract.

| | Original script | **Enhanced (preset S1 + guard)** | Enhanced (preset S4 + guard) |
|---|---|---|---|
| Profit factor | 0.88 | **1.31** | 1.29 |
| Net P&L | −$62,962 | **+$114,348** | +$58,545 |
| Max drawdown | −$65,063 | **−$20,420** | −$12,082 |
| Return / max drawdown | −0.97 | **5.60** | 4.85 |
| Worst day | −$10,300 | **−$3,850** | −$3,382 |
| Profitable months | 39% | **57%** | 61% |
| Sharpe ratio (daily) | −1.15 | **1.42** | 1.57 |
| Trades | 4,542 | 1,334 | 1,384 |

Split into the selection window (2022–23) and the confirmation window (2024–26):

| | 2022–23 PF | 2024–26 PF | 2022–23 max DD | 2024–26 max DD |
|---|---|---|---|---|
| Original | 0.88 | 0.89 | −$35.6k | −$36.1k |
| S1 + guard | 1.35 | 1.28 | −$11.3k | −$20.4k |
| S4 + guard | 1.34 | 1.25 | −$9.9k | −$12.1k |

Per symbol, S1, 1 contract each, profit factor 2022–23 / 2024–26: ES 1.27/1.29, MES 1.18/1.25,
MNQ 1.17/1.18, YM 1.89/1.64. The original scores 0.88–0.95 on every symbol.

![equity](results/equity_curve.png)

### Read this before trading it

- **It depends on big trend days.** Profit factor drops to **1.16** without April 2025 (the
  tariff-shock month, +$58k), and to **1.07** without the 10 best days. Expect long flat
  stretches. 2024 lost (PF 0.89, −$8.6k), and May 2025 to March 2026 is −$7.7k. S4 depends less
  on outliers (PF 1.21 without April 2025, 1.10 without the top 10 days) but makes less money.
- **The edge has been weaker recently.** Since mid-2025 the equity curve is flat to down. The
  model is retrained every January, so the 2026 model includes 2025, but there's no guarantee it
  adapts.
- **MGC (gold) is excluded.** The signal and the model lose money on gold in every variant
  (PF 0.66–0.88).
- **RTH chart required.** The model was trained on 09:30–16:00 New York bars. On an
  extended-hours chart the ATR, RSI and trail values differ, so the model's inputs differ.
- **The Pine Script hasn't been compiled here** (no TradingView in this environment). Load it,
  run it on a 5-minute RTH chart of MES/ES/MNQ/YM, and send back the List of Trades so I can
  reconcile it with the Python engine.

## Key findings that drove the design

1. **The HMA leg is degenerate.** With length 2, `ta.hma(close, 2) = close + (close − close[1])/3`.
   So "close crosses over the HMA" happens exactly when the close is *lower* than the prior close:
   an HMA "buy" fires on a down bar. Combined with the conflict-reset rule, this means **Smart
   Trend flips never become trades. Every trade comes from the pullback-recovery signal.**
   Replacing the leg (HMA 9/21, or removing it) made results *worse*, so the accidental "enter
   on a counter-bar" timing is kept.
2. **The original target is `min(1.25 × ATR, $150)`.** On full-size contracts the $150 cap
   always applies: 3 points on ES, 7.5 on NQ, 0.03 on SI. That is why those symbols win 85–90%
   of trades and still lose money.
3. **The raw signal has no edge after costs.** The average move after a signal is about
   +0.10 ATR, while costs are about 0.15–0.2 ATR. Across 360 stop/target/time-limit combinations
   the best profit factor is about 1.04. No exit design can rescue it on its own.
4. **Static filters tuned on 2020–23 failed on 2024–26.** Efficiency ratio, VWAP extension,
   15-minute agreement and late-session timing all looked strong in-sample and turned flat or
   negative out of sample.
5. **A walk-forward meta-label model fixes the selection problem.** It's a logistic regression
   on 24 causal features, pooled across the index futures and retrained every January on
   earlier years only. Selected trades score PF 1.36–1.53 out of sample, across every
   regularisation strength and every stop from 2 to 4 ATR, against about 1.05 for all signals.
   The coefficients keep the same sign in every training window. The model favours:
   - price near the day's high (low for shorts);
   - later in the session;
   - DMI agreeing with the trade;
   - a gap in the trade direction.

   It penalises shock bars and an overstretched RSI, and it prefers the 60-minute trend to be
   still *against* the trade, which catches early trend-day turns.
6. **Wrong sizing kills it.** The edge sits in higher-ATR trades. Sizing by fixed dollar risk
   down-weights those trades, and MES and MNQ fell to PF about 1.0. Use fixed contracts.

## All 13 enhancements: what each one did

Each was tested on top of the meta-filter strategy (2022–26, per symbol) unless noted.

| # | Enhancement | Result | In the final config? |
|---|---|---|---|
| 1 | Exit when the Smart Trend regime flips | Net −35%, lower PF | Off (input available) |
| 2 | Time stop for trades that don't follow through | Neutral to slightly worse | Off (input available) |
| 3 | Volatility-shock guard (range > x ATR, ATR spike) | No change (the model already uses bar range) | Off. "Skip the first 30 min" is in preset S4 |
| 4 | Emergency stop + daily loss limits | 3 ATR stop: worst day −$5.2k → −$3.1k (1 contract per symbol). Max-losers/day is in S4 | **3 ATR stop on**; daily rules in S4 |
| 5 | ATR target/stop with no $150 cap | Removing the cap helps. A fixed target then hurts: hold to the session close is best | No fixed target |
| 6 | Scale out half + break-even + chandelier runner | Lower drawdown, less net, least outlier-dependent | Preset **S4** |
| 7 | Replace HMA(2) | Worse (gPF 0.91 → 0.83–0.88) | Original kept |
| 8 | Trend-quality filter (ER / ADX) | Failed out of sample as a static filter | Used as model features |
| 9 | Higher-timeframe agreement (15m / 60m) | Failed out of sample as a static filter | Used as model features |
| 10 | Location filter (VWAP / trail distance) | Failed out of sample as a static filter | Used as model features |
| 11 | Meta-label ML filter (walk-forward) | **PF 0.92 → 1.35 per symbol** | **On** |
| 12 | Regime-adaptive exits (scale out only if ER ≥ 0.3) | Similar to S2 | Input available (S3) |
| 13 | Correlation guard (max 2 index positions) + portfolio daily stop | DD −27.1k → −20.4k, worst day −5.4k → −3.9k, net −24% | **On** (operating rule) |
| – | Size by risk (fixed $ per trade) | Rejected: removes the edge (see finding 6) | Off |
| – | Adaptive on/off switch from recent signal performance | No consistent value | Not built into Pine |
| – | Realistic fills (target must trade 1 tick through) | Original PF 0.95 → 0.91 | Used in every test |

The final configuration (S1 + guard) was chosen by return/drawdown on **2022–23 only**.
2024–26 was not used for any choice. The one exception is the 3 ATR label stop: the exit grid
that suggested it looked at both windows, but the meta-model result holds for every stop
from 2 to 4 ATR.

## Using the Pine Script

1. Open a **5-minute** chart of MES, ES, MNQ or YM (MYM/NQ should work, but weren't tested). Set
   the session to **regular trading hours**.
2. Add `SmartTrend_Enhanced.pine`. Preset **Selected (S1)** is the tested default. **Smoother
   (S4)** trades lower drawdown for lower profit.
3. Sizing: **fixed contracts** ("Size by risk" off). The research used about $200k notional per
   market (6 MES / 5 MNQ / 1 YM). Scale down to what your account's drawdown limit allows.
   For example, 1 MES + 1 MNQ + 1 MYM is roughly 1/6 of the research size, so expect a max
   drawdown of about −$3.5k and a worst day of about −$650.
4. Portfolio rules (can't be enforced inside a single-symbol script; apply at account level):
   - at most **2 index positions open** at a time;
   - stop for the day after the portfolio is down **$1,500** at the research size; scale this
     with your size.
5. A score label prints the model probability on every raw signal. Faded circles are signals the
   filter skipped.

## Reproduce / extend

```bash
pip install numpy pandas numba scikit-learn lightgbm matplotlib pytest
```

```bash
python3 run_baseline.py
```

```bash
python3 run_final.py
```

```bash
python3 make_charts.py
```

```bash
python3 -m pytest -q tests
```

Data goes in `data/<SYMBOL>_5min_RTH.csv` (Databento-style columns
`ts_event,symbol,open,high,low,close,volume`). The data files are git-ignored. New index
symbols (MYM, M2K, RTY, NQ) are picked up automatically by `run_final.py` once their files are
present, and the model is retrained to include them. Non-index markets (MCL, gold) need their own
evaluation: the model is index-only.
