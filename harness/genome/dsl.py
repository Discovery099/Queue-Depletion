"""Expression DSL: one definition of every technique, two back ends (SPEC 9, 13.2, 14.2).

An atom is written once as an expression tree.  `Ctx.ev` evaluates the tree on numpy arrays for
research; `Pine.em` emits Pine v6 with the same semantics for the deliverable.  The DSL has no
operation that can read the future: `shift` rejects negative lags, every rolling window ends at
the current bar, and higher-timeframe values are published only on confirmation (SPEC 14.8).
That makes most lookahead impossible to express, and the dynamic truncation audit checks the rest.

Lengths are either bar counts `B(n)` (pattern logic that is truly about bars) or clock minutes
`M(m)` (logic about time).  Minutes are converted to bars for the timeframe in use; a conversion
to fewer than 2 bars disables the atom on that timeframe (SPEC 13.2 rule 2).
"""
import math

import numpy as np

from engine import features as F


class AtomDisabled(Exception):
    """A clock-minute lookback converts to fewer than 2 bars on this timeframe."""


def B(n):
    return ("b", int(n))


def M(m):
    return ("m", float(m))


class E:
    """Expression node.  typ is 'f' (float series) or 'b' (bool series)."""
    __slots__ = ("op", "a", "typ", "_k")

    def __init__(self, op, *a, typ="f"):
        self.op, self.a, self.typ, self._k = op, a, typ, None

    def key(self):
        if self._k is None:
            self._k = self.op + "(" + ",".join(x.key() if isinstance(x, E) else repr(x) for x in self.a) + ")"
        return self._k

    # arithmetic
    def __add__(s, o): return E("add", s, w(o))
    def __radd__(s, o): return E("add", w(o), s)
    def __sub__(s, o): return E("sub", s, w(o))
    def __rsub__(s, o): return E("sub", w(o), s)
    def __mul__(s, o): return E("mul", s, w(o))
    def __rmul__(s, o): return E("mul", w(o), s)
    def __truediv__(s, o): return E("div", s, w(o))
    def __rtruediv__(s, o): return E("div", w(o), s)
    def __neg__(s): return E("neg", s)
    # comparisons (NaN compares false, like Pine na)
    def __gt__(s, o): return E("gt", s, w(o), typ="b")
    def __lt__(s, o): return E("lt", s, w(o), typ="b")
    def __ge__(s, o): return E("ge", s, w(o), typ="b")
    def __le__(s, o): return E("le", s, w(o), typ="b")
    # logic
    def __and__(s, o): return E("and", s, o, typ="b")
    def __or__(s, o): return E("or", s, o, typ="b")
    def __invert__(s): return E("not", s, typ="b")

    def __getitem__(s, k):
        return shift(s, k)


def w(x):
    return x if isinstance(x, E) else E("const", float(x))


# ---- leaves
O, H, L, C, V = (E("src", n) for n in ("open", "high", "low", "close", "volume"))
HL2 = E("src", "hl2")
HLC3 = E("src", "hlc3")
MSO = E("mso")            # minutes since the session open, measured at bar close
FIRST = E("first", typ="b")
SCOUNT = E("scount")      # bars since the session's first bar (0 on the first bar)
DOW = E("dow")            # 1 = Monday ... 5 = Friday
MINTGT = E("mintgt")      # 3 x round-trip base cost, in price units (SPEC 11.2 minimum target)
TRUE = E("true", typ="b")
FALSE = E("false", typ="b")
OC, OH, OL, OV = (E("other", n) for n in ("close", "high", "low", "volume"))   # the other instrument, same bar


def ext(name):
    """A series supplied by the feature store rather than derived from this instrument's bars."""
    return E("ext", name)


# ---- functions
def shift(x, k):
    if k < 0:
        raise ValueError("negative shift is lookahead")
    if k == 0 or x.op in ("const", "true", "false", "mintgt"):     # a constant has no history to look back into
        return x
    return E("shift", x, int(k), typ=x.typ)


def absx(x): return E("abs", w(x))
def maxx(a, b): return E("max", w(a), w(b))
def minx(a, b): return E("min", w(a), w(b))
def where(c, a, b): return E("where", c, w(a), w(b))
def nz(x, v=0.0): return E("nz", x, float(v))
def b2f(c): return E("b2f", c)
def sma(x, n): return E("sma", x, n)
def ema(x, n): return E("ema", x, n)
def rma(x, n): return E("rma", x, n)
def wma(x, n): return E("wma", x, n)
def hma(x, n): return E("hma", x, n)
def stdev(x, n): return E("stdev", x, n)
def highest(x, n): return E("highest", x, n)
def lowest(x, n): return E("lowest", x, n)
def rsum(x, n): return E("sum", x, n)
def meandev(x, n): return E("meandev", x, n)
def prank(x, n): return E("prank", x, n)
def change(x, k=1): return x - shift(x, k)
def barssince(c): return E("barssince", c)
def valuewhen(c, x): return E("valuewhen", c, x)
def atr(n): return E("atr", n)
def rsi(x, n): return E("rsi", x, n)
def scumsum(x): return E("scumsum", x)
def scummax(x): return E("scummax", x)
def scummin(x): return E("scummin", x)
def sfirst(x): return E("sfirst", x)
def prevlast(x): return E("prevlast", x)
def frozen(x, minutes): return E("frozen", x, float(minutes))
def trail(atr_len, factor): return E("trail", atr_len, float(factor))
def supertrend(n, mult): return E("supertrend", n, float(mult))
def htf(field, k): return E("htf", field, int(k))
def htfema(k, n): return E("htfema", int(k), int(n))
def htfago(k, j): return E("htfago", int(k), int(j))
def rtick(x): return E("rtick", w(x))                     # round a price to the instrument's tick grid
def sqrt(x): return E("sqrt", w(x))
def roundlvl(mult): return E("roundlvl", float(mult))     # nearest round-number level to the close
def crossover(a, b): return (w(a) > w(b)) & (shift(w(a), 1) <= shift(w(b), 1))
def crossunder(a, b): return (w(a) < w(b)) & (shift(w(a), 1) >= shift(w(b), 1))
def any_in(c, n): return rsum(b2f(c), n) > 0.5          # true if c was true in the last n bars
def vwma(x, n): return sma(x * V, n) / sma(V, n)

TR = E("tr")
SVWAP = scumsum(HLC3 * V) / scumsum(V)                    # running session VWAP
SHIGH, SLOW, SOPEN = scummax(H), scummin(L), sfirst(O)    # running session high / low, session open
PDH, PDL, PDC = prevlast(scummax(H)), prevlast(scummin(L)), prevlast(C)


# ============================================================ numpy back end
class Ctx:
    """Evaluation context for one instrument at one timeframe.  Results are cached by node key."""

    def __init__(self, bars, other=None, ext=None):
        self.b, self.other, self.ext = bars, other, ({} if ext is None else ext)
        self.cache = {}
        self._sc = None

    def n(self, ln):
        kind, v = ln
        if kind == "b":
            return v
        k = int(math.floor(v / self.b.tf + 0.5))
        if k < 2:
            raise AtomDisabled(f"{v:g} minutes is fewer than 2 bars at {self.b.tf} minutes")
        return k

    def ev(self, e):
        k = e.key()
        r = self.cache.get(k)
        if r is None:
            r = self._ev(e)
            self.cache[k] = r
        return r

    def _ev(self, e):
        b, op, a = self.b, e.op, e.a
        ev = self.ev
        if op == "src":
            n = a[0]
            if n == "hl2":
                return (b.h + b.l) / 2.0
            if n == "hlc3":
                return (b.h + b.l + b.c) / 3.0
            return {"open": b.o, "high": b.h, "low": b.l, "close": b.c, "volume": b.v}[n]
        if op == "const":
            return np.full(b.n, a[0])
        if op == "true":
            return np.ones(b.n, np.bool_)
        if op == "false":
            return np.zeros(b.n, np.bool_)
        if op == "mso":
            return b.mclose.astype(np.float64)
        if op == "mintgt":
            return np.full(b.n, 3.0 * (2.0 * 1.25 / b.pv + 2.0 * b.tick))
        if op == "first":
            return b.first
        if op == "scount":
            return F.sess_count(b.first)
        if op == "dow":
            return ((self._days(b.date.astype("int64")) + 3) % 7 + 1).astype(np.float64)   # 1 = Monday
        if op == "other":
            if self.other is None:
                return np.full(b.n, np.nan)
            return self.other[a[0]]
        if op == "ext":
            return self.ext[a[0]]
        with np.errstate(invalid="ignore", divide="ignore"):
            if op == "add":
                return ev(a[0]) + ev(a[1])
            if op == "sub":
                return ev(a[0]) - ev(a[1])
            if op == "mul":
                return ev(a[0]) * ev(a[1])
            if op == "div":
                x, y = ev(a[0]), ev(a[1])
                return np.where(y != 0, x / np.where(y != 0, y, 1.0), np.nan)
            if op == "neg":
                return -ev(a[0])
            if op == "abs":
                return np.abs(ev(a[0]))
            if op == "rtick":
                return np.floor(ev(a[0]) / b.tick + 0.5) * b.tick
            if op == "sqrt":
                x = ev(a[0])
                return np.sqrt(np.where(x >= 0, x, np.nan))
            if op == "roundlvl":
                step = 10.0 ** np.floor(np.log10(b.c)) / 100.0 * a[0]
                return np.floor(b.c / step + 0.5) * step
            if op == "max":
                x, y = ev(a[0]), ev(a[1])
                return np.where(np.isnan(x) | np.isnan(y), np.nan, np.maximum(x, y))
            if op == "min":
                x, y = ev(a[0]), ev(a[1])
                return np.where(np.isnan(x) | np.isnan(y), np.nan, np.minimum(x, y))
            if op == "gt":
                return ev(a[0]) > ev(a[1])
            if op == "lt":
                return ev(a[0]) < ev(a[1])
            if op == "ge":
                return ev(a[0]) >= ev(a[1])
            if op == "le":
                return ev(a[0]) <= ev(a[1])
        if op == "and":
            return ev(a[0]) & ev(a[1])
        if op == "or":
            return ev(a[0]) | ev(a[1])
        if op == "not":
            return ~ev(a[0])
        if op == "where":
            return np.where(ev(a[0]), ev(a[1]), ev(a[2]))
        if op == "nz":
            x = ev(a[0])
            return np.where(np.isnan(x), a[1], x)
        if op == "b2f":
            return ev(a[0]).astype(np.float64)
        if op == "shift":
            return F.shift(ev(a[0]), a[1])
        if op in ("sma", "ema", "rma", "wma", "hma", "stdev", "highest", "lowest", "sum", "meandev", "prank"):
            fn = {"sma": F.sma, "ema": F.ema, "rma": F.rma, "wma": F.wma, "hma": F.hma, "stdev": F.stdev,
                  "highest": F.highest, "lowest": F.lowest, "sum": F.rsum, "meandev": F.meandev,
                  "prank": F.percentrank}[op]
            return fn(np.ascontiguousarray(ev(a[0]), dtype=np.float64), self.n(a[1]))
        if op == "barssince":
            return F.barssince(ev(a[0]))
        if op == "valuewhen":
            return F.valuewhen(ev(a[0]), np.ascontiguousarray(ev(a[1]), dtype=np.float64))
        if op == "tr":
            return F.true_range(b.h, b.l, b.c)
        if op == "atr":
            return F.atr(b.h, b.l, b.c, self.n(a[0]))
        if op == "rsi":
            return F.rsi(np.ascontiguousarray(ev(a[0]), dtype=np.float64), self.n(a[1]))
        if op == "scumsum":
            return F.sess_cumsum(np.ascontiguousarray(ev(a[0]), dtype=np.float64), b.first)
        if op == "scummax":
            return F.sess_cummax(np.ascontiguousarray(ev(a[0]), dtype=np.float64), b.first)
        if op == "scummin":
            return F.sess_cummin(np.ascontiguousarray(ev(a[0]), dtype=np.float64), b.first)
        if op == "sfirst":
            return F.sess_first(np.ascontiguousarray(ev(a[0]), dtype=np.float64), b.first)
        if op == "prevlast":
            return F.prev_sess_last(np.ascontiguousarray(ev(a[0]), dtype=np.float64), b.first)
        if op == "frozen":
            return F.frozen_after(np.ascontiguousarray(ev(a[0]), dtype=np.float64), b.first, b.mclose, a[1])
        if op == "trail":
            n = self.n(a[0])
            raw = F.atr(b.h, b.l, b.c, n)
            _, reg = F.smart_trail(b.c, a[1] * F.ema(raw, 10), 1)
            return reg.astype(np.float64)
        if op == "supertrend":
            return F.supertrend_dir(b.h, b.l, b.c, F.atr(b.h, b.l, b.c, self.n(a[0])), a[1])
        if op == "htf":
            ho, hh, hl, hc = self._htf(a[1])
            return {"open": ho, "high": hh, "low": hl, "close": hc}[a[0]]
        if op == "htfema":
            return F.ema_on_event(b.c, F.htf_confirm(b.first, a[0]), a[1])
        if op == "htfago":
            return F.nth_event_value(b.c, F.htf_confirm(b.first, a[0]), a[1])
        raise ValueError(f"unknown op {op}")

    def _days(self, d):
        u, inv = np.unique(d, return_inverse=True)
        days = np.array([np.datetime64(f"{x // 10000:04d}-{x // 100 % 100:02d}-{x % 100:02d}") for x in u]).astype("int64")
        return days[inv]

    def _htf(self, k):
        key = ("htf", k)
        r = self.cache.get(key)
        if r is None:
            b = self.b
            r = F.htf_ohlc(b.o, b.h, b.l, b.c, b.first, k)
            self.cache[key] = r
        return r


# ============================================================ Pine v6 back end
def num(v):
    if float(v) == int(v) and abs(v) < 1e12:
        return f"{int(v)}.0"
    return repr(float(f"{v:.10g}"))


class Pine:
    """Emits Pine v6 global-scope statements for expression trees.  Every non-leaf node becomes one
    named series, so each ta.* call runs on every bar as Pine requires."""

    PREAMBLE = [
        "tfMin   = timeframe.in_seconds() / 60.0",
        "newSess = session.isfirstbar_regular",
        "var int sessOpenT = na",
        "sessOpenT := newSess ? time : sessOpenT",
        "mso     = (time_close - sessOpenT) / 60000.0",
        "minTgt  = 3.0 * (2.0 * 1.25 / syminfo.pointvalue + 2.0 * syminfo.mintick)",
        "var int sCount = 0",
        "sCount  := newSess ? 0 : sCount + 1",
    ]

    def __init__(self):
        self.lines = list(self.PREAMBLE)
        self.names = {}
        self.lens = {}
        self.mins_of = {}     # node key -> set of minute lookbacks it depends on
        self.htf_done = set()
        self.i = 0

    def new(self, prefix="x"):
        self.i += 1
        return f"{prefix}{self.i}"

    def ln(self, ln, used):
        kind, v = ln
        if kind == "b":
            return str(v)
        name = "L" + f"{v:g}".replace(".", "p")
        if name not in self.lens:
            self.lens[name] = v
            self.lines.append(f"{name} = math.max(2, math.round({num(v)} / tfMin))")
            self.lines.append(f"ok{name} = math.round({num(v)} / tfMin) >= 2")
        used.add(name)
        return name

    def em(self, e):
        """Return (pine expression name, set of minute-length names used)."""
        k = e.key()
        if k in self.names:
            return self.names[k], self.mins_of[k]
        used = set()
        name = self._em(e, used)
        self.names[k], self.mins_of[k] = name, used
        return name, used

    def _sub(self, x, used):
        n, u = self.em(x)
        used |= u
        return n

    def _em(self, e, used):
        op, a = e.op, e.a
        s = lambda x: self._sub(x, used)
        if op == "src":
            return a[0]
        if op == "const":
            return num(a[0])
        if op == "true":
            return "true"
        if op == "false":
            return "false"
        if op == "mso":
            return "mso"
        if op == "mintgt":
            return "minTgt"
        if op == "first":
            return "newSess"
        if op == "scount":
            return "sCount"
        if op == "ext":
            raise ValueError("store-only series cannot be exported to Pine")
        v = self.new()
        add = self.lines.append
        binop = {"add": "+", "sub": "-", "mul": "*", "gt": ">", "lt": "<", "ge": ">=", "le": "<=", "and": "and", "or": "or"}
        if op in binop:
            add(f"{v} = ({s(a[0])} {binop[op]} {s(a[1])})")
        elif op == "div":
            x, y = s(a[0]), s(a[1])
            add(f"{v} = ({y} != 0 ? {x} / {y} : na)")
        elif op == "neg":
            add(f"{v} = (0.0 - {s(a[0])})")
        elif op == "abs":
            add(f"{v} = math.abs({s(a[0])})")
        elif op in ("max", "min"):
            add(f"{v} = math.{op}({s(a[0])}, {s(a[1])})")
        elif op == "rtick":
            add(f"{v} = math.floor({s(a[0])} / syminfo.mintick + 0.5) * syminfo.mintick")
        elif op == "sqrt":
            x = s(a[0])
            add(f"{v} = ({x} >= 0 ? math.sqrt({x}) : na)")
        elif op == "roundlvl":
            add(f"{v}s = math.pow(10.0, math.floor(math.log10(close))) / 100.0 * {num(a[0])}")
            add(f"{v} = math.floor(close / {v}s + 0.5) * {v}s")
        elif op == "not":
            add(f"{v} = (not {s(a[0])})")
        elif op == "where":
            add(f"{v} = ({s(a[0])} ? {s(a[1])} : {s(a[2])})")
        elif op == "nz":
            add(f"{v} = nz({s(a[0])}, {num(a[1])})")
        elif op == "b2f":
            add(f"{v} = ({s(a[0])} ? 1.0 : 0.0)")
        elif op == "shift":
            add(f"{v} = {s(a[0])}[{a[1]}]")
        elif op == "dow":
            add(f"{v} = dayofweek(time, \"America/New_York\") - 1.0")
        elif op == "other":
            add(f"{v} = request.security(otherSymbol, timeframe.period, {a[0]}, lookahead = barmerge.lookahead_off)")
        elif op in ("sma", "ema", "rma", "wma", "hma", "stdev", "highest", "lowest", "sum", "meandev", "prank"):
            fn = {"sma": "ta.sma", "ema": "ta.ema", "rma": "ta.rma", "wma": "ta.wma", "hma": "ta.hma", "stdev": "ta.stdev",
                  "highest": "ta.highest", "lowest": "ta.lowest", "sum": "math.sum", "meandev": "ta.dev",
                  "prank": "ta.percentrank"}[op]
            add(f"{v} = {fn}({s(a[0])}, {self.ln(a[1], used)})")
        elif op == "barssince":
            add(f"{v} = ta.barssince({s(a[0])})")
        elif op == "valuewhen":
            add(f"{v} = ta.valuewhen({s(a[0])}, {s(a[1])}, 0)")
        elif op == "tr":
            add(f"{v} = ta.tr(true)")
        elif op == "atr":
            add(f"{v} = ta.atr({self.ln(a[0], used)})")
        elif op == "rsi":
            add(f"{v} = ta.rsi({s(a[0])}, {self.ln(a[1], used)})")
        elif op == "scumsum":
            x = s(a[0])
            add(f"var float {v} = 0.0")
            add(f"{v} := newSess ? nz({x}) : {v} + nz({x})")
        elif op in ("scummax", "scummin"):
            x = s(a[0])
            add(f"var float {v} = na")
            add(f"{v} := newSess ? {x} : math.{op[4:]}({v}, {x})")
        elif op == "sfirst":
            x = s(a[0])
            add(f"var float {v} = na")
            add(f"{v} := newSess ? {x} : {v}")
        elif op == "prevlast":
            x = s(a[0])
            add(f"var float {v} = na")
            add(f"{v} := newSess ? {x}[1] : {v}")
        elif op == "frozen":
            x = s(a[0])
            add(f"var float {v} = na")
            add(f"{v} := newSess ? na : {v}")
            add(f"{v} := na({v}) and mso >= {num(a[1])} ? {x} : {v}")
        elif op == "trail":
            n = self.ln(a[0], used)
            add(f"{v}a = ta.ema(ta.atr({n}), 10) * {num(a[1])}")
            add(f"var float {v}t = na")
            add(f"var float {v} = 0.0")
            add(f"{v}i = na({v}t) and not na({v}a)")
            add(f"{v} := {v}i ? (close > close[1] ? 1.0 : -1.0) : {v}")
            add(f"{v}t := {v}i ? close : {v}t")
            add(f"{v}f = not na({v}t) and not na({v}a) and ({v} == 1.0 ? close < math.max({v}t, close - {v}a) : close > math.min({v}t, close + {v}a))")
            add(f"{v} := {v}f ? 0.0 - {v} : {v}")
            add(f"{v}t := na({v}t) or na({v}a) ? {v}t : {v}f ? ({v} == 1.0 ? close - {v}a : close + {v}a) : ({v} == 1.0 ? math.max({v}t, close - {v}a) : math.min({v}t, close + {v}a))")
        elif op == "supertrend":
            n = self.ln(a[0], used)
            m = num(a[1])
            add(f"{v}a = ta.atr({n})")
            add(f"var float {v}u = na")
            add(f"var float {v}l = na")
            add(f"var float {v} = 0.0")
            add(f"{v}n = {v} == 0.0 and not na({v}a)")
            add(f"{v}u := na({v}a) ? {v}u : {v}n ? hl2 + {m} * {v}a : (hl2 + {m} * {v}a < {v}u or close[1] > {v}u ? hl2 + {m} * {v}a : {v}u)")
            add(f"{v}l := na({v}a) ? {v}l : {v}n ? hl2 - {m} * {v}a : (hl2 - {m} * {v}a > {v}l or close[1] < {v}l ? hl2 - {m} * {v}a : {v}l)")
            add(f"{v} := na({v}a) ? {v} : {v}n ? 1.0 : {v} == 1.0 and close < {v}l ? -1.0 : {v} == -1.0 and close > {v}u ? 1.0 : {v}")
        elif op in ("htf", "htfema", "htfago"):
            k = a[1] if op == "htf" else a[0]
            self._htf(k)
            if op == "htf":
                return f"h{k}{a[0][0]}"
            if op == "htfago":
                add(f"{v} = ta.valuewhen(h{k}conf, close, {a[1]})")
            else:
                al = num(2.0 / (a[1] + 1.0))
                add(f"var float {v} = na")
                add(f"{v} := h{k}conf ? (na({v}) ? close : {al} * close + (1.0 - {al}) * {v}) : {v}")
        else:
            raise ValueError(f"no Pine emitter for op {op}")
        return v

    def _htf(self, k):
        """Higher-timeframe bar built by counting chart bars from the session open: no request.security,
        so historical and real-time values are identical and nothing is published before the bar closes."""
        if k in self.htf_done:
            return
        self.htf_done.add(k)
        p = f"h{k}"
        self.lines += [
            f"var int {p}n = 0",
            f"{p}n := newSess ? 1 : {p}n + 1",
            f"{p}conf = {p}n % {k} == 0",
            f"var float {p}do = na",
            f"var float {p}dh = na",
            f"var float {p}dl = na",
            f"{p}do := ({p}n - 1) % {k} == 0 ? open : {p}do",
            f"{p}dh := ({p}n - 1) % {k} == 0 ? high : math.max({p}dh, high)",
            f"{p}dl := ({p}n - 1) % {k} == 0 ? low : math.min({p}dl, low)",
            f"var float {p}o = na",
            f"var float {p}h = na",
            f"var float {p}l = na",
            f"var float {p}c = na",
            f"{p}o := {p}conf ? {p}do : {p}o",
            f"{p}h := {p}conf ? {p}dh : {p}h",
            f"{p}l := {p}conf ? {p}dl : {p}l",
            f"{p}c := {p}conf ? close : {p}c",
        ]
