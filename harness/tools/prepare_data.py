"""One-time Generation 0 data preparation (SPEC 4.1, 5.1, B.1 steps 3-4).

Validates the raw CSVs, writes data/DATA_QUALITY.md, computes and locks the
partition, and physically separates research rows from vault rows.

This is the only research-side program that touches the raw files, which contain
vault rows.  It never prints, summarises or inspects vault PRICES: for rows after
the research block it handles only timestamps and row counts, then writes them
to data/vault/ and hashes them.  All price statistics below are restricted to the
Research block.
"""
import hashlib
import json
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = {"ES": "data/raw/ES_5min_RTH_6year.csv", "YM": "data/raw/YM_5min_RTH_6year.csv"}
SPECS = {"ES": {"tick": 0.25, "tick_value": 12.5, "point_value": 50.0},
         "YM": {"tick": 1.0, "tick_value": 5.0, "point_value": 5.0}}
RESEARCH_SHARE, EMBARGO, INNER_HOLDOUT_SHARE = 0.70, 5, 0.15


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha_rows(df):
    """Canonical hash of a block's rows, independent of the parquet encoding."""
    h = hashlib.sha256()
    cols = ["ts_event", "open", "high", "low", "close", "volume"]
    h.update(df[cols].to_csv(index=False, lineterminator="\n").encode())
    return h.hexdigest()


def load(sym):
    df = pd.read_csv(os.path.join(ROOT, RAW[sym]))
    ts = pd.to_datetime(df.ts_event, utc=True).dt.tz_convert("America/New_York")
    df["ts"] = ts
    df["date"] = (ts.dt.year * 10000 + ts.dt.month * 100 + ts.dt.day).astype(np.int32)
    df["mod"] = (ts.dt.hour * 60 + ts.dt.minute).astype(np.int32)  # minute of day, bar open
    return df


def to_store(df, sess_index):
    out = pd.DataFrame({
        "ts_utc_ns": df.ts.dt.tz_convert("UTC").dt.tz_localize(None).astype("datetime64[ns]").astype(np.int64),
        "date": df.date.values,
        "sess": df.date.map(sess_index).astype(np.int32).values,
        "slot": ((df["mod"] - 570) // 5).astype(np.int16).values,  # 0 = 09:30 bar
        "open": df.open.values, "high": df.high.values, "low": df.low.values,
        "close": df.close.values, "volume": df.volume.astype(np.float64).values,
        "filler": (df.symbol.isna() | (df.volume == 0)).astype(np.int8).values,
    })
    return out


def main():
    lock_path = os.path.join(ROOT, "config/partition.lock.json")
    if os.path.exists(lock_path):
        sys.exit("partition.lock.json already exists: the split is frozen (Article 3). Refusing to recompute.")
    d = {s: load(s) for s in RAW}
    q = []  # DATA_QUALITY lines
    q.append("# Data quality report (Generation 0)\n")
    q.append("Price statistics in this file use the Research block only. For the vault "
             "period only timestamps and row counts were examined.\n")
    q.append("## Raw files\n")
    q.append("| File | sha256 | rows | sessions | first | last |\n|---|---|---|---|---|---|")
    for s, df in d.items():
        q.append(f"| {RAW[s]} | `{sha_file(os.path.join(ROOT, RAW[s]))}` | {len(df)} | {df.date.nunique()} | {df.date.min()} | {df.date.max()} |")

    # ---- structural validation on all rows (timestamps only) ----
    problems = []
    for s, df in d.items():
        if list(df.columns[:7]) != ["ts_event", "symbol", "open", "high", "low", "close", "volume"]:
            problems.append(f"{s}: unexpected columns")
        if df.ts.duplicated().any():
            problems.append(f"{s}: duplicate timestamps")
        if not df.ts.is_monotonic_increasing:
            problems.append(f"{s}: timestamps not increasing")
        if ((df["mod"] < 570) | (df["mod"] > 955) | (df["mod"] % 5 != 0)).any():
            problems.append(f"{s}: bars outside 09:30-15:55 or off the 5-minute grid")
        first = df.groupby("date")["mod"].min()
        if (first != 570).any():
            problems.append(f"{s}: {int((first != 570).sum())} sessions do not start at 09:30")
        offs = set(df.ts_event.str[-6:])
        if not offs <= {"-05:00", "-04:00"}:
            problems.append(f"{s}: unexpected UTC offsets {offs}")
        syms = set(df.symbol.dropna())
        if syms != {f"{s}.v.0"}:
            problems.append(f"{s}: unexpected symbols {syms}")
    if problems:
        sys.exit("DATA VALIDATION FAILED:\n" + "\n".join(problems))

    # ---- common calendar and partition (5.1) ----
    common = sorted(set(d["ES"].date) & set(d["YM"].date))
    n = len(common)
    n_res = int(n * RESEARCH_SHARE)
    research_dates = common[:n_res]
    embargo_dates = common[n_res:n_res + EMBARGO]
    vault_dates = common[n_res + EMBARGO:]
    n_va = (2 * len(vault_dates)) // 3
    vault_a, vault_b = vault_dates[:n_va], vault_dates[n_va:]
    n_search = int(n_res * (1 - INNER_HOLDOUT_SHARE))
    sess_index = {dt: i for i, dt in enumerate(common)}
    only = {s: sorted(set(d[s].date) - set(common)) for s in d}

    lock = {
        "created_note": "Computed once in Generation 0. Never changed (Constitution Article 3).",
        "rule": "first 70% of common sessions (rounded down) = Research; next 5 sessions = embargo; rest = Vault; "
                "Vault-A = first two-thirds of vault sessions, Vault-B = final third; "
                "inner holdout = final 15% of Research sessions",
        "common_sessions": n,
        "research": {"sessions": n_res, "first": research_dates[0], "last": research_dates[-1],
                     "search_sessions": n_search, "search_last": research_dates[n_search - 1],
                     "inner_holdout_sessions": n_res - n_search, "inner_holdout_first": research_dates[n_search]},
        "embargo": {"sessions": EMBARGO, "first": embargo_dates[0], "last": embargo_dates[-1]},
        "vault": {"sessions": len(vault_dates), "first": vault_dates[0], "last": vault_dates[-1],
                  "vault_a": {"sessions": len(vault_a), "first": vault_a[0], "last": vault_a[-1]},
                  "vault_b": {"sessions": len(vault_b), "first": vault_b[0], "last": vault_b[-1]}},
        "sessions_not_common_dropped": only,
        "instruments": SPECS,
        "raw_sha256": {s: sha_file(os.path.join(ROOT, RAW[s])) for s in RAW},
        "blocks": {},
    }
    os.makedirs(os.path.join(ROOT, "data/research"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "data/vault"), exist_ok=True)
    rs, vs = set(research_dates), set(vault_dates)
    research = {}
    for s, df in d.items():
        r = df[df.date.isin(rs)]
        v = df[df.date.isin(vs)]
        research[s] = r
        to_store(r, sess_index).to_parquet(os.path.join(ROOT, f"data/research/{s}.parquet"), compression="zstd", index=False)
        to_store(v, sess_index).to_parquet(os.path.join(ROOT, f"data/vault/{s}.parquet"), compression="zstd", index=False)
        lock["blocks"][s] = {"research_rows": int(len(r)), "research_sha256": sha_rows(r),
                             "vault_rows": int(len(v)), "vault_sha256": sha_rows(v),
                             "embargo_rows": int(df.date.isin(set(embargo_dates)).sum())}
    del d  # raw frames (which include vault rows) are not used below
    lock_body = json.dumps(lock, indent=1, sort_keys=True)
    lock["self_sha256"] = hashlib.sha256(lock_body.encode()).hexdigest()
    with open(lock_path, "w") as f:
        json.dump(lock, f, indent=1, sort_keys=True)
    os.chmod(lock_path, 0o444)

    # ---- quality findings on the Research block ----
    q.append("\n## Partition\n")
    q.append(f"- Common sessions: {n}. Research: {n_res} ({research_dates[0]} to {research_dates[-1]}). "
             f"Embargo: {EMBARGO} ({embargo_dates[0]} to {embargo_dates[-1]}). Vault: {len(vault_dates)} "
             f"(Vault-A {len(vault_a)}, Vault-B {len(vault_b)}).")
    q.append(f"- Inside Research: {n_search} search sessions (walk-forward folds) and "
             f"{n_res - n_search} inner-holdout sessions starting {research_dates[n_search]}.")
    q.append(f"- Sessions present in only one file, dropped from every block: {only}.")
    q.append("\n## Findings and decisions (Research block)\n")
    for s, r in research.items():
        tick = SPECS[s]["tick"]
        q.append(f"### {s}\n")
        px = r[["open", "high", "low", "close"]]
        bad = int(((r.high < px.max(axis=1)) | (r.low > px.min(axis=1))).sum())
        offtick = int(((px / tick) % 1 != 0).sum().sum())
        q.append(f"- Rows: {len(r)}. OHLC inconsistencies: {bad}. Prices off the tick grid: {offtick}.")
        ms = r[r.symbol.isna()]
        zv = r[r.volume == 0]
        q.append(f"- Rows with a missing symbol: {len(ms)}; zero-volume rows: {len(zv)}; identical sets: "
                 f"{set(ms.index) == set(zv.index)}. Dates: {sorted(set(ms.date))}. Every one has open = high = low = close "
                 f"({bool((ms.high == ms.low).all())}), i.e. it is a filler bar carried forward while the market did not trade. "
                 "**Decision:** keep the rows so the 5-minute grid stays intact, flag them `filler=1`; the engine "
                 "never fills on a zero-volume bar (SPEC 7.3) and volume features guard against division by zero.")
        bps = r.groupby("date").size()
        short = bps[bps < 78]
        q.append(f"- Session lengths (bars: count): {bps.value_counts().sort_index().to_dict()}. Short sessions: {len(short)}. "
                 "Most are 42- or 45-bar holiday sessions. The session calendar is built from the data; "
                 "nothing assumes 78 bars, and strategies may not use session length (SPEC 9.5).")
        q.append(f"- Short sessions: {', '.join(f'{k}({v})' for k, v in short.items())}.")
        g = r.groupby("date").agg(o=("open", "first"), c=("close", "last"))
        gap = (g.o - g.c.shift(1)) / g.c.shift(1) * 100
        dt = pd.to_datetime(g.index.astype(str))
        q.append(f"- Overnight gap, absolute percent: median {gap.abs().median():.3f}, 95th pct {gap.abs().quantile(.95):.3f}, "
                 f"99th pct {gap.abs().quantile(.99):.3f}.")
        # roll test: quarterly months, days 6-20
        rw = (dt.month % 3 == 0) & (dt.day >= 6) & (dt.day <= 20)
        rows = []
        for y in sorted(set(dt.year)):
            for m in (3, 6, 9, 12):
                w = (dt.year == y) & (dt.month == m) & (dt.day >= 6) & (dt.day <= 20)
                if w.sum():
                    gw = gap[w]
                    i = gw.abs().idxmax()
                    rows.append((y, m, int(i), float(gw[i]), float(gw.abs().median())))
        q.append("- Roll-adjustment test. Largest overnight gap inside each quarterly roll window "
                 "(days 6 to 20 of March, June, September, December):\n")
        q.append("  | year | month | date | gap % | median abs gap % in window |\n  |---|---|---|---|---|")
        for y, m, i, gv, med in rows:
            q.append(f"  | {y} | {m} | {i} | {gv:+.2f} | {med:.2f} |")
        inw, outw = gap[rw].dropna(), gap[~rw].dropna()
        q.append(f"\n  Mean signed gap inside roll windows {inw.mean():+.3f}% (n={len(inw)}) versus outside "
                 f"{outw.mean():+.3f}% (n={len(outw)}); median absolute gap inside {inw.abs().median():.3f}% versus "
                 f"outside {outw.abs().median():.3f}%.")
    q.append("""
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
""")
    j = pd.merge(research["ES"][["ts"]].assign(es=1), research["YM"][["ts"]].assign(ym=1), on="ts", how="outer")
    eo, yo = j[j.ym.isna()], j[j.es.isna()]
    q.append(f"- Research bars present in ES only: {len(eo)}; in YM only: {len(yo)}.")
    for name, x in (("ES only", eo), ("YM only", yo)):
        if len(x):
            byd = x.ts.dt.strftime("%Y-%m-%d").value_counts().sort_index()
            q.append(f"  - {name}: " + ", ".join(f"{k} ({v} bars)" for k, v in byd.items()))
    q.append("""
## Other notes

- Timestamps are bar-open times, parsed timezone-aware and converted to America/New_York. Offsets -05:00 and
  -04:00 only.
- The data is regular hours only: a position held overnight would see a gap the bars do not show. The search
  never holds overnight (see above).
- Timeframes below 5 minutes cannot be built from this data and are never claimed.
- Errata: before the specification had been read, the agent's first look at the raw files printed the final
  three bars of each file (2026-03-06, 15:45 to 15:55), which lie in the vault period. Six bars were seen
  once; they inform no design choice. Recorded here and in reports/ERRATA.md.
""")
    with open(os.path.join(ROOT, "data/DATA_QUALITY.md"), "w") as f:
        f.write("\n".join(q) + "\n")
    os.chmod(os.path.join(ROOT, "data/vault"), 0o000)  # sealed; only vault/keeper.py reopens it
    print("research block written; vault sealed; partition locked:", lock["self_sha256"][:16])
    print("research", n_res, "search", n_search, "inner holdout", n_res - n_search, "embargo", EMBARGO,
          "vault", len(vault_dates), "(A", len(vault_a), "B", str(len(vault_b)) + ")")


if __name__ == "__main__":
    main()
