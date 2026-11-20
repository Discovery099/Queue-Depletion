"""Experiment harness: evaluate one configuration on every symbol, in-sample and out-of-sample."""
import json
import warnings

import numpy as np
import pandas as pd

from .backtest import Market, metrics

warnings.filterwarnings("ignore")

IS = ("2020-01-01", "2024-01-01")    # selection period (4 years)
OOS = ("2024-01-01", "2026-04-01")   # untouched confirmation period (~2.2 years)

_cache = {}


def market(sym, sig_kw):
    key = (sym, json.dumps(sig_kw, sort_keys=True))
    if key not in _cache:
        base = None
        for (s2, _), m in _cache.items():
            if s2 == sym:
                base = m.b
                break
        _cache[key] = Market(sym, sig_kw=sig_kw, bars=base)
    return _cache[key]


def evaluate(syms, cfg, keep_trades=False):
    """cfg = dict(sig={...}, filt={...}, eng={...}). Returns DataFrame of metrics."""
    rows = []
    trades = {}
    for s in syms:
        m = market(s, cfg.get("sig", {}))
        filt = dict(cfg.get("filt", {}))
        if "ml_masks" in cfg:
            filt["ml_mask"] = cfg["ml_masks"][s]
        t = m.run(filt=filt, **cfg.get("eng", {}))
        if keep_trades:
            trades[s] = t
        for name, (a, b) in (("IS", IS), ("OOS", OOS)):
            r = metrics(t, a, b)
            r.update(symbol=s, period=name)
            rows.append(r)
    df = pd.DataFrame(rows)
    return (df, trades) if keep_trades else df


def score(df, period="IS"):
    d = df[df.period == period]
    pf = d.pf.clip(0.05, 5.0)
    return float(np.mean(np.log(pf))), float(d.ret_dd.clip(-5, 20).mean()), int(d.trades.sum())


def summary_line(label, df):
    out = []
    for p in ("IS", "OOS"):
        d = df[df.period == p]
        lp, rdd, n = score(df, p)
        out.append(f"{p}: gPF={np.exp(lp):4.2f} ret/DD={rdd:5.2f} n={n:5d} net={d.net.sum():9.0f} "
                   f"DD(sum)={d.max_dd.sum():9.0f} worstDay={d.worst_day.min():7.0f}")
    pfs = " ".join(f"{r.symbol}:{r.pf:4.2f}/{df[(df.symbol==r.symbol)&(df.period=='OOS')].pf.iloc[0]:4.2f}"
                   for r in df[df.period == "IS"].itertuples())
    return f"{label:42s} | " + " | ".join(out) + f" | PF IS/OOS {pfs}"
