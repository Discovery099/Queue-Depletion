"""Python reproduction of the owner's Smart Trend V1 (baseline/smart_trend_v1.pine), SPEC 4.3.

Signal logic reproduced: ATR(14) smoothed by EMA(10), times factor 3.0, drives the Smart Trail state
machine; a regime flip to bull is a BUY arrow, to bear a SELL arrow; confirm bars = 1, signal
delay = 0.  With the default minimum strength of 1 and the ADX filter off, the strength score and
both higher-timeframe requests filter nothing, so arrows equal regime flips.

The strategy is always in the market and has no stop, so it violates Article 9.  It is a reference
row only and can never be certified.  Two timings are reported:
  PINE_PARITY : fills at the signal bar's close (the script's process_orders_on_close=true);
  DEFAULT     : fills at the next bar's open, carrying overnight (the harness timing).
"""
import numpy as np

from engine import features as F
from engine import sim

DEFAULTS = {"atr_len": 14, "factor": 3.0, "confirm": 1, "use_adapt": True, "adapt_len": 10}


def arrows(bars, atr_len=14, factor=3.0, confirm=1, use_adapt=True, adapt_len=10):
    raw = F.atr(bars.h, bars.l, bars.c, atr_len)
    a = F.ema(raw, adapt_len) if use_adapt else raw
    trail, regime = F.smart_trail(bars.c, factor * a, confirm)
    prev = np.r_[np.int8(0), regime[:-1]]
    buy = (regime == 1) & (prev == -1)
    sell = (regime == -1) & (prev == 1)
    return buy, sell, trail, regime


def run(bars, cost, at_close, **params):
    buy, sell, _, _ = arrows(bars, **{**DEFAULTS, **params})
    return sim.run_reversal(bars, buy, sell, cost, at_close)
