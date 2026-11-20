"""Portfolio test: S1 exit vs Trend-runner exit vs hybrid (runner exit armed after +k ATR).
Selection on 2022-23 by return/max-drawdown, confirmation 2024-26. 6 MES + 5 MNQ + 1 YM, guard on."""
import os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from st.research import market
from st.meta import walk_forward_masks
from st.portfolio import combine, equity_metrics
TZ = "America/New_York"
IDX = ["ES", "MES", "MNQ", "YM"]; QTY = {"MES": 6, "MNQ": 5, "YM": 1}
M = {s: market(s, {}) for s in IDX}
masks, _ = walk_forward_masks(M, dict(stop_atr=3.0, target_atr=0.0))
R = dict(trade_through_ticks=1, cap_cash=0, use_target=0, stop_atr=3.0)
CFG = {"S1 hold to close": R, "Runner (flip exit)": dict(R, inval_mode=1)}
for k in (0.5, 1.0, 1.5, 2.0, 3.0):
    CFG[f"Hybrid: flip exit after +{k} ATR"] = dict(R, inval_mode=1, inval_min_mfe_atr=k)
pf = lambda x: x[x > 0].sum() / max(1e-9, -x[x < 0].sum())
rows = []
for name, e in CFG.items():
    tr = {}
    for s, q in QTY.items():
        t = M[s].run(filt={"ml_mask": masks[s]}, **dict(e, qty=q))
        tr[s] = t[t.entry_time >= pd.Timestamp("2022-01-01", tz=TZ)]
    P = combine(tr, max_per_group=2, daily_stop_usd=1500.0)
    P["exit_time"] = pd.to_datetime(P.exit_time)
    for per, (a, b) in (("2022-23", ("2022-01-01", "2024-01-01")), ("2024-26", ("2024-01-01", "2026-04-01")), ("ALL", ("2022-01-01", "2026-04-01"))):
        m = equity_metrics(P, a, b)
        Q = P[(P.entry_time >= pd.Timestamp(a, tz=TZ)) & (P.entry_time < pd.Timestamp(b, tz=TZ))]
        apr = (Q.exit_time.dt.year == 2025) & (Q.exit_time.dt.month == 4)
        day = Q.groupby(Q.exit_time.dt.date).pnl.sum(); top = Q.exit_time.dt.date.isin(day.nlargest(10).index)
        rows.append(dict(cfg=name, period=per, **m, pf_ex_apr25=pf(Q[~apr].pnl.values), pf_ex_top10=pf(Q[~top].pnl.values),
                         **{f"pf_{s}": pf(Q[Q.symbol == s].pnl.values) for s in QTY}))
D = pd.DataFrame(rows)
D.to_csv("results/hybrid_portfolio.csv", index=False)
for r in D.itertuples():
    print(f"{r.cfg:34s} {r.period:7s} PF {r.pf:.2f} net {r.net:8.0f} DD {r.max_dd:7.0f} ret/DD {r.ret_dd:5.2f} worstDay {r.worst_day:6.0f} +mo {r.pos_months:3.0f}% "
          f"| exApr25 {r.pf_ex_apr25:.2f} exTop10 {r.pf_ex_top10:.2f} | MES {r.pf_MES:.2f} MNQ {r.pf_MNQ:.2f} YM {r.pf_YM:.2f}")
sel = D[D.period == "2022-23"].sort_values("ret_dd", ascending=False).iloc[0]
print("\nChosen on 2022-23 by ret/DD:", sel.cfg)
