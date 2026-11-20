"""Entry filters (enhancements 3, 7, 8, 9, 10). All are causal: they only use data up to the
signal bar close."""
import numpy as np
import pandas as pd

from . import indicators as ind


def sma(x, n):
    return pd.Series(x).rolling(n, min_periods=n).mean().to_numpy()


def htf_regime(b, minutes, atr_len=14, smooth_len=10, factor=2.0):
    """Smart Trend regime on a higher timeframe built from the 5m RTH bars, mapped back so
    that each 5m bar only sees HTF bars that have fully closed."""
    k = minutes // 5
    bucket = b.bar_of_day // k
    key = b.day_id * 1000 + bucket
    df = pd.DataFrame(dict(key=key, o=b.o, h=b.h, l=b.l, c=b.c))
    g = df.groupby("key", sort=False)
    hb = pd.DataFrame(dict(o=g.o.first(), h=g.h.max(), l=g.l.min(), c=g.c.last()))
    raw = ind.atr(hb.h.to_numpy(), hb.l.to_numpy(), hb.c.to_numpy(), atr_len)
    a = ind.ema(raw, smooth_len)
    _, reg = ind.smart_trend(hb.c.to_numpy(), factor * a)
    hreg = pd.Series(reg, index=hb.index)
    pos_of_key = pd.Series(np.arange(len(hb)), index=hb.index)
    idx = pos_of_key.loc[key].to_numpy()
    # Pine non-repainting convention: request.security(tf, regime[1], lookahead_on) -> the HTF bar
    # BEFORE the one the current 5m bar belongs to
    vis = idx - 1
    out = np.where(vis >= 0, reg[np.maximum(vis, 0)], 0)
    return out


def features(b, s, cfg_lens=None):
    """Feature arrays used by filters and by the meta-label model."""
    L = dict(er=20, adx=14, hma_slope=21, vol_base=390)
    if cfg_lens:
        L.update(cfg_lens)
    f = {}
    f["er"] = ind.efficiency_ratio(b.c, L["er"])
    f["adx"], f["pdi"], f["mdi"] = ind.adx(b.h, b.l, b.c, L["adx"])
    hm = ind.hma(b.c, L["hma_slope"])
    f["hma_slope"] = np.r_[np.nan, np.diff(hm)] / s["atr"]
    f["range_atr"] = (b.h - b.l) / s["atr"]
    f["atr_ratio"] = s["raw_atr"] / sma(s["raw_atr"], L["vol_base"])
    f["trail_ext"] = (b.c - s["trail"]) / s["atr"]          # signed distance from the trail
    vw = ind.session_vwap(b.h, b.l, b.c, b.v, b.day_id)
    f["vwap_ext"] = (b.c - vw) / s["atr"]                   # signed distance from VWAP
    f["bar_of_day"] = b.bar_of_day.astype(float)
    bars_per_day = pd.Series(b.bar_of_day).groupby(b.day_id).transform("max").to_numpy()
    f["bars_to_end"] = (bars_per_day - b.bar_of_day).astype(float)
    f["rsi_fast"] = s["fast_rsi"]
    f["rsi_spread"] = s["fast_rsi"] - s["slow_rsi"]
    f["atr_pct"] = s["atr"] / b.c * 100
    f["regime"] = s["regime"].astype(float)
    return f


def allow_masks(b, s, f, cfg, htf_cache=None):
    """cfg keys (all optional):
      regime_agree, shock_range_atr, shock_atr_ratio, skip_open_bars, skip_close_bars,
      er_min, adx_min, hma_slope, htf_minutes, max_trail_ext, vwap_side, max_vwap_ext, ml_mask
    """
    n = b.n
    al = np.ones(n, bool)
    ash = np.ones(n, bool)
    if cfg.get("regime_agree"):
        al &= s["regime"] == 1
        ash &= s["regime"] == -1
    if cfg.get("shock_range_atr"):
        ok = ~(f["range_atr"] > cfg["shock_range_atr"])
        al &= ok; ash &= ok
    if cfg.get("shock_atr_ratio"):
        ok = ~(f["atr_ratio"] > cfg["shock_atr_ratio"])
        al &= ok; ash &= ok
    if cfg.get("skip_open_bars"):
        ok = f["bar_of_day"] >= cfg["skip_open_bars"]
        al &= ok; ash &= ok
    if cfg.get("skip_close_bars"):
        ok = f["bars_to_end"] >= cfg["skip_close_bars"]
        al &= ok; ash &= ok
    if cfg.get("er_min"):
        ok = f["er"] >= cfg["er_min"]
        al &= ok; ash &= ok
    if cfg.get("adx_min"):
        ok = f["adx"] >= cfg["adx_min"]
        al &= ok; ash &= ok
    if cfg.get("hma_slope"):
        al &= f["hma_slope"] > 0
        ash &= f["hma_slope"] < 0
    if cfg.get("htf_minutes"):
        m = cfg["htf_minutes"]
        if htf_cache is not None and m in htf_cache:
            hr = htf_cache[m]
        else:
            hr = htf_regime(b, m)
            if htf_cache is not None:
                htf_cache[m] = hr
        al &= hr == 1
        ash &= hr == -1
    if cfg.get("max_trail_ext"):
        ok = np.abs(f["trail_ext"]) <= cfg["max_trail_ext"]
        al &= ok; ash &= ok
    if cfg.get("vwap_side"):
        al &= f["vwap_ext"] > 0
        ash &= f["vwap_ext"] < 0
    if cfg.get("max_vwap_ext"):
        ok = np.abs(f["vwap_ext"]) <= cfg["max_vwap_ext"]
        al &= ok; ash &= ok
    if cfg.get("ml_mask") is not None:
        al &= cfg["ml_mask"]
        ash &= cfg["ml_mask"]
    return al, ash
