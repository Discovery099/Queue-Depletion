"""SPEC 7.8 item 5: the baseline reproduction in parity mode matches a reference trade list produced
independently from the Pine logic for a 30-session sample, to the tick.

The reference below is a line-by-line, bar-by-bar transliteration of baseline/smart_trend_v1.pine
written without numpy and without any engine code: its own Wilder ATR, its own EMA, its own trail
state machine and its own order book-keeping (process_orders_on_close=true, slippage 1 tick,
commission 1.25 per contract per side, quantity 1).
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from engine import read_json, path  # noqa: E402
from engine.data import research_bars  # noqa: E402
from engine.sim import C  # noqa: E402
from baseline import smart_trend_v1 as st  # noqa: E402

BASE = read_json(path("config/costs.lock.json"))["levels"]["base"]


def pine_reference(O, H, L, Cl, tick, point_value, atr_len=14, factor=3.0, confirm=1, adapt_len=10):
    na = None
    n = len(Cl)
    # ta.atr: ta.rma(ta.tr(true), 14)
    tr = []
    for i in range(n):
        if i == 0:
            tr.append(H[i] - L[i])
        else:
            tr.append(max(H[i] - L[i], abs(H[i] - Cl[i - 1]), abs(L[i] - Cl[i - 1])))
    raw_atr = [na] * n
    for i in range(n):
        if i == atr_len - 1:
            raw_atr[i] = sum(tr[:atr_len]) / atr_len
        elif i >= atr_len:
            raw_atr[i] = (raw_atr[i - 1] * (atr_len - 1) + tr[i]) / atr_len
    # ta.ema(_rawAtr, 10): seeded with the simple average of the first 10 defined values
    atr = [na] * n
    k = 2.0 / (adapt_len + 1)
    start = atr_len - 1 + adapt_len - 1
    for i in range(n):
        if i == start:
            atr[i] = sum(raw_atr[atr_len - 1:start + 1]) / adapt_len
        elif i > start:
            atr[i] = k * raw_atr[i] + (1 - k) * atr[i - 1]
    trail_level, regime, confirm_count, prev_regime = na, 0, 0, 0
    position, entry_price, entry_bar = 0, 0.0, 0
    commission = 2 * 1.25 / point_value
    trades = []
    for i in range(n):
        close = Cl[i]
        buffer = na if atr[i] is na else factor * atr[i]
        if trail_level is na and atr[i] is not na:
            trail_level = close
            regime = 1 if close > Cl[i - 1] else -1
            confirm_count = 0
        if trail_level is not na and buffer is not na:
            raw_regime = regime
            if regime == 1:
                raw_trail = max(trail_level, close - buffer)
                if close < raw_trail:
                    raw_regime = -1
            else:
                raw_trail = min(trail_level, close + buffer)
                if close > raw_trail:
                    raw_regime = 1
            if raw_regime != regime:
                confirm_count += 1
                if confirm_count >= confirm:
                    regime = raw_regime
                    confirm_count = 0
                    trail_level = close - buffer if regime == 1 else close + buffer
                else:
                    trail_level = max(trail_level, close - buffer) if regime == 1 else min(trail_level, close + buffer)
            else:
                confirm_count = 0
                trail_level = max(trail_level, close - buffer) if regime == 1 else min(trail_level, close + buffer)
        bull_cross = regime == 1 and prev_regime == -1
        bear_cross = regime == -1 and prev_regime == 1
        prev_regime = regime
        for arrow, side in ((bull_cross, 1), (bear_cross, -1)):
            if arrow and position != side:
                if position != 0:                       # strategy.close: fills at this close, 1 tick against
                    exit_price = close - position * tick
                    trades.append((entry_bar, i, position, entry_price, exit_price,
                                   position * (exit_price - entry_price) - commission))
                position, entry_bar = side, i           # strategy.entry: fills at this close, 1 tick against
                entry_price = close + side * tick
    return trades


@pytest.mark.parametrize("sym", ["ES", "YM"])
@pytest.mark.parametrize("tf", [5, 15])
def test_parity_reproduction_matches_independent_reference_on_30_sessions(sym, tf):
    b = research_bars(sym, tf)
    lo = 200                                              # 30 consecutive research sessions
    m = b.mask_sessions(lo, lo + 30)
    i0, i1 = m.argmax(), m.argmax() + m.sum()
    ref = pine_reference(list(b.o), list(b.h), list(b.l), list(b.c), b.tick, b.pv)
    T, _ = st.run(b, BASE, at_close=True)
    got = [(int(r[C["entry_idx"]]), int(r[C["exit_idx"]]), int(r[C["dir"]]), r[C["entry_px"]], r[C["exit_px"]],
            r[C["net_pts"]]) for r in T if r[C["reason"]] == 6]
    ref_s = [t for t in ref if i0 <= t[0] < i1]
    got_s = [t for t in got if i0 <= t[0] < i1]
    assert len(ref_s) >= 10 and len(ref_s) == len(got_s)
    for a, z in zip(ref_s, got_s):
        assert a[:3] == z[:3]
        assert abs(a[3] - z[3]) < 1e-9 and abs(a[4] - z[4]) < 1e-9     # prices, to the tick
        assert abs(a[5] - z[5]) < 1e-9
    assert len(ref) == len(got)                            # and the whole research block agrees in count
