"""Portfolio choices with the new markets. Training pool x portfolio composition, chosen on 2022-23
by return/max-drawdown, confirmed on 2024-26. S1 exit, guard (max 2 index positions + daily stop)."""
import os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from st.research import market
from st.meta import walk_forward_masks_cross
from st.portfolio import combine, equity_metrics
TZ = "America/New_York"
ALL = ["ES", "MES", "MNQ", "YM", "MYM", "RTY", "M2K"]
M = {s: market(s, {}) for s in ALL}
LABEL = dict(stop_atr=3.0, target_atr=0.0)
POOLS = {"pool: ES/MES/MNQ/YM": ["ES", "MES", "MNQ", "YM"], "pool: + MYM/RTY/M2K": ALL}
PORTS = {
    "6 MES + 5 MNQ + 1 YM (previous)": {"MES": 6, "MNQ": 5, "YM": 1},
    "6 MES + 5 MNQ + 10 MYM (all micro)": {"MES": 6, "MNQ": 5, "MYM": 10},
    "all micro + 16 M2K": {"MES": 6, "MNQ": 5, "MYM": 10, "M2K": 16},
}
S1 = dict(trade_through_ticks=1, cap_cash=0, use_target=0, stop_atr=3.0)
pf = lambda x: x[x > 0].sum() / max(1e-9, -x[x < 0].sum())
rows = []
for pname, pool in POOLS.items():
    masks = walk_forward_masks_cross({s: M[s] for s in pool}, {s: M[s] for s in ALL}, LABEL)
    for qname, qty in PORTS.items():
        tr = {}
        for s, q in qty.items():
            t = M[s].run(filt={"ml_mask": masks[s]}, **dict(S1, qty=q))
            tr[s] = t[t.entry_time >= pd.Timestamp("2022-01-01", tz=TZ)]
        P = combine(tr, max_per_group=2, daily_stop_usd=1500.0)
        P["exit_time"] = pd.to_datetime(P.exit_time)
        for per, (a, b) in (("2022-23", ("2022-01-01", "2024-01-01")), ("2024-26", ("2024-01-01", "2026-04-01")), ("ALL", ("2022-01-01", "2026-04-01"))):
            m = equity_metrics(P, a, b)
            Q = P[(P.entry_time >= pd.Timestamp(a, tz=TZ)) & (P.entry_time < pd.Timestamp(b, tz=TZ))]
            apr = (Q.exit_time.dt.year == 2025) & (Q.exit_time.dt.month == 4)
            rows.append(dict(pool=pname, port=qname, period=per, **m, pf_ex_apr25=pf(Q[~apr].pnl.values),
                             by_sym=" ".join(f"{s}:{pf(Q[Q.symbol==s].pnl.values):.2f}" for s in qty)))
            r = rows[-1]
            print(f"{pname:22s} | {qname:36s} | {per:7s} PF {r['pf']:.2f} net {r['net']:8.0f} DD {r['max_dd']:7.0f} ret/DD {r['ret_dd']:5.2f} "
                  f"worstDay {r['worst_day']:6.0f} +mo {r['pos_months']:3.0f}% exApr25 {r['pf_ex_apr25']:.2f} | {r['by_sym']}", flush=True)
D = pd.DataFrame(rows); D.to_csv("results/portfolio_v2.csv", index=False)
sel = D[D.period == "2022-23"].sort_values("ret_dd", ascending=False).iloc[0]
print("\nChosen on 2022-23 by ret/DD:", sel.pool, "|", sel.port)
