"""Phase 2: walk-forward gradient-boosted combiner of every library technique."""
import json
import sys
import time

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.ensemble import HistGradientBoostingRegressor

from .core import SYMS, N_SEARCH, bars, F, S, COSTS, session_frame, noise_sigma, rt, summ, line
from qr.common import fold_of_session, RT_USD, FOLDS
from library.atoms import catalog as CAT
from genome.dsl import Ctx
from orchestrator.evaluate import other_arrays


def features(sym):
    b = bars(sym, 5)
    ob = bars("YM" if sym == "ES" else "ES", 5)
    ctx = Ctx(b, other=other_arrays(b, ob))
    cols = {}
    for a in CAT.ATOMS.values():
        if a.typ not in ("TRIGGER", "STATE", "FILTER", "LOCATION"):
            continue
        try:
            ex = a.build()
            L = np.asarray(ctx.ev(ex["long"]), bool)
            Sx = np.asarray(ctx.ev(ex["short"]), bool)
        except Exception:
            continue
        cols[a.id] = L.astype(np.int8) - Sx.astype(np.int8)
    so, pc, vwap, atr, sid = session_frame(b)
    sig = noise_sigma(b, so, sid, 14)
    c = b.c
    num = {"n_tod": b.mclose / 390.0, "n_noise_z": (c / so - 1.0) / sig, "n_vwap": (c - vwap) / atr, "n_gap": (so - pc) / pc * 100.0,
           "n_rsi": F.rsi(c, 14), "n_volr": b.v / F.sma(b.v, 20), "n_atr_ratio": atr / F.atr(b.h, b.l, c, 100),
           "n_range_pos": (c - F.sess_cummin(b.l, b.first)) / np.maximum(F.sess_cummax(b.h, b.first) - F.sess_cummin(b.l, b.first), b.tick),
           "n_sess_ret": (c - so) / atr, "n_body": (c - b.o) / atr, "n_rng": (b.h - b.l) / atr, "n_dow": pd.to_datetime(b.date.astype(str)).dayofweek.values,
           "n_is_es": np.full(b.n, 1.0 if sym == "ES" else 0.0)}
    for k in (1, 3, 6, 12, 24, 48, 78):
        num[f"n_ret{k}"] = (c - F.shift(c, k)) / atr
    X = pd.DataFrame({**cols, **num}).astype(np.float32)
    idx = np.arange(b.n)
    y = {}
    ent = b.o[np.minimum(idx + 1, b.n - 1)]
    for H in (6, 0):
        j = idx + 1 + H
        px = np.where((H > 0) & (j <= b.sess_end), b.o[np.minimum(j, b.n - 1)], b.c[b.sess_end])
        y[H] = np.clip((px - ent) / atr, -6, 6)
    ok = ~b.last & ~np.isnan(atr) & ~np.isnan(sig) & (b.sess >= 20)
    return b, X, y, ok, atr


t0 = time.time()
data = {s: features(s) for s in SYMS}
ncol = data["ES"][1].shape[1]
print(f"features: {ncol} columns, {time.time() - t0:.0f}s", flush=True)
res = {}
for H in (6, 0):
    hname = "30 minutes" if H else "to the close"
    pred = {s: np.full(data[s][0].n, np.nan) for s in SYMS}
    imp = np.zeros(ncol)
    for k in range(2, 8):
        lo = FOLDS[k][0]
        Xtr, ytr = [], []
        for s in SYMS:
            b, X, y, ok, atr = data[s]
            m = ok & (b.sess < lo - 2)
            Xtr.append(X[m]); ytr.append(y[H][m])
        mdl = HistGradientBoostingRegressor(max_iter=300, max_depth=4, learning_rate=0.03, min_samples_leaf=200,
                                            l2_regularization=1.0, random_state=7)
        mdl.fit(pd.concat(Xtr), np.concatenate(ytr))
        for s in SYMS:
            b, X, y, ok, atr = data[s]
            m = ok & (b.sess >= lo) & (b.sess < FOLDS[k][1])
            pred[s][m] = mdl.predict(X[m])
        print(f"  H={hname}: fold {k + 1} trained on {len(np.concatenate(ytr)):,} bars, {time.time() - t0:.0f}s", flush=True)
    # diagnostics on out-of-sample predictions
    P, Y, Cc = [], [], []
    for s in SYMS:
        b, X, y, ok, atr = data[s]
        m = ~np.isnan(pred[s])
        P.append(pred[s][m]); Y.append(y[H][m]); Cc.append((RT_USD[s] / b.pv / atr)[m])
    P, Y, Cc = np.concatenate(P), np.concatenate(Y), np.concatenate(Cc)
    ic = spearmanr(P, Y)[0]
    print(f"\n=== horizon {hname}: out-of-sample rank correlation of prediction with outcome: {ic:+.4f} on {len(P):,} bars")
    sweep = []
    ap = np.abs(P)
    for q in (0.5, 0.8, 0.9, 0.95, 0.99, 0.995):
        m = ap >= np.quantile(ap, q)
        g = (np.sign(P[m]) * Y[m]).mean()
        sweep.append(dict(top_pct=100 * (1 - q), gross=float(g), net=float(g - Cc[m].mean()), hit=float((np.sign(P[m]) * Y[m] > 0).mean() * 100)))
        print(f"   strongest {100 * (1 - q):5.1f}% of predictions: move in predicted direction {g:+.3f} ATR, after costs {g - Cc[m].mean():+.3f}, right {sweep[-1]['hit']:.0f}%")
    # the pre-registered trade rule
    out = []
    for level in ("base", "stress"):
        rows = []
        for s in SYMS:
            b, X, y, ok, atr = data[s]
            thr = 2.0 * RT_USD[s] / b.pv / atr
            p = S.Plan(b.n)
            p.sigL = np.nan_to_num(pred[s], nan=0.0) >= thr
            p.sigS = np.nan_to_num(pred[s], nan=0.0) <= -thr
            p.stpL, p.stpS = rt(b, b.c - 4.0 * atr), rt(b, b.c + 4.0 * atr)
            p.time_stop_bars = H
            p.cooldown_bars, p.max_trades, p.loss_standdown = 0, 1000, 0
            T = S.run(b, p, COSTS[level])[0]
            ei = T[:, 1].astype(np.int64)
            rows.append(pd.DataFrame({"sym": s, "sess": b.sess[ei], "ts": b.ts[ei], "date": b.date[ei], "dir": T[:, 3], "net": T[:, 13] * b.pv, "win": T[:, 17] > 0}))
        out.append(pd.concat(rows, ignore_index=True))
    df, st = out
    df["fold"] = fold_of_session(df["sess"].values)
    ns = N_SEARCH - FOLDS[2][0]
    r = {"ic": float(ic), "sweep": sweep, "pooled": summ(df, ns * 2)}
    print("   trade rule pooled", line(r["pooled"]))
    for s in SYMS:
        r[s] = summ(df[df.sym == s], ns)
        print(f"   {s}               ", line(r[s]))
    r["stress"] = summ(st, ns * 2)
    print("   2x costs         ", line(r["stress"]))
    r["folds"] = [summ(df[df.fold == k], 1)["pf"] for k in range(2, 8)]
    print("   PF by fold 3..8  ", " ".join(f"{x:.2f}" for x in r["folds"]))
    res[hname] = r
    np.savez_compressed(f"reports/phase2_pred_H{H}.npz", **{s: pred[s] for s in SYMS})
json.dump(res, open("reports/phase2.json", "w"), indent=1, default=float)
