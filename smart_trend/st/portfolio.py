"""Enhancement 13 + portfolio risk: correlation guard, portfolio daily loss stop, equity metrics.

Works on per-symbol trade lists produced by the engine. Trades are processed in entry-time
order; a trade is rejected if
  * the correlation group already has `max_per_group` open positions at its entry time, or
  * the portfolio's realized loss for that day has already reached `daily_stop_usd`.
"""
import numpy as np
import pandas as pd

from .specs import SPECS


def combine(trades: dict, max_per_group=None, daily_stop_usd=None):
    T = pd.concat(trades.values(), ignore_index=True).sort_values(["entry_time", "symbol"])
    T["group"] = T.symbol.map(lambda s: SPECS[s]["group"])
    kept = []
    open_pos = []            # (exit_time, group)
    day_realized = {}        # date -> realized pnl of kept trades that have exited
    exits_by_day = []        # (exit_time, pnl, date)
    for r in T.itertuples():
        t = r.entry_time
        open_pos = [(e, g) for e, g in open_pos if e > t]
        if max_per_group is not None and sum(1 for _, g in open_pos if g == r.group) >= max_per_group:
            continue
        if daily_stop_usd is not None:
            d = t.date()
            realized = sum(p for e, p, dd in exits_by_day if dd == d and e <= t)
            if realized <= -daily_stop_usd:
                continue
        kept.append(r.Index)
        open_pos.append((r.exit_time, r.group))
        exits_by_day.append((r.exit_time, r.pnl, r.exit_time.date()))
    return T.loc[kept].sort_values("exit_time")


def equity_metrics(T, start=None, end=None):
    if start is not None:
        T = T[T.entry_time >= pd.Timestamp(start, tz="America/New_York")]
    if end is not None:
        T = T[T.entry_time < pd.Timestamp(end, tz="America/New_York")]
    T = T.sort_values("exit_time")
    p = T.pnl.to_numpy()
    eq = np.cumsum(p)
    dd = float(min(0.0, (eq - np.maximum.accumulate(np.maximum(eq, 0))).min())) if len(p) else 0.0
    day = T.groupby(T.exit_time.dt.date).pnl.sum()
    mon = T.groupby([T.exit_time.dt.year, T.exit_time.dt.month]).pnl.sum()
    gw, gl = p[p > 0].sum(), -p[p < 0].sum()
    return dict(trades=len(p), net=float(p.sum()), pf=float(gw / gl) if gl > 0 else np.inf,
                wr=float((p > 0).mean() * 100) if len(p) else np.nan, max_dd=dd,
                ret_dd=float(p.sum() / -dd) if dd < 0 else np.inf,
                worst_day=float(day.min()) if len(day) else 0.0,
                best_day=float(day.max()) if len(day) else 0.0,
                pos_days=float((day > 0).mean() * 100) if len(day) else np.nan,
                pos_months=float((mon > 0).mean() * 100) if len(mon) else np.nan,
                sharpe=float(day.mean() / day.std() * np.sqrt(252)) if day.std() > 0 else np.nan)
