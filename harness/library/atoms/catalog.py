"""Atom catalogue (SPEC 8.2, 8.3): every reusable technique, written once in the DSL.

All code here is an original re-implementation of a concept; no library script text is copied
(Article 22).  Each atom is defined for a trade direction `d` (+1 long, -1 short) through the
mirror helper `D`, so long and short rules are mirror images with shared parameters (SPEC 9.1).

Indicator lookbacks are bar counts: the same oscillator or average on any chart timeframe.
Session logic (opening range, time windows, time stops) is in clock minutes (SPEC 13.2).
Distances are multiples of ATR(14) of the trading timeframe or fractions of price.

`ev` is the evidence pattern used to count supporting scripts and collect citations:
(set of built-in calls that must all appear, optional keyword regex on the lower-cased source).
`hz` lists the hazards commonly found in those source scripts; every atom here is a hazard-free
re-implementation and is admitted only after it passes the truncation audit on its own.
"""
from types import SimpleNamespace

from genome.dsl import *  # noqa: F401,F403
from genome import dsl as X

A = atr(B(14))            # the distance unit everywhere
RNG = H - L
BODY = absx(C - O)

FAMILIES = {
    "trend": "trend continuation", "meanrev": "mean reversion to value", "sweep": "liquidity sweep and reversal",
    "volexp": "volatility expansion", "volcon": "volatility contraction", "open": "opening auction",
    "close": "closing auction", "exhaust": "exhaustion", "bofail": "breakout failure",
    "intermarket": "inter-market lead-lag", "season": "seasonality within the session",
}
ATOMS = {}


class D:
    """Mirror helper: write a rule for longs, get the short rule by reflection."""

    def __init__(s, d):
        s.d = d
        s.hi, s.lo = (H, L) if d > 0 else (L, H)                 # favourable / adverse bar extreme
        s.pdh, s.pdl = (PDH, PDL) if d > 0 else (PDL, PDH)       # resistance / support side
        s.shigh, s.slow = (SHIGH, SLOW) if d > 0 else (SLOW, SHIGH)
        s.ohi, s.olo = (OH, OL) if d > 0 else (OL, OH)

    def gt(s, a, b): return (w(a) > w(b)) if s.d > 0 else (w(a) < w(b))
    def lt(s, a, b): return (w(a) < w(b)) if s.d > 0 else (w(a) > w(b))
    def ge(s, a, b): return (w(a) >= w(b)) if s.d > 0 else (w(a) <= w(b))
    def le(s, a, b): return (w(a) <= w(b)) if s.d > 0 else (w(a) >= w(b))
    def up(s, a, b): return (w(a) + w(b)) if s.d > 0 else (w(a) - w(b))       # move a by b my way
    def dn(s, a, b): return (w(a) - w(b)) if s.d > 0 else (w(a) + w(b))       # move a by b against me
    def sg(s, x): return w(x) if s.d > 0 else -w(x)                           # signed quantity
    def osc(s, x): return w(x) if s.d > 0 else (100.0 - w(x))                 # mirrored 0..100 oscillator
    def xo(s, a, b): return crossover(a, b) if s.d > 0 else crossunder(a, b)
    def top(s, n): return highest(H, n) if s.d > 0 else lowest(L, n)          # favourable n-bar extreme
    def bot(s, n): return lowest(L, n) if s.d > 0 else highest(H, n)          # adverse n-bar extreme
    def orx(s, m): return frozen(SHIGH, m) if s.d > 0 else frozen(SLOW, m)    # opening-range resistance side
    def orn(s, m): return frozen(SLOW, m) if s.d > 0 else frozen(SHIGH, m)    # opening-range support side
    def wick_adv(s): return (minx(O, C) - L) if s.d > 0 else (H - maxx(O, C))  # rejection wick against me
    def wick_fav(s): return (H - maxx(O, C)) if s.d > 0 else (minx(O, C) - L)
    def pos(s): return s.sg(C - (SHIGH + SLOW) / 2.0) / (SHIGH - SLOW) + 0.5   # 1 = at my favourable extreme
    def swing_adv(s, r):                                                       # last confirmed adverse swing level
        x = L if s.d > 0 else H
        ext = lowest(L, B(2 * r + 1)) if s.d > 0 else highest(H, B(2 * r + 1))
        ev = s.le(shift(x, r), ext)
        return ev, valuewhen(ev, shift(x, r))
    def swing_fav(s, r):
        x = H if s.d > 0 else L
        ext = highest(H, B(2 * r + 1)) if s.d > 0 else lowest(L, B(2 * r + 1))
        ev = s.ge(shift(x, r), ext)
        return ev, valuewhen(ev, shift(x, r))


class Atom:
    def __init__(self, id, typ, fam, desc, params, fn, ev, hz=(), tw=0):
        self.id, self.typ, self.fam, self.desc, self.fn = id, typ, fam, desc, fn
        self.grid = {k: list(v[0]) for k, v in params.items()}
        self.default = {k: v[1] for k, v in params.items()}
        self.ev, self.hz, self.tw = ev, tuple(hz), tw
        for k, g in self.grid.items():
            assert len(g) <= 12 and self.default[k] in g, (id, k)

    def build(self, params=None):
        """Return {'long': E, 'short': E, 'lvl_long': E or None, 'lvl_short': E or None}."""
        p = SimpleNamespace(**{**self.default, **(params or {})})
        out = {}
        for name, d in (("long", 1), ("short", -1)):
            r = self.fn(p, D(d))
            cond, lvl = r if isinstance(r, tuple) else (r, None)
            out[name], out["lvl_" + name] = cond, lvl
        return out


def atom(id, typ, fam, desc, ev, hz=(), tw=0, **params):
    def deco(fn):
        assert id not in ATOMS, id
        ATOMS[id] = Atom(id, typ, fam, desc, params, fn, ev, hz, tw)
        return fn
    return deco


def G(*vals, d=None):
    """Parameter grid (at most 12 values) with its default."""
    return (list(vals), vals[len(vals) // 2] if d is None else d)


# shared building blocks ------------------------------------------------------------------------
def macd_lines(s):
    m = ema(C, B(12 * s)) - ema(C, B(26 * s))
    return m, ema(m, B(9 * s))


def dmi(n):
    up, dn = change(H), -change(L)
    pdm = where((up > dn) & (up > 0), up, 0.0)
    mdm = where((dn > up) & (dn > 0), dn, 0.0)
    trn = rma(TR, B(n))
    pdi, mdi = 100.0 * rma(pdm, B(n)) / trn, 100.0 * rma(mdm, B(n)) / trn
    adx = rma(100.0 * absx(pdi - mdi) / (pdi + mdi), B(n))
    return pdi, mdi, adx


def stoch_k(n):
    return sma(100.0 * (C - lowest(L, B(n))) / (highest(H, B(n)) - lowest(L, B(n))), B(3))


def cci(n):
    return (HLC3 - sma(HLC3, B(n))) / (0.015 * meandev(HLC3, B(n)))


def mfi(n):
    mf = HLC3 * V
    pos = rsum(where(change(HLC3) > 0, mf, 0.0), B(n))
    neg = rsum(where(change(HLC3) < 0, mf, 0.0), B(n))
    return 100.0 * pos / (pos + neg)


def cmo(n):
    up = rsum(maxx(change(C), 0.0), B(n))
    dn = rsum(maxx(-change(C), 0.0), B(n))
    return 100.0 * (up - dn) / (up + dn)


VW_SD = sqrt(scumsum(V * HLC3 * HLC3) / scumsum(V) - SVWAP * SVWAP)      # session VWAP deviation
O_VWAP = scumsum(OC * OV) / scumsum(OV)
SRANGE = SHIGH - SLOW
MTC = 390.0 - MSO                                                          # minutes until the regular close
SQUEEZE = lambda n, m: (2.0 * stdev(C, B(n))) < (m * atr(B(n)))           # noqa: E731

T, S_, LOC, FLT = "TRIGGER", "STATE", "LOCATION", "FILTER"
MAc = {"ta.ema"}

# =============================================================== STATE atoms (directional regime)
@atom("st_trail_regime", S_, "trend", "Trend regime from the owner's ATR trail: price holds above a ratcheting ATR buffer.",
      ({"ta.atr"}, r"trail"), n=G(7, 10, 14, 20, 28), f=G(2.0, 2.5, 3.0, 3.5, 4.0))
def _(p, d): return d.sg(trail(B(p.n), p.f)) > 0


@atom("st_supertrend", S_, "trend", "Supertrend direction: close above the ratcheting lower band.",
      ({"ta.supertrend"}, None), n=G(7, 10, 14, 20), m=G(2.0, 3.0, 4.0))
def _(p, d): return d.sg(supertrend(B(p.n), p.m)) > 0


@atom("st_ema_stack", S_, "trend", "Fast average above slow average.", ({"ta.ema"}, r"fast|slow"),
      f=G(8, 13, 21, 34), s=G(50, 89, 144, 200))
def _(p, d): return d.gt(ema(C, B(p.f)), ema(C, B(p.s)))


@atom("st_price_vs_ema", S_, "trend", "Close on the trend side of a moving average.", ({"ta.ema"}, r"close\s*[<>]"),
      n=G(20, 34, 50, 100, 200))
def _(p, d): return d.gt(C, ema(C, B(p.n)))


@atom("st_ema_slope", S_, "trend", "Moving average rising by more than a fraction of ATR over 5 bars.",
      ({"ta.ema", "ta.atr"}, r"slope|rising|falling"), n=G(20, 50, 100), k=G(0.0, 0.1, 0.25, 0.5))
def _(p, d): return d.sg(change(ema(C, B(p.n)), 5)) > p.k * A


@atom("st_hma_slope", S_, "trend", "Hull average pointing in the trade direction.", ({"ta.hma"}, None),
      n=G(16, 25, 36, 49, 64))
def _(p, d): return d.sg(change(hma(C, B(p.n)), 1)) > 0


@atom("st_htf_bar_dir", S_, "trend", "Last confirmed higher-timeframe bar closed in the trade direction.",
      ({"request.security"}, r"close\s*>\s*\w*open|htf"), hz=("SECURITY_LOOKAHEAD", "HTF_CLOSE_INTRABAR"), k=G(3, 4, 6, 12, d=4))
def _(p, d): return d.gt(htf("close", p.k), htf("open", p.k))


@atom("st_htf_ema", S_, "trend", "Higher-timeframe close on the trend side of its own average.",
      ({"request.security", "ta.ema"}, None), hz=("SECURITY_LOOKAHEAD", "HTF_CLOSE_INTRABAR"), k=G(3, 4, 6, 12, d=4), n=G(5, 10, 20))
def _(p, d): return d.gt(htf("close", p.k), htfema(p.k, p.n))


@atom("st_htf_momentum", S_, "trend", "Higher-timeframe close beyond its close several bars earlier.",
      ({"request.security"}, r"mom|roc|change"), hz=("SECURITY_LOOKAHEAD",), k=G(3, 4, 6, 12, d=4), j=G(2, 3, 5))
def _(p, d): return d.gt(htf("close", p.k), htfago(p.k, p.j))


@atom("st_adx_trend", S_, "trend", "ADX above a threshold with the directional index on the trade side.",
      ({"ta.dmi"}, None), n=G(10, 14, 20), thr=G(15, 20, 25, 30))
def _(p, d):
    pdi, mdi, adx = dmi(p.n)
    return (adx > p.thr) & d.gt(pdi, mdi)


@atom("st_donchian_mid", S_, "trend", "Close on the trade side of the channel midline.", ({"ta.highest", "ta.lowest"}, r"donchian|mid|basis"),
      n=G(20, 40, 55, 100))
def _(p, d): return d.gt(C, (highest(H, B(p.n)) + lowest(L, B(p.n))) / 2.0)


@atom("st_vwap_side", S_, "trend", "Close on the trade side of the running session VWAP.", ({"ta.vwap"}, None),
      hz=("SESSION_VALUE_LEAK",))
def _(p, d): return d.gt(C, SVWAP)


@atom("st_session_open_side", S_, "open", "Close on the trade side of the session's opening price.",
      (set(), r"session.*open|open.*session|daily open|day open"), hz=("SECURITY_LOOKAHEAD",))
def _(p, d): return d.gt(C, SOPEN)


@atom("st_prior_close_side", S_, "trend", "Close on the trade side of the prior session's close.",
      ({"request.security"}, r"prev\w*\s*(day)?\s*close|yesterday"), hz=("SECURITY_LOOKAHEAD", "HTF_CLOSE_INTRABAR"))
def _(p, d): return d.gt(C, PDC)


@atom("st_efficiency_trend", S_, "trend", "Kaufman efficiency ratio high and net move in the trade direction.",
      ({"math.sum", "math.abs"}, r"efficiency|kaufman|\ber\b"), n=G(10, 20, 40), thr=G(0.2, 0.3, 0.4, 0.5))
def _(p, d):
    er = absx(change(C, p.n)) / rsum(absx(change(C)), B(p.n))
    return (er > p.thr) & (d.sg(change(C, p.n)) > 0)


@atom("st_macd_side", S_, "trend", "MACD line on the trade side of its signal line.", ({"ta.macd"}, None), s=G(1, 2, 3, d=1))
def _(p, d):
    m, sig = macd_lines(p.s)
    return d.gt(m, sig)


@atom("st_swing_structure", S_, "trend", "Confirmed swing highs and lows both stepping in the trade direction.",
      ({"ta.pivothigh", "ta.pivotlow"}, r"higher high|hh|hl|structure"), hz=("PIVOT_UNCONFIRMED", "FUTURE_OFFSET"), r=G(2, 3, 5))
def _(p, d):
    e1, f = d.swing_fav(p.r)
    e2, a = d.swing_adv(p.r)
    return d.gt(f, valuewhen(e1, shift(f, 1))) & d.gt(a, valuewhen(e2, shift(a, 1)))


@atom("st_ichimoku_cloud", S_, "trend", "Close beyond both cloud spans, each plotted with its causal displacement.",
      ({"ta.highest", "ta.lowest"}, r"ichimoku|kijun|tenkan|senkou"), hz=("FUTURE_OFFSET",), s=G(1, 2, d=1))
def _(p, d):
    mid = lambda n: (highest(H, B(n)) + lowest(L, B(n))) / 2.0   # noqa: E731
    a = shift((mid(9 * p.s) + mid(26 * p.s)) / 2.0, 26 * p.s)
    b = shift(mid(52 * p.s), 26 * p.s)
    return d.gt(C, a) & d.gt(C, b)


@atom("st_opening_range_side", S_, "open", "Close beyond the completed opening range on the trade side.",
      (set(), r"opening range|\borb\b"), hz=("SESSION_VALUE_LEAK",), tw=1, m=G(15, 30, 60))
def _(p, d): return d.gt(C, d.orx(p.m))


@atom("st_session_range_position", S_, "trend", "Close in the favourable part of the session's range so far.",
      (set(), r"range position|position in range|%\s*of range"), thr=G(0.5, 0.6, 0.7, 0.8))
def _(p, d): return (d.pos() > p.thr) & (MSO >= 30)


@atom("st_rsi_regime", S_, "trend", "RSI holding on the trade side of its midline.", ({"ta.rsi"}, r"50"),
      n=G(14, 21, 30), band=G(0, 5, 10))
def _(p, d): return d.osc(rsi(C, B(p.n))) > 50.0 + p.band


@atom("st_gap_direction", S_, "open", "Session opened with a gap in the trade direction, as a fraction of price.",
      (set(), r"\bgap\b"), hz=("SECURITY_LOOKAHEAD",), g=G(0.0005, 0.001, 0.002, 0.004))
def _(p, d): return d.sg(SOPEN - PDC) / PDC > p.g


@atom("st_first_minutes_direction", S_, "open", "Net move of the opening window in the trade direction.",
      (set(), r"first\s*\d+\s*min|opening drive|initial balance"), tw=1, m=G(15, 30, 60), k=G(0.0, 0.5, 1.0))
def _(p, d): return d.sg(frozen(C, p.m) - SOPEN) > p.k * frozen(A, p.m)


@atom("st_late_session_trend", S_, "close", "During the final stretch, price has moved in the trade direction since the stretch began.",
      (set(), r"power hour|last hour|closing|moc\b|market on close"), tw=1, start=G(300, 315, 330, 345))
def _(p, d): return (MSO >= p.start) & (d.sg(C - frozen(C, p.start)) > 0)


@atom("st_first_half_hour_sign_late", S_, "season", "Intraday momentum: late in the session, trade with the sign of the first half hour's move from the prior close.",
      (set(), r"intraday momentum|first half|last half"), tw=1, start=G(300, 330, 345, 360, d=330))
def _(p, d): return (MSO >= p.start) & (d.sg(frozen(C, 30) - PDC) > 0)


@atom("st_other_instrument_trend", S_, "intermarket", "The companion index future is on the trade side of its own average.",
      ({"request.security", "ta.ema"}, r"\bes\b|\bym\b|\bnq\b|spx|correlat|intermarket"), n=G(20, 50, 100))
def _(p, d): return d.gt(OC, ema(OC, B(p.n)))


@atom("st_relative_strength", S_, "intermarket", "This instrument has outperformed the companion since the open.",
      ({"request.security"}, r"relative strength|outperform|ratio"), thr=G(0.0, 0.0005, 0.001))
def _(p, d): return d.sg(C / sfirst(C) - OC / sfirst(OC)) > p.thr


@atom("st_both_vwap_side", S_, "intermarket", "Both instruments on the trade side of their own session VWAP.",
      ({"request.security", "ta.vwap"}, None))
def _(p, d): return d.gt(C, SVWAP) & d.gt(OC, O_VWAP)


@atom("st_spread_zscore", S_, "intermarket", "The ratio to the companion is stretched against the trade direction (reversion bias).",
      ({"request.security", "ta.stdev"}, r"spread|pair|ratio|z-?score"), n=G(50, 100, 200), k=G(1.0, 1.5, 2.0))
def _(p, d):
    r = C / OC
    return d.sg((r - sma(r, B(p.n))) / stdev(r, B(p.n))) < -p.k


@atom("st_session_overextended", S_, "exhaust", "Session range already exceeds the prior session's and price sits at the adverse extreme (fade bias).",
      (set(), r"average daily range|\badr\b|exhaust"), thr=G(1.0, 1.25, 1.5))
def _(p, d): return (SRANGE / prevlast(SRANGE) > p.thr) & (d.pos() < 0.25)


# =============================================================== LOCATION atoms (with a level where one exists)
def near(lvl, k): return absx(C - lvl) < k * A


KN = G(0.5, 1.0, 1.5, 2.0)


@atom("loc_prior_day_extreme", LOC, "sweep", "Price near the prior session's low (for longs) or high (for shorts).",
      ({"request.security"}, r"pdh|pdl|prev\w*\s*day\s*(high|low)|yesterday"), hz=("SECURITY_LOOKAHEAD", "SESSION_VALUE_LEAK"), k=KN)
def _(p, d): return near(d.pdl, p.k), d.pdl


@atom("loc_prior_close", LOC, "meanrev", "Price near the prior session's close.", ({"request.security"}, r"prev\w*\s*close|pdc"),
      hz=("SECURITY_LOOKAHEAD", "HTF_CLOSE_INTRABAR"), k=KN)
def _(p, d): return near(PDC, p.k) & d.ge(C, PDC), PDC


@atom("loc_opening_range_extreme", LOC, "open", "Price near the supportive edge of the completed opening range.",
      (set(), r"opening range|\borb\b"), hz=("SESSION_VALUE_LEAK",), tw=1, m=G(15, 30, 60), k=KN)
def _(p, d): return near(d.orn(p.m), p.k), d.orn(p.m)


@atom("loc_confirmed_swing", LOC, "sweep", "Price near the last swing low (for longs), known only after its right-side bars.",
      ({"ta.pivotlow"}, None), hz=("PIVOT_UNCONFIRMED", "FUTURE_OFFSET"), r=G(2, 3, 5), k=KN)
def _(p, d):
    _e, lvl = d.swing_adv(p.r)
    return near(lvl, p.k), lvl


@atom("loc_session_extreme", LOC, "sweep", "Price near the session low so far (for longs).", (set(), r"session (high|low)|day (high|low)|hod|lod"),
      hz=("SESSION_VALUE_LEAK",), k=KN)
def _(p, d): return near(shift(d.slow, 1), p.k) & (MSO >= 30), shift(d.slow, 1)


@atom("loc_round_number", LOC, "sweep", "Price just on the trade side of a round-number level.", (set(), r"round number|psychological|whole number"),
      mult=G(1.0, 2.5, 5.0), k=KN)
def _(p, d):
    lvl = roundlvl(p.mult)
    return near(lvl, p.k) & d.ge(C, lvl), lvl


@atom("loc_unfilled_gap", LOC, "open", "Session gapped against the trade direction and the prior close has not been revisited.",
      (set(), r"gap fill|unfilled gap|fair value gap|fvg"), hz=("SECURITY_LOOKAHEAD",), g=G(0.001, 0.002, 0.003))
def _(p, d): return (d.sg(SOPEN - PDC) / PDC < -p.g) & d.lt(d.shigh, PDC), PDC


@atom("loc_vwap", LOC, "meanrev", "Price near session VWAP, on the trade side.", ({"ta.vwap"}, None), hz=("SESSION_VALUE_LEAK",), k=KN)
def _(p, d): return near(SVWAP, p.k) & d.ge(C, SVWAP), SVWAP


@atom("loc_vwap_band", LOC, "meanrev", "Price stretched beyond a VWAP deviation band against the trade direction.",
      ({"ta.vwap", "ta.stdev"}, r"band|dev"), hz=("SESSION_VALUE_LEAK",), k=G(1.0, 1.5, 2.0, 2.5))
def _(p, d): return (d.sg(C - SVWAP) < -p.k * VW_SD) & (MSO >= 30), SVWAP


@atom("loc_bollinger_outer", LOC, "meanrev", "Close beyond the outer Bollinger band against the trade direction.",
      ({"ta.sma", "ta.stdev"}, r"bollinger|\bbb\b"), n=G(20, 30, 50), k=G(1.5, 2.0, 2.5))
def _(p, d): return d.sg(C - sma(C, B(p.n))) < -p.k * stdev(C, B(p.n)), sma(C, B(p.n))


@atom("loc_keltner_outer", LOC, "meanrev", "Close beyond the outer Keltner band against the trade direction.",
      ({"ta.ema", "ta.atr"}, r"keltner|\bkc\b"), n=G(20, 30, 50), k=G(1.5, 2.0, 2.5, 3.0))
def _(p, d): return d.sg(C - ema(C, B(p.n))) < -p.k * atr(B(p.n)), ema(C, B(p.n))


@atom("loc_vwap_distance", LOC, "meanrev", "Close several ATR away from VWAP against the trade direction.",
      ({"ta.vwap", "ta.atr"}, None), hz=("SESSION_VALUE_LEAK",), k=G(1.0, 2.0, 3.0, 4.0))
def _(p, d): return d.sg(C - SVWAP) < -p.k * A, SVWAP


@atom("loc_rsi_zone", LOC, "meanrev", "RSI in its oversold zone (for longs).", ({"ta.rsi"}, r"oversold|overbought"),
      n=G(7, 14, 21), lvl=G(20, 25, 30, 35))
def _(p, d): return d.osc(rsi(C, B(p.n))) < p.lvl


@atom("loc_stochastic_zone", LOC, "meanrev", "Stochastic in its oversold zone (for longs).", ({"ta.stoch"}, None),
      n=G(9, 14, 21), lvl=G(10, 20, 30))
def _(p, d): return d.osc(stoch_k(p.n)) < p.lvl


@atom("loc_session_range_extreme", LOC, "meanrev", "Close in the adverse tail of the session range so far.",
      (set(), r"range position|premium|discount"), thr=G(0.1, 0.15, 0.2, 0.3))
def _(p, d): return (d.pos() < p.thr) & (MSO >= 30), (SHIGH + SLOW) / 2.0


@atom("loc_ema_distance", LOC, "meanrev", "Close stretched several ATR from a moving average against the trade direction.",
      ({"ta.ema", "ta.atr"}, r"distance|stretch|extension"), n=G(20, 50), k=G(1.0, 1.5, 2.0, 3.0))
def _(p, d): return d.sg(C - ema(C, B(p.n))) < -p.k * A, ema(C, B(p.n))


@atom("loc_prior_day_mid", LOC, "meanrev", "Price near the prior session's midpoint, on the trade side.",
      ({"request.security"}, r"mid|equilibrium|50%"), hz=("SECURITY_LOOKAHEAD", "SESSION_VALUE_LEAK"), k=KN)
def _(p, d): return near((PDH + PDL) / 2.0, p.k) & d.ge(C, (PDH + PDL) / 2.0), (PDH + PDL) / 2.0


@atom("loc_htf_bar_extreme", LOC, "sweep", "Price near the low (for longs) of the last confirmed higher-timeframe bar.",
      ({"request.security"}, r"htf|higher time"), hz=("SECURITY_LOOKAHEAD", "SESSION_VALUE_LEAK"), k=KN, m=G(3, 4, 6, 12, d=4))
def _(p, d):
    lvl = htf("low" if d.d > 0 else "high", p.m)
    return near(lvl, p.k), lvl


@atom("loc_initial_balance_extreme", LOC, "open", "After the first hour, price near the supportive edge of the initial balance.",
      (set(), r"initial balance|\bib\b"), hz=("SESSION_VALUE_LEAK",), tw=1, k=KN)
def _(p, d): return near(d.orn(60), p.k), d.orn(60)


# =============================================================== TRIGGER atoms
# ---- trend continuation
@atom("tr_trail_flip", T, "trend", "The owner's arrow: the ATR-trail regime flips to the trade direction.",
      ({"ta.atr"}, r"trail"), n=G(7, 10, 14, 20, 28), f=G(2.0, 2.5, 3.0, 3.5, 4.0))
def _(p, d):
    r = d.sg(trail(B(p.n), p.f))
    return (r > 0) & (shift(r, 1) < 0)


@atom("tr_supertrend_flip", T, "trend", "Supertrend flips to the trade direction.", ({"ta.supertrend"}, None),
      n=G(7, 10, 14, 20), m=G(2.0, 3.0, 4.0))
def _(p, d):
    r = d.sg(supertrend(B(p.n), p.m))
    return (r > 0) & (shift(r, 1) < 0)


@atom("tr_ema_cross", T, "trend", "Fast average crosses the slow average.", ({"ta.ema", "ta.crossover"}, None),
      f=G(5, 8, 13, 21), s=G(21, 34, 55, 89))
def _(p, d): return d.xo(ema(C, B(p.f)), ema(C, B(p.s)))


@atom("tr_price_ema_cross", T, "trend", "Close crosses a moving average.", ({"ta.ema", "ta.crossover"}, r"close"),
      n=G(10, 20, 34, 50))
def _(p, d): return d.xo(C, ema(C, B(p.n)))


@atom("tr_macd_signal_cross", T, "trend", "MACD line crosses its signal line.", ({"ta.macd", "ta.crossover"}, None), s=G(1, 2, 3, d=1))
def _(p, d):
    m, sig = macd_lines(p.s)
    return d.xo(m, sig)


@atom("tr_macd_zero_cross", T, "trend", "MACD line crosses zero.", ({"ta.macd"}, r"zero|\b0\b"), s=G(1, 2, 3, d=1))
def _(p, d): return d.xo(macd_lines(p.s)[0], w(0.0))


@atom("tr_donchian_break", T, "trend", "Close breaks the prior channel extreme for the first time.",
      ({"ta.highest", "ta.lowest"}, r"breakout|donchian|turtle"), n=G(10, 20, 40, 55))
def _(p, d): return d.xo(C, shift(d.top(B(p.n)), 1))


@atom("tr_momentum_bar", T, "trend", "A wide bar that closes near its favourable extreme.", ({"ta.atr"}, r"momentum candle|marubozu|displacement|impulse"),
      k=G(1.5, 2.0, 2.5, 3.0))
def _(p, d): return (RNG > p.k * A) & (d.wick_fav() < 0.25 * RNG) & d.gt(C, O)


@atom("tr_pullback_resume", T, "trend", "In a trend, price dipped to the fast average and then closes beyond the prior bar's extreme.",
      ({"ta.ema"}, r"pullback|retrace"), f=G(10, 20, 34), s=G(50, 100, 200))
def _(p, d):
    return d.gt(C, ema(C, B(p.s))) & d.le(shift(d.bot(B(3)), 1), shift(ema(C, B(p.f)), 1)) & d.gt(C, shift(d.hi, 1))


@atom("tr_three_bar_run", T, "trend", "Three consecutive closes and adverse extremes stepping in the trade direction.",
      (set(), r"three (white )?soldiers|three black crows|3 bar"))
def _(p, d):
    return d.gt(C, C[1]) & d.gt(C[1], C[2]) & d.gt(C[2], C[3]) & d.gt(d.lo, shift(d.lo, 1)) & d.gt(shift(d.lo, 1), shift(d.lo, 2))


@atom("tr_swing_break", T, "trend", "Close crosses the last confirmed swing extreme (break of structure).",
      ({"ta.pivothigh"}, r"bos|break of structure|choch"), hz=("PIVOT_UNCONFIRMED", "FUTURE_OFFSET", "REPEATED_SIGNAL_DELETE"), r=G(2, 3, 5))
def _(p, d): return d.xo(C, d.swing_fav(p.r)[1])


@atom("tr_rsi_midline_cross", T, "trend", "RSI crosses its midline.", ({"ta.rsi", "ta.crossover"}, r"50"), n=G(7, 14, 21))
def _(p, d): return d.xo(rsi(C, B(p.n)), w(50.0))


@atom("tr_stochastic_cross", T, "trend", "Stochastic %K crosses its %D.", ({"ta.stoch", "ta.crossover"}, None), n=G(9, 14, 21))
def _(p, d):
    k = stoch_k(p.n)
    return d.xo(k, sma(k, B(3)))


@atom("tr_di_cross", T, "trend", "Directional index lines cross.", ({"ta.dmi"}, r"cross"), n=G(10, 14, 20))
def _(p, d):
    pdi, mdi, _ = dmi(p.n)
    return d.xo(pdi, mdi)


@atom("tr_vwap_cross", T, "trend", "Close crosses the running session VWAP.", ({"ta.vwap", "ta.crossover"}, None), hz=("SESSION_VALUE_LEAK",))
def _(p, d): return d.xo(C, SVWAP) & (MSO >= 15)


@atom("tr_roc_thrust", T, "trend", "Net move over a few bars exceeds a multiple of ATR for the first time.",
      ({"ta.roc"}, None), n=G(3, 5, 8, 12), k=G(1.5, 2.0, 3.0))
def _(p, d):
    x = d.sg(change(C, p.n)) / A
    return (x > p.k) & (shift(x, 1) <= p.k)


@atom("tr_hma_turn", T, "trend", "Hull average turns in the trade direction.", ({"ta.hma"}, None), n=G(16, 25, 36, 49))
def _(p, d):
    s = d.sg(change(hma(C, B(p.n)), 1))
    return (s > 0) & (shift(s, 1) <= 0)


@atom("tr_cci_breakout", T, "trend", "CCI crosses beyond +100 in the trade direction.", ({"ta.cci"}, None), n=G(14, 20, 30))
def _(p, d): return crossover(d.sg(cci(p.n)), w(100.0))


@atom("tr_new_session_extreme", T, "trend", "First new session high (for longs) after a pause.", (set(), r"new (session|day) high|hod break|high of day"),
      hz=("SESSION_VALUE_LEAK",), tw=1, m=G(30, 60, 90), q=G(3, 6, 12))
def _(p, d):
    nh = d.gt(d.hi, shift(d.shigh, 1)) & (MSO >= p.m)
    return nh & ~any_in(shift(nh, 1), B(p.q))


@atom("tr_keltner_break", T, "trend", "Close crosses beyond the Keltner band in the trade direction.", ({"ta.ema", "ta.atr"}, r"keltner"),
      n=G(20, 30), k=G(1.0, 1.5, 2.0))
def _(p, d): return d.xo(C, d.up(ema(C, B(p.n)), p.k * atr(B(p.n))))


@atom("tr_pullback_depth", T, "trend", "Inside a trail up-regime, price has retraced a set distance from its recent high and ticks back up.",
      ({"ta.atr", "ta.highest"}, r"pullback|retrace|dip"), n=G(10, 20), k=G(1.0, 1.5, 2.0))
def _(p, d):
    return (d.sg(trail(B(14), 3.0)) > 0) & (d.sg(d.top(B(p.n)) - C) > p.k * A) & d.gt(C, C[1])


@atom("tr_vwap_retest_hold", T, "trend", "Price dips through VWAP intrabar and closes back on the trade side while it was there before.",
      ({"ta.vwap"}, r"retest|reclaim|bounce"), hz=("SESSION_VALUE_LEAK",))
def _(p, d): return d.lt(d.lo, SVWAP) & d.gt(C, SVWAP) & d.gt(C[1], shift(SVWAP, 1)) & (MSO >= 30)


# ---- mean reversion to value
@atom("tr_bollinger_reentry", T, "meanrev", "Close returns inside the Bollinger band after closing outside it.",
      ({"ta.sma", "ta.stdev", "ta.crossover"}, r"bollinger|\bbb\b"), n=G(20, 30, 50), k=G(1.5, 2.0, 2.5))
def _(p, d): return d.xo(C, d.dn(sma(C, B(p.n)), p.k * stdev(C, B(p.n))))


@atom("tr_keltner_reentry", T, "meanrev", "Close returns inside the Keltner band after closing outside it.",
      ({"ta.ema", "ta.atr", "ta.crossover"}, r"keltner"), n=G(20, 30, 50), k=G(1.5, 2.0, 2.5))
def _(p, d): return d.xo(C, d.dn(ema(C, B(p.n)), p.k * atr(B(p.n))))


@atom("tr_rsi_hook", T, "meanrev", "RSI hooks back out of its extreme zone.", ({"ta.rsi", "ta.crossover"}, r"oversold|overbought"),
      n=G(5, 7, 10, 14), lvl=G(20, 25, 30, 35))
def _(p, d): return crossover(d.osc(rsi(C, B(p.n))), w(p.lvl))


@atom("tr_stochastic_hook", T, "meanrev", "Stochastic hooks back out of its extreme zone.", ({"ta.stoch", "ta.crossover"}, r"oversold|overbought|20|80"),
      n=G(9, 14, 21), lvl=G(15, 20, 25, 30))
def _(p, d): return crossover(d.osc(stoch_k(p.n)), w(p.lvl))


@atom("tr_cci_hook", T, "meanrev", "CCI hooks back from an extreme.", ({"ta.cci", "ta.crossover"}, None), n=G(14, 20, 30), lvl=G(100, 150, 200))
def _(p, d): return crossover(d.sg(cci(p.n)), w(-p.lvl))


@atom("tr_mfi_hook", T, "meanrev", "Money-flow index hooks back out of its extreme zone.", ({"ta.mfi"}, None),
      n=G(10, 14, 20), lvl=G(15, 20, 25, 30))
def _(p, d): return crossover(d.osc(mfi(p.n)), w(p.lvl))


@atom("tr_williams_hook", T, "meanrev", "Raw stochastic (Williams %R) hooks back out of its extreme zone.", ({"ta.wpr"}, None),
      n=G(10, 14, 21), lvl=G(10, 15, 20))
def _(p, d):
    x = 100.0 * (C - lowest(L, B(p.n))) / (highest(H, B(p.n)) - lowest(L, B(p.n)))
    return crossover(d.osc(x), w(p.lvl))


@atom("tr_zscore_revert", T, "meanrev", "Z-score of the close turns back from an extreme.", ({"ta.sma", "ta.stdev"}, r"z-?score"),
      n=G(20, 30, 50), k=G(1.5, 2.0, 2.5))
def _(p, d): return crossover(d.sg((C - sma(C, B(p.n))) / stdev(C, B(p.n))), w(-p.k))


@atom("tr_vwap_band_reentry", T, "meanrev", "Close returns inside a VWAP deviation band.", ({"ta.vwap", "ta.stdev"}, r"band"),
      hz=("SESSION_VALUE_LEAK",), k=G(1.0, 1.5, 2.0, 2.5))
def _(p, d): return d.xo(C, d.dn(SVWAP, p.k * VW_SD)) & (MSO >= 30)


@atom("tr_rsi2_extreme", T, "meanrev", "Two-bar RSI at an extreme (short-term exhaustion of the pullback).", ({"ta.rsi"}, r"rsi\s*\(?\s*2|connors"),
      lvl=G(5, 10, 15))
def _(p, d): return d.osc(rsi(C, B(2))) < p.lvl


@atom("tr_run_then_reverse", T, "meanrev", "Several consecutive closes against the trade direction, then a close with it.",
      (set(), r"consecutive|streak|in a row"), n=G(3, 4, 5))
def _(p, d): return (shift(rsum(b2f(d.lt(C, C[1])), B(p.n)), 1) > p.n - 0.5) & d.gt(C, C[1])


@atom("tr_snapback", T, "meanrev", "Price stretched from its average, then a bar closes back toward it.", ({"ta.ema", "ta.atr"}, r"snap|mean reversion|revert"),
      n=G(20, 50), k=G(1.5, 2.0, 2.5, 3.0))
def _(p, d): return (d.sg(C - ema(C, B(p.n))) < -p.k * A) & d.gt(C, O) & d.gt(C, C[1])


@atom("tr_internal_bar_strength", T, "meanrev", "A normal-sized bar closes at its adverse extreme (internal bar strength).", (set(), r"\bibs\b|internal bar strength"),
      thr=G(0.1, 0.15, 0.2, 0.25))
def _(p, d): return (d.sg(C - (H + L) / 2.0) / RNG + 0.5 < p.thr) & (RNG > 0.75 * A)


@atom("tr_cmo_hook", T, "meanrev", "Chande momentum hooks back from an extreme.", ({"ta.cmo"}, None), n=G(9, 14, 20), lvl=G(40, 50, 60))
def _(p, d): return crossover(d.sg(cmo(p.n)), w(-p.lvl))


@atom("tr_vwap_stretch_turn", T, "meanrev", "Price several ATR from VWAP, then a bar closes back toward it.", ({"ta.vwap", "ta.atr"}, None),
      hz=("SESSION_VALUE_LEAK",), k=G(1.5, 2.0, 3.0, 4.0))
def _(p, d): return (d.sg(C - SVWAP) < -p.k * A) & d.gt(C, O) & d.gt(C, C[1])


@atom("tr_range_tail_turn", T, "meanrev", "Close in the adverse tail of the session range, then a close beyond the prior bar's extreme.",
      (set(), r"range|premium|discount"), thr=G(0.1, 0.15, 0.2, 0.3))
def _(p, d): return (d.pos() < p.thr) & (MSO >= 45) & d.gt(C, shift(d.hi, 1))


# ---- liquidity sweep and reversal
@atom("tr_sweep_prior_day", T, "sweep", "Price trades through the prior session's low and closes back above it (for longs).",
      ({"request.security"}, r"sweep|liquidity|stop hunt|raid"), hz=("SECURITY_LOOKAHEAD", "SESSION_VALUE_LEAK"))
def _(p, d): return d.lt(d.lo, d.pdl) & d.gt(C, d.pdl), d.pdl


@atom("tr_sweep_swing", T, "sweep", "Price trades through the last confirmed swing low and closes back above it.",
      ({"ta.pivotlow"}, r"sweep|liquidity|grab|stop hunt"), hz=("PIVOT_UNCONFIRMED", "FUTURE_OFFSET", "REPEATED_SIGNAL_DELETE"), r=G(2, 3, 5))
def _(p, d):
    _e, lvl = d.swing_adv(p.r)
    return d.lt(d.lo, lvl) & d.gt(C, lvl), lvl


@atom("tr_sweep_session_extreme", T, "sweep", "Price makes a new session low and closes back above the old one.",
      (set(), r"sweep|liquidity|lod|hod|session low|session high"), hz=("SESSION_VALUE_LEAK",), tw=1, m=G(30, 60, 90))
def _(p, d):
    lvl = shift(d.slow, 1)
    return d.lt(d.lo, lvl) & d.gt(C, lvl) & (MSO >= p.m) & ~FIRST, lvl


@atom("tr_sweep_opening_range", T, "sweep", "Price trades through the opening-range low and closes back inside.",
      (set(), r"opening range|\borb\b"), hz=("SESSION_VALUE_LEAK",), tw=1, m=G(15, 30, 60))
def _(p, d): return d.lt(d.lo, d.orn(p.m)) & d.gt(C, d.orn(p.m)), d.orn(p.m)


@atom("tr_sweep_n_bar", T, "sweep", "Price trades through the prior n-bar low and closes back above it.",
      ({"ta.lowest", "ta.highest"}, r"sweep|liquidity|false break|fakeout"), n=G(10, 20, 40))
def _(p, d):
    lvl = shift(d.bot(B(p.n)), 1)
    return d.lt(d.lo, lvl) & d.gt(C, lvl), lvl


@atom("tr_turtle_soup", T, "sweep", "A new n-bar low that had stood untouched for several bars is rejected on the same bar.",
      ({"ta.lowest"}, r"turtle soup"), n=G(20, 40))
def _(p, d):
    lvl = shift(d.bot(B(p.n)), 1)
    return d.lt(d.lo, lvl) & d.gt(C, lvl) & d.gt(shift(d.bot(B(3)), 1), lvl), lvl


@atom("tr_wick_rejection", T, "sweep", "A long rejection wick at an n-bar extreme.", (set(), r"wick|pin ?bar|hammer|rejection|shooting star"),
      k=G(2.0, 3.0), n=G(5, 10, 20))
def _(p, d): return (d.wick_adv() > p.k * BODY) & (d.wick_adv() > 0.5 * A) & d.le(d.lo, d.bot(B(p.n)))


@atom("tr_htf_extreme_sweep", T, "sweep", "Price trades through the last confirmed higher-timeframe bar's low and closes back above it.",
      ({"request.security"}, r"sweep|liquidity|htf"), hz=("SECURITY_LOOKAHEAD", "SESSION_VALUE_LEAK"), k=G(3, 4, 6, 12, d=4))
def _(p, d):
    lvl = htf("low" if d.d > 0 else "high", p.k)
    return d.lt(d.lo, lvl) & d.gt(C, lvl), lvl


@atom("tr_double_tap", T, "sweep", "Price tests the last swing low within a quarter ATR without breaking it and closes up.",
      ({"ta.pivotlow"}, r"double (bottom|top)|equal (lows|highs)"), hz=("PIVOT_UNCONFIRMED",), r=G(2, 3, 5))
def _(p, d):
    _e, lvl = d.swing_adv(p.r)
    return (absx(d.lo - lvl) < 0.25 * A) & d.ge(d.lo, d.dn(lvl, 0.25 * A)) & d.gt(C, O), lvl


@atom("tr_round_number_reject", T, "sweep", "Price trades through a round-number level and closes back on the trade side.",
      (set(), r"round number|psychological"), mult=G(1.0, 2.5, 5.0))
def _(p, d):
    lvl = roundlvl(p.mult)
    return d.lt(d.lo, lvl) & d.gt(C, lvl) & d.gt(O, lvl), lvl


@atom("tr_sweep_prior_close", T, "sweep", "Price trades through the prior session's close and closes back on the trade side.",
      ({"request.security"}, r"prev\w*\s*close"), hz=("SECURITY_LOOKAHEAD", "HTF_CLOSE_INTRABAR"))
def _(p, d): return d.lt(d.lo, PDC) & d.gt(C, PDC) & d.gt(C[1], PDC), PDC


@atom("tr_initial_balance_sweep", T, "sweep", "After the first hour, price trades through the initial-balance low and closes back inside.",
      (set(), r"initial balance|\bib\b"), hz=("SESSION_VALUE_LEAK",), tw=1)
def _(p, d): return d.lt(d.lo, d.orn(60)) & d.gt(C, d.orn(60)), d.orn(60)


# ---- volatility expansion
@atom("tr_range_expansion_break", T, "volexp", "The widest bar of the lookback closes beyond the prior n-bar extreme.",
      ({"ta.highest", "ta.atr"}, r"expansion|wide range|wrb"), n=G(5, 10, 20))
def _(p, d): return (RNG >= highest(RNG, B(p.n))) & d.gt(C, shift(d.top(B(p.n)), 1))


@atom("tr_volume_climax_follow", T, "volexp", "Highest volume of the lookback on a bar closing in the trade direction near its extreme.",
      ({"ta.highest"}, r"volume (spike|climax|surge)|high volume"), n=G(10, 20, 40))
def _(p, d): return (V >= highest(V, B(p.n))) & d.gt(C, O) & (d.wick_fav() < 0.33 * RNG)


@atom("tr_band_width_expansion", T, "volexp", "Bollinger band width crosses above its own average while price is on the trade side of the basis.",
      ({"ta.stdev", "ta.sma"}, r"width|bbw|squeeze"), n=G(20, 30), m=G(20, 50))
def _(p, d):
    bw = stdev(C, B(p.n)) / sma(C, B(p.n))
    return crossover(bw, sma(bw, B(p.m))) & d.gt(C, sma(C, B(p.n)))


@atom("tr_bollinger_break", T, "volexp", "Close crosses beyond the outer Bollinger band in the trade direction.",
      ({"ta.sma", "ta.stdev", "ta.crossover"}, r"bollinger|\bbb\b"), n=G(20, 30), k=G(1.5, 2.0, 2.5))
def _(p, d): return d.xo(C, d.up(sma(C, B(p.n)), p.k * stdev(C, B(p.n))))


@atom("tr_true_range_spike", T, "volexp", "True range, gap included, far above ATR on a bar closing in the trade direction.",
      ({"ta.tr", "ta.atr"}, None), k=G(2.0, 2.5, 3.0))
def _(p, d): return (TR > p.k * shift(A, 1)) & d.gt(C, C[1]) & d.gt(C, O)


# ---- volatility contraction
@atom("tr_squeeze_release", T, "volcon", "Bollinger bands leave the inside of the Keltner channel; direction from price versus the basis.",
      ({"ta.stdev", "ta.atr"}, r"squeeze|ttm"), n=G(14, 20, 30), m=G(1.0, 1.5, 2.0))
def _(p, d): return shift(SQUEEZE(p.n, p.m), 1) & ~SQUEEZE(p.n, p.m) & d.gt(C, sma(C, B(p.n)))


@atom("tr_narrow_range_break", T, "volcon", "The prior bar had the narrowest range of the lookback; this bar closes beyond its extreme.",
      ({"ta.lowest"}, r"\bnr7\b|\bnr4\b|narrow range"), n=G(4, 7, 10))
def _(p, d): return (shift(RNG, 1) <= shift(lowest(RNG, B(p.n)), 1)) & d.gt(C, shift(d.hi, 1))


@atom("tr_inside_bar_break", T, "volcon", "The prior bar was an inside bar; this bar closes beyond the mother bar.",
      (set(), r"inside bar"), )
def _(p, d): return (H[1] <= H[2]) & (L[1] >= L[2]) & d.gt(C, shift(d.hi, 2))


@atom("tr_coil_break", T, "volcon", "A tight n-bar range, then a close beyond it.", ({"ta.highest", "ta.lowest", "ta.atr"}, r"consolidation|coil|tight|flag|box"),
      n=G(4, 6, 8, 12), k=G(1.0, 1.5, 2.0, 3.0))
def _(p, d): return (shift(highest(H, B(p.n)) - lowest(L, B(p.n)), 1) < p.k * A) & d.gt(C, shift(d.top(B(p.n)), 1))


@atom("tr_low_volatility_break", T, "volcon", "ATR low in its own history, then a channel break.", ({"ta.atr", "ta.percentrank"}, None),
      q=G(20, 30, 40), n=G(10, 20))
def _(p, d): return (prank(A, B(200)) < p.q) & d.xo(C, shift(d.top(B(p.n)), 1))


# ---- opening auction
@atom("tr_opening_range_break", T, "open", "First close beyond the completed opening range.", (set(), r"opening range|\borb\b"),
      hz=("SESSION_VALUE_LEAK", "SECURITY_LOOKAHEAD"), tw=1, m=G(15, 30, 60))
def _(p, d): return d.xo(C, d.orx(p.m))


@atom("tr_opening_drive", T, "open", "The opening window ends with a strong net move; enter with it.", (set(), r"opening drive|open drive|first\s*\d+\s*min"),
      tw=1, m=G(15, 30, 45), k=G(1.0, 2.0, 3.0))
def _(p, d): return (MSO >= p.m) & (shift(MSO, 1) < p.m) & ~FIRST & (d.sg(C - SOPEN) > p.k * A)


@atom("tr_gap_fade", T, "open", "Session gapped against the trade direction; early on, a bar closes beyond the prior bar toward the gap fill.",
      (set(), r"gap (fade|fill)|fade the gap"), hz=("SECURITY_LOOKAHEAD",), tw=1, g=G(0.001, 0.002, 0.004), wnd=G(30, 60, 90))
def _(p, d): return (d.sg(SOPEN - PDC) / PDC < -p.g) & (MSO <= p.wnd) & ~FIRST & d.gt(C, shift(d.hi, 1)), PDC


@atom("tr_gap_and_go", T, "open", "Session gapped in the trade direction and price crosses the first bar's extreme.",
      (set(), r"gap and go|gap up|gap down"), hz=("SECURITY_LOOKAHEAD",), tw=1, g=G(0.001, 0.002, 0.004), wnd=G(30, 60, 90))
def _(p, d):
    fb = sfirst(H) if d.d > 0 else sfirst(L)
    return (d.sg(SOPEN - PDC) / PDC > p.g) & (MSO <= p.wnd) & d.xo(C, fb)


@atom("tr_opening_range_retest", T, "open", "After a break of the opening range, price returns to its edge and closes back beyond it.",
      (set(), r"retest|opening range"), hz=("SESSION_VALUE_LEAK",), tw=1, m=G(15, 30, 60), q=G(6, 12))
def _(p, d):
    e = d.orx(p.m)
    return any_in(shift(d.gt(C, d.up(e, 0.5 * A)), 1), B(p.q)) & d.le(d.lo, d.up(e, 0.25 * A)) & d.gt(C, e) & d.gt(C, O), e


@atom("tr_initial_balance_extension", T, "open", "Close crosses a fractional extension of the first hour's range.",
      (set(), r"initial balance|\bib\b|extension"), hz=("SESSION_VALUE_LEAK",), tw=1, x=G(0.25, 0.5, 1.0))
def _(p, d): return d.xo(C, d.up(d.orx(60), p.x * (frozen(SHIGH, 60) - frozen(SLOW, 60))))


@atom("tr_first_bar_break", T, "open", "Within the first hour, close crosses the first bar's extreme.", (set(), r"first (bar|candle)|opening candle"),
      tw=1)
def _(p, d): return d.xo(C, sfirst(H) if d.d > 0 else sfirst(L)) & (MSO <= 60)


# ---- closing auction
@atom("tr_late_session_extreme", T, "close", "Late in the session, a new session high (for longs).", (set(), r"power hour|last hour|closing"),
      hz=("SESSION_VALUE_LEAK",), tw=1, m=G(300, 330, 345))
def _(p, d): return (MSO >= p.m) & d.gt(d.hi, shift(d.shigh, 1)) & d.gt(C, O)


@atom("tr_close_extreme_fade", T, "close", "Late in the session, price at the adverse extreme of the day's range turns back.",
      (set(), r"moc|market on close|closing|end of day"), tw=1, m=G(330, 345, 360))
def _(p, d): return (MSO >= p.m) & (d.pos() < 0.1) & d.gt(C, shift(d.hi, 1))


@atom("tr_late_vwap_cross", T, "close", "In the final 90 minutes, close crosses VWAP.", ({"ta.vwap"}, r"close|eod|power"), hz=("SESSION_VALUE_LEAK",), tw=1)
def _(p, d): return (MSO >= 300) & d.xo(C, SVWAP)


@atom("tr_final_hour_thrust", T, "close", "In the final hour, the move since the hour began first exceeds a multiple of ATR.",
      (set(), r"power hour|last hour|final hour"), tw=1, k=G(1.0, 1.5, 2.0, 3.0))
def _(p, d):
    x = d.sg(C - frozen(C, 330)) / A
    return (MSO > 330) & (x > p.k) & (shift(x, 1) <= p.k)


# ---- exhaustion
@atom("tr_climax_reversal", T, "exhaust", "After a move against the trade direction, the highest-volume wide bar at an n-bar extreme closes in its favourable half.",
      ({"ta.highest"}, r"climax|capitulation|exhaustion"), n=G(10, 20, 40))
def _(p, d):
    return (V >= highest(V, B(p.n))) & (RNG > 1.5 * A) & d.lt(C[1], C[6]) & d.gt(C, (H + L) / 2.0) & d.le(d.lo, d.bot(B(p.n)))


@atom("tr_engulfing", T, "exhaust", "An engulfing bar after closes against the trade direction.", (set(), r"engulf"))
def _(p, d):
    return d.lt(C[1], O[1]) & d.gt(C, O) & d.ge(C, O[1]) & d.le(O, C[1]) & (shift(rsum(b2f(d.lt(C, C[1])), B(3)), 1) > 1.5)


@atom("tr_pin_bar", T, "exhaust", "A wide bar with a dominant rejection wick and a small opposite wick.", (set(), r"pin ?bar|hammer|shooting star|doji"))
def _(p, d): return (d.wick_adv() > 2.0 * BODY) & (d.wick_fav() < 0.5 * d.wick_adv()) & (RNG > A)


@atom("tr_rsi_divergence", T, "exhaust", "A confirmed swing low below the previous one while RSI at the swing is higher.",
      ({"ta.rsi", "ta.pivotlow"}, r"diverg"), hz=("PIVOT_UNCONFIRMED", "FUTURE_OFFSET", "REPEATED_SIGNAL_DELETE"), r=G(2, 3, 5), n=G(9, 14))
def _(p, d):
    ev, lvl = d.swing_adv(p.r)
    rr = shift(rsi(C, B(p.n)), p.r)
    return ev & d.lt(lvl, shift(lvl, 1)) & d.gt(rr, shift(valuewhen(ev, rr), 1))


@atom("tr_outside_bar_reversal", T, "exhaust", "An outside bar closing beyond the prior bar's extreme after drift against the trade direction.",
      (set(), r"outside bar"))
def _(p, d): return (H > H[1]) & (L < L[1]) & d.gt(C, shift(d.hi, 1)) & d.lt(C[1], C[4])


@atom("tr_macd_histogram_fade", T, "exhaust", "Momentum against the trade direction has waned for two bars at an n-bar extreme.",
      ({"ta.macd"}, r"hist"), n=G(10, 20))
def _(p, d):
    m, sig = macd_lines(1)
    hh = d.sg(m - sig)
    return (hh < 0) & (hh > shift(hh, 1)) & (shift(hh, 1) > shift(hh, 2)) & d.le(d.lo, d.bot(B(p.n)))


@atom("tr_volume_dryup_extreme", T, "exhaust", "A new n-bar extreme against the trade direction on unusually light volume.",
      ({"ta.sma"}, r"volume dry|low volume|no supply|no demand"), n=G(10, 20), k=G(0.5, 0.7))
def _(p, d): return d.le(d.lo, d.bot(B(p.n))) & (V < p.k * sma(V, B(p.n))) & d.gt(C, O)


@atom("tr_key_reversal", T, "exhaust", "A new n-bar low followed, on the same bar, by a close above the prior bar's high.",
      ({"ta.lowest"}, r"key reversal|reversal bar"), n=G(10, 20, 40))
def _(p, d): return d.lt(d.lo, shift(d.bot(B(p.n)), 1)) & d.gt(C, shift(d.hi, 1))


@atom("tr_range_exhaustion_turn", T, "exhaust", "Session range exceeds the prior session's, price is at the adverse extreme, and a bar closes beyond the prior bar.",
      (set(), r"average daily range|\badr\b"), thr=G(1.0, 1.25, 1.5))
def _(p, d): return (SRANGE / prevlast(SRANGE) > p.thr) & (d.pos() < 0.2) & d.gt(C, shift(d.hi, 1))


# ---- breakout failure
@atom("tr_failed_break", T, "bofail", "A close through the n-bar extreme against the trade direction is reversed within a few bars.",
      ({"ta.lowest", "ta.highest"}, r"false break|failed break|fakeout|trap"), n=G(10, 20, 40), q=G(2, 4, 8))
def _(p, d):
    lvl = shift(d.bot(B(p.n)), 1)
    brk = d.lt(C, lvl)
    bs = barssince(brk)
    return (bs >= 1) & (bs <= p.q) & d.gt(C, valuewhen(brk, lvl)), valuewhen(brk, lvl)


@atom("tr_band_break_failure", T, "bofail", "A close outside the Bollinger band is followed by a close back inside and beyond the prior bar.",
      ({"ta.sma", "ta.stdev"}, r"bollinger|\bbb\b"), n=G(20, 30), k=G(1.5, 2.0, 2.5))
def _(p, d):
    band = d.dn(sma(C, B(p.n)), p.k * stdev(C, B(p.n)))
    return d.lt(C[1], shift(band, 1)) & d.gt(C, band) & d.gt(C, shift(d.hi, 1))


@atom("tr_false_break_prior_day", T, "bofail", "Recent closes beyond the prior session's extreme against the trade direction, now a close back inside.",
      ({"request.security"}, r"false break|failed|trap|fakeout"), hz=("SECURITY_LOOKAHEAD", "SESSION_VALUE_LEAK"), q=G(2, 4, 8))
def _(p, d): return any_in(shift(d.lt(C, d.pdl), 1), B(p.q)) & d.gt(C, d.pdl), d.pdl


@atom("tr_swing_break_failure", T, "bofail", "Recent closes beyond the confirmed swing against the trade direction, now a close back inside.",
      ({"ta.pivotlow"}, r"false break|failed|trap|fakeout"), hz=("PIVOT_UNCONFIRMED",), r=G(2, 3, 5), q=G(2, 4, 8))
def _(p, d):
    _e, lvl = d.swing_adv(p.r)
    return any_in(shift(d.lt(C, lvl), 1), B(p.q)) & d.gt(C, lvl), lvl


@atom("tr_two_bar_reversal", T, "bofail", "A strong bar against the trade direction is fully retraced by the next bar.",
      (set(), r"two bar reversal|2 bar reversal|tweezer"))
def _(p, d): return d.lt(C[1], O[1]) & (shift(RNG, 1) > 1.2 * shift(A, 1)) & d.gt(C, O[1])


@atom("tr_opening_range_failure", T, "bofail", "Recent closes beyond the opening range against the trade direction, now a close back inside.",
      (set(), r"opening range|\borb\b"), hz=("SESSION_VALUE_LEAK",), tw=1, m=G(15, 30, 60), q=G(3, 6, 12))
def _(p, d): return any_in(shift(d.lt(C, d.orn(p.m)), 1), B(p.q)) & d.gt(C, d.orn(p.m)), d.orn(p.m)


# ---- inter-market lead-lag
@atom("tr_companion_leads_break", T, "intermarket", "The companion future has broken its n-bar extreme while this one has not yet.",
      ({"request.security", "ta.highest"}, r"lead|lag|correlat|confirm"), n=G(10, 20, 40))
def _(p, d):
    otop = highest(OH, B(p.n)) if d.d > 0 else lowest(OL, B(p.n))
    return d.gt(OC, shift(otop, 1)) & d.le(C, shift(d.top(B(p.n)), 1)) & d.gt(C, C[1])


@atom("tr_divergence_at_session_extreme", T, "intermarket", "This instrument makes a new session low while the companion does not, and the bar closes up.",
      ({"request.security"}, r"smt|diverg"), hz=("SESSION_VALUE_LEAK",))
def _(p, d):
    ox = scummin(OL) if d.d > 0 else scummax(OH)
    return d.lt(d.lo, shift(d.slow, 1)) & d.gt(d.olo, shift(ox, 1)) & d.gt(C, O) & (MSO >= 30) & ~FIRST


@atom("tr_companion_reclaim", T, "intermarket", "The companion sweeps and reclaims its own prior-session low on this bar.",
      ({"request.security"}, r"sweep|reclaim"), hz=("SECURITY_LOOKAHEAD",))
def _(p, d):
    olvl = prevlast(scummin(OL)) if d.d > 0 else prevlast(scummax(OH))
    return d.lt(d.olo, olvl) & d.gt(OC, olvl)


@atom("tr_relative_strength_turn", T, "intermarket", "Relative performance since the open crosses to the trade side.",
      ({"request.security"}, r"relative strength|ratio"))
def _(p, d): return d.xo(C / sfirst(C) - OC / sfirst(OC), w(0.0)) & (MSO >= 30)


@atom("tr_companion_impulse", T, "intermarket", "The companion prints an impulse bar that this instrument has not yet matched.",
      ({"request.security", "ta.atr"}, r"lead|lag"), k=G(1.0, 1.5, 2.0))
def _(p, d):
    oatr = rma(maxx(OH - OL, absx(OC - shift(OC, 1))), B(14))
    return (d.sg(OC - shift(OC, 1)) > p.k * oatr) & (absx(C - C[1]) < 0.5 * p.k * A)


# =============================================================== FILTER atoms
@atom("f_session_segment", FLT, "season", "Trade only inside one fixed session segment: first 30 minutes, morning, midday, afternoon, last 30 minutes.",
      (set(), r"session|time filter|trading hours"), tw=1, seg=G(0, 1, 2, 3, 4, d=1))
def _(p, d):
    lo, hi = [(0, 30), (30, 150), (150, 270), (270, 360), (360, 9999)][int(p.seg)]
    return (MSO > lo) & (MSO <= hi)


@atom("f_skip_open", FLT, "season", "No entries during the first minutes of the session.", (set(), r"skip|avoid.*open|first\s*\d+"),
      tw=1, m=G(5, 10, 15, 30, 45, 60, d=15))
def _(p, d): return MSO > p.m


@atom("f_stop_before_close", FLT, "season", "No entries during the last minutes before the regular close.", (set(), r"close|end of day|eod"),
      tw=1, m=G(15, 30, 45, 60, 90, d=30))
def _(p, d): return MTC >= p.m


@atom("f_not_midday", FLT, "season", "No entries during the midday lull.", (set(), r"lunch|midday|noon"), tw=1)
def _(p, d): return ~((MSO > 150) & (MSO <= 270))


@atom("f_weekday_block", FLT, "season", "Block one weekday.", (set(), r"dayofweek|monday|friday"), tw=1, day=G(1, 2, 3, 4, 5, d=3))
def _(p, d): return (DOW < p.day - 0.5) | (DOW > p.day + 0.5)


@atom("f_relative_volume_high", FLT, "volexp", "Bar volume above a multiple of its average.", ({"ta.sma"}, r"volume\s*>|relative volume|rvol"),
      k=G(1.0, 1.2, 1.5, 2.0), n=G(20, 50))
def _(p, d): return V > p.k * sma(V, B(p.n))


@atom("f_relative_volume_low", FLT, "volcon", "Bar volume below a multiple of its average.", ({"ta.sma"}, r"volume\s*<|low volume"),
      k=G(0.5, 0.7, 0.85, 1.0), n=G(20, 50))
def _(p, d): return V < p.k * sma(V, B(p.n))


@atom("f_volatility_expanding", FLT, "volexp", "Fast ATR above slow ATR.", ({"ta.atr"}, r"expan|ratio"), thr=G(1.0, 1.2, 1.5))
def _(p, d): return atr(B(5)) / atr(B(50)) > p.thr


@atom("f_volatility_contracting", FLT, "volcon", "Fast ATR below slow ATR.", ({"ta.atr"}, r"contract|compress|ratio"), thr=G(0.6, 0.75, 0.9))
def _(p, d): return atr(B(5)) / atr(B(50)) < p.thr


@atom("f_squeeze_on", FLT, "volcon", "Bollinger bands inside the Keltner channel.", ({"ta.stdev", "ta.atr"}, r"squeeze|ttm"),
      n=G(14, 20, 30), m=G(1.0, 1.5, 2.0))
def _(p, d): return SQUEEZE(p.n, p.m)


@atom("f_choppy", FLT, "volcon", "Net range small relative to the path travelled (range-bound conditions).", ({"math.sum"}, r"chop"),
      n=G(14, 20, 30), thr=G(0.2, 0.25, 0.3))
def _(p, d): return (highest(H, B(p.n)) - lowest(L, B(p.n))) / rsum(TR, B(p.n)) < p.thr


@atom("f_directional", FLT, "volexp", "Net range large relative to the path travelled (directional conditions).", ({"math.sum"}, r"chop|trend"),
      n=G(14, 20, 30), thr=G(0.35, 0.4, 0.5))
def _(p, d): return (highest(H, B(p.n)) - lowest(L, B(p.n))) / rsum(TR, B(p.n)) > p.thr


@atom("f_atr_rank_high", FLT, "volexp", "ATR high in its own recent history.", ({"ta.atr", "ta.percentrank"}, None), n=G(100, 200, 390), q=G(60, 70, 80))
def _(p, d): return prank(A, B(p.n)) > p.q


@atom("f_atr_rank_low", FLT, "volcon", "ATR low in its own recent history.", ({"ta.atr", "ta.percentrank"}, None), n=G(100, 200, 390), q=G(20, 30, 40))
def _(p, d): return prank(A, B(p.n)) < p.q


@atom("f_adx_high", FLT, "trend", "ADX above a threshold.", ({"ta.dmi"}, r"adx\s*>"), n=G(10, 14, 20), thr=G(15, 20, 25, 30))
def _(p, d): return dmi(p.n)[2] > p.thr


@atom("f_adx_low", FLT, "meanrev", "ADX below a threshold.", ({"ta.dmi"}, r"adx\s*<"), n=G(10, 14, 20), thr=G(15, 20, 25, 30))
def _(p, d): return dmi(p.n)[2] < p.thr


@atom("f_room_to_session_extreme", FLT, "trend", "Enough distance left to the session extreme in the trade direction.",
      (set(), r"room|distance to"), k=G(0.5, 1.0, 2.0, 3.0))
def _(p, d): return d.sg(d.shigh - C) > p.k * A


@atom("f_not_extended_from_vwap", FLT, "meanrev", "Price within a set distance of VWAP.", ({"ta.vwap"}, r"distance|extended"), k=G(1.0, 2.0, 3.0, 4.0))
def _(p, d): return absx(C - SVWAP) < p.k * A


@atom("f_signal_bar_not_huge", FLT, "exhaust", "Signal bar range below a multiple of ATR.", ({"ta.atr"}, r"candle size|bar size|range\s*<"),
      k=G(1.5, 2.0, 3.0))
def _(p, d): return RNG < p.k * A


@atom("f_body_ratio", FLT, "trend", "Signal bar body is a large share of its range.", (set(), r"body"), r=G(0.4, 0.5, 0.6, 0.7))
def _(p, d): return BODY > p.r * RNG


@atom("f_close_location", FLT, "trend", "Signal bar closes in its favourable third.", (set(), r"close location|closes? near (the )?(high|low)"))
def _(p, d): return d.wick_fav() < 0.34 * RNG


@atom("f_inside_prior_day_range", FLT, "meanrev", "Price inside the prior session's range.", ({"request.security"}, r"inside (day|range)|prev\w* (day )?range"),
      hz=("SECURITY_LOOKAHEAD", "SESSION_VALUE_LEAK"))
def _(p, d): return (C < PDH) & (C > PDL)


@atom("f_outside_prior_day_range", FLT, "trend", "Price outside the prior session's range.", ({"request.security"}, r"breakout|outside|prev\w* (day )?(high|low)"),
      hz=("SECURITY_LOOKAHEAD", "SESSION_VALUE_LEAK"))
def _(p, d): return (C > PDH) | (C < PDL)


@atom("f_small_gap", FLT, "open", "Session opened close to the prior close.", (set(), r"\bgap\b"), hz=("SECURITY_LOOKAHEAD",), g=G(0.001, 0.002, 0.004))
def _(p, d): return absx(SOPEN - PDC) / PDC < p.g


@atom("f_session_range_developed", FLT, "volexp", "Session range so far exceeds a multiple of ATR.", (set(), r"session range|day range"),
      k=G(2.0, 3.0, 4.0, 6.0))
def _(p, d): return SRANGE > p.k * A


@atom("f_companion_confirms", FLT, "intermarket", "The companion's bar moved in the trade direction.", ({"request.security"}, r"confirm|agree"))
def _(p, d): return d.gt(OC, shift(OC, 1))


@atom("f_volume_trend_up", FLT, "volexp", "Short volume average above long volume average.", ({"ta.sma"}, r"volume (ma|sma|average)"))
def _(p, d): return sma(V, B(5)) > sma(V, B(20))


@atom("f_rsi_not_extreme", FLT, "trend", "RSI away from both extremes.", ({"ta.rsi"}, r"and.*rsi|rsi.*and"), n=G(14,), band=G(20, 25, 30))
def _(p, d): return (rsi(C, B(p.n)) > p.band) & (rsi(C, B(p.n)) < 100.0 - p.band)


@atom("f_htf_agrees", FLT, "trend", "Last confirmed higher-timeframe bar closed in the trade direction.", ({"request.security"}, r"htf|higher time|mtf"),
      hz=("SECURITY_LOOKAHEAD", "HTF_CLOSE_INTRABAR"), k=G(3, 4, 6, 12, d=4))
def _(p, d): return d.gt(htf("close", p.k), htf("open", p.k))


@atom("f_midday_only", FLT, "season", "Only during the midday lull.", (set(), r"lunch|midday|noon"), tw=1)
def _(p, d): return (MSO > 150) & (MSO <= 270)


# =============================================================== EXIT atoms (interpreted by the genome compiler)
# fn returns a dict understood by genome/compile_py.py; d is the trade direction helper.
EX = "EXIT"


def xatom(id, fam, desc, ev, kind, **params):
    ATOMS[id] = Atom(id, EX, fam, desc, params, None, ev)
    ATOMS[id].kind = kind


xatom("x_target_r", "trend", "Profit target at a multiple of the initial risk.", ({"strategy.exit"}, r"risk.?reward|\brr\b|r multiple"), "target",
      k=G(0.4, 0.5, 0.6, 0.8, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, d=1.0))
xatom("x_target_atr", "volexp", "Profit target at a multiple of ATR.", ({"strategy.exit", "ta.atr"}, r"take ?profit|tp"), "target",
      k=G(0.5, 0.75, 1.0, 1.5, 2.0, 3.0))
xatom("x_target_vwap", "meanrev", "Profit target at the session VWAP as it stood at the signal.", ({"ta.vwap"}, r"target|exit|take ?profit"), "target")
xatom("x_target_prior_extreme", "trend", "Profit target at the prior n-bar extreme in the trade direction.", ({"ta.highest"}, r"target|take ?profit"),
      "target", n=G(10, 20, 40))
xatom("x_target_location_level", "meanrev", "Profit target at the level supplied by the location or trigger atom.", (set(), r"target"), "target")
xatom("x_target_session_mid", "meanrev", "Profit target at the midpoint of the session range so far.", (set(), r"mid|equilibrium"), "target")
xatom("x_target_prior_close", "open", "Profit target at the prior session's close.", ({"request.security"}, r"gap fill|prev\w* close"), "target")
xatom("x_target_opposite_range_edge", "meanrev", "Profit target at the far edge of the opening range.", (set(), r"opening range"), "target", m=G(15, 30, 60))
xatom("x_time_stop", "season", "Exit after a fixed holding time in clock minutes.", (set(), r"bars? (held|since entry)|time (stop|exit)|max (bars|hold)"),
      "time", m=G(15, 30, 45, 60, 90, 120, 180, 240, d=60))
xatom("x_trail_r", "trend", "After a set favourable move, trail the stop at a fraction of the initial risk behind the best price.",
      ({"strategy.exit"}, r"trail"), "trail", start=G(0.5, 1.0, 1.5), dist=G(0.5, 0.75, 1.0, 1.5))
xatom("x_breakeven", "trend", "After a set favourable move, move the stop to the entry price.", (set(), r"break ?even|\bbe\b"), "be",
      r=G(0.5, 0.75, 1.0, 1.5))
xatom("x_partial", "trend", "Take half off at a first target and move the stop to entry; still one trade.", (set(), r"partial|tp1|scale out"),
      "partial", r=G(0.5, 0.75, 1.0, 1.5))
xatom("x_invalidate_ema", "trend", "Exit when a bar closes on the wrong side of a moving average.", ({"ta.ema", "strategy.close"}, None), "inval",
      n=G(10, 20, 34, 50))
xatom("x_invalidate_trail_flip", "trend", "Exit when the ATR-trail regime flips against the trade.", ({"ta.atr", "strategy.close"}, r"trail"), "inval")
xatom("x_invalidate_vwap", "meanrev", "Exit when a bar closes on the wrong side of VWAP.", ({"ta.vwap", "strategy.close"}, None), "inval")
xatom("x_invalidate_structure", "sweep", "Exit when a bar closes beyond the adverse extreme of the last few bars.", ({"ta.lowest", "strategy.close"}, None),
      "inval", n=G(3, 5, 8))
xatom("x_invalidate_rsi_mid", "meanrev", "Exit when RSI crosses its midline against the trade.", ({"ta.rsi", "strategy.close"}, None), "inval", n=G(7, 14, 21))
xatom("x_invalidate_supertrend", "trend", "Exit when supertrend flips against the trade.", ({"ta.supertrend", "strategy.close"}, None), "inval")
xatom("x_invalidate_macd", "trend", "Exit when MACD crosses its signal against the trade.", ({"ta.macd", "strategy.close"}, None), "inval")
xatom("x_invalidate_two_closes", "exhaust", "Exit after two consecutive closes against the trade.", ({"strategy.close"}, r"consecutive|two"), "inval")

# initial stop rules (risk slot); every stop is clamped by the structural limits of SPEC 11.2
xatom("r_stop_atr", "volexp", "Initial stop a multiple of ATR from the reference entry price.", ({"strategy.exit", "ta.atr"}, r"stop"), "stop",
      k=G(0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, d=1.25))
xatom("r_stop_signal_bar", "sweep", "Initial stop beyond the signal bar's adverse extreme plus a small ATR buffer.", ({"strategy.exit"}, r"stop.*(low|high)"),
      "stop", buf=G(0.05, 0.1, 0.25, 0.5))
xatom("r_stop_swing", "sweep", "Initial stop beyond the adverse extreme of the last n bars plus a small ATR buffer.", ({"strategy.exit", "ta.lowest"}, r"stop"),
      "stop", n=G(3, 5, 8, 12), buf=G(0.05, 0.1, 0.25, 0.5))
xatom("r_stop_level", "sweep", "Initial stop beyond the level supplied by the location or trigger atom plus a small ATR buffer.",
      ({"strategy.exit"}, r"stop.*(level|zone|support|resistance)"), "stop", buf=G(0.1, 0.25, 0.5, 0.75))
xatom("r_stop_percent", "volexp", "Initial stop a fixed fraction of price from the reference entry price.", ({"strategy.exit"}, r"stop.*(%|percent)"),
      "stop", pct=G(0.001, 0.0015, 0.002, 0.003, 0.004))
xatom("r_stop_session_extreme", "sweep", "Initial stop beyond the session's adverse extreme so far plus a small ATR buffer.",
      ({"strategy.exit"}, r"stop.*(session|day)"), "stop", buf=G(0.05, 0.1, 0.25))


def exit_inval(atom_id, p, d):
    """Invalidation condition for direction d: true on the bar whose close cancels the trade premise."""
    if atom_id == "x_invalidate_ema":
        return d.lt(C, ema(C, B(p.n)))
    if atom_id == "x_invalidate_trail_flip":
        return d.sg(trail(B(14), 3.0)) < 0
    if atom_id == "x_invalidate_vwap":
        return d.lt(C, SVWAP)
    if atom_id == "x_invalidate_structure":
        return d.lt(C, shift(d.bot(B(p.n)), 1))
    if atom_id == "x_invalidate_rsi_mid":
        return d.osc(rsi(C, B(p.n))) < 50.0
    if atom_id == "x_invalidate_supertrend":
        return d.sg(supertrend(B(10), 3.0)) < 0
    if atom_id == "x_invalidate_macd":
        m, sig = macd_lines(1)
        return d.lt(m, sig)
    if atom_id == "x_invalidate_two_closes":
        return d.lt(C, C[1]) & d.lt(C[1], C[2])
    raise KeyError(atom_id)


def target_level(atom_id, p, d, ref, risk, lvl):
    """Target price for direction d given the reference entry price, the risk distance and an optional level."""
    if atom_id == "x_target_r":
        return d.up(ref, p.k * risk)
    if atom_id == "x_target_atr":
        return d.up(ref, p.k * A)
    if atom_id == "x_target_vwap":
        return SVWAP
    if atom_id == "x_target_prior_extreme":
        return shift(d.top(B(p.n)), 1)
    if atom_id == "x_target_location_level":
        return lvl if lvl is not None else d.up(ref, risk)
    if atom_id == "x_target_session_mid":
        return (SHIGH + SLOW) / 2.0
    if atom_id == "x_target_prior_close":
        return PDC
    if atom_id == "x_target_opposite_range_edge":
        return d.orx(p.m)
    raise KeyError(atom_id)


def stop_distance(atom_id, p, d, ref, lvl):
    """Raw stop distance (positive) from the reference entry price, before the structural clamp."""
    if atom_id == "r_stop_atr":
        return p.k * A
    if atom_id == "r_stop_signal_bar":
        return d.sg(ref - d.lo) + p.buf * A
    if atom_id == "r_stop_swing":
        return d.sg(ref - d.bot(B(p.n))) + p.buf * A
    if atom_id == "r_stop_level":
        base = lvl if lvl is not None else d.lo
        return d.sg(ref - base) + p.buf * A
    if atom_id == "r_stop_percent":
        return p.pct * C
    if atom_id == "r_stop_session_extreme":
        return d.sg(ref - d.slow) + p.buf * A
    raise KeyError(atom_id)


def by_type(typ):
    return [a for a in ATOMS.values() if a.typ == typ]


def summary():
    import collections
    return {"atoms": len(ATOMS), "by_type": dict(collections.Counter(a.typ for a in ATOMS.values())),
            "by_family": dict(collections.Counter(a.fam for a in ATOMS.values()))}
