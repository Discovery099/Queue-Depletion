"""Baseline (original script) on the 6-year RTH data + reconciliation against TradingView exports."""
import glob, sys, time
import pandas as pd, numpy as np
from st.backtest import Market, metrics, fmt

SYMS = sys.argv[1].split(",") if len(sys.argv) > 1 else ["ES", "MES", "MNQ", "YM", "MGC"]
UP = "/root/.claude/uploads/a431acad-0d81-51ce-b416-bb0d3f2e89d7"
TV = {"ES": "ff678d6f", "MES": "2471935b", "MNQ": "785a72a7", "YM": "290d34f9", "MGC": "69e5562b"}

for s in SYMS:
    t0 = time.time()
    m = Market(s)
    t = m.run()
    print(f"{s:4s} ALL  {fmt(metrics(t))}  ({time.time()-t0:.1f}s)")
    for y in range(2020, 2027):
        print(f"     {y} {fmt(metrics(t, f'{y}-01-01', f'{y+1}-01-01'))}")
    print("     exits:", t.reason_name.value_counts().to_dict())
    # reconciliation vs TradingView (RTH entries only, overlap window)
    f = glob.glob(f"{UP}/{TV[s]}-*.csv")
    if f:
        d = pd.read_csv(f[0], encoding="utf-8-sig")
        e = d[d.Type.str.startswith("Entry")].copy()
        e["t"] = pd.to_datetime(e["Date and time"]).dt.tz_localize("America/New_York")
        lo, hi = m.b.ts_series.iloc[0], m.b.ts_series.iloc[-1]
        # TV export times: assume chart in exchange/NY time; keep RTH entries inside the data window
        mins = e.t.dt.hour * 60 + e.t.dt.minute
        first_min = m.b.minute.min(); last_min = m.b.minute.max()
        e = e[(e.t >= max(lo, pd.Timestamp("2025-11-20", tz="America/New_York"))) & (e.t <= hi)
              & (mins > first_min + 60) & (mins <= last_min)]
        mine = t[(t.entry_time >= e.t.min()) & (t.entry_time <= e.t.max())]
        mine_keys = set(zip(mine.entry_time, np.where(mine.dir == 1, "Entry long", "Entry short")))
        tv_keys = set(zip(e.t, e.Type))
        both = tv_keys & mine_keys
        print(f"     TV reconciliation (RTH, after the first hour): TV entries {len(tv_keys)}, mine {len(mine_keys)}, "
              f"identical time+side {len(both)} ({len(both)/max(1,len(tv_keys))*100:.0f}% of TV)")
