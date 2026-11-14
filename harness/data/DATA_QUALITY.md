# Data quality report (Generation 0)

Price statistics in this file use the Research block only. For the vault period only timestamps and row counts were examined.

## Raw files

| File | sha256 | rows | sessions | first | last |
|---|---|---|---|---|---|
| data/raw/ES_5min_RTH_6year.csv | `ead01c6e2173c3925d897b5e160350e31c71ceb06e6c7f2d1a029d22b16f47f1` | 122295 | 1594 | 20200102 | 20260306 |
| data/raw/YM_5min_RTH_6year.csv | `77dd831221c15938a00dd0f6ea922c70f7cb2ee5353aecefe89bccc342adddfd` | 122241 | 1593 | 20200102 | 20260306 |

## Partition

- Common sessions: 1593. Research: 1115 (20200102 to 20240429). Embargo: 5 (20240430 to 20240506). Vault: 473 (Vault-A 315, Vault-B 158).
- Inside Research: 947 search sessions (walk-forward folds) and 168 inner-holdout sessions starting 20230904.
- Sessions present in only one file, dropped from every block: {'ES': [20200228], 'YM': []}.

## Findings and decisions (Research block)

### ES

- Rows: 85695. OHLC inconsistencies: 0. Prices off the tick grid: 0.
- Rows with a missing symbol: 7; zero-volume rows: 7; identical sets: True. Dates: [20200309, 20200312, 20200316, 20200318]. Every one has open = high = low = close (True), i.e. it is a filler bar carried forward while the market did not trade. **Decision:** keep the rows so the 5-minute grid stays intact, flag them `filler=1`; the engine never fills on a zero-volume bar (SPEC 7.3) and volume features guard against division by zero.
- Session lengths (bars: count): {9: 1, 42: 28, 45: 6, 78: 1080}. Short sessions: 35. Most are 42- or 45-bar holiday sessions. The session calendar is built from the data; nothing assumes 78 bars, and strategies may not use session length (SPEC 9.5).
- Short sessions: 20200120(42), 20200217(42), 20200525(42), 20200630(9), 20200703(42), 20200907(42), 20201126(42), 20201127(45), 20201224(45), 20210118(42), 20210215(42), 20210531(42), 20210705(42), 20210906(42), 20211125(42), 20211126(45), 20220117(42), 20220221(42), 20220530(42), 20220620(42), 20220704(42), 20220905(42), 20221124(42), 20221125(45), 20230116(42), 20230220(42), 20230529(42), 20230619(42), 20230703(45), 20230704(42), 20230904(42), 20231123(42), 20231124(45), 20240115(42), 20240219(42).
- Overnight gap, absolute percent: median 0.356, 95th pct 1.546, 99th pct 3.463.
- Roll-adjustment test. Largest overnight gap inside each quarterly roll window (days 6 to 20 of March, June, September, December):

  | year | month | date | gap % | median abs gap % in window |
  |---|---|---|---|---|
  | 2020 | 3 | 20200318 | -7.69 | 3.82 |
  | 2020 | 6 | 20200616 | +2.77 | 1.07 |
  | 2020 | 9 | 20200908 | -1.96 | 0.66 |
  | 2020 | 12 | 20201215 | +0.78 | 0.40 |
  | 2021 | 3 | 20210309 | +1.07 | 0.35 |
  | 2021 | 6 | 20210618 | -0.87 | 0.17 |
  | 2021 | 9 | 20210920 | -1.49 | 0.20 |
  | 2021 | 12 | 20211207 | +1.23 | 0.61 |
  | 2022 | 3 | 20220309 | +2.15 | 0.56 |
  | 2022 | 6 | 20220613 | -2.58 | 0.89 |
  | 2022 | 9 | 20220913 | -2.24 | 0.63 |
  | 2022 | 12 | 20221213 | +2.86 | 0.34 |
  | 2023 | 3 | 20230314 | +1.34 | 0.21 |
  | 2023 | 6 | 20230614 | +1.09 | 0.22 |
  | 2023 | 9 | 20230913 | +1.13 | 0.36 |
  | 2023 | 12 | 20231213 | +1.16 | 0.20 |
  | 2024 | 3 | 20240313 | +1.27 | 0.41 |

  Mean signed gap inside roll windows -0.105% (n=181) versus outside +0.052% (n=933); median absolute gap inside 0.427% versus outside 0.338%.
### YM

- Rows: 85659. OHLC inconsistencies: 0. Prices off the tick grid: 0.
- Rows with a missing symbol: 7; zero-volume rows: 7; identical sets: True. Dates: [20200309, 20200312, 20200316, 20200318]. Every one has open = high = low = close (True), i.e. it is a filler bar carried forward while the market did not trade. **Decision:** keep the rows so the 5-minute grid stays intact, flag them `filler=1`; the engine never fills on a zero-volume bar (SPEC 7.3) and volume features guard against division by zero.
- Session lengths (bars: count): {9: 1, 42: 29, 45: 6, 78: 1079}. Short sessions: 36. Most are 42- or 45-bar holiday sessions. The session calendar is built from the data; nothing assumes 78 bars, and strategies may not use session length (SPEC 9.5).
- Short sessions: 20200120(42), 20200217(42), 20200227(42), 20200525(42), 20200630(9), 20200703(42), 20200907(42), 20201126(42), 20201127(45), 20201224(45), 20210118(42), 20210215(42), 20210531(42), 20210705(42), 20210906(42), 20211125(42), 20211126(45), 20220117(42), 20220221(42), 20220530(42), 20220620(42), 20220704(42), 20220905(42), 20221124(42), 20221125(45), 20230116(42), 20230220(42), 20230529(42), 20230619(42), 20230703(45), 20230704(42), 20230904(42), 20231123(42), 20231124(45), 20240115(42), 20240219(42).
- Overnight gap, absolute percent: median 0.326, 95th pct 1.483, 99th pct 3.516.
- Roll-adjustment test. Largest overnight gap inside each quarterly roll window (days 6 to 20 of March, June, September, December):

  | year | month | date | gap % | median abs gap % in window |
  |---|---|---|---|---|
  | 2020 | 3 | 20200318 | -7.66 | 3.68 |
  | 2020 | 6 | 20200616 | +3.38 | 1.23 |
  | 2020 | 9 | 20200908 | -1.65 | 0.43 |
  | 2020 | 12 | 20201215 | +0.60 | 0.34 |
  | 2021 | 3 | 20210310 | +0.61 | 0.16 |
  | 2021 | 6 | 20210618 | -1.17 | 0.13 |
  | 2021 | 9 | 20210920 | -1.61 | 0.24 |
  | 2021 | 12 | 20211220 | -1.18 | 0.41 |
  | 2022 | 3 | 20220309 | +2.02 | 0.51 |
  | 2022 | 6 | 20220613 | -2.28 | 0.68 |
  | 2022 | 9 | 20220913 | -1.80 | 0.54 |
  | 2022 | 12 | 20221213 | +2.26 | 0.28 |
  | 2023 | 3 | 20230314 | +1.02 | 0.33 |
  | 2023 | 6 | 20230614 | +0.49 | 0.09 |
  | 2023 | 9 | 20230913 | +1.03 | 0.24 |
  | 2023 | 12 | 20231213 | +1.03 | 0.18 |
  | 2024 | 3 | 20240313 | +1.37 | 0.29 |

  Mean signed gap inside roll windows -0.128% (n=181) versus outside +0.047% (n=933); median absolute gap inside 0.349% versus outside 0.322%.

### Roll adjustment: finding and rule

The symbols are `ES.v.0` and `YM.v.0`, a volume-rolled front-month continuous series. In 2020 to 2022 no
roll-window gap stands clear of the ordinary overnight-gap distribution. From March 2023 to March 2024,
however, every quarterly window in ES (and four of five in YM) contains one gap of about +1.0% to +1.4%,
always positive and three to five times the window's median gap. A same-sign jump of that size once per
quarter is what an UNADJUSTED roll looks like when the next contract trades at a carry premium, and it is
too regular to be chance. **Finding:** the series are most likely unadjusted. **Decision:** treat them as
UNADJUSTED. The data-derived roll dates where the jump is visible are the dates in the tables for 2023-03
onward; earlier rolls cannot be located from regular-hours bars because the jump is smaller than ordinary
gaps. Consequences:
1. All search uses `INTRADAY_FLAT`: every position is closed by the last bar of its session, so no trade
   can hold across a roll and no false roll profit or loss can enter any metric.
2. `OVERNIGHT_CARRY` is not offered to the search. It is used only for the reference reproduction of the
   owner's always-in-market baseline, whose results therefore include any roll jumps, exactly as a
   TradingView continuous chart would. This is stated wherever baseline numbers are reported.
3. Indicators that span sessions treat the overnight gap (including any roll jump) as one true-range
   observation.

## Alignment between the two files

- The two files share the 09:30 to 15:55 Eastern grid. Sessions present in one file only are dropped (above).
- Within common sessions, each instrument keeps its own bars. Cross-instrument features join on timestamp and
  are undefined (no signal) where the other instrument has no bar.

- Research bars present in ES only: 36; in YM only: 0.
  - ES only: 2020-02-27 (36 bars)

## Other notes

- Timestamps are bar-open times, parsed timezone-aware and converted to America/New_York. Offsets -05:00 and
  -04:00 only.
- The data is regular hours only: a position held overnight would see a gap the bars do not show. The search
  never holds overnight (see above).
- Timeframes below 5 minutes cannot be built from this data and are never claimed.
- Errata: before the specification had been read, the agent's first look at the raw files printed the final
  three bars of each file (2026-03-06, 15:45 to 15:55), which lie in the vault period. Six bars were seen
  once; they inform no design choice. Recorded here and in reports/ERRATA.md.

