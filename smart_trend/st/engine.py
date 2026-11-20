"""Bar-by-bar execution engine with TradingView fill semantics.

TV rules reproduced:
  * signals are evaluated on the bar close; market orders fill at the NEXT bar open +/- slippage
  * strategy.exit(profit=ticks) is a limit relative to the actual fill price and can fill on the
    entry bar
  * intrabar path: if the open is closer to the high, price goes open->high->low->close,
    otherwise open->low->high->close
  * strategy.close_all(immediately=true) fills at the current bar close
  * a reversal (opposite entry while in a position) closes and re-opens at the next open

Every enhancement is a parameter; with the defaults the engine is the original script.
"""
import numpy as np
from numba import njit

PARAMS = dict(
    tick=0.25, pv=5.0, slip_ticks=1.0, comm_rt=2.5, qty=1.0,
    trade_through_ticks=0.0,     # 0 = TV touch fill for limit targets; 1 = price must trade 1 tick through
    use_target=1.0, target_atr=1.25, cap_cash=150.0,   # cap_cash<=0 -> no cap
    stop_atr=0.0,                # catastrophe / initial stop in ATR (0 = none, the original)
    inval_mode=0.0,              # 1 = exit next open when Smart Trend regime flips against us
                                 # 2 = stop order resting at the Smart Trail line
    inval_buffer_atr=0.0,        # extra buffer beyond the trail for mode 2
    ts_bars=0.0, ts_min_mfe_atr=0.0,  # failure-to-progress: after N bars, MFE < k*ATR -> exit
    max_bars=0.0,                # hard max holding time
    partial_frac=0.0, partial_r=1.0,  # scale out partial_frac at partial_r * initial risk
    be_offset_r=0.0,             # after the partial, stop -> entry + offset*R
    runner_mode=0.0,             # 0 = runner rests on BE stop / other exits, 1 = trail on Smart Trail,
                                 # 2 = chandelier (highest high - k*ATR)
    runner_atr=3.0, runner_target_r=0.0,
    adaptive_er=0.0,             # >0: use partial/runner only if ER at entry >= this, else plain target
    dll_usd=0.0,                 # daily loss limit per symbol (realized + open), 0 = off
    max_losses_day=0.0,          # stop for the day after N losing trades
    risk_usd=0.0, max_qty=50.0,  # risk-based sizing: qty = floor(risk_usd / (stop distance * pv))
    opp_mode=1.0,                # 1 = reverse on opposite agreement (original), 2 = exit only, 0 = ignore
)
PIDX = {k: i for i, k in enumerate(PARAMS)}

# exit reasons
R_TARGET, R_STOP, R_REVERSE, R_SESSION, R_INVAL, R_TIME, R_BE, R_RUNNER, R_DLL, R_OPP = range(1, 11)
REASON_NAMES = {1: "target", 2: "stop", 3: "reverse", 4: "session/roll", 5: "invalidation",
                6: "time stop", 7: "breakeven/runner stop", 8: "runner trail", 9: "daily limit",
                10: "opposite exit"}


def make_params(**kw):
    p = dict(PARAMS)
    for k, v in kw.items():
        if k not in p:
            raise KeyError(k)
        p[k] = v
    return np.array([float(p[k]) for k in PARAMS], dtype=np.float64)


@njit(cache=True)
def _rt(x, tick):
    return np.round(x / tick) * tick


@njit(cache=True)
def run(o, h, l, c, atr, trail, regime, mbuy, msell, allow_long, allow_short, force_exit,
        block_entry, day_id, er, P):
    tick = P[0]; pv = P[1]; slip = P[2] * tick; comm = P[3]; qty0 = P[4]
    tt = P[5] * tick
    use_target = P[6] > 0; target_atr = P[7]; cap_cash = P[8]
    stop_atr = P[9]; inval_mode = int(P[10]); inval_buf = P[11]
    ts_bars = int(P[12]); ts_min = P[13]; max_bars = int(P[14])
    pfrac = P[15]; pr = P[16]; be_off = P[17]; runner_mode = int(P[18]); runner_atr = P[19]
    runner_tr = P[20]; adaptive_er = P[21]; dll = P[22]; max_losses = int(P[23])
    risk_usd = P[24]; max_qty = P[25]; opp_mode = int(P[26])

    n = c.size
    cap = n // 2 + 10
    t_ent = np.zeros(cap, np.int64); t_exit = np.zeros(cap, np.int64)
    t_dir = np.zeros(cap, np.int64); t_epx = np.zeros(cap); t_xpx = np.zeros(cap)
    t_qty = np.zeros(cap); t_pnl = np.zeros(cap); t_mfe = np.zeros(cap); t_mae = np.zeros(cap)
    t_reason = np.zeros(cap, np.int64); t_risk = np.zeros(cap); t_atr = np.zeros(cap)
    t_sig = np.zeros(cap, np.int64)
    nt = 0

    pos = 0            # +1 / -1 / 0
    q = 0.0            # open quantity
    qi = 0.0           # initial quantity
    epx = 0.0
    realized = 0.0     # realized $ of the current trade (partials)
    ent_i = -1
    sig_i = -1
    tgt = np.nan; stp = np.nan; ptgt = np.nan
    risk = 0.0         # initial risk distance (price)
    e_atr = 0.0
    part_done = False
    use_runner = False
    mfe = 0.0; mae = 0.0
    hh = 0.0; ll = 0.0

    pend_dir = 0       # pending entry direction for next open
    pend_atr = 0.0
    pend_sig = -1
    pend_exit = 0      # pending exit reason for next open

    cur_day = -1
    day_pnl = 0.0
    day_losses = 0
    day_block = False

    for i in range(n):
        if day_id[i] != cur_day:
            cur_day = day_id[i]
            day_pnl = 0.0
            day_losses = 0
            day_block = False

        # ---------------------------------------------------------------- 1. orders at the open
        if pend_dir != 0 or pend_exit != 0:
            if pos != 0 and (pend_exit != 0 or pend_dir == -pos):
                px = o[i] - slip if pos == 1 else o[i] + slip
                pnl = realized + (px - epx) * pos * pv * q - comm * qi
                t_ent[nt] = ent_i; t_exit[nt] = i; t_dir[nt] = pos; t_epx[nt] = epx; t_xpx[nt] = px
                t_qty[nt] = qi; t_pnl[nt] = pnl; t_mfe[nt] = mfe; t_mae[nt] = mae
                t_reason[nt] = pend_exit if pend_exit != 0 else R_REVERSE
                t_risk[nt] = risk; t_atr[nt] = e_atr; t_sig[nt] = sig_i; nt += 1
                day_pnl += pnl
                if pnl < 0:
                    day_losses += 1
                pos = 0; q = 0.0
            if pend_dir != 0 and pos == 0:
                pos = pend_dir
                epx = o[i] + slip if pos == 1 else o[i] - slip
                e_atr = pend_atr
                # target distance: min(ATR multiple, cash cap) in ticks, as in the script
                tdist = 0.0
                if use_target:
                    atr_ticks = np.ceil(target_atr * e_atr / tick)
                    if cap_cash > 0:
                        cap_ticks = np.floor(cap_cash / (tick * pv * qty0))
                        tdist = max(1.0, min(cap_ticks, atr_ticks)) * tick
                    else:
                        tdist = max(1.0, atr_ticks) * tick
                risk = stop_atr * e_atr if stop_atr > 0 else e_atr   # 1 ATR reference if no stop
                if risk_usd > 0 and stop_atr > 0:
                    qi = np.floor(risk_usd / (risk * pv))
                    qi = min(max(qi, 1.0), max_qty)
                else:
                    qi = qty0
                q = qi
                realized = 0.0
                use_runner = pfrac > 0 and (adaptive_er <= 0 or (not np.isnan(er[pend_sig]) and er[pend_sig] >= adaptive_er))
                if use_runner:
                    ptgt = _rt(epx + pos * pr * risk, tick)
                    tgt = _rt(epx + pos * runner_tr * risk, tick) if runner_tr > 0 else np.nan
                else:
                    ptgt = np.nan
                    tgt = epx + pos * tdist if use_target else np.nan
                stp = _rt(epx - pos * stop_atr * e_atr, tick) if stop_atr > 0 else np.nan
                part_done = False
                ent_i = i; sig_i = pend_sig
                mfe = 0.0; mae = 0.0
                hh = h[i]; ll = l[i]
            pend_dir = 0; pend_exit = 0

        # ---------------------------------------------------------------- 2. resting orders intrabar
        if pos != 0:
            # effective stop
            s = stp
            if inval_mode == 2 and i > ent_i and not np.isnan(trail[i - 1]):
                ts_ = trail[i - 1] - pos * inval_buf * e_atr
                if np.isnan(s) or (pos == 1 and ts_ > s) or (pos == -1 and ts_ < s):
                    s = ts_
            # transform to long-space: x' = pos*x  (so "high" is favourable)
            if pos == 1:
                O = o[i]; H = h[i]; L = l[i]
            else:
                O = -o[i]; H = -l[i]; L = -h[i]
            S = pos * s if not np.isnan(s) else np.nan
            T = pos * tgt if not np.isnan(tgt) else np.nan
            PT = pos * ptgt if (not np.isnan(ptgt) and not part_done) else np.nan
            up_first = (h[i] - o[i]) <= (o[i] - l[i])
            if pos == -1:
                up_first = not up_first
            exit_px = np.nan
            reason = 0
            # gap at the open
            if not np.isnan(S) and O <= S:
                exit_px = O - slip; reason = R_STOP if not part_done else R_BE
            elif not np.isnan(T) and O >= T + tt:
                exit_px = O; reason = R_TARGET
            else:
                for seg in range(2):
                    going_up = (seg == 0) == up_first
                    if going_up:
                        if not np.isnan(PT) and H >= PT + tt:
                            # partial fill
                            # whole contracts only (as in Pine); with 1 lot there is no scale-out,
                            # but the break-even / runner management still activates
                            qp = np.floor(qi * pfrac)
                            # long-space distance PT - pos*epx equals the real favourable distance
                            realized += (PT - pos * epx) * pv * qp
                            q -= qp
                            part_done = True
                            PT = np.nan
                        if not np.isnan(T) and H >= T + tt:
                            exit_px = T; reason = R_TARGET
                            break
                    else:
                        if not np.isnan(S) and L <= S:
                            exit_px = S - slip; reason = R_STOP if not part_done else R_BE
                            if inval_mode == 2 and (np.isnan(stp) or S > pos * stp):
                                reason = R_INVAL
                            break
            if reason != 0:
                px = exit_px * pos   # back to real prices
                pnl = realized + (px - epx) * pos * pv * q - comm * qi
                # excursions before closing
                fav = H - pos * epx
                adv = L - pos * epx
                mfe = max(mfe, fav); mae = min(mae, adv)
                t_ent[nt] = ent_i; t_exit[nt] = i; t_dir[nt] = pos; t_epx[nt] = epx; t_xpx[nt] = px
                t_qty[nt] = qi; t_pnl[nt] = pnl; t_mfe[nt] = mfe; t_mae[nt] = mae
                t_reason[nt] = reason; t_risk[nt] = risk; t_atr[nt] = e_atr; t_sig[nt] = sig_i; nt += 1
                day_pnl += pnl
                if pnl < 0:
                    day_losses += 1
                pos = 0; q = 0.0

        # ---------------------------------------------------------------- 3. bar close decisions
        if pos != 0:
            fav = (h[i] - epx) if pos == 1 else (epx - l[i])
            adv = (l[i] - epx) if pos == 1 else (epx - h[i])
            mfe = max(mfe, fav); mae = min(mae, adv)
            hh = max(hh, h[i]); ll = min(ll, l[i])
            close_now = 0
            if force_exit[i]:
                close_now = R_SESSION
            elif dll > 0 and day_pnl + realized + (c[i] - epx) * pos * pv * q - comm * qi <= -dll:
                close_now = R_DLL
            if close_now != 0:
                px = c[i] - slip if pos == 1 else c[i] + slip
                pnl = realized + (px - epx) * pos * pv * q - comm * qi
                t_ent[nt] = ent_i; t_exit[nt] = i; t_dir[nt] = pos; t_epx[nt] = epx; t_xpx[nt] = px
                t_qty[nt] = qi; t_pnl[nt] = pnl; t_mfe[nt] = mfe; t_mae[nt] = mae
                t_reason[nt] = close_now; t_risk[nt] = risk; t_atr[nt] = e_atr; t_sig[nt] = sig_i; nt += 1
                day_pnl += pnl
                if pnl < 0:
                    day_losses += 1
                pos = 0; q = 0.0
            else:
                bars_in = i - ent_i + 1
                if inval_mode == 1 and regime[i] == -pos:
                    pend_exit = R_INVAL
                elif ts_bars > 0 and bars_in >= ts_bars and mfe < ts_min * e_atr and not part_done:
                    pend_exit = R_TIME
                elif max_bars > 0 and bars_in >= max_bars:
                    pend_exit = R_TIME
                # stop management for the runner (takes effect from the next bar)
                if part_done:
                    be = _rt(epx + pos * be_off * risk, tick)
                    if np.isnan(stp) or (pos == 1 and be > stp) or (pos == -1 and be < stp):
                        stp = be
                    if runner_mode == 1:
                        if regime[i] == -pos:
                            pend_exit = R_RUNNER
                        elif not np.isnan(trail[i]):
                            if (pos == 1 and trail[i] > stp) or (pos == -1 and trail[i] < stp):
                                stp = trail[i]
                    elif runner_mode == 2:
                        ch = hh - runner_atr * atr[i] if pos == 1 else ll + runner_atr * atr[i]
                        if (pos == 1 and ch > stp) or (pos == -1 and ch < stp):
                            stp = _rt(ch, tick)

        if dll > 0 and day_pnl <= -dll:
            day_block = True
        if max_losses > 0 and day_losses >= max_losses:
            day_block = True

        # entries
        permitted = (not block_entry[i]) and (not force_exit[i]) and (not day_block) and not np.isnan(atr[i])
        go_long = mbuy[i] and permitted and allow_long[i]
        go_short = msell[i] and permitted and allow_short[i]
        if go_long:
            if pos <= 0:
                if pos == -1 and opp_mode == 0:
                    pass
                elif pos == -1 and opp_mode == 2:
                    pend_exit = R_OPP
                else:
                    pend_dir = 1; pend_atr = atr[i]; pend_sig = i; pend_exit = 0
        elif go_short:
            if pos >= 0:
                if pos == 1 and opp_mode == 0:
                    pass
                elif pos == 1 and opp_mode == 2:
                    pend_exit = R_OPP
                else:
                    pend_dir = -1; pend_atr = atr[i]; pend_sig = i; pend_exit = 0
        elif pos != 0 and opp_mode == 2:
            # opposite agreement that was filtered out still counts as an exit signal
            if (pos == 1 and msell[i]) or (pos == -1 and mbuy[i]):
                if pend_exit == 0:
                    pend_exit = R_OPP

    return (t_ent[:nt], t_exit[:nt], t_dir[:nt], t_epx[:nt], t_xpx[:nt], t_qty[:nt], t_pnl[:nt],
            t_mfe[:nt], t_mae[:nt], t_reason[:nt], t_risk[:nt], t_atr[:nt], t_sig[:nt])
