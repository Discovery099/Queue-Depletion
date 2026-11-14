"""Metric definitions, implemented once (SPEC Appendix A.1, Article 17).

All money figures are net of commission and modelled slippage, for 1 contract.
A win is a net result greater than one tick's dollar value; everything else is a loss.
"""
import math

import numpy as np
import pandas as pd

from .sim import C, REASONS

RT_COST_USD = {"ES": 27.5, "YM": 12.5}  # base level: two commissions plus two ticks


def trades_frame(T, bars, generation=-1, fold_of_sess=None, regime_of_sess=None, entry_type="market"):
    """Trade record (SPEC A.2) from the simulator's trade matrix."""
    if len(T) == 0:
        obj = {"instrument", "entry_order_type", "exit_reason"}
        return pd.DataFrame({c: pd.Series(dtype="object" if c in obj else "bool" if c == "is_win" else "float64") for c in TRADE_COLUMNS})
    ei = T[:, C["entry_idx"]].astype(np.int64)
    xi = T[:, C["exit_idx"]].astype(np.int64)
    si = T[:, C["sig_idx"]].astype(np.int64)
    tick = bars.tick
    net_pts = T[:, C["net_pts"]]
    risk = T[:, C["risk_pts"]]
    tgt = T[:, C["tgt_init"]]
    d = T[:, C["dir"]]
    tdist = d * (tgt - T[:, C["entry_px"]])
    sess = bars.sess[ei]
    df = pd.DataFrame({
        "generation": generation,
        "instrument": bars.sym,
        "timeframe_min": bars.tf,
        "fold": -1 if fold_of_sess is None else fold_of_sess[sess],
        "regime_cell": -1 if regime_of_sess is None else regime_of_sess[sess],
        "direction": d.astype(np.int8),
        "entry_ts": bars.ts[ei] + 0,
        "entry_price": T[:, C["entry_px"]],
        "entry_order_type": entry_type,
        "initial_stop": T[:, C["stop_init"]],
        "initial_target": tgt,
        "stop_to_target_ratio": np.where(tdist > 0, risk / np.where(tdist > 0, tdist, 1.0), np.nan),
        "exit_ts": bars.ts[xi] + 0,
        "exit_price": T[:, C["exit_px"]],
        "exit_reason": [REASONS[int(r)] for r in T[:, C["reason"]]],
        "bars_held": T[:, C["bars_held"]].astype(np.int32),
        "minutes_held": (bars.mclose[xi] - bars.mopen[ei]).astype(np.int32),
        "partial_fills": T[:, C["partial"]].astype(np.int8),
        "mae_ticks": T[:, C["mae_pts"]] / tick,
        "mfe_ticks": T[:, C["mfe_pts"]] / tick,
        "mae_pct_of_stop": np.where(risk > 0, T[:, C["mae_pts"]] / np.where(risk > 0, risk, 1.0), np.nan),
        "gross_ticks": T[:, C["gross_pts"]] / tick,
        "cost_ticks": (T[:, C["gross_pts"]] - net_pts) / tick,
        "net_ticks": net_pts / tick,
        "net_usd": net_pts * bars.pv,
        "is_win": T[:, C["is_win"]].astype(np.bool_),
        "minutes_since_open": bars.mopen[ei].astype(np.int32),
        "session_date": bars.date[ei],
        "sess": sess,
        "sig_idx": si,
        "entry_idx": ei,
        "exit_idx": xi,
    })
    df.insert(0, "trade_id", np.arange(len(df)))
    return df


TRADE_COLUMNS = ["trade_id", "generation", "instrument", "timeframe_min", "fold", "regime_cell", "direction",
                 "entry_ts", "entry_price", "entry_order_type", "initial_stop", "initial_target",
                 "stop_to_target_ratio", "exit_ts", "exit_price", "exit_reason", "bars_held", "minutes_held",
                 "partial_fills", "mae_ticks", "mfe_ticks", "mae_pct_of_stop", "gross_ticks", "cost_ticks",
                 "net_ticks", "net_usd", "is_win", "minutes_since_open", "session_date", "sess", "sig_idx",
                 "entry_idx", "exit_idx"]


def wilson(k, n, z=1.959964):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    den = 1 + z * z / n
    mid = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (mid - half, mid + half)


def loss_streak_p99(n, q):
    """99th percentile of the longest run of losses in n independent trades with loss probability q."""
    if n <= 0 or q <= 0:
        return 0.0
    if q >= 1:
        return float(n)
    # P(longest < k) ~ exp(-n (1-q) q^k)  ->  solve for the 0.99 quantile
    x = -math.log(0.99) / (n * (1 - q))
    return max(1.0, math.log(x) / math.log(q))


def basic(net, tick_value):
    """Core figures from an array of net dollar results. `tick_value` scalar or array."""
    n = len(net)
    if n == 0:
        return {"n": 0, "win_rate": 0.0, "profit_factor": 0.0, "payoff": 0.0, "expectancy_usd": 0.0,
                "net_usd": 0.0, "avg_win": 0.0, "avg_loss": 0.0, "largest_loss": 0.0}
    win = net > tick_value
    gp = float(net[win].sum())
    gl = float(-net[~win].sum())
    nw = int(win.sum())
    aw = gp / nw if nw else 0.0
    al = gl / (n - nw) if n > nw else 0.0
    return {"n": n, "wins": nw, "win_rate": nw / n,
            "profit_factor": (gp / gl) if gl > 0 else (99.0 if gp > 0 else 0.0),
            "payoff": (aw / al) if al > 0 else (99.0 if aw > 0 else 0.0),
            "expectancy_usd": float(net.mean()), "net_usd": float(net.sum()),
            "avg_win": aw, "avg_loss": al, "gross_profit": gp, "gross_loss": gl,
            "largest_loss": float(max(0.0, -net.min()))}


def daily_series(trades, sess_ids):
    """Net dollars per session over the given session ids (zeros where no trade closed)."""
    s = pd.Series(0.0, index=np.asarray(sess_ids))
    if len(trades):
        g = trades.groupby("sess")["net_usd"].sum()
        g = g[g.index.isin(s.index)]
        s.loc[g.index] = g.values
    return s


def sharpe(daily):
    sd = daily.std(ddof=1)
    return float(daily.mean() / sd * math.sqrt(252)) if sd > 0 else 0.0


def drawdown(eq):
    """Maximum drawdown and longest underwater stretch of a cumulative net series."""
    if len(eq) == 0:
        return 0.0, 0
    peak = np.maximum.accumulate(np.maximum(eq, 0.0))
    dd = peak - eq
    under = dd > 0
    longest = cur = 0
    for u in under:
        cur = cur + 1 if u else 0
        longest = max(longest, cur)
    return float(dd.max()), int(longest)


def evaluate(trades, sess_ids, tick_value_by_inst, rt_cost=RT_COST_USD, bars_per_session=None):
    """Full metric block for a trade set over `sess_ids` (the sessions of the slice, per instrument).

    Pooled results put both instruments' trades, in dollars per contract, in one list."""
    m = {}
    n_sess = len(sess_ids)
    if len(trades) == 0:
        m.update(basic(np.array([]), 1.0))
        m.update({"sessions": n_sess, "trades_per_year": 0.0, "session_share": 0.0, "max_gap_sessions": n_sess,
                  "wilson_lo": 0.0, "wilson_hi": 0.0, "expectancy_costs": 0.0, "expectancy_ticks": 0.0})
        return m
    net = trades["net_usd"].values
    tv = trades["instrument"].map(tick_value_by_inst).values.astype(float)
    rc = trades["instrument"].map(rt_cost).values.astype(float)
    m.update(basic(net, tv))
    n = m["n"]
    lo, hi = wilson(m["wins"], n)
    m["wilson_lo"], m["wilson_hi"] = lo, hi
    n_inst = trades["instrument"].nunique()
    m["sessions"] = n_sess
    m["trades_per_year"] = n / (n_sess * n_inst) * 252 if n_sess else 0.0   # per instrument
    per_inst_share = []
    max_gap = 0
    for inst, g in trades.groupby("instrument"):
        traded = np.isin(np.asarray(sess_ids), g["sess"].unique())
        per_inst_share.append(traded.mean())
        gap = cur = 0
        for x in traded:
            cur = 0 if x else cur + 1
            gap = max(gap, cur)
        max_gap = max(max_gap, gap)
    m["session_share"] = float(min(per_inst_share))
    m["max_gap_sessions"] = int(max_gap)
    m["expectancy_ticks"] = float((trades["net_ticks"]).mean())
    m["expectancy_costs"] = float((net / rc).mean())
    aw = m["avg_win"]
    m["largest_loss_in_avg_wins"] = (m["largest_loss"] / aw) if aw > 0 else 99.0
    # tail share: losses of the worst 5% of trades as a share of gross profit
    k = max(1, int(math.ceil(0.05 * n)))
    worst = np.sort(net)[:k]
    m["tail_share"] = float(-worst[worst < 0].sum() / m["gross_profit"]) if m.get("gross_profit", 0) > 0 else 99.0
    r = net / rc
    sd = r.std()
    m["skew"] = float(((r - r.mean()) ** 3).mean() / sd ** 3) if sd > 0 else 0.0
    m["kurt"] = float(((r - r.mean()) ** 4).mean() / sd ** 4) if sd > 0 else 3.0
    # longest losing streak versus the independent-trades expectation
    win = trades["is_win"].values
    order = np.lexsort((trades["entry_ts"].values, trades["instrument"].values))
    streak = cur = 0
    prev_inst = None
    inst = trades["instrument"].values
    for i in order:
        if inst[i] != prev_inst:
            cur = 0
            prev_inst = inst[i]
        cur = 0 if win[i] else cur + 1
        streak = max(streak, cur)
    m["loss_streak"] = int(streak)
    m["loss_streak_p99"] = loss_streak_p99(n / n_inst, 1 - m["win_rate"])
    w = trades[trades["is_win"]]
    lz = trades[~trades["is_win"]]
    m["mae_winner_median_pct_stop"] = float(w["mae_pct_of_stop"].median()) if len(w) else 0.0
    m["scratch_share"] = float((trades["net_ticks"].abs() <= 2).mean())
    mw = float(w["minutes_held"].median()) if len(w) else 0.0
    ml = float(lz["minutes_held"].median()) if len(lz) else 0.0
    m["median_minutes_win"], m["median_minutes_loss"] = mw, ml
    m["time_asymmetry"] = (ml / mw) if mw > 0 else (99.0 if ml > 0 else 0.0)
    tot = m["net_usd"]
    sp = float(trades.loc[trades["exit_reason"] == "session", "net_usd"].sum())
    m["session_exit_profit_share"] = (sp / tot) if tot > 0 else 0.0
    m["same_bar_share"] = float((trades["bars_held"] == 0).mean())
    m["median_minutes_held"] = float(trades["minutes_held"].median())
    m["long_share"] = float((trades["direction"] > 0).mean())
    m["reasons"] = trades["exit_reason"].value_counts().to_dict()
    d = daily_series(trades, sess_ids)
    m["sharpe"] = sharpe(d)
    dd, uw = drawdown(d.cumsum().values)
    m["max_dd_daily_usd"], m["underwater_sessions"] = dd, uw
    m["dd_ratio"] = (dd / tot) if tot > 0 else 99.0
    return m


def rolling_window_share(trades, sess_ids, window_sessions):
    """Share of rolling windows (step: one fifth of the window) with positive net profit."""
    d = daily_series(trades, sess_ids).values
    n = len(d)
    if n < window_sessions:
        return 0.0, 0
    step = max(1, window_sessions // 5)
    cs = np.r_[0.0, d.cumsum()]
    starts = np.arange(0, n - window_sessions + 1, step)
    prof = (cs[starts + window_sessions] - cs[starts]) > 0
    return float(prof.mean()), int(len(starts))
