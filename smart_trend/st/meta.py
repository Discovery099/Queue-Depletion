"""Walk-forward meta-label masks for the engine (enhancement 11)."""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .ml import signal_table, FEATS


def fit_logit(T, C=0.05):
    y = (T.net_usd > 0).astype(int)
    clf = make_pipeline(StandardScaler(), LogisticRegression(C=C, max_iter=3000))
    clf.fit(T[FEATS].fillna(0), y)
    return clf


def walk_forward_masks(markets, label_exit, C=0.05, q=0.6, first_test_year=2022):
    """markets: dict sym -> Market. Pooled expanding-window logistic model retrained every
    January on all earlier years. Threshold = q-quantile of the training-set probabilities.
    Returns (masks dict sym -> bool array over bars, table with probabilities)."""
    T = pd.concat([signal_table(m, label_exit, k) for k, m in enumerate(markets.values())],
                  ignore_index=True)
    p = np.full(len(T), np.nan)
    thr = np.full(len(T), np.nan)
    for yr in sorted(T.year.unique()):
        if yr < first_test_year:
            continue
        tr = (T.year < yr).to_numpy()
        te = (T.year == yr).to_numpy()
        clf = fit_logit(T[tr], C)
        p[te] = clf.predict_proba(T.loc[te, FEATS].fillna(0))[:, 1]
        thr[te] = np.quantile(clf.predict_proba(T.loc[tr, FEATS].fillna(0))[:, 1], q)
    T["p"] = p
    T["thr"] = thr
    masks = {}
    for s, m in markets.items():
        mk = np.zeros(m.b.n, bool)
        r = T[(T.sym == s) & (T.p >= T.thr)]
        mk[r.idx.to_numpy()] = True
        masks[s] = mk
    return masks, T


def walk_forward_masks_cross(train_markets, apply_markets, label_exit, C=0.05, q=0.6, first_test_year=2022):
    """Train on `train_markets` (expanding window by year), score signals of `apply_markets`
    (which may include markets not in the training pool)."""
    Ttr = pd.concat([signal_table(m, label_exit, k) for k, m in enumerate(train_markets.values())],
                    ignore_index=True)
    tabs = {s: signal_table(m, label_exit, 0) for s, m in apply_markets.items()}
    masks = {s: np.zeros(m.b.n, bool) for s, m in apply_markets.items()}
    for yr in sorted(set(Ttr.year.unique()) | {y for t in tabs.values() for y in t.year.unique()}):
        if yr < first_test_year:
            continue
        tr = Ttr[Ttr.year < yr]
        clf = fit_logit(tr, C)
        thr = np.quantile(clf.predict_proba(tr[FEATS].fillna(0))[:, 1], q)
        for s, T in tabs.items():
            te = T[T.year == yr]
            if len(te):
                pr = clf.predict_proba(te[FEATS].fillna(0))[:, 1]
                masks[s][te.idx.to_numpy()[pr >= thr]] = True
    return masks
