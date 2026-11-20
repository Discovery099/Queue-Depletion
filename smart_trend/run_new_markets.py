"""Cross-market test: the walk-forward meta model trained ONLY on ES/MES/MNQ/YM is applied, unchanged,
to markets it never saw (RTY, M2K, MYM, MCL). Each year uses the model fitted on prior years only."""
import os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from st.research import market
from st.ml import signal_table, FEATS
from st.meta import fit_logit
from st.backtest import metrics

TZ = "America/New_York"
TRAIN = ["ES", "MES", "MNQ", "YM"]
NEW = ["RTY", "M2K", "MYM", "MCL"]
LABEL = dict(stop_atr=3.0, target_atr=0.0)
M = {s: market(s, {}) for s in TRAIN + NEW}
Ttr = pd.concat([signal_table(M[s], LABEL, k) for k, s in enumerate(TRAIN)], ignore_index=True)
Tnew = {s: signal_table(M[s], LABEL, 0) for s in NEW}

masks = {s: np.zeros(M[s].b.n, bool) for s in NEW}
for yr in range(2022, 2027):
    tr = Ttr[Ttr.year < yr]
    clf = fit_logit(tr)
    thr = np.quantile(clf.predict_proba(tr[FEATS].fillna(0))[:, 1], 0.6)
    for s in NEW:
        te = Tnew[s][Tnew[s].year == yr]
        if len(te):
            p = clf.predict_proba(te[FEATS].fillna(0))[:, 1]
            masks[s][te.idx.to_numpy()[p >= thr]] = True

REAL = dict(trade_through_ticks=1)
S1 = dict(REAL, cap_cash=0, use_target=0, stop_atr=3.0)
RUN = {"Original script": (None, REAL), "S1 exit, no filter": (None, S1), "S1 + meta (frozen index model)": ("ml", S1),
       "Trend runner, no filter": (None, dict(REAL, use_target=0, inval_mode=1))}
rows = []
for s in NEW:
    for name, (f, e) in RUN.items():
        t = M[s].run(filt={"ml_mask": masks[s]} if f else {}, **e)
        t = t[t.entry_time >= pd.Timestamp("2022-01-01", tz=TZ)]
        for per, (a, b) in (("2022-23", ("2022-01-01", "2024-01-01")), ("2024-26", ("2024-01-01", "2026-04-01")), ("2022-26", ("2022-01-01", "2026-04-01"))):
            r = metrics(t, a, b)
            rows.append(dict(symbol=s, cfg=name, period=per, **r))
D = pd.DataFrame(rows)
D.to_csv("results/new_markets.csv", index=False)
for s in NEW:
    print(f"\n{s}")
    for name in RUN:
        x = D[(D.symbol == s) & (D.cfg == name)].set_index("period")
        print(f"  {name:32s} PF 22-23 {x.loc['2022-23','pf']:.2f} | 24-26 {x.loc['2024-26','pf']:.2f} | all {x.loc['2022-26','pf']:.2f} "
              f"net {x.loc['2022-26','net']:9.0f} DD {x.loc['2022-26','max_dd']:8.0f} worstDay {x.loc['2022-26','worst_day']:7.0f} n {int(x.loc['2022-26','trades'])}")
# yearly PF of the meta strategy on the unseen markets
print("\nS1 + meta by year (unseen markets):")
for s in NEW:
    t = M[s].run(filt={"ml_mask": masks[s]}, **S1); t = t[t.entry_time >= pd.Timestamp("2022-01-01", tz=TZ)]
    print(f"  {s}:", t.groupby(t.exit_time.dt.year).pnl.apply(lambda x: round(x[x>0].sum()/max(1e-9,-x[x<0].sum()),2)).to_dict())
