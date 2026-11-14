"""Order simulator (SPEC 7).  Signals come in as arrays; this module alone decides fills.

Default engine timing (7.2):
  * features for bar t are final at the close of bar t;
  * a market order decided at the close of t fills at the open of t+1 plus adverse slippage;
  * limit and stop orders placed at the close of t are live from t+1;
  * an order placed at the close of a session's last bar is cancelled (INTRADAY_FLAT);
  * the session's last bar forces flat at its close minus adverse slippage.
Fill rules (7.3) are pessimistic: stop before target, stop reachable in the entry bar is hit,
targets and limit entries need a 1-tick trade-through, gaps fill at the open, zero-volume bars
never fill, bars thinner than `min_vol` refuse the fill.

Trade matrix columns (one row per flat-to-flat trade, Article 7):
"""
import numpy as np
from numba import njit

COLS = ("sig_idx", "entry_idx", "exit_idx", "dir", "entry_px", "exit_px", "stop_init", "tgt_init",
        "reason", "mae_pts", "mfe_pts", "gross_pts", "slip_pts", "net_pts", "partial", "bars_held",
        "risk_pts", "is_win")
C = {k: i for i, k in enumerate(COLS)}
NCOL = len(COLS)
REASONS = {1: "target", 2: "stop", 3: "time", 4: "invalidation", 5: "session", 6: "reverse"}
MARKET, LIMIT, STOP = 0, 1, 2


@njit(cache=True)
def _simulate(o, h, l, c, v, first, last, edge,
              sigL, sigS, etype, epxL, epxS, valid_bars,
              stpL, stpS, tgtL, tgtS, exL, exS,
              tick, slip_ticks, edge_extra, comm_pts,
              time_stop_bars, be_R, trail_start_R, trail_R, part_R,
              cooldown_bars, max_trades, loss_standdown,
              optimistic, min_vol, fill_at_close):
    n = len(c)
    T = np.zeros((n + 1, NCOL))
    eq = np.zeros(n)
    inpos = np.zeros(n, np.bool_)
    nt = 0
    liq_miss = 0
    realized_total = 0.0
    pos = 0
    frac = 1.0
    entry_px = 0.0
    stop = 0.0
    tgt = np.nan
    risk = 0.0
    mfe = 0.0
    mae = 0.0
    part_realized = 0.0
    partial = 0
    slip_acc = 0.0
    entry_idx = 0
    sig_idx = 0
    bars_held = 0
    pend_exit = 0
    stop_init = 0.0
    ord_dir = 0
    ord_px = 0.0
    ord_stop = 0.0
    ord_tgt = np.nan
    ord_expiry = -1
    ord_sig = 0
    trades_today = 0
    consec_losses = 0
    stand_down = False
    last_loss_dir = 0
    last_loss_bar = -10 ** 9

    for t in range(n):
        if first[t]:
            trades_today = 0
            consec_losses = 0
            stand_down = False
            ord_dir = 0
        tradable = v[t] > 0.0 and v[t] >= min_vol
        slip = (slip_ticks + (edge_extra if edge[t] else 0.0)) * tick
        entered_now = False

        # ---- 1. pending entry order ----
        if pos == 0 and ord_dir != 0:
            if t > ord_expiry:
                ord_dir = 0
            elif not tradable:
                if v[t] > 0.0:
                    liq_miss += 1
                if etype == 0:
                    ord_dir = 0
            else:
                d = ord_dir
                fill = np.nan
                eslip = 0.0
                if etype == 0:
                    fill = o[t] + d * slip
                    eslip = slip
                elif etype == 1:
                    # fills at the limit price, or at the worst in-range price when the whole bar is through it
                    if d == 1 and l[t] <= ord_px - tick:
                        fill = min(ord_px, h[t])
                    elif d == -1 and h[t] >= ord_px + tick:
                        fill = max(ord_px, l[t])
                else:
                    if d == 1 and h[t] >= ord_px:
                        fill = max(ord_px, o[t]) + slip
                        eslip = slip
                    elif d == -1 and l[t] <= ord_px:
                        fill = min(ord_px, o[t]) - slip
                        eslip = slip
                if not np.isnan(fill):
                    pos = d
                    entry_px = fill
                    stop = ord_stop
                    stop_init = ord_stop
                    tgt = ord_tgt
                    risk = d * (fill - stop)
                    if risk < tick:
                        risk = tick
                    frac = 1.0
                    part_realized = 0.0
                    partial = 0
                    slip_acc = eslip
                    mfe = 0.0
                    mae = 0.0
                    bars_held = 0
                    entry_idx = t
                    sig_idx = ord_sig
                    pend_exit = 0
                    trades_today += 1
                    entered_now = True
                    ord_dir = 0
                elif etype == 0:
                    ord_dir = 0

        # ---- 2. manage the open position ----
        if pos != 0:
            d = pos
            done = False
            xpx = 0.0
            reason = 0
            if pend_exit != 0 and not entered_now and v[t] > 0.0:
                xpx = o[t] - d * slip
                slip_acc += frac * slip
                reason = pend_exit
                done = True
            if not done and tradable:
                hit_stop = (d == 1 and l[t] <= stop) or (d == -1 and h[t] >= stop)
                hit_tgt = False
                if not np.isnan(tgt):
                    hit_tgt = (d == 1 and h[t] >= tgt + tick) or (d == -1 and l[t] <= tgt - tick)
                if entered_now and etype != 0:
                    hit_tgt = False
                if hit_stop and hit_tgt and optimistic:
                    hit_stop = False
                if hit_stop:
                    gap = (d == 1 and o[t] <= stop) or (d == -1 and o[t] >= stop)
                    xpx = (o[t] if gap else stop) - d * slip
                    slip_acc += frac * slip
                    reason = 2
                    done = True
                elif hit_tgt:
                    xpx = max(tgt, l[t]) if d == 1 else min(tgt, h[t])
                    reason = 1
                    done = True
                elif part_R > 0.0 and frac == 1.0 and not (entered_now and etype != 0):
                    t1 = entry_px + d * part_R * risk
                    if (d == 1 and h[t] >= t1 + tick) or (d == -1 and l[t] <= t1 - tick):
                        t1 = max(t1, l[t]) if d == 1 else min(t1, h[t])
                        part_realized = 0.5 * d * (t1 - entry_px)
                        frac = 0.5
                        partial = 1
                        if d * (entry_px - stop) > 0.0:
                            stop = entry_px
            # excursions from the entry price, using bar highs and lows
            if d == 1:
                mfe = max(mfe, h[t] - entry_px)
                mae = max(mae, entry_px - l[t])
            else:
                mfe = max(mfe, entry_px - l[t])
                mae = max(mae, h[t] - entry_px)
            if not done:
                # stops may only tighten (Article 9)
                if be_R > 0.0 and mfe >= be_R * risk and d * (entry_px - stop) > 0.0:
                    stop = entry_px
                if trail_R > 0.0 and mfe >= trail_start_R * risk:
                    ns = entry_px + d * (mfe - trail_R * risk)
                    if d * (ns - stop) > 0.0:
                        stop = ns
                bars_held += 1
                if time_stop_bars > 0 and bars_held >= time_stop_bars:
                    pend_exit = 3
                if (d == 1 and exL[t]) or (d == -1 and exS[t]):
                    pend_exit = 4
                if last[t]:
                    xpx = c[t] - d * slip
                    slip_acc += frac * slip
                    reason = 5
                    done = True
            if done:
                net_px = part_realized + frac * d * (xpx - entry_px)
                net = net_px - comm_pts
                T[nt, 0] = sig_idx
                T[nt, 1] = entry_idx
                T[nt, 2] = t
                T[nt, 3] = d
                T[nt, 4] = entry_px
                T[nt, 5] = xpx
                T[nt, 6] = stop_init
                T[nt, 7] = tgt
                T[nt, 8] = reason
                T[nt, 9] = mae
                T[nt, 10] = mfe
                T[nt, 11] = net_px + slip_acc
                T[nt, 12] = slip_acc
                T[nt, 13] = net
                T[nt, 14] = partial
                T[nt, 15] = t - entry_idx
                T[nt, 16] = risk
                win = net > tick
                T[nt, 17] = 1.0 if win else 0.0
                nt += 1
                realized_total += net
                if win:
                    consec_losses = 0
                else:
                    consec_losses += 1
                    last_loss_dir = d
                    last_loss_bar = t
                    if loss_standdown > 0 and consec_losses >= loss_standdown:
                        stand_down = True
                pos = 0
                pend_exit = 0

        # ---- 3. decisions at the close of bar t ----
        if pos == 0 and not last[t] and not stand_down and trades_today < max_trades:
            want = 0
            if sigL[t] and not sigS[t]:
                want = 1
            elif sigS[t] and not sigL[t]:
                want = -1
            if want != 0 and want == last_loss_dir and t - last_loss_bar < cooldown_bars:
                want = 0
            if want != 0:
                s_ = stpL[t] if want == 1 else stpS[t]
                g_ = tgtL[t] if want == 1 else tgtS[t]
                p_ = epxL[t] if want == 1 else epxS[t]
                if not np.isnan(s_) and (etype == 0 or not np.isnan(p_)):
                    if fill_at_close and etype == 0:
                        # PINE_PARITY mode only: fill at the signal bar's close (never used by a gate)
                        pos = want
                        entry_px = c[t] + want * slip
                        stop = s_
                        stop_init = s_
                        tgt = g_
                        risk = max(want * (entry_px - stop), tick)
                        frac = 1.0
                        part_realized = 0.0
                        partial = 0
                        slip_acc = slip
                        mfe = 0.0
                        mae = 0.0
                        bars_held = 0
                        entry_idx = t
                        sig_idx = t
                        pend_exit = 0
                        trades_today += 1
                    else:
                        ord_dir = want
                        ord_px = p_
                        ord_stop = s_
                        ord_tgt = g_
                        ord_expiry = t + (1 if etype == 0 else valid_bars)
                        ord_sig = t
        if last[t]:
            ord_dir = 0
        inpos[t] = pos != 0
        eq[t] = realized_total
        if pos != 0:
            eq[t] += part_realized + frac * pos * (c[t] - entry_px)
    return T[:nt], eq, inpos, liq_miss


class Plan:
    """Everything the signal layer hands to the simulator.  Built by the genome compiler."""

    def __init__(self, n):
        f = np.full(n, np.nan)
        z = np.zeros(n, np.bool_)
        self.sigL, self.sigS = z.copy(), z.copy()
        self.etype, self.valid_bars = MARKET, 1
        self.epxL, self.epxS = f.copy(), f.copy()
        self.stpL, self.stpS = f.copy(), f.copy()
        self.tgtL, self.tgtS = f.copy(), f.copy()
        self.exL, self.exS = z.copy(), z.copy()
        self.time_stop_bars = 0
        self.be_R = self.trail_start_R = self.trail_R = self.part_R = 0.0
        self.cooldown_bars, self.max_trades, self.loss_standdown = 2, 6, 3

    def copy(self):
        p = Plan.__new__(Plan)
        for k, v in self.__dict__.items():
            setattr(p, k, v.copy() if isinstance(v, np.ndarray) else v)
        return p


def run(bars, plan, cost, optimistic=False, fill_at_close=False, loss_standdown=None):
    """Run the default engine.  `cost` is a level dict from config/costs.lock.json.

    Returns (trades matrix, bar equity in points, in-position mask, liquidity misses)."""
    comm_pts = 2.0 * cost["commission_per_side_usd"] / bars.pv
    edge = bars.edge10 if cost.get("edge_extra_ticks", 0) else np.zeros(bars.n, np.bool_)
    return _simulate(bars.o, bars.h, bars.l, bars.c, bars.v, bars.first, bars.last, edge,
                     plan.sigL, plan.sigS, plan.etype, plan.epxL, plan.epxS, plan.valid_bars,
                     plan.stpL, plan.stpS, plan.tgtL, plan.tgtS, plan.exL, plan.exS,
                     bars.tick, float(cost["slippage_ticks_per_side"]), float(cost.get("edge_extra_ticks", 0)), comm_pts,
                     int(plan.time_stop_bars), float(plan.be_R), float(plan.trail_start_R), float(plan.trail_R),
                     float(plan.part_R), int(plan.cooldown_bars), int(plan.max_trades),
                     int(plan.loss_standdown if loss_standdown is None else loss_standdown),
                     bool(optimistic), float(cost.get("min_vol", 20.0)), bool(fill_at_close))


@njit(cache=True)
def _reversal(o, c, last, buy, sell, tick, slip_ticks, comm_pts, at_close, h, l):
    """Always-in-market reversal engine for the owner's baseline (reference only, Article 9 exempt).

    at_close=True  : PINE_PARITY, fills at the signal bar's close (process_orders_on_close=true).
    at_close=False : default timing, fills at the next bar's open, carrying overnight.
    The open position at the end is closed at the last price with costs (Article 8)."""
    n = len(c)
    T = np.zeros((n + 1, NCOL))
    eq = np.zeros(n)
    nt = 0
    pos = 0
    entry_px = 0.0
    entry_idx = 0
    sig_idx = 0
    mfe = 0.0
    mae = 0.0
    realized = 0.0
    slip = slip_ticks * tick
    pend = 0
    pend_sig = 0
    for t in range(n):
        want = 0
        wsig = t
        px = 0.0
        if not at_close and pend != 0:
            want = pend
            wsig = pend_sig
            px = o[t]
            pend = 0
        if want != 0 and want != pos:
            if pos != 0:
                xpx = px - pos * slip
                net = pos * (xpx - entry_px) - comm_pts
                T[nt, 0] = sig_idx; T[nt, 1] = entry_idx; T[nt, 2] = t; T[nt, 3] = pos
                T[nt, 4] = entry_px; T[nt, 5] = xpx; T[nt, 6] = np.nan; T[nt, 7] = np.nan; T[nt, 8] = 6
                T[nt, 9] = mae; T[nt, 10] = mfe; T[nt, 11] = net + comm_pts + 2 * slip; T[nt, 12] = 2 * slip
                T[nt, 13] = net; T[nt, 15] = t - entry_idx; T[nt, 17] = 1.0 if net > tick else 0.0
                nt += 1
                realized += net
            pos = want
            entry_px = px + want * slip
            entry_idx = t
            sig_idx = wsig
            mfe = 0.0
            mae = 0.0
        if pos == 1:
            mfe = max(mfe, h[t] - entry_px); mae = max(mae, entry_px - l[t])
        elif pos == -1:
            mfe = max(mfe, entry_px - l[t]); mae = max(mae, h[t] - entry_px)
        s = 1 if buy[t] else (-1 if sell[t] else 0)
        if s != 0 and s != pos:
            if at_close:
                if pos != 0:
                    xpx = c[t] - pos * slip
                    net = pos * (xpx - entry_px) - comm_pts
                    T[nt, 0] = sig_idx; T[nt, 1] = entry_idx; T[nt, 2] = t; T[nt, 3] = pos
                    T[nt, 4] = entry_px; T[nt, 5] = xpx; T[nt, 6] = np.nan; T[nt, 7] = np.nan; T[nt, 8] = 6
                    T[nt, 9] = mae; T[nt, 10] = mfe; T[nt, 11] = net + comm_pts + 2 * slip; T[nt, 12] = 2 * slip
                    T[nt, 13] = net; T[nt, 15] = t - entry_idx; T[nt, 17] = 1.0 if net > tick else 0.0
                    nt += 1
                    realized += net
                pos = s
                entry_px = c[t] + s * slip
                entry_idx = t
                sig_idx = t
                mfe = 0.0
                mae = 0.0
            else:
                pend = s
                pend_sig = t
        eq[t] = realized + (pos * (c[t] - entry_px) if pos != 0 else 0.0)
    if pos != 0:
        t = n - 1
        xpx = c[t] - pos * slip
        net = pos * (xpx - entry_px) - comm_pts
        T[nt, 0] = sig_idx; T[nt, 1] = entry_idx; T[nt, 2] = t; T[nt, 3] = pos
        T[nt, 4] = entry_px; T[nt, 5] = xpx; T[nt, 6] = np.nan; T[nt, 7] = np.nan; T[nt, 8] = 5
        T[nt, 9] = mae; T[nt, 10] = mfe; T[nt, 11] = net + comm_pts + 2 * slip; T[nt, 12] = 2 * slip
        T[nt, 13] = net; T[nt, 15] = t - entry_idx; T[nt, 17] = 1.0 if net > tick else 0.0
        nt += 1
        eq[t] = realized + net
    return T[:nt], eq


def run_reversal(bars, buy, sell, cost, at_close):
    comm_pts = 2.0 * cost["commission_per_side_usd"] / bars.pv
    return _reversal(bars.o, bars.c, bars.last, buy, sell, bars.tick, float(cost["slippage_ticks_per_side"]),
                     comm_pts, bool(at_close), bars.h, bars.l)


# ---------------------------------------------------------------- stress switches (7.6)
def delay_entries(plan, bars, k):
    """Delay every entry by k bars inside the session (the order prices travel with the signal)."""
    p = plan.copy()
    for name in ("sigL", "sigS", "epxL", "epxS", "stpL", "stpS", "tgtL", "tgtS"):
        a = getattr(plan, name)
        b = np.zeros_like(a) if a.dtype == np.bool_ else np.full_like(a, np.nan)
        b[k:] = a[:-k]
        same = np.r_[np.zeros(k, np.bool_), bars.sess[k:] == bars.sess[:-k]]
        if a.dtype == np.bool_:
            b &= same
        else:
            b[~same] = np.nan
        setattr(p, name, b)
    return p


def delay_exits(plan, bars, k=1):
    p = plan.copy()
    for name in ("exL", "exS"):
        a = getattr(plan, name)
        b = np.zeros_like(a)
        b[k:] = a[:-k]
        b &= np.r_[np.zeros(k, np.bool_), bars.sess[k:] == bars.sess[:-k]]
        setattr(p, name, b)
    if p.time_stop_bars:
        p.time_stop_bars += k
    return p


def drop_entries(plan, rng, share=0.10):
    p = plan.copy()
    keep = rng.random(len(p.sigL)) >= share
    p.sigL = p.sigL & keep
    p.sigS = p.sigS & keep
    return p


def jitter_bars(bars, rng):
    """Independent +/- 1 tick noise on each bar's high and low, never crossing open or close."""
    import copy
    b = copy.copy(bars)
    jh = rng.integers(-1, 2, bars.n) * bars.tick
    jl = rng.integers(-1, 2, bars.n) * bars.tick
    b.h = np.maximum(bars.h + jh, np.maximum(bars.o, bars.c))
    b.l = np.minimum(bars.l + jl, np.minimum(bars.o, bars.c))
    return b
