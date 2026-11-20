"""Signal generation: Smart Trend flips + pullback recovery, HMA events, RSI events and the
three-signal agreement state machine, translated line by line from the Pine script."""
import numpy as np
from numba import njit

from . import indicators as ind


@njit(cache=True)
def recovery_events(o, h, l, c, trail, regime, atr, roll_blocked, epoch_min, use_recovery):
    n = c.size
    flip_buy = np.zeros(n, np.bool_)
    flip_sell = np.zeros(n, np.bool_)
    rec_buy = np.zeros(n, np.bool_)
    rec_sell = np.zeros(n, np.bool_)
    prev_reg = 0
    armed = 0
    rbar = -1
    rtime = -1
    for i in range(n):
        reg = regime[i]
        fb = reg == 1 and prev_reg == -1
        fs = reg == -1 and prev_reg == 1
        flip_buy[i] = fb
        flip_sell[i] = fs
        prev_reg = reg
        if (not use_recovery) or fb or fs or roll_blocked[i] or reg == 0 or np.isnan(atr[i]) or np.isnan(trail[i]):
            armed = 0
            rbar = -1
            rtime = -1
            continue
        expired = armed != 0 and (armed != reg or i - rbar > 6 or epoch_min[i] - rtime > 30)
        if expired:
            armed = 0
            rbar = -1
            rtime = -1
        fired = False
        if armed != 0 and i > rbar:
            if reg == 1 and c[i] > h[i - 1] and c[i] > o[i]:
                rec_buy[i] = True
                fired = True
                armed = 0
                rbar = -1
                rtime = -1
            elif reg == -1 and c[i] < l[i - 1] and c[i] < o[i]:
                rec_sell[i] = True
                fired = True
                armed = 0
                rbar = -1
                rtime = -1
        if armed == 0 and not fired:
            if reg == 1 and l[i] <= trail[i] + 0.5 * atr[i]:
                armed = 1
                rbar = i
                rtime = epoch_min[i]
            elif reg == -1 and h[i] >= trail[i] - 0.5 * atr[i]:
                armed = -1
                rbar = i
                rtime = epoch_min[i]
    return flip_buy, flip_sell, rec_buy, rec_sell


@njit(cache=True)
def hma_events(c, hma):
    n = c.size
    buy = np.zeros(n, np.bool_)
    sell = np.zeros(n, np.bool_)
    shadow = 0
    for i in range(1, n):
        if np.isnan(hma[i]) or np.isnan(hma[i - 1]):
            continue
        up = c[i] > hma[i] and c[i - 1] <= hma[i - 1]
        dn = c[i] < hma[i] and c[i - 1] >= hma[i - 1]
        if up and shadow != 1:
            buy[i] = True
            shadow = 1
        elif dn and shadow != -1:
            sell[i] = True
            shadow = -1
    return buy, sell


@njit(cache=True)
def match_signals(smart_buy, smart_sell, hma_buy, hma_sell, rsi_buy, rsi_sell,
                  roll_blocked, max_gap, use_hma, use_rsi):
    n = smart_buy.size
    mbuy = np.zeros(n, np.bool_)
    msell = np.zeros(n, np.bool_)
    sp = 0; hp = 0; rp = 0
    sb = -1; hb = -1; rb = -1
    for i in range(n):
        if roll_blocked[i]:
            sp = 0; hp = 0; rp = 0; sb = -1; hb = -1; rb = -1
            continue
        if sp != 0 and i - sb > max_gap:
            sp = 0; sb = -1
        if hp != 0 and i - hb > max_gap:
            hp = 0; hb = -1
        if rp != 0 and i - rb > max_gap:
            rp = 0; rb = -1
        hB = hma_buy[i] and use_hma
        hS = hma_sell[i] and use_hma
        rB = rsi_buy[i] and use_rsi
        rS = rsi_sell[i] and use_rsi
        up = smart_buy[i] or hB or rB
        dn = smart_sell[i] or hS or rS
        if up and dn:
            sp = 0; hp = 0; rp = 0; sb = -1; hb = -1; rb = -1
            continue
        se = 1 if smart_buy[i] else (-1 if smart_sell[i] else 0)
        he = 1 if hB else (-1 if hS else 0)
        re = 1 if rB else (-1 if rS else 0)
        ed = se if se != 0 else (he if he != 0 else re)
        if ed != 0:
            if sp != 0 and sp != ed:
                sp = 0; sb = -1
            if hp != 0 and hp != ed:
                hp = 0; hb = -1
            if rp != 0 and rp != ed:
                rp = 0; rb = -1
        if se != 0:
            sp = se; sb = i
        if he != 0:
            hp = he; hb = i
        if re != 0:
            rp = re; rb = i
        hp_eff = hp if use_hma else sp
        rp_eff = rp if use_rsi else sp
        if sp != 0 and sp == hp_eff and sp == rp_eff:
            mbuy[i] = sp == 1
            msell[i] = sp == -1
            sp = 0; hp = 0; rp = 0; sb = -1; hb = -1; rb = -1
    return mbuy, msell


def build(b, atr_len=14, trail_factor=2.0, smooth_atr=True, smooth_len=10, use_recovery=True,
          hma_len=2, use_hma=True, rsi_fast=25, rsi_slow=100, use_rsi=True, max_gap=4,
          roll_guard=True):
    """Compute everything the strategy needs. Returns a dict of arrays."""
    raw_atr = ind.atr(b.h, b.l, b.c, atr_len)
    atr = ind.ema(raw_atr, smooth_len) if smooth_atr else raw_atr
    trail, regime = ind.smart_trend(b.c, trail_factor * atr)
    roll = b.roll_blocked if roll_guard else np.zeros(b.n, bool)
    fb, fs, rb_, rs_ = recovery_events(b.o, b.h, b.l, b.c, trail, regime, atr, roll, b.epoch_min, use_recovery)
    smart_buy = fb | rb_
    smart_sell = fs | rs_
    hma = ind.hma(b.c, hma_len)
    hb, hs = hma_events(b.c, hma)
    fr = ind.rsi(b.c, rsi_fast)
    sr = ind.rsi(b.c, rsi_slow)
    cu = (fr > sr) & (np.roll(fr, 1) <= np.roll(sr, 1))
    cd = (fr < sr) & (np.roll(fr, 1) >= np.roll(sr, 1))
    cu[0] = cd[0] = False
    rsi_buy = np.r_[False, cu[:-1]]   # next-bar approximation used in the script
    rsi_sell = np.r_[False, cd[:-1]]
    mbuy, msell = match_signals(smart_buy, smart_sell, hb, hs, rsi_buy, rsi_sell, roll, max_gap,
                                use_hma, use_rsi)
    return dict(raw_atr=raw_atr, atr=atr, trail=trail, regime=regime, smart_buy=smart_buy,
                smart_sell=smart_sell, flip_buy=fb, flip_sell=fs, rec_buy=rb_, rec_sell=rs_,
                hma_buy=hb, hma_sell=hs, rsi_buy=rsi_buy, rsi_sell=rsi_sell, fast_rsi=fr,
                slow_rsi=sr, match_buy=mbuy, match_sell=msell, roll=roll)
