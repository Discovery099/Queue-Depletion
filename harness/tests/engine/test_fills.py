"""Engine acceptance tests (SPEC 7.8 items 1, 2, 4, 6): hand-computed fills for scripted scenarios.

Instrument used: ES-like, tick 0.25, point value 50.  Base costs: 1 tick slippage per side,
commission 1.25 per side = 0.05 points per round trip.
"""
import os
import sys
import time

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from engine import read_json, path  # noqa: E402
from engine.data import Bars  # noqa: E402
from engine import sim  # noqa: E402
from engine.sim import C, Plan, MARKET, LIMIT, STOP  # noqa: E402

COSTS = read_json(path("config/costs.lock.json"))["levels"]
BASE, STRESS, SHOCK = COSTS["base"], COSTS["stress"], COSTS["shock"]
Q = (100, 100.5, 99.5, 100)        # quiet bar


def mk(rows, sessions=None, tick=0.25, pv=50.0):
    """rows: (o,h,l,c) or (o,h,l,c,vol).  sessions: list of bar counts per session."""
    n = len(rows)
    b = Bars()
    a = np.array([r[:4] for r in rows], float)
    b.o, b.h, b.l, b.c = a[:, 0].copy(), a[:, 1].copy(), a[:, 2].copy(), a[:, 3].copy()
    b.v = np.array([r[4] if len(r) > 4 else 1000.0 for r in rows], float)
    sessions = sessions or [n]
    b.sess = np.repeat(np.arange(len(sessions)), sessions).astype(np.int32)
    b.first = np.r_[True, b.sess[1:] != b.sess[:-1]]
    b.last = np.r_[b.sess[1:] != b.sess[:-1], True]
    slot = np.concatenate([np.arange(k) for k in sessions])
    b.mopen = (slot * 5).astype(np.int32)
    b.mclose = b.mopen + 5
    slen = np.repeat(np.array(sessions) * 5, sessions)
    b.edge10 = (b.mopen < 10) | (b.mclose > slen - 10)
    b.n, b.tick, b.pv, b.tick_value, b.sym, b.tf = n, tick, pv, tick * pv, "ES", 5
    return b


def plan_for(b, L=(), S=(), stop_long=None, stop_short=None, tgt_long=None, tgt_short=None,
             etype=MARKET, px_long=None, px_short=None, valid=1, exL=(), exS=(), **kw):
    p = Plan(b.n)
    for i in L:
        p.sigL[i] = True
    for i in S:
        p.sigS[i] = True
    if stop_long is not None:
        p.stpL[:] = stop_long
    if stop_short is not None:
        p.stpS[:] = stop_short
    if tgt_long is not None:
        p.tgtL[:] = tgt_long
    if tgt_short is not None:
        p.tgtS[:] = tgt_short
    if px_long is not None:
        p.epxL[:] = px_long
    if px_short is not None:
        p.epxS[:] = px_short
    p.etype, p.valid_bars = etype, valid
    for i in exL:
        p.exL[i] = True
    for i in exS:
        p.exS[i] = True
    p.cooldown_bars, p.max_trades, p.loss_standdown = 2, 6, 3
    for k, v in kw.items():
        setattr(p, k, v)
    return p


def rows(T):
    return [(int(r[C["entry_idx"]]), r[C["entry_px"]], int(r[C["exit_idx"]]), r[C["exit_px"]],
             int(r[C["reason"]]), round(float(r[C["net_pts"]]), 9)) for r in T]


def check(bars, plan, expected, cost=BASE, **kw):
    T, eq, inpos, liq = sim.run(bars, plan, cost, **kw)
    got = rows(T)
    assert len(got) == len(expected), got
    for g, e in zip(got, expected):
        assert g[0] == e[0] and g[2] == e[2] and g[4] == e[4], (g, e)
        assert g[1] == pytest.approx(e[1], abs=1e-9) and g[3] == pytest.approx(e[3], abs=1e-9), (g, e)
        assert g[5] == pytest.approx(e[5], abs=1e-9), (g, e)
    if len(T):
        assert eq[-1] == pytest.approx(T[:, C["net_pts"]].sum(), abs=1e-9)
    return T, eq, inpos, liq


# ----------------------------------------------------------------------------- market orders
def test_01_market_long_fills_next_open_plus_tick_and_session_exit():
    b = mk([(100, 101, 99, 100), (100.5, 101, 100, 100.75), (100.75, 101, 100.5, 101)])
    check(b, plan_for(b, L=[0], stop_long=98), [(1, 100.75, 2, 100.75, 5, -0.05)])


def test_02_market_short_fills_next_open_minus_tick():
    b = mk([(100, 101, 99, 100), (100.5, 101, 100, 100.75), (100.75, 101, 100.5, 101)])
    check(b, plan_for(b, S=[0], stop_short=102), [(1, 100.25, 2, 101.25, 5, -1.05)])


# ----------------------------------------------------------------------------- stop orders
def test_03_stop_long_fills_at_stop_plus_tick_adverse():
    b = mk([Q, Q, (100, 100.25, 97.5, 98), (98, 98.5, 97.5, 98)])
    check(b, plan_for(b, L=[0], stop_long=98), [(1, 100.25, 2, 97.75, 2, -2.55)])


def test_04_stop_long_gap_fills_at_open():
    b = mk([Q, Q, (97, 97.5, 96, 97), (97, 97.5, 96.5, 97)])
    check(b, plan_for(b, L=[0], stop_long=98), [(1, 100.25, 2, 96.75, 2, -3.55)])


def test_05_stop_short_fills_at_stop_plus_tick_adverse():
    b = mk([Q, Q, (100, 102.5, 99.75, 102), (102, 102.5, 101.5, 102)])
    check(b, plan_for(b, S=[0], stop_short=102), [(1, 99.75, 2, 102.25, 2, -2.55)])


def test_06_stop_short_gap_fills_at_open():
    b = mk([Q, Q, (103, 103.5, 102.5, 103), (103, 103.5, 102.5, 103)])
    check(b, plan_for(b, S=[0], stop_short=102), [(1, 99.75, 2, 103.25, 2, -3.55)])


def test_07_stop_exactly_touched_is_triggered():
    b = mk([Q, Q, (100, 100.25, 98, 98.5), Q])
    check(b, plan_for(b, L=[0], stop_long=98), [(1, 100.25, 2, 97.75, 2, -2.55)])


# ----------------------------------------------------------------------------- profit targets
def test_08_target_long_needs_one_tick_trade_through():
    b = mk([Q, Q, (100, 102, 99.5, 101.5), (101.5, 102.25, 101, 102), (102, 102.5, 101.5, 102)])
    check(b, plan_for(b, L=[0], stop_long=98, tgt_long=102), [(1, 100.25, 3, 102.0, 1, 1.70)])


def test_09_target_short_needs_one_tick_trade_through():
    b = mk([Q, Q, (100, 100.5, 98, 98.5), (98.5, 99, 97.75, 98), (98, 98.5, 97.5, 98)])
    check(b, plan_for(b, S=[0], stop_short=102, tgt_short=98), [(1, 99.75, 3, 98.0, 1, 1.70)])


def test_10_stop_and_target_in_one_bar_stop_first():
    b = mk([Q, Q, (100, 103, 97, 100), Q])
    check(b, plan_for(b, L=[0], stop_long=98, tgt_long=102), [(1, 100.25, 2, 97.75, 2, -2.55)])


def test_11_intrabar_optimistic_switch_reverses_the_order():
    b = mk([Q, Q, (100, 103, 97, 100), Q])
    check(b, plan_for(b, L=[0], stop_long=98, tgt_long=102), [(1, 100.25, 2, 102.0, 1, 1.70)], optimistic=True)


# ----------------------------------------------------------------------------- entry bar
def test_12_entry_and_stop_reachable_in_entry_bar_stop_is_hit():
    b = mk([Q, (100, 100.5, 97.5, 99), Q])
    T, *_ = check(b, plan_for(b, L=[0], stop_long=98), [(1, 100.25, 1, 97.75, 2, -2.55)])
    assert T[0, C["bars_held"]] == 0


def test_13_entry_bar_opens_beyond_stop_exits_at_open():
    b = mk([Q, (97, 97.5, 96.5, 97), (97, 97.5, 96.5, 97)])
    check(b, plan_for(b, L=[0], stop_long=98), [(1, 97.25, 1, 96.75, 2, -0.55)])


def test_14_market_entry_can_reach_target_in_entry_bar_when_stop_is_not_reachable():
    b = mk([Q, (100, 103, 99.5, 102.5), (102.5, 103, 102, 102.5)])
    check(b, plan_for(b, L=[0], stop_long=98, tgt_long=102), [(1, 100.25, 1, 102.0, 1, 1.70)])


# ----------------------------------------------------------------------------- limit entries
def test_15_limit_long_needs_trade_through_and_fills_at_limit():
    b = mk([Q, (100, 100.5, 99.5, 100), (100, 100.25, 99.25, 99.75), (99.75, 100, 99.5, 100)])
    check(b, plan_for(b, L=[0], stop_long=97, etype=LIMIT, px_long=99.5, valid=3), [(2, 99.5, 3, 99.75, 5, 0.20)])


def test_16_limit_long_fills_at_limit_even_if_bar_opens_below():
    b = mk([Q, (99, 99.5, 98.75, 99.25), (99.25, 99.5, 99, 99.25)])
    check(b, plan_for(b, L=[0], stop_long=97, etype=LIMIT, px_long=99.5, valid=3), [(1, 99.5, 2, 99.0, 5, -0.55)])


def test_17_limit_entry_cannot_reach_target_in_entry_bar():
    b = mk([Q, (100, 101, 99.25, 100.75), (100.75, 101, 100.5, 100.75), Q])
    check(b, plan_for(b, L=[0], stop_long=97, tgt_long=100.5, etype=LIMIT, px_long=99.5, valid=3),
          [(1, 99.5, 2, 100.5, 1, 0.95)])


def test_18_limit_entry_with_stop_reachable_in_entry_bar():
    b = mk([Q, (100, 100, 98.75, 99.25), Q])
    check(b, plan_for(b, L=[0], stop_long=99.0, etype=LIMIT, px_long=99.5, valid=3), [(1, 99.5, 1, 98.75, 2, -0.80)])


def test_19_limit_short_trade_through():
    b = mk([Q, (100, 100.75, 99.75, 100.25), (100.25, 100.5, 100, 100.25)])
    check(b, plan_for(b, S=[0], stop_short=103, etype=LIMIT, px_short=100.5, valid=3), [(1, 100.5, 2, 100.5, 5, -0.05)])


def test_20_limit_order_expires_after_validity():
    q2 = (100, 100.5, 99.75, 100)
    b = mk([Q, q2, q2, (100, 100.25, 99, 99.5), Q])
    check(b, plan_for(b, L=[0], stop_long=97, etype=LIMIT, px_long=99.5, valid=2), [])


# ----------------------------------------------------------------------------- stop entries
def test_21_stop_entry_long_triggered_at_price():
    b = mk([Q, (100, 101, 99.75, 100.75), (100.75, 101, 100.5, 100.75)])
    check(b, plan_for(b, L=[0], stop_long=99, etype=STOP, px_long=101, valid=3), [(1, 101.25, 2, 100.5, 5, -0.80)])


def test_22_stop_entry_long_gap_fills_at_open():
    b = mk([Q, (101.5, 102, 101.25, 101.75), (101.75, 102, 101.5, 101.75)])
    check(b, plan_for(b, L=[0], stop_long=99, etype=STOP, px_long=101, valid=3), [(1, 101.75, 2, 101.5, 5, -0.30)])


def test_23_stop_entry_short():
    b = mk([Q, (100, 100.25, 98.75, 99), (99, 99.25, 98.75, 99)])
    check(b, plan_for(b, S=[0], stop_short=101, etype=STOP, px_short=99, valid=3), [(1, 98.75, 2, 99.25, 5, -0.55)])


# ----------------------------------------------------------------------------- volume rules
def test_24_zero_volume_bar_cancels_market_entry():
    b = mk([Q, (100, 100, 100, 100, 0), Q, Q])
    check(b, plan_for(b, L=[0], stop_long=98), [])


def test_25_zero_volume_bar_never_fills_a_stop():
    b = mk([Q, Q, (97, 97, 97, 97, 0), Q])
    check(b, plan_for(b, L=[0], stop_long=98), [(1, 100.25, 3, 99.75, 5, -0.55)])


def test_26_thin_bar_refuses_fill_and_logs_liquidity_miss():
    b = mk([Q, (100, 100.5, 99.5, 100, 10), Q, Q])
    *_, liq = check(b, plan_for(b, L=[0], stop_long=98), [])
    assert liq == 1


# ----------------------------------------------------------------------------- session rules
def test_27_order_at_close_of_last_bar_is_cancelled():
    b = mk([Q, Q, Q, Q, Q], sessions=[2, 3])
    check(b, plan_for(b, L=[1], stop_long=98), [])


def test_28_resting_limit_does_not_carry_into_next_session():
    b = mk([Q, (100, 100.5, 99.75, 100), (100, 100.25, 99, 99.5), Q, Q], sessions=[2, 3])
    check(b, plan_for(b, L=[0], stop_long=97, etype=LIMIT, px_long=99.5, valid=10), [])


def test_29_session_last_bar_forces_flat_for_short():
    b = mk([Q, Q, (100, 100.25, 99.5, 99.75)])
    check(b, plan_for(b, S=[0], stop_short=103), [(1, 99.75, 2, 100.0, 5, -0.30)])


# ----------------------------------------------------------------------------- exits
def test_30_time_stop_exits_at_next_open():
    b = mk([Q, Q, Q, (100.5, 101, 100, 100.5), Q])
    check(b, plan_for(b, L=[0], stop_long=95, time_stop_bars=2), [(1, 100.25, 3, 100.25, 3, -0.05)])


def test_31_invalidation_exit_at_next_open():
    b = mk([Q, Q, Q, (99, 99.5, 98.5, 99), Q])
    check(b, plan_for(b, L=[0], stop_long=95, exL=[2]), [(1, 100.25, 3, 98.75, 4, -1.55)])


def test_32_break_even_stop_counts_as_a_loss():
    b = mk([Q, (100, 101.5, 99.5, 101), (101, 101.25, 100, 100.5), Q])
    T, *_ = check(b, plan_for(b, L=[0], stop_long=99.25, be_R=1.0), [(1, 100.25, 2, 100.0, 2, -0.30)])
    assert T[0, C["is_win"]] == 0.0


def test_33_trailing_stop_only_tightens():
    b = mk([Q, (100, 102.25, 99.5, 102), (102, 102.5, 101.5, 102), Q])
    T, *_ = check(b, plan_for(b, L=[0], stop_long=99.25, trail_start_R=1.0, trail_R=0.5),
                  [(1, 100.25, 2, 101.5, 2, 1.20)])
    assert T[0, C["is_win"]] == 1.0 and T[0, C["stop_init"]] == 99.25


def test_34_partial_exit_is_one_trade():
    b = mk([Q, (100, 101.5, 99.5, 101), (101, 101.25, 100, 100.5), Q])
    T, *_ = check(b, plan_for(b, L=[0], stop_long=99.25, part_R=1.0), [(1, 100.25, 2, 100.0, 2, 0.325)])
    assert T[0, C["partial"]] == 1 and T[0, C["is_win"]] == 1.0
    assert T[0, C["slip_pts"]] == pytest.approx(0.375) and T[0, C["gross_pts"]] == pytest.approx(0.75)


# ----------------------------------------------------------------------------- sequencing
def test_35_cooldown_after_loss_same_direction():
    b = mk([Q, (100, 100.5, 97.5, 99), Q, Q, Q, Q])
    T, *_ = sim.run(b, plan_for(b, L=[0, 1, 2, 3], stop_long=98), BASE)
    assert [int(x) for x in T[:, C["entry_idx"]]] == [1, 4]


def test_36_opposite_direction_allowed_during_cooldown():
    b = mk([Q, (100, 100.5, 97.5, 99), Q, Q])
    T, *_ = sim.run(b, plan_for(b, L=[0], S=[1], stop_long=98, stop_short=103), BASE)
    assert [int(x) for x in T[:, C["entry_idx"]]] == [1, 2] and T[1, C["dir"]] == -1


def test_37_max_trades_per_session():
    b = mk([Q, Q, Q, Q, Q, Q])
    kw = dict(L=[0], S=[2], stop_long=95, stop_short=105, time_stop_bars=1)
    T1, *_ = sim.run(b, plan_for(b, max_trades=1, **kw), BASE)
    T6, *_ = sim.run(b, plan_for(b, max_trades=6, **kw), BASE)
    assert len(T1) == 1 and len(T6) == 2


def test_38_stand_down_after_three_consecutive_losses():
    wild = (100, 103, 97, 100)
    b = mk([wild] * 7)
    kw = dict(L=[0, 2, 4], S=[1, 3], stop_long=98, stop_short=102)
    T, *_ = sim.run(b, plan_for(b, **kw), BASE)
    assert len(T) == 3
    T0, *_ = sim.run(b, plan_for(b, **kw), BASE, loss_standdown=0)
    assert len(T0) == 5


def test_39_both_signals_on_one_bar_no_entry():
    b = mk([Q, Q, Q])
    check(b, plan_for(b, L=[0], S=[0], stop_long=98, stop_short=102), [])


# ----------------------------------------------------------------------------- cost levels and parity mode
def test_40_stress_cost_level():
    b = mk([(100, 101, 99, 100), (100.5, 101, 100, 100.75), (100.75, 101, 100.5, 101)])
    check(b, plan_for(b, L=[0], stop_long=95), [(1, 101.0, 2, 100.5, 5, -0.60)], cost=STRESS)


def test_41_shock_level_extra_tick_in_first_and_last_ten_minutes():
    b = mk([Q] * 6)
    assert list(b.edge10) == [True, True, False, False, True, True]
    check(b, plan_for(b, L=[0], stop_long=90, time_stop_bars=1), [(1, 101.0, 2, 99.25, 3, -1.85)], cost=SHOCK)


def test_42_pine_parity_mode_fills_at_signal_close():
    b = mk([Q, (100.5, 101, 100, 100.75), (100.75, 101, 100.5, 101)])
    check(b, plan_for(b, L=[0], stop_long=95), [(0, 100.25, 2, 100.75, 5, 0.45)], fill_at_close=True)


# ----------------------------------------------------------------------------- 7.8 item 2 and 4
def _tick_walk(n, seed, tick=0.25):
    rng = np.random.default_rng(seed)
    step = rng.choice(np.array([-1.0, 1.0]), n) * tick
    c = 10000.0 + np.cumsum(step)
    o = c - step
    return [(a, max(a, z), min(a, z), z) for a, z in zip(o, c)]


def test_buy_every_bar_exit_next_bar_loses_exactly_the_cost():
    b = mk(_tick_walk(200_000, 7))
    p = plan_for(b, stop_long=1.0, time_stop_bars=1, max_trades=10 ** 9, loss_standdown=0, cooldown_bars=0)
    p.sigL[:] = True
    T, eq, *_ = sim.run(b, p, BASE)
    ei, xi = T[:, C["entry_idx"]].astype(int), T[:, C["exit_idx"]].astype(int)
    raw = b.o[xi] - b.o[ei]
    cost = 2 * 0.25 + 0.05
    keep = T[:, C["reason"]] == 3
    assert np.allclose(T[keep, C["net_pts"]], raw[keep] - cost, atol=1e-9)       # exact identity per trade
    se = raw[keep].std() / np.sqrt(keep.sum())
    assert abs(T[keep, C["net_pts"]].mean() + cost) < 4 * se                      # average loss is the cost


def test_random_entry_symmetric_stop_target_matches_cost_adjusted_geometry():
    """One-tick-per-bar random walk, stop S ticks below and target S ticks above the raw entry.
    The stop is absorbed at -S; the target needs a 1-tick trade-through, so it is absorbed at S+1:
    win probability S/(2S+1); expectancy -2 ticks of slippage minus commission."""
    S, tick = 8, 0.25
    b = mk(_tick_walk(1_000_000, 11))
    rng = np.random.default_rng(3)
    p = plan_for(b, max_trades=10 ** 9, loss_standdown=0, cooldown_bars=0)
    long = rng.random(b.n) < 0.5
    p.sigL, p.sigS = long, ~long
    nxt = np.r_[b.o[1:], b.o[-1]]                      # raw fill price of an order placed at this close
    p.stpL, p.tgtL = nxt - S * tick, nxt + S * tick
    p.stpS, p.tgtS = nxt + S * tick, nxt - S * tick
    T, eq, *_ = sim.run(b, p, BASE)
    T = T[T[:, C["reason"]] != 5]
    n = len(T)
    assert n > 5000
    wr = T[:, C["is_win"]].mean()
    p0 = S / (2 * S + 1)
    assert abs(wr - p0) < 4 * np.sqrt(p0 * (1 - p0) / n)
    net = T[:, C["net_pts"]]
    assert abs(net.mean() + (2 * tick + 0.05)) < 4 * net.std() / np.sqrt(n)


# ----------------------------------------------------------------------------- 7.8 item 6: properties
@pytest.mark.parametrize("seed", range(6))
def test_properties_random_plans(seed):
    rng = np.random.default_rng(seed)
    n, tick = 4000, 0.25
    step = np.round(rng.normal(0, 4, n)) * tick
    c = 5000 + np.cumsum(step)
    o = np.r_[5000, c[:-1]] + np.round(rng.normal(0, 1, n)) * tick
    h = np.maximum(o, c) + rng.integers(0, 6, n) * tick
    l = np.minimum(o, c) - rng.integers(0, 6, n) * tick
    vol = rng.integers(0, 3, n) * 500.0
    b = mk(list(zip(o, h, l, c, vol)), sessions=[40] * 100)
    for etype in (MARKET, LIMIT, STOP):
        p = Plan(n)
        p.sigL, p.sigS = rng.random(n) < 0.2, rng.random(n) < 0.2
        d = rng.integers(4, 20, n) * tick
        off = rng.integers(1, 6, n) * tick * (-1 if etype == LIMIT else 1)
        p.etype, p.valid_bars = etype, 3
        p.epxL, p.epxS = c + off, c - off
        refL = c if etype == MARKET else p.epxL
        refS = c if etype == MARKET else p.epxS
        p.stpL, p.stpS = refL - d, refS + d
        p.tgtL, p.tgtS = refL + d, refS - d
        p.exL, p.exS = rng.random(n) < 0.05, rng.random(n) < 0.05
        p.time_stop_bars, p.be_R, p.trail_start_R, p.trail_R, p.part_R = 9, 1.0, 1.5, 1.0, 0.75
        T, eq, inpos, liq = sim.run(b, p, BASE)
        assert len(T) > 20
        ei, xi = T[:, C["entry_idx"]].astype(int), T[:, C["exit_idx"]].astype(int)
        d_ = T[:, C["dir"]]
        slip = tick
        # no fill outside the bar's range (prices net of the modelled slippage)
        raw_e = T[:, C["entry_px"]] - (d_ * slip if etype != LIMIT else 0)
        assert np.all(raw_e <= b.h[ei] + 1e-9) and np.all(raw_e >= b.l[ei] - 1e-9)
        r = T[:, C["reason"]]
        raw_x = T[:, C["exit_px"]] + np.where(r == 1, 0, d_ * slip)
        assert np.all(raw_x <= b.h[xi] + 1e-9) and np.all(raw_x >= b.l[xi] - 1e-9)
        assert np.all(b.v[ei] > 0) and np.all(b.v[xi][r != 5] > 0)          # never a fill on a zero-volume bar
        assert np.all(xi >= ei) and np.all(ei[1:] >= xi[:-1])                # flat to flat, no overlap
        assert np.all(b.sess[ei] == b.sess[xi])                              # intraday flat
        assert np.all(T[:, C["sig_idx"]] < ei) and np.all(b.sess[T[:, C["sig_idx"]].astype(int)] == b.sess[ei])
        # no position change without an order: position mask is exactly the union of trade spans
        m = np.zeros(n, bool)
        for a, z in zip(ei, xi):
            m[a:z] = True
        assert np.array_equal(m, inpos)
        # equity equals the sum of trade results (flat at the end)
        assert eq[-1] == pytest.approx(T[:, C["net_pts"]].sum(), abs=1e-6)
        # the stop is never widened: a stopped long never exits below initial stop minus slippage unless it gapped
        st = (r == 2)
        worse = d_[st] * (T[st, C["exit_px"]] + d_[st] * slip - T[st, C["stop_init"]])
        gapped = d_[st] * (b.o[xi[st]] - T[st, C["stop_init"]]) <= 0
        assert np.all((worse >= -1e-9) | gapped)


def test_determinism_bit_identical():
    b = mk(_tick_walk(50_000, 5))
    rng = np.random.default_rng(1)
    p = plan_for(b, stop_long=1.0, stop_short=1e9, max_trades=10 ** 9)
    p.sigL = rng.random(b.n) < 0.1
    p.stpL = b.c - 2.0
    p.tgtL = b.c + 2.0
    a = sim.run(b, p, BASE)[0]
    z = sim.run(b, p, BASE)[0]
    assert a.tobytes() == z.tobytes()


def test_speed_at_least_two_million_bars_per_second():
    b = mk(_tick_walk(2_000_000, 9))
    p = plan_for(b, max_trades=10 ** 9, loss_standdown=0)
    p.sigL[::7] = True
    p.stpL, p.tgtL = b.c - 2.0, b.c + 2.0
    sim.run(b, p, BASE)
    t0 = time.perf_counter()
    sim.run(b, p, BASE)
    rate = b.n / (time.perf_counter() - t0)
    print(f"simulator speed: {rate / 1e6:.1f} million bars per second")
    assert rate > 2e6
