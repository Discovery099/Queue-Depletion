OUTCOME: nothing profitable was found. Three published intraday rules, a machine-learning model combining every
library technique, and the three best candidates from all earlier work were tested. On 168 sessions that none of
them had ever seen (September 2023 to April 2024), all three candidates lost money.

# Daytrend project report (2026-11-16)

Data: ES and YM, 5-minute, regular hours. After costs ($1.25 a side, 1 tick slippage a side), entry at the next
candle's open, flat at 16:00, 1 contract. Rules fixed in advance in `PROTOCOL.md`; the one change to them (opening
the Holdout) was written down and committed before the Holdout was opened.

## 1. Three published intraday rules, at their published settings (947 sessions, 2020 to September 2023)

| Rule | Trades a day | Win rate | Profit factor ES / YM | Doubled costs | Folds profitable |
|---|---|---|---|---|---|
| Noise-area momentum (Zarattini, Aziz, Barbon 2024) | 0.79 | 37% | 1.21 / 0.93 | 1.01 | 7 of 8 |
| Last-half-hour momentum (Gao, Han, Li, Zhou 2018) | 0.96 | 44% | 0.82 / 0.80 | 0.73 | 2 of 8 |
| 5-minute opening-range breakout (Zarattini, Aziz 2023) | 0.99 | 21% | 0.98 / 0.85 | 0.86 | 3 of 8 |

None met the bar fixed beforehand (profit factor 1.30 pooled and 1.15 on each instrument). Their published results
were on other markets or periods and, for the first, on SPY with lower relative costs.

## 2. Machine-learning combiner of every library technique

190 inputs (every trigger, state, filter and location technique in the catalogue, plus 20 plain descriptors), one
pre-set gradient-boosted model, trained walk-forward so every prediction is on data the model had not seen.

| Horizon | Correlation of prediction with outcome | Trades a day | Win rate | Profit factor |
|---|---|---|---|---|
| Next 30 minutes | +0.012 | 4.0 | 48% | 0.93 |
| To the close | +0.043 | 1.4 | 46% | 1.02 (0.99 at doubled costs) |

With all 190 techniques combined, the model ranks the next 30 minutes almost no better than chance. The
to-the-close model finds a small trend-day effect, gone after costs.

## 3. One-time Holdout audit (168 sessions, September 2023 to April 2024, never seen before)

The three candidates with the best record across all three projects, frozen exactly:

| Candidate | Search record | Holdout trades | Holdout win rate | Holdout profit factor | Holdout net (1 contract each) |
|---|---|---|---|---|---|
| Project 1, generation 25968 (5 min) | 73% wins, PF 1.19 | 510 | 69% | 0.91 | -$7,290 |
| Project 1, generation 44439 (15 min) | 69% wins, PF 1.51 | 222 | 61% | 0.80 | -$9,642 |
| Noise-area momentum, published | PF 1.08 (ES 1.21) | 311 | 35% | 0.95 (ES 1.10, YM 0.78) | -$3,060 |

The win rates held up; the money did not. A 69% win rate paired with wins 0.40 the size of the losses is a losing
strategy. With 168 sessions this test is weak, but three of three negative is not what a real edge looks like.

## 4. What this adds up to

Across three projects about 200,000 rule candidates, 8,320 indicator agreements, three published rules and one
model built from the whole library were tested on this data. The best of them were small trend-day effects that
did not survive the next eight months. Technical indicators on 5-minute ES and YM regular-hours bars do not appear to
carry enough information to pay round-trip costs reliably, let alone reach 5 trades a day at a profit factor of 2.
More searching over the same scripts and the same data would only produce better-looking fits.

## 5. What could change the answer

Different information, not more combinations of the same:
1. NQ (you trade it) and the overnight session. 24-hour 1-minute data would let the overnight and the open be tested.
2. Order-flow data (bid/ask volume, depth). The library scripts are price-and-volume only.
3. Longer holding periods (days, not minutes), where costs are a small fraction of the move.

The vault (473 sessions after April 2024) is still sealed and remains a clean test for any of these.

Nothing here is financial advice, and no backtest result is a promise of live performance.
