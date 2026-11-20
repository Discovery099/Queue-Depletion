"""End-to-end evaluation of the enhanced strategy.

Protocol
  * Meta-label model: pooled logistic regression on the index futures, retrained every January on
    all earlier years only (expanding window). First out-of-sample year = 2022.
  * Stacked enhancements are chosen on 2022-2023 (SELECTION) and confirmed on 2024-2026-03 (CONFIRM).
  * Realistic fills: market/stop orders 1 tick slippage, limit targets must trade 1 tick through,
    $2.50 round-turn commission per contract.
Outputs go to results/.
"""
import json
import os
import pickle
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from st.research import market                         # noqa: E402
from st.meta import walk_forward_masks, fit_logit      # noqa: E402
from st.backtest import metrics                        # noqa: E402
from st.portfolio import combine, equity_metrics       # noqa: E402
from st.ml import FEATS, signal_table                  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(OUT, exist_ok=True)
IDX = [s for s in ["ES", "MES", "MNQ", "YM", "MYM", "M2K", "RTY", "NQ"]
       if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", f"{s}_5min_RTH.csv"))]
SEL = ("2022-01-01", "2024-01-01")
CONF = ("2024-01-01", "2026-04-01")
TZ = "America/New_York"
REAL = dict(trade_through_ticks=1)

M = {s: market(s, {}) for s in IDX}
LABEL_EXIT = dict(stop_atr=3.0, target_atr=0.0)
masks, T = walk_forward_masks(M, LABEL_EXIT, C=0.05, q=0.6)
T.to_csv(os.path.join(OUT, "meta_signals_oos.csv"), index=False)

CORE = dict(REAL, cap_cash=0, use_target=0, stop_atr=3.0)
STACKS = {
    "S0 original script": (dict(), dict(REAL), False),
    "S1 ML + 3ATR stop + hold to close": (dict(), CORE, True),
    "S2 S1 + skip first 30min + max 2 losers/day": (dict(skip_open_bars=6), dict(CORE, max_losses_day=2), True),
    "S3 S2 + scale-out 50% at +1ATR only if ER>=0.3": (dict(skip_open_bars=6),
                                          dict(CORE, max_losses_day=2, partial_frac=0.5, partial_r=1 / 3, adaptive_er=0.3), True),
    "S4 S2 + scale-out 50% at +1ATR, BE + 3ATR chandelier": (dict(skip_open_bars=6),
                                                 dict(CORE, max_losses_day=2, partial_frac=0.5, partial_r=1 / 3, runner_mode=2, runner_atr=3.0), True),
    "S5 S2 + time stop 18 bars": (dict(skip_open_bars=6), dict(CORE, max_losses_day=2, ts_bars=18, ts_min_mfe_atr=0.5), True),
}


def run_stack(filt, eng, ml, risk_usd=0.0):
    out = {}
    for s in IDX:
        f = dict(filt)
        if ml:
            f["ml_mask"] = masks[s]
        e = dict(eng)
        if risk_usd and e.get("stop_atr", 0) > 0:
            e.update(risk_usd=risk_usd)
        t = M[s].run(filt=f, **e)
        out[s] = t[t.entry_time >= pd.Timestamp(SEL[0], tz=TZ)]
    return out


rows = []
all_trades = {}
for name, (filt, eng, ml) in STACKS.items():
    tr = run_stack(filt, eng, ml)
    all_trades[name] = tr
    for s, t in tr.items():
        for per, (a, b) in (("SELECT 2022-23", SEL), ("CONFIRM 2024-26", CONF)):
            r = metrics(t, a, b)
            r.update(stack=name, symbol=s, period=per)
            rows.append(r)
R = pd.DataFrame(rows)
R.to_csv(os.path.join(OUT, "stack_metrics.csv"), index=False)


def gpf(d):
    return float(np.exp(np.mean(np.log(d.pf.clip(0.05, 5)))))


print("\nPer-symbol, 1 contract each (geo-mean PF across symbols)")
summary = []
for name in STACKS:
    line = {"stack": name}
    for per in ("SELECT 2022-23", "CONFIRM 2024-26"):
        d = R[(R["stack"] == name) & (R.period == per)]
        line[f"{per} gPF"] = round(gpf(d), 2)
        line[f"{per} net"] = round(d.net.sum())
        line[f"{per} DDsum"] = round(d.max_dd.sum())
        line[f"{per} worstDay"] = round(d.worst_day.min())
        line[f"{per} PF by sym"] = " ".join(f"{r.symbol}:{r.pf:.2f}" for r in d.itertuples())
    summary.append(line)
S = pd.DataFrame(summary)
print(S.to_string(index=False))
S.to_csv(os.path.join(OUT, "stack_summary.csv"), index=False)

# ------------------------------------------------------------------ portfolio
# Fixed, notional-matched contracts (~$200k notional per market). Risk-parity sizing was tested and
# rejected: the meta edge sits in the higher-ATR trades, which risk-parity sizing down-weights
# (MES/MNQ fell to PF ~1.0 with it).
PORT_QTY = {s: q for s, q in {"MES": 6, "MNQ": 5, "YM": 1, "MYM": 10, "M2K": 8}.items() if s in IDX}
GUARD = dict(max_per_group=2, daily_stop_usd=1500.0)


def run_port(filt, eng, ml):
    tr = {}
    for s, q in PORT_QTY.items():
        f = dict(filt)
        if ml:
            f["ml_mask"] = masks[s]
        t = M[s].run(filt=f, **dict(eng, qty=q))
        tr[s] = t[t.entry_time >= pd.Timestamp(SEL[0], tz=TZ)]
    return tr


port_rows = []
port_trades = {}
for name, (filt, eng, ml) in STACKS.items():
    tr = run_port(filt, eng, ml)
    for glabel, gkw in (("no guard", {}), ("guard", GUARD)):
        P = combine(tr, **gkw)
        port_trades[(name, glabel)] = P
        for per, (a, b) in (("SELECT 2022-23", SEL), ("CONFIRM 2024-26", CONF), ("ALL 2022-26", (SEL[0], CONF[1]))):
            r = equity_metrics(P, a, b)
            r.update(stack=name, guard=glabel, period=per)
            for s in PORT_QTY:
                q = P[(P.symbol == s) & (P.entry_time >= pd.Timestamp(a, tz=TZ)) & (P.entry_time < pd.Timestamp(b, tz=TZ))].pnl
                r[f"pf_{s}"] = float(q[q > 0].sum() / max(1e-9, -q[q < 0].sum()))
            port_rows.append(r)
PR = pd.DataFrame(port_rows)
PR.to_csv(os.path.join(OUT, "portfolio_metrics.csv"), index=False)
print(f"\nPortfolio {PORT_QTY} (fixed contracts):")
print(PR[["stack", "guard", "period", "trades", "net", "pf", "max_dd", "ret_dd", "worst_day", "pos_months", "sharpe"]
         + [f"pf_{s}" for s in PORT_QTY]].round(2).to_string(index=False))

# choose the final configuration on the SELECTION window only: best return / max drawdown
cand = PR[(PR["stack"] != "S0 original script") & (PR.period == "SELECT 2022-23")]
best = cand.sort_values("ret_dd", ascending=False).iloc[0]
final_name, final_guard = best["stack"], best["guard"]
print(f"\nChosen on 2022-23 only (best ret/DD): {final_name} [{final_guard}]")
final_port = port_trades[(final_name, final_guard)]
port_trades[("S0 original script", "no guard")].to_csv(os.path.join(OUT, "original_portfolio_trades.csv"), index=False)
final_port.to_csv(os.path.join(OUT, "final_portfolio_trades.csv"), index=False)
yr = final_port.groupby(final_port.exit_time.dt.year).pnl.agg(
    trades="count", net="sum", pf=lambda x: x[x > 0].sum() / max(1e-9, -x[x < 0].sum()))
print("\nFinal portfolio by year:\n", yr.round(2).to_string())
mon = final_port.groupby([final_port.exit_time.dt.year.rename("year"), final_port.exit_time.dt.month.rename("month")]).pnl.sum().unstack().round(0)
mon.to_csv(os.path.join(OUT, "final_portfolio_monthly.csv"))
print("\nMonthly P&L:\n", mon.to_string())

# ------------------------------------------------------------------ export the model for Pine
Tall = pd.concat([signal_table(M[s], LABEL_EXIT, k) for k, s in enumerate(IDX)], ignore_index=True)
clf = fit_logit(Tall, C=0.05)
sc, lr = clf[0], clf[-1]
p_train = clf.predict_proba(Tall[FEATS].fillna(0))[:, 1]
model = dict(features=FEATS, mean=sc.mean_.tolist(), std=sc.scale_.tolist(), coef=lr.coef_[0].tolist(),
             intercept=float(lr.intercept_[0]), threshold=float(np.quantile(p_train, 0.6)),
             trained_on=f"{Tall.year.min()}-{Tall.year.max()} {IDX}", n=len(Tall), final_stack=final_name)
json.dump(model, open(os.path.join(OUT, "meta_model.json"), "w"), indent=1)
pickle.dump(dict(R=R, S=S, PR=PR), open(os.path.join(OUT, "final.pkl"), "wb"))
print("\nmodel exported:", model["trained_on"], "threshold", round(model["threshold"], 4))
