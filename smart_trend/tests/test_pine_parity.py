"""The literal Python port of the Pine regular-hours engine must reproduce the research engine's
signals and all 24 model features (MES, Jan-Jun 2024)."""
import os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from st import data as dmod
from st.backtest import Market
from st.ml import signal_table, FEATS
import pine_port


def test_pine_engine_matches_research_engine():
    b = dmod.load("MES", start="2024-01-01", end="2024-07-01")
    m = Market("MES", bars=b)
    p = pine_port.run(b, m.s["roll"])
    # signals and core series
    assert (p["match_buy"] == m.s["match_buy"]).all()
    assert (p["match_sell"] == m.s["match_sell"]).all()
    assert np.allclose(p["atr"], m.s["atr"], equal_nan=True)
    assert np.allclose(p["trail"], m.s["trail"], equal_nan=True)
    assert (p["regime"] == m.s["regime"]).all()
    # the 24 model features at every tradeable signal
    T = signal_table(m, dict(stop_atr=3.0, target_atr=0.0))
    assert len(T) > 100
    i = T.idx.to_numpy(); d = T.dir.to_numpy().astype(float); a = p["atr"][i]
    mine = pd.DataFrame(dict(
        er10=p["er10"][i], er20=p["er20"][i], er40=p["er40"][i], adx=p["adx"][i], di_spread=(p["dip"][i] - p["dim"][i]) * d,
        vwap_ext=(b.c[i] - p["vwap"][i]) / a * d, trail_ext=(b.c[i] - p["trail"][i]) / a * d, range_atr=(b.h[i] - b.l[i]) / a,
        atr_ratio=m.s["raw_atr"][i] / p["atrbase"][i], bod=p["barOfDay"][i], rsi_spread=(p["fast"][i] - p["slow"][i]) * d,
        fast_rsi_dir=(p["fast"][i] - 50) * d, hma_slope=p["hslope"][i] / a * d, htf15=p["htf15"][i] * d, htf60=p["htf60"][i] * d,
        atr_pct=a / b.c[i] * 100, dow=pd.to_datetime(b.date[i]).dayofweek.to_numpy(), gap_atr=p["gap"][i] / a * d,
        day_pos=p["daypos"][i] * d, from_open_atr=p["fromopen"][i] / a * d, prev_day_atr=p["prevday"][i] / a * d,
        ret6_atr=p["ret6"][i] / a * d, ret24_atr=p["ret24"][i] / a * d, vol_ratio=b.v[i] / p["volbase"][i]))
    bad = [f for f in FEATS if not np.allclose(mine[f].fillna(0).to_numpy(), T[f].fillna(0).to_numpy(), rtol=1e-7, atol=1e-9)]
    assert not bad, bad
