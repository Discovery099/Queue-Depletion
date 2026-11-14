"""Independent Pine replay (SPEC 14.4, 14.7, 18.3).

A small Pine-semantics interpreter for the subset of Pine v6 that the exporter emits in the signal
layer.  It reads the exported .pine TEXT, executes it bar by bar with its own streaming built-ins
(`ta.*`, `math.*`, history references, `var` state), and compares every order input the strategy
uses (entry signals, entry prices, stops, targets, exit signals) with the vectorised research
engine, then compares the trade lists.  It shares no code with genome/compile_py.py or with the
numba feature primitives.

Scope, stated plainly: the signal layer of the Pine file is executed from text; the order section
(strategy.entry / strategy.exit calls) is not, because TradingView's broker emulator is not
reproduced here.  Trade lists are compared by feeding the replayed series to the default engine.
"""
import math
import re
from collections import deque

import numpy as np

NAN = float("nan")
TOKEN = re.compile(r"\s*(?:(\d+\.\d+|\d+)|([A-Za-z_][\w.]*)|(\"[^\"]*\")|(<=|>=|==|!=|:=|[-+*/%<>?:()\[\],=]))")


def isna(x):
    return x is None or (isinstance(x, float) and x != x)


# ------------------------------------------------------------------ parser
class Parser:
    def __init__(self, text):
        self.t = []
        pos = 0
        text = text.strip()
        while pos < len(text):
            m = TOKEN.match(text, pos)
            if not m:
                raise SyntaxError(f"cannot tokenise: {text[pos:pos + 30]!r}")
            pos = m.end()
            num, ident, s, op = m.groups()
            self.t.append(("num", float(num)) if num else ("id", ident) if ident else ("str", s[1:-1]) if s is not None else ("op", op))
        self.i = 0

    def peek(self, kind=None, val=None):
        if self.i >= len(self.t):
            return False
        k, v = self.t[self.i]
        return (kind is None or k == kind) and (val is None or v == val)

    def eat(self, kind=None, val=None):
        if not self.peek(kind, val):
            raise SyntaxError(f"expected {val or kind} at token {self.i}: {self.t[self.i:self.i + 3]}")
        self.i += 1
        return self.t[self.i - 1][1]

    def expr(self):
        c = self.or_()
        if self.peek("op", "?"):
            self.eat()
            a = self.expr()
            self.eat("op", ":")
            return ("if", c, a, self.expr())
        return c

    def or_(self):
        a = self.and_()
        while self.peek("id", "or"):
            self.eat()
            a = ("or", a, self.and_())
        return a

    def and_(self):
        a = self.not_()
        while self.peek("id", "and"):
            self.eat()
            a = ("and", a, self.not_())
        return a

    def not_(self):
        if self.peek("id", "not"):
            self.eat()
            return ("not", self.not_())
        return self.cmp()

    def cmp(self):
        a = self.add()
        if self.peek("op") and self.t[self.i][1] in ("<", ">", "<=", ">=", "==", "!="):
            op = self.eat()
            return ("cmp", op, a, self.add())
        return a

    def add(self):
        a = self.mul()
        while self.peek("op") and self.t[self.i][1] in ("+", "-"):
            op = self.eat()
            a = ("bin", op, a, self.mul())
        return a

    def mul(self):
        a = self.unary()
        while self.peek("op") and self.t[self.i][1] in ("*", "/", "%"):
            op = self.eat()
            a = ("bin", op, a, self.unary())
        return a

    def unary(self):
        if self.peek("op", "-"):
            self.eat()
            return ("bin", "-", ("num", 0.0), self.unary())
        return self.postfix()

    def postfix(self):
        a = self.primary()
        while self.peek("op", "["):
            self.eat()
            k = int(self.eat("num"))
            self.eat("op", "]")
            if a[0] != "var":
                raise SyntaxError("history reference on a non-variable")
            a = ("hist", a[1], k)
        return a

    def primary(self):
        if self.peek("num"):
            return ("num", self.eat())
        if self.peek("str"):
            return ("str", self.eat())
        if self.peek("op", "("):
            self.eat()
            e = self.expr()
            self.eat("op", ")")
            return e
        name = self.eat("id")
        if self.peek("op", "("):
            self.eat()
            args = []
            while not self.peek("op", ")"):
                if self.peek("id") and self.i + 1 < len(self.t) and self.t[self.i + 1] == ("op", "="):
                    self.eat()
                    self.eat()
                    self.expr()                       # named arguments (lookahead = ...) carry no value we need
                else:
                    args.append(self.expr())
                if self.peek("op", ","):
                    self.eat()
            self.eat("op", ")")
            return ("call", name, args, [None])       # last slot: per-call-site state
        return ("var", name)


def parse_signal_layer(src):
    """Statements between the signal-layer and order-layer markers of an exported file."""
    body = src.split("// ---- Signal layer")[1].split("// ---- Order layer")[0]
    out = []
    for ln in body.splitlines()[1:]:
        ln = ln.strip()
        if not ln or ln.startswith("//"):
            continue
        m = re.match(r"(?:(var)\s+(?:float|int|bool)\s+)?([A-Za-z_]\w*)\s*(:=|=)\s*(.*)$", ln)
        if not m:
            raise SyntaxError(f"unsupported statement: {ln}")
        out.append({"var": bool(m.group(1)), "name": m.group(2), "reassign": m.group(3) == ":=", "expr": Parser(m.group(4)).expr()})
    return out


def order_inputs(src):
    """Names of the series the order section reads, recovered from the Pine text."""
    w = re.search(r"wantL = (\w+) and not (\w+) and", src)
    stops = re.findall(r"curStop := (\w+)\n", src)
    tgts = re.findall(r"curTgt  := (\w+)\n", src)
    refs = re.findall(r"strategy\.entry\([^\n]*?(?:limit|stop) = (\w+),", src)
    ex = re.search(r"if \(inLong and (\w+)\) or \(inShort and (\w+)\)", src)
    return {"sigL": w.group(1), "sigS": w.group(2), "stpL": stops[-2], "stpS": stops[-1], "tgtL": tgts[-2], "tgtS": tgts[-1],
            "epxL": refs[0] if refs else None, "epxS": refs[1] if len(refs) > 1 else None, "exL": ex.group(1), "exS": ex.group(2)}


# ------------------------------------------------------------------ streaming built-ins (own implementations)
class Roll:
    def __init__(self, n):
        self.n, self.q = int(n), deque(maxlen=int(n))

    def push(self, x):
        self.q.append(x)
        return len(self.q) == self.n and not any(isna(v) for v in self.q)


def _sma(st, x, n):
    st[0] = st[0] or Roll(n)
    return sum(st[0].q) / st[0].n if st[0].push(x) else NAN


def _recursive(st, x, n, alpha):
    if st[0] is None:
        st[0] = {"v": NAN, "s": 0.0, "c": 0}
    s = st[0]
    n = int(n)
    if isna(s["v"]):
        if isna(x):
            s["s"], s["c"] = 0.0, 0
        else:
            s["s"] += x
            s["c"] += 1
            if s["c"] == n:
                s["v"] = s["s"] / n
        return s["v"]
    if not isna(x):
        s["v"] = alpha * x + (1 - alpha) * s["v"]
    return s["v"]


def _wma_of(r):
    n = r.n
    return sum(v * (i + 1) for i, v in enumerate(r.q)) / (n * (n + 1) / 2.0)


def _wma(st, x, n):
    st[0] = st[0] or Roll(n)
    return _wma_of(st[0]) if st[0].push(x) else NAN


def _hma(st, x, n):
    n = int(n)
    if st[0] is None:
        st[0] = (Roll(max(1, n // 2)), Roll(n), Roll(max(1, int(math.floor(math.sqrt(n))))))
    a, b, c = st[0]
    oka, okb = a.push(x), b.push(x)
    d = 2.0 * _wma_of(a) - _wma_of(b) if oka and okb else NAN
    return _wma_of(c) if c.push(d) else NAN


def _stdev(st, x, n):
    st[0] = st[0] or Roll(n)
    if not st[0].push(x):
        return NAN
    mu = sum(st[0].q) / st[0].n
    return math.sqrt(sum((v - mu) ** 2 for v in st[0].q) / st[0].n)


def _dev(st, x, n):
    st[0] = st[0] or Roll(n)
    if not st[0].push(x):
        return NAN
    mu = sum(st[0].q) / st[0].n
    return sum(abs(v - mu) for v in st[0].q) / st[0].n


def _highest(st, x, n):
    st[0] = st[0] or Roll(n)
    return max(st[0].q) if st[0].push(x) else NAN


def _lowest(st, x, n):
    st[0] = st[0] or Roll(n)
    return min(st[0].q) if st[0].push(x) else NAN


def _sum(st, x, n):
    st[0] = st[0] or Roll(n)
    return sum(st[0].q) if st[0].push(x) else NAN


def _prank(st, x, n):
    st[0] = st[0] or deque(maxlen=int(n) + 1)
    q = st[0]
    q.append(x)
    if len(q) <= int(n) or any(isna(v) for v in q):
        return NAN
    prev = list(q)[:-1]
    return 100.0 * sum(1 for v in prev if v <= x) / int(n)


def _barssince(st, c):
    if c:
        st[0] = 0
    elif st[0] is not None:
        st[0] += 1
    return NAN if st[0] is None else float(st[0])


def _valuewhen(st, c, x, k):
    st[0] = st[0] if st[0] is not None else deque(maxlen=int(k) + 1)
    if c:
        st[0].appendleft(x)
    return st[0][int(k)] if len(st[0]) > int(k) else NAN


class Replay:
    def __init__(self, stmts, b, other):
        self.stmts, self.b, self.other = stmts, b, other
        self.hist = {s["name"]: [] for s in stmts}
        self.env = {}
        self.i = 0
        self.days = (np.array([np.datetime64(f"{d // 10000:04d}-{d // 100 % 100:02d}-{d % 100:02d}") for d in b.date.tolist()]).astype("int64") + 3) % 7 + 1

    def var(self, name, back=0):
        i, b = self.i - back, self.b
        if name in self.hist:
            h = self.hist[name]
            if back == 0:
                return self.env.get(name, NAN)
            return h[i] if 0 <= i < len(h) else NAN
        if i < 0:
            return NAN
        if name == "close":
            return b.c[i]
        if name == "open":
            return b.o[i]
        if name == "high":
            return b.h[i]
        if name == "low":
            return b.l[i]
        if name == "volume":
            return b.v[i]
        if name == "hl2":
            return (b.h[i] + b.l[i]) / 2.0
        if name == "hlc3":
            return (b.h[i] + b.l[i] + b.c[i]) / 3.0
        if name == "time":
            return float(b.ts[i]) / 1e6
        if name == "time_close":
            return float(b.ts[i]) / 1e6 + (b.mclose[i] - b.mopen[i]) * 60000.0
        if name == "session.isfirstbar_regular":
            return bool(b.first[i])
        if name == "syminfo.mintick":
            return b.tick
        if name == "syminfo.pointvalue":
            return b.pv
        if name == "na":
            return NAN
        if name == "true":
            return True
        if name == "false":
            return False
        raise NameError(name)

    def ev(self, e):
        k = e[0]
        if k == "num":
            return e[1]
        if k == "var":
            return self.var(e[1])
        if k == "hist":
            return self.var(e[1], e[2])
        if k == "if":
            return self.ev(e[2]) if self.ev(e[1]) else self.ev(e[3])
        if k == "or":
            return bool(self.ev(e[1])) or bool(self.ev(e[2]))
        if k == "and":
            return bool(self.ev(e[1])) and bool(self.ev(e[2]))
        if k == "not":
            return not self.ev(e[1])
        if k == "cmp":
            a, c = self.ev(e[2]), self.ev(e[3])
            if isna(a) or isna(c):
                return False
            return {"<": a < c, ">": a > c, "<=": a <= c, ">=": a >= c, "==": a == c, "!=": a != c}[e[1]]
        if k == "bin":
            a, c = self.ev(e[2]), self.ev(e[3])
            if isna(a) or isna(c):
                return NAN
            op = e[1]
            if op == "+":
                return a + c
            if op == "-":
                return a - c
            if op == "*":
                return a * c
            if op == "/":
                return a / c if c != 0 else NAN
            return float(int(a) % int(c))
        if k == "call":
            return self.call(e)
        raise ValueError(k)

    def call(self, e):
        name, args, st = e[1], e[2], e[3]
        a = [self.ev(x) for x in args] if name != "request.security" else None
        if name == "ta.sma":
            return _sma(st, a[0], a[1])
        if name == "ta.ema":
            return _recursive(st, a[0], a[1], 2.0 / (a[1] + 1.0))
        if name == "ta.rma":
            return _recursive(st, a[0], a[1], 1.0 / a[1])
        if name == "ta.wma":
            return _wma(st, a[0], a[1])
        if name == "ta.hma":
            return _hma(st, a[0], a[1])
        if name == "ta.stdev":
            return _stdev(st, a[0], a[1])
        if name == "ta.dev":
            return _dev(st, a[0], a[1])
        if name == "ta.highest":
            return _highest(st, a[0], a[1])
        if name == "ta.lowest":
            return _lowest(st, a[0], a[1])
        if name == "math.sum":
            return _sum(st, a[0], a[1])
        if name == "ta.percentrank":
            return _prank(st, a[0], a[1])
        if name == "ta.barssince":
            return _barssince(st, bool(a[0]))
        if name == "ta.valuewhen":
            return _valuewhen(st, bool(a[0]), a[1], a[2])
        if name in ("ta.tr", "ta.atr"):
            i, b = self.i, self.b
            tr = b.h[i] - b.l[i] if i == 0 else max(b.h[i] - b.l[i], abs(b.h[i] - b.c[i - 1]), abs(b.l[i] - b.c[i - 1]))
            return tr if name == "ta.tr" else _recursive(st, tr, a[0], 1.0 / a[0])
        if name == "ta.rsi":
            if st[0] is None:
                st[0] = {"p": NAN, "u": [None], "d": [None]}
            s = st[0]
            x = a[0]
            ch = NAN if isna(s["p"]) or isna(x) else x - s["p"]
            s["p"] = x
            up = _recursive(s["u"], NAN if isna(ch) else max(ch, 0.0), a[1], 1.0 / a[1])
            dn = _recursive(s["d"], NAN if isna(ch) else max(-ch, 0.0), a[1], 1.0 / a[1])
            if isna(up):
                return NAN
            if dn == 0:
                return 50.0 if up == 0 else 100.0
            return 100.0 - 100.0 / (1.0 + up / dn)
        if name == "nz":
            return a[1] if isna(a[0]) else a[0]
        if name == "na":
            return isna(a[0])
        if name == "math.max":
            return NAN if isna(a[0]) or isna(a[1]) else max(a[0], a[1])
        if name == "math.min":
            return NAN if isna(a[0]) or isna(a[1]) else min(a[0], a[1])
        if name == "math.abs":
            return NAN if isna(a[0]) else abs(a[0])
        if name == "math.sqrt":
            return NAN if isna(a[0]) or a[0] < 0 else math.sqrt(a[0])
        if name == "math.floor":
            return NAN if isna(a[0]) else float(math.floor(a[0]))
        if name == "math.ceil":
            return NAN if isna(a[0]) else float(math.ceil(a[0]))
        if name == "math.round":
            return NAN if isna(a[0]) else float(math.floor(a[0] + 0.5))
        if name == "math.pow":
            return a[0] ** a[1]
        if name == "math.log10":
            return math.log10(a[0])
        if name == "timeframe.in_seconds":
            return self.b.tf * 60.0
        if name == "dayofweek":
            return float(self.days[self.i]) + 1.0
        if name == "request.security":
            field = args[2][1]
            return float(self.other[field][self.i])
        raise NameError(name)

    def run(self):
        b = self.b
        for i in range(b.n):
            self.i = i
            for s in self.stmts:
                nm = s["name"]
                if s["var"]:
                    if i == 0:
                        self.env[nm] = self.ev(s["expr"])
                    continue
                self.env[nm] = self.ev(s["expr"])
            for nm, h in self.hist.items():
                h.append(self.env.get(nm, NAN))
        return self.hist


# ------------------------------------------------------------------ parity check
def parity(g, src, sessions=120, warm=40, tfs=None, seed=0):
    """Compare the replayed Pine signal layer with the research engine on `sessions` research sessions
    per instrument at two timeframes (SPEC 18.3).  Returns {'match': bool, 'details': [...]}."""
    from engine import sim
    from genome import compile_py
    from genome.dsl import Ctx
    from orchestrator import evaluate as EV
    stmts_src = src
    names = order_inputs(src)
    tf0 = g["primary_timeframe_min"]
    tfs = tfs or [tf0, 15 if tf0 != 15 else 5]
    rng = np.random.default_rng([4711, seed])
    out = {"match": True, "details": [], "vanished": 0, "late": 0, "sessions_per_instrument": sessions, "timeframes": tfs}
    for tf in tfs:
        start = int(rng.integers(100, EV.N_SEARCH - sessions - warm - 1))
        for sym in EV.INSTRUMENTS:
            full = EV.bars_for(sym, tf)
            ofull = EV.other_arrays(full, EV.bars_for("YM" if sym == "ES" else "ES", tf))
            m = (full.sess >= start) & (full.sess < start + warm + sessions)
            b = EV.subset(full, m)
            other = {k: v[m] for k, v in ofull.items()}
            plan, aux = compile_py.to_plan(g, Ctx(b, other=other))
            hist = Replay(parse_signal_layer(stmts_src), b, other).run()
            chk = b.sess >= start + warm
            rp = plan.copy()
            bad = []
            for field, nm in names.items():
                if nm is None or nm in ("na", "false", "true"):
                    continue
                vec = getattr(plan, field)
                rep = np.array(hist[nm], dtype=vec.dtype if vec.dtype == np.bool_ else float)
                if vec.dtype == np.bool_:
                    diff = (vec != rep) & chk
                    if field in ("sigL", "sigS"):
                        out["vanished"] += int((rep & ~vec & chk).sum())
                        out["late"] += int((vec & ~rep & chk).sum())
                else:
                    live = chk & (plan.sigL if field.endswith("L") else plan.sigS)      # prices matter where an order is placed
                    with np.errstate(invalid="ignore"):
                        diff = live & ~((np.isnan(vec) & np.isnan(rep)) | (np.abs(vec - rep) <= 1e-9 * np.maximum(1.0, np.abs(vec))))
                if diff.any():
                    bad.append({"series": field, "pine_name": nm, "first_bar": int(np.flatnonzero(diff)[0]), "count": int(diff.sum())})
                setattr(rp, field, rep)
            Tv, *_ = sim.run(b, plan, EV.COSTS["base"])
            Tr, *_ = sim.run(b, rp, EV.COSTS["base"])
            kv = Tv[b.sess[Tv[:, sim.C["entry_idx"]].astype(int)] >= start + warm] if len(Tv) else Tv
            kr = Tr[b.sess[Tr[:, sim.C["entry_idx"]].astype(int)] >= start + warm] if len(Tr) else Tr
            same = kv.shape == kr.shape and bool(np.allclose(kv[:, :9], kr[:, :9], atol=1e-9, equal_nan=True))
            out["details"].append({"instrument": sym, "timeframe": tf, "first_session": start + warm, "bars_checked": int(chk.sum()),
                                   "series_mismatches": bad, "trades_engine": int(len(kv)), "trades_replay": int(len(kr)), "trade_lists_equal": same})
            out["match"] = out["match"] and not bad and same
    out["scope"] = ("Signal layer of the Pine file executed from text by an independent interpreter; order section not executed "
                    "(TradingView's broker emulator is not reproduced). Trade lists compared by feeding both signal sets to the default engine.")
    return out
