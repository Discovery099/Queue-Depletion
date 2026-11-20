"""Independent per-signal trade simulator (triple barrier) used for research grids and for
meta-label targets. Each signal is simulated on its own (no position interaction)."""
import numpy as np
from numba import njit


@njit(cache=True)
def simulate(idx, dirs, o, h, l, c, atr, trail, regime, day_last, tick, slip_ticks,
             stop_atr, target_atr, max_bars, entry_limit_atr, limit_wait, trail_exit,
             be_trigger_atr, chand_atr, tt_ticks):
    """Returns gross P&L in price units per signal (nan = no fill) and holding bars.
    entry_limit_atr > 0 -> limit entry at signal close - dir*x*ATR, valid limit_wait bars.
    trail_exit 1 -> exit next open if Smart Trend regime flips against the trade.
    be_trigger_atr > 0 -> once MFE >= trigger, stop moves to entry.
    chand_atr > 0 -> chandelier trailing stop k*ATR from the best price (activated after BE trigger
    if be_trigger_atr > 0, otherwise from entry)."""
    ns = idx.size
    out = np.full(ns, np.nan)
    hold = np.zeros(ns, np.int64)
    slip = slip_ticks * tick
    tt = tt_ticks * tick
    for k in range(ns):
        i = idx[k]
        d = dirs[k]
        a = atr[i]
        last = day_last[i]
        if i + 1 > last:
            continue
        # entry
        j = i + 1
        if entry_limit_atr > 0:
            lp = c[i] - d * entry_limit_atr * a
            lp = np.round(lp / tick) * tick
            filled = -1
            for jj in range(i + 1, min(i + 1 + limit_wait, last + 1)):
                if (d == 1 and l[jj] < lp - tt + 1e-12 + 0 * tick) or (d == -1 and h[jj] > lp + tt - 1e-12):
                    filled = jj
                    break
            if filled < 0:
                continue
            j = filled
            epx = min(o[j], lp) if d == 1 else max(o[j], lp)
        else:
            epx = o[j] + d * slip
        stp = epx - d * stop_atr * a if stop_atr > 0 else np.nan
        tgt = epx + d * target_atr * a if target_atr > 0 else np.nan
        best = epx
        be_on = False
        exit_px = np.nan
        jj = j
        pend = False
        while True:
            if pend:
                exit_px = o[jj] - d * slip
                break
            O = o[jj] * d; H = (h[jj] if d == 1 else l[jj]) * d; L = (l[jj] if d == 1 else h[jj]) * d
            S = stp * d if not np.isnan(stp) else np.nan
            T = tgt * d if not np.isnan(tgt) else np.nan
            upf = (h[jj] - o[jj]) <= (o[jj] - l[jj])
            if d == -1:
                upf = not upf
            done = False
            if not np.isnan(S) and O <= S:
                exit_px = (O - slip) * d; done = True
            elif not np.isnan(T) and O >= T + tt:
                exit_px = O * d; done = True
            else:
                for seg in range(2):
                    up = (seg == 0) == upf
                    if up:
                        if not np.isnan(T) and H >= T + tt:
                            exit_px = T * d; done = True; break
                    else:
                        if not np.isnan(S) and L <= S:
                            exit_px = (S - slip) * d; done = True; break
            if done:
                break
            # bar close updates
            if d == 1:
                best = max(best, h[jj])
            else:
                best = min(best, l[jj])
            mfe = (best - epx) * d
            if be_trigger_atr > 0 and not be_on and mfe >= be_trigger_atr * a:
                be_on = True
                if np.isnan(stp) or (stp - epx) * d < 0:
                    stp = epx
            if chand_atr > 0 and (be_on or be_trigger_atr <= 0):
                ch = best - d * chand_atr * atr[jj]
                if np.isnan(stp) or (ch - stp) * d > 0:
                    stp = ch
            if jj >= last:
                exit_px = c[jj] - d * slip
                break
            if max_bars > 0 and jj - j + 1 >= max_bars:
                pend = True
            if trail_exit == 1 and regime[jj] == -d:
                pend = True
            jj += 1
        out[k] = (exit_px - epx) * d
        hold[k] = jj - j
    return out, hold
