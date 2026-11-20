"""Enhancement 11: meta-labeling. For every raw agreement signal we compute causal features and
the outcome of an independent trade (triple barrier). A model trained ONLY on earlier years scores
the signals of the next year (expanding-window walk-forward). Signals below a probability
threshold are skipped."""
import numpy as np
import pandas as pd

from .barrier import simulate
from .filters import htf_regime
from .specs import SPECS, COMMISSION_RT

FEATS = ["er10", "er20", "er40", "adx", "di_spread", "vwap_ext", "trail_ext", "range_atr", "atr_ratio",
         "bod", "rsi_spread", "fast_rsi_dir", "hma_slope", "htf15", "htf60", "atr_pct", "dow",
         "gap_atr", "day_pos", "from_open_atr", "prev_day_atr", "ret6_atr", "ret24_atr", "vol_ratio"]


def signal_table(m, exit_kw, symbol_code=0):
    """One row per tradeable raw signal with direction-adjusted features and barrier outcome."""
    from . import indicators as ind
    b, s, f = m.b, m.s, m.f
    idx = np.where(s["match_buy"] | s["match_sell"])[0]
    idx = idx[~b.last_bar[idx] & ~s["roll"][idx] & ~np.isnan(s["atr"][idx])]
    d = np.where(s["match_buy"][idx], 1, -1).astype(np.int64)
    a = s["atr"]
    last = (np.searchsorted(b.day_id, b.day_id, side="right") - 1).astype(np.int64)
    first = np.searchsorted(b.day_id, b.day_id, side="left")
    # day context (causal: running high/low since the open)
    df = pd.DataFrame(dict(day=b.day_id, h=b.h, l=b.l, c=b.c, o=b.o, v=b.v))
    run_hi = df.groupby("day").h.cummax().to_numpy()
    run_lo = df.groupby("day").l.cummin().to_numpy()
    day_open = b.o[first]
    day_close = df.groupby("day").c.last()
    prev_close = day_close.shift(1).reindex(b.day_id).to_numpy()
    prev_ret = (day_close - day_close.shift(1)).shift(1).reindex(b.day_id).to_numpy()
    vol_avg = pd.Series(b.v).rolling(390, min_periods=50).mean().to_numpy()
    er10 = ind.efficiency_ratio(b.c, 10)
    er40 = ind.efficiency_ratio(b.c, 40)
    h15 = m.htf.get(15)
    if h15 is None:
        h15 = m.htf[15] = htf_regime(b, 15)
    h60 = m.htf.get(60)
    if h60 is None:
        h60 = m.htf[60] = htf_regime(b, 60)
    c6 = np.r_[np.full(6, np.nan), b.c[6:] - b.c[:-6]]
    c24 = np.r_[np.full(24, np.nan), b.c[24:] - b.c[:-24]]
    X = pd.DataFrame(dict(
        er10=er10[idx], er20=f["er"][idx], er40=er40[idx], adx=f["adx"][idx],
        di_spread=(f["pdi"][idx] - f["mdi"][idx]) * d,
        vwap_ext=f["vwap_ext"][idx] * d, trail_ext=f["trail_ext"][idx] * d,
        range_atr=f["range_atr"][idx], atr_ratio=f["atr_ratio"][idx], bod=b.bar_of_day[idx],
        rsi_spread=f["rsi_spread"][idx] * d, fast_rsi_dir=(s["fast_rsi"][idx] - 50) * d,
        hma_slope=f["hma_slope"][idx] * d, htf15=(h15[idx] * d).astype(float),
        htf60=(h60[idx] * d).astype(float), atr_pct=f["atr_pct"][idx],
        dow=pd.to_datetime(b.date[idx]).dayofweek.to_numpy(),
        gap_atr=(day_open[idx] - prev_close[idx]) / a[idx] * d,
        day_pos=np.where(run_hi[idx] > run_lo[idx], (b.c[idx] - run_lo[idx]) / (run_hi[idx] - run_lo[idx]), 0.5) * d,
        from_open_atr=(b.c[idx] - day_open[idx]) / a[idx] * d,
        prev_day_atr=prev_ret[idx] / a[idx] * d,
        ret6_atr=c6[idx] / a[idx] * d, ret24_atr=c24[idx] / a[idx] * d,
        vol_ratio=b.v[idx] / vol_avg[idx],
    ))
    sp = SPECS[m.symbol]
    g, hold = simulate(idx, d, b.o, b.h, b.l, b.c, a, s["trail"], s["regime"].astype(np.int64), last,
                       sp["tick"], 1.0, exit_kw.get("stop_atr", 1.5), exit_kw.get("target_atr", 2.0),
                       exit_kw.get("max_bars", 0), 0.0, 3, exit_kw.get("trail_exit", 0),
                       0.0, 0.0, 1.0)
    net = g * sp["pv"] - COMMISSION_RT
    X["symbol"] = symbol_code
    X["idx"] = idx
    X["dir"] = d
    X["year"] = b.year[idx]
    X["net_usd"] = net
    X["net_atr"] = net / (a[idx] * sp["pv"])
    X["sym"] = m.symbol
    return X[~np.isnan(g)].reset_index(drop=True)


def walk_forward(T, model="lgbm", first_test_year=2022, label="win", seed=0):
    """Expanding window by calendar year. Returns out-of-sample probabilities (nan for years that
    were never out-of-sample)."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    import lightgbm as lgb

    y = (T.net_usd > 0).astype(int) if label == "win" else (T.net_atr > 0.25).astype(int)
    feats = FEATS + ["symbol"]
    p = np.full(len(T), np.nan)
    for yr in sorted(T.year.unique()):
        if yr < first_test_year:
            continue
        tr = T.year < yr
        te = T.year == yr
        Xtr = T.loc[tr, feats].fillna(0).to_numpy()
        Xte = T.loc[te, feats].fillna(0).to_numpy()
        if model == "lgbm":
            clf = lgb.LGBMClassifier(n_estimators=200, learning_rate=0.03, num_leaves=8, max_depth=3,
                                     min_child_samples=100, subsample=0.8, subsample_freq=1,
                                     colsample_bytree=0.8, reg_lambda=5.0, random_state=seed, verbose=-1)
        else:
            clf = make_pipeline(StandardScaler(), LogisticRegression(C=0.05, max_iter=2000))
        clf.fit(Xtr, y[tr])
        p[te.to_numpy()] = clf.predict_proba(Xte)[:, 1]
    return p
