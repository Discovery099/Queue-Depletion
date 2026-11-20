"""No-lookahead and logic tests. Run: python3 -m pytest -q tests (from smart_trend/)."""
import os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from st import data as dmod, indicators as ind
from st.backtest import Market
from st.ml import signal_table, FEATS


def _truncate(b, k):
    c = dmod.Bars()
    for name, v in vars(b).items():
        if isinstance(v, np.ndarray) and v.shape[:1] == (b.n,):
            setattr(c, name, v[:k])
        elif isinstance(v, pd.Series) and len(v) == b.n:
            setattr(c, name, v.iloc[:k].reset_index(drop=True))
        else:
            setattr(c, name, v)
    c.n = k
    c.last_bar = b.last_bar[:k].copy()   # last_bar is known in advance from the session calendar
    return c


def test_hma2_is_down_close():
    c = np.array([100, 101, 100.5, 100.2, 100.8, 101.5, 101.0])
    h = ind.hma(c, 2)
    up = (c[1:] > h[1:]) & (c[:-1] <= h[:-1])
    down_close = c[1:] < c[:-1]
    prev_up = np.r_[False, c[1:-1] >= c[:-2]]
    assert np.all(up[1:] == (down_close & prev_up)[1:])


def test_features_and_signals_have_no_lookahead():
    full = Market("MES")
    b = full.b
    rng = np.random.default_rng(0)
    cuts = rng.integers(20000, b.n - 10, size=4)
    T_full = signal_table(full, dict(stop_atr=3.0, target_atr=0.0))
    for k in cuts:
        part = Market("MES", bars=_truncate(b, int(k)))
        for key in ("atr", "trail", "regime", "match_buy", "match_sell"):
            a, p = full.s[key][:k], part.s[key]
            assert np.allclose(np.nan_to_num(a.astype(float)), np.nan_to_num(p.astype(float))), key
        for key in ("er", "adx", "vwap_ext", "trail_ext", "atr_ratio", "hma_slope"):
            assert np.allclose(np.nan_to_num(full.f[key][:k]), np.nan_to_num(part.f[key])), key
        T_part = signal_table(part, dict(stop_atr=3.0, target_atr=0.0))
        # features of signals that occurred before the cut must be identical (outcomes may differ)
        m = T_full.merge(T_part, on="idx", suffixes=("_f", "_p"))
        assert len(m) > 50
        for f in FEATS:
            assert np.allclose(m[f + "_f"].fillna(0), m[f + "_p"].fillna(0)), f


def test_engine_original_target_is_capped_at_150_on_es():
    m = Market("ES")
    t = m.run()
    tg = t[t.reason_name == "target"]
    # $150 cap = 12 ticks on ES -> gross 150, net 147.5
    assert (np.isclose(tg.pnl, 147.5) | (tg.pnl < 147.5)).all()
    assert np.isclose(tg.pnl, 147.5).mean() > 0.8
