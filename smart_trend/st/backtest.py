"""Glue: data + signals + filters + engine -> trades DataFrame and metrics."""
import numpy as np
import pandas as pd

from . import data as dmod
from . import engine as eng
from . import filters as flt
from . import signals as sig
from .specs import SPECS, COMMISSION_RT, SLIPPAGE_TICKS


class Market:
    """Caches bars, signals and features for one symbol and one signal configuration."""

    def __init__(self, symbol, sig_kw=None, bars=None):
        self.symbol = symbol
        self.b = bars if bars is not None else dmod.load(symbol)
        self.spec = SPECS[symbol]
        self.sig_kw = sig_kw or {}
        self.s = sig.build(self.b, **self.sig_kw)
        self.f = flt.features(self.b, self.s)
        self.htf = {}

    def run(self, filt=None, flatten_last_bar=True, **eng_kw):
        b, s = self.b, self.s
        kw = dict(tick=self.spec["tick"], pv=self.spec["pv"], comm_rt=COMMISSION_RT,
                  slip_ticks=SLIPPAGE_TICKS)
        kw.update(eng_kw)
        P = eng.make_params(**kw)
        al, ash = flt.allow_masks(b, s, self.f, filt or {}, self.htf)
        force = s["roll"].copy()
        if flatten_last_bar:
            force |= b.last_bar
        block = b.last_bar.copy()
        r = eng.run(b.o, b.h, b.l, b.c, s["atr"], s["trail"], s["regime"].astype(np.int64),
                    s["match_buy"], s["match_sell"], al, ash, force, block, b.day_id,
                    self.f["er"], P)
        return trades_frame(self, r)


def trades_frame(m, r):
    ent, ex, d, epx, xpx, qty, pnl, mfe, mae, reason, risk, atr, sigi = r
    b = m.b
    t = pd.DataFrame(dict(entry_i=ent, exit_i=ex, sig_i=sigi, dir=d, entry_px=epx, exit_px=xpx,
                          qty=qty, pnl=pnl, mfe=mfe, mae=mae, reason=reason, risk=risk, atr=atr))
    t["symbol"] = m.symbol
    t["entry_time"] = b.ts_series.iloc[ent].to_numpy()
    t["exit_time"] = b.ts_series.iloc[ex].to_numpy()
    t["bars"] = ex - ent
    t["reason_name"] = t.reason.map(eng.REASON_NAMES)
    pv = m.spec["pv"]
    t["R"] = t.pnl / (t.risk * pv * t.qty)
    return t


def metrics(t, start=None, end=None):
    if start is not None:
        t = t[t.entry_time >= pd.Timestamp(start, tz="America/New_York")]
    if end is not None:
        t = t[t.entry_time < pd.Timestamp(end, tz="America/New_York")]
    if len(t) == 0:
        return dict(trades=0, net=0.0, pf=np.nan, wr=np.nan, max_dd=0.0, ret_dd=np.nan,
                    avg_win=np.nan, avg_loss=np.nan, worst_trade=0.0, worst_day=0.0,
                    pos_months=np.nan, sharpe=np.nan, avg_R=np.nan)
    p = t.pnl.to_numpy()
    eq = np.cumsum(p)
    dd = float(min(0.0, (eq - np.maximum.accumulate(np.maximum(eq, 0))).min()))
    gw = p[p > 0].sum()
    gl = -p[p < 0].sum()
    day = t.groupby(t.exit_time.dt.date).pnl.sum()
    mon = t.groupby(t.exit_time.dt.to_period("M")).pnl.sum()
    sharpe = day.mean() / day.std() * np.sqrt(252) if day.std() > 0 else np.nan
    return dict(trades=len(t), net=float(p.sum()), pf=float(gw / gl) if gl > 0 else np.inf,
                wr=float((p > 0).mean() * 100), max_dd=dd,
                ret_dd=float(p.sum() / -dd) if dd < 0 else np.inf,
                avg_win=float(p[p > 0].mean()) if (p > 0).any() else 0.0,
                avg_loss=float(p[p < 0].mean()) if (p < 0).any() else 0.0,
                worst_trade=float(p.min()), worst_day=float(day.min()),
                pos_months=float((mon > 0).mean() * 100), sharpe=float(sharpe),
                avg_R=float(t.R.mean()))


def fmt(mdict):
    m = mdict
    return (f"n={m['trades']:5d} net={m['net']:10.0f} PF={m['pf']:5.2f} WR={m['wr']:5.1f}% "
            f"DD={m['max_dd']:9.0f} ret/DD={m['ret_dd']:6.2f} worstDay={m['worst_day']:8.0f} "
            f"worstTrade={m['worst_trade']:8.0f} +mo={m['pos_months']:5.1f}% Sh={m['sharpe']:5.2f}")
