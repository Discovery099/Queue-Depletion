"""Long-bias diagnosis and fixes (forward TradingView test Aug-Nov 2026 showed ~90% longs in a falling market)."""
import os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from st.research import market
from st.ml import signal_table, FEATS
from st.portfolio import combine, equity_metrics

TZ = "America/New_York"; IDX = ["ES", "MES", "MNQ", "YM"]; QTY = {"MES": 6, "MNQ": 5, "YM": 1}
M = {s: market(s, {}) for s in IDX}


def daily_trend(m, n):
    """causal: current price vs SMA of the previous n RTH daily closes, in ATR, and 5-day return"""
    b = m.b
    dc = pd.Series(b.c).groupby(b.day_id).last()
    sma = dc.rolling(n).mean().shift(1).reindex(b.day_id).to_numpy()
    c5 = dc.shift(1).reindex(b.day_id).to_numpy(); c5b = dc.shift(6).reindex(b.day_id).to_numpy()
    return (b.c - sma) / m.s["atr"], (c5 - c5b) / m.s["atr"]


tabs = []
for k, s in enumerate(IDX):
    T = signal_table(M[s], dict(stop_atr=3.0, target_atr=0.0), k)
    for n in (20, 50):
        d, _ = daily_trend(M[s], n); T[f"dtrend{n}"] = d[T.idx] * T.dir
    _, r5 = daily_trend(M[s], 20); T["ret5d"] = r5[T.idx] * T.dir
    tabs.append(T)
T = pd.concat(tabs, ignore_index=True)
y = (T.net_usd > 0).astype(int)


def wf(feats, per_dir=False, q=0.6):
    p = np.full(len(T), np.nan); thr = np.full(len(T), np.nan)
    for yr in range(2022, 2027):
        tr = (T.year < yr).to_numpy(); te = (T.year == yr).to_numpy()
        clf = make_pipeline(StandardScaler(), LogisticRegression(C=0.05, max_iter=3000)).fit(T.loc[tr, feats].fillna(0), y[tr])
        p[te] = clf.predict_proba(T.loc[te, feats].fillna(0))[:, 1]
        ptr = clf.predict_proba(T.loc[tr, feats].fillna(0))[:, 1]
        if per_dir:
            for d in (1, -1):
                mt = te & (T.dir == d).to_numpy()
                thr[mt] = np.quantile(ptr[(T.dir[tr] == d).to_numpy()], q)
        else:
            thr[te] = np.quantile(ptr, q)
    return p >= thr


VARIANTS = {
    "A current model": wf(FEATS),
    "B long-only (current model)": wf(FEATS) & (T.dir == 1).to_numpy(),
    "C current + daily-trend gate (50d)": wf(FEATS) & (T.dtrend50 > 0).to_numpy(),
    "D current + daily-trend gate (20d)": wf(FEATS) & (T.dtrend20 > 0).to_numpy(),
    "E per-direction thresholds": wf(FEATS, per_dir=True),
    "F model + daily-trend features": wf(FEATS + ["dtrend20", "dtrend50", "ret5d"]),
    "G F + per-direction thresholds": wf(FEATS + ["dtrend20", "dtrend50", "ret5d"], per_dir=True),
    "H F + daily-trend gate (50d)": wf(FEATS + ["dtrend20", "dtrend50", "ret5d"]) & (T.dtrend50 > 0).to_numpy(),
}
S1 = dict(trade_through_ticks=1, cap_cash=0, use_target=0, stop_atr=3.0)
pf = lambda x: x[x > 0].sum() / max(1e-9, -x[x < 0].sum())
rows = []
for name, sel in VARIANTS.items():
    tr = {}
    for s, q in QTY.items():
        mk = np.zeros(M[s].b.n, bool); r = T[(T.sym == s) & sel]; mk[r.idx.to_numpy()] = True
        t = M[s].run(filt={"ml_mask": mk}, **dict(S1, qty=q)); tr[s] = t[t.entry_time >= pd.Timestamp("2022-01-01", tz=TZ)]
    P = combine(tr, max_per_group=2, daily_stop_usd=1500.0); P["exit_time"] = pd.to_datetime(P.exit_time)
    yr = P.groupby(P.exit_time.dt.year).pnl.apply(lambda x: round(pf(x.values), 2)).to_dict()
    lp = P.groupby("dir").pnl.apply(lambda x: round(pf(x.values), 2)).to_dict()
    out = {}
    for per, (a, b) in (("22-23", ("2022-01-01", "2024-01-01")), ("24-26", ("2024-01-01", "2026-04-01")), ("all", ("2022-01-01", "2026-04-01"))):
        out[per] = equity_metrics(P, a, b)
    rows.append(dict(variant=name, pf_2223=out["22-23"]["pf"], pf_2426=out["24-26"]["pf"], pf_all=out["all"]["pf"], net=out["all"]["net"],
                     dd=out["all"]["max_dd"], ret_dd_2223=out["22-23"]["ret_dd"], long_share=(P.dir == 1).mean(), pf_long=lp.get(1), pf_short=lp.get(-1), **{f"y{k}": v for k, v in yr.items()}))
    r = rows[-1]
    print(f"{name:38s} PF 22-23 {r['pf_2223']:.2f} | 24-26 {r['pf_2426']:.2f} | all {r['pf_all']:.2f} net {r['net']:8.0f} DD {r['dd']:7.0f} | long% {r['long_share']*100:3.0f} "
          f"PF L/S {r['pf_long']}/{r['pf_short']} | by year {yr}", flush=True)
pd.DataFrame(rows).to_csv("results/bias_fixes.csv", index=False)
T.to_pickle("/tmp/claude-0/-home-user-Queue-Depletion/a431acad-0d81-51ce-b416-bb0d3f2e89d7/scratchpad/T_bias.pkl")
