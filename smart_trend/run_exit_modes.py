"""The 'One-Year Exit Comparison' script's three exit models, tested on the 6-year RTH data,
alone and combined with the walk-forward meta filter (existing label, and relabelled per exit)."""
import os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from st.research import market
from st.meta import walk_forward_masks
from st.backtest import metrics
from st.portfolio import combine, equity_metrics

SY = ["ES", "MES", "MNQ", "YM", "MGC"]
IDX = ["ES", "MES", "MNQ", "YM"]
TZ = "America/New_York"
REAL = dict(trade_through_ticks=1)
MODES = {
    "Original (capped target)": dict(REAL),
    "Timed exit (1.25ATR tgt, 12 bars)": dict(REAL, cap_cash=0, target_atr=1.25, max_bars=12),
    "Trend runner (exit on regime flip)": dict(REAL, use_target=0, inval_mode=1),
    "Trend runner + 3ATR stop": dict(REAL, use_target=0, inval_mode=1, stop_atr=3.0),
    "Enhanced S1 exit (3ATR stop, hold to close)": dict(REAL, cap_cash=0, use_target=0, stop_atr=3.0),
}
LABELS = {  # barrier-simulator equivalents for relabelling the meta model
    "Timed exit (1.25ATR tgt, 12 bars)": dict(stop_atr=0.0, target_atr=1.25, max_bars=12),
    "Trend runner (exit on regime flip)": dict(stop_atr=0.0, target_atr=0.0, trail_exit=1),
    "Trend runner + 3ATR stop": dict(stop_atr=3.0, target_atr=0.0, trail_exit=1),
    "Enhanced S1 exit (3ATR stop, hold to close)": dict(stop_atr=3.0, target_atr=0.0),
}
M = {s: market(s, {}) for s in SY}
pf = lambda x: x[x > 0].sum() / max(1e-9, -x[x < 0].sum())

print("A) Exit models alone, per symbol, 1 contract, 2020-01..2026-03")
rows = []
for name, e in MODES.items():
    line = []
    for s in SY:
        t = M[s].run(**e)
        r = metrics(t); line.append(f"{s}:{r['pf']:.2f}")
        rows.append(dict(mode=name, symbol=s, **r))
    d = pd.DataFrame([x for x in rows if x["mode"] == name])
    print(f"  {name:45s} gPF {np.exp(np.log(d.pf.clip(0.05)).mean()):.2f}  net {d.net.sum():9.0f}  DDsum {d.max_dd.sum():9.0f}  worstDay {d.worst_day.min():7.0f}  | {' '.join(line)}")
pd.DataFrame(rows).to_csv("results/exit_modes_alone.csv", index=False)

print("\nB) With the meta filter, 2022-01..2026-03 (walk-forward), index futures, 1 contract")
base_masks, _ = walk_forward_masks({s: M[s] for s in IDX}, dict(stop_atr=3.0, target_atr=0.0))
rows = []
for name, e in MODES.items():
    if name.startswith("Original"):
        continue
    variants = [("S1 label", base_masks)]
    if name in LABELS and name != "Enhanced S1 exit (3ATR stop, hold to close)":
        variants.append(("own label", walk_forward_masks({s: M[s] for s in IDX}, LABELS[name])[0]))
    for vlab, masks in variants:
        res = {}
        for s in IDX:
            t = M[s].run(filt={"ml_mask": masks[s]}, **e)
            res[s] = t[t.entry_time >= pd.Timestamp("2022-01-01", tz=TZ)]
        for per, (a, b) in (("2022-23", ("2022-01-01", "2024-01-01")), ("2024-26", ("2024-01-01", "2026-04-01"))):
            ms = {s: metrics(t, a, b) for s, t in res.items()}
            g = np.exp(np.mean([np.log(max(0.05, m["pf"])) for m in ms.values()]))
            rows.append(dict(mode=name, label=vlab, period=per, gpf=g, net=sum(m["net"] for m in ms.values()),
                             dd=sum(m["max_dd"] for m in ms.values()), worst=min(m["worst_day"] for m in ms.values()),
                             **{f"pf_{s}": m["pf"] for s, m in ms.items()}))
            print(f"  {name:45s} [{vlab:9s}] {per}: gPF {g:.2f} net {rows[-1]['net']:9.0f} DDsum {rows[-1]['dd']:8.0f} worstDay {rows[-1]['worst']:7.0f} | "
                  + " ".join(f"{s}:{m['pf']:.2f}" for s, m in ms.items()), flush=True)
pd.DataFrame(rows).to_csv("results/exit_modes_meta.csv", index=False)
