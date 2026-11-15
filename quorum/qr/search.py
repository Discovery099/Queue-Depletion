"""Quorum genomes: representation, evaluation on fold cells, mutation.  Used by phase 3 (search) and phase 4."""
import json

import numpy as np

from .common import SYMS, bars, atr14, fold_of_session, F, S, COSTS
from . import lc, voters
from .consensus import quorum, make_plan

FACTORS = (1.0, 1.5, 2.0, 2.5, 3.0)
STOPS = (0.75, 1.0, 1.5, 2.0, 3.0)
RS = (0.33, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0)
NBARS = (2, 4, 6, 8, 12, 24)
DISCOVER = (0, 2, 4, 6)
CONFIRM = (1, 3, 5, 7)
_ENV = {}


def env(tf=5, block="search"):
    key = (tf, block)
    if key in _ENV:
        return _ENV[key]
    e = {}
    for sym in SYMS:
        b = bars(sym, tf, block)
        names, fams, EV, ids, params = voters.build(sym, tf, block)
        base = {}
        for f in FACTORS:
            trail, reg, aL, aS = lc.smart_arrows(b, factor=f)
            base[f] = dict(trail=trail, reg=reg, bsL=F.barssince(aL), bsS=F.barssince(aS))
        fold = fold_of_session(b.sess)
        nsess = np.array([len(np.unique(b.sess[fold == k])) for k in range(8)])
        e[sym] = dict(b=b, EV=EV, atr=atr14(b), base=base, fold=fold, nsess=nsess)
    e["names"], e["fams"], e["ids"], e["params"] = names, fams, ids, params
    _ENV[key] = e
    return e


def gkey(g):
    return json.dumps([g["mode"], g["factor"], sorted(g["panel"]), g["m"], g["W"], list(g["exit"]), g["be"], g["part"]])


def signals(g, c):
    """Entry signals and plan for one instrument context."""
    bs = c["base"][g["factor"]]
    if g["mode"] == "arrow":
        baseL, baseS = bs["bsL"] <= g["W"], bs["bsS"] <= g["W"]
    else:
        baseL, baseS = bs["reg"] == 1, bs["reg"] == -1
    L, Sx = quorum(c["EV"], np.array(g["panel"], np.int64), g["W"], g["m"], True, baseL, baseS)
    return L, Sx, bs


def plan_for(g, c, L, Sx, bs):
    b = c["b"]
    ex = tuple(g["exit"])
    kw = {}
    if ex[0] == "trail":
        kw = dict(exL=bs["reg"] == -1, exS=bs["reg"] == 1, trail=bs["trail"])
    p = make_plan(b, L, Sx, ex, c["atr"], max_trades=20, cooldown=1, **kw)
    if ex[0] == "atr":
        p.be_R, p.part_R = float(g["be"]), float(g["part"])
    return p


def run(g, e, level="base", **kw):
    """Returns {sym: trade matrix}."""
    out = {}
    for sym in SYMS:
        c = e[sym]
        L, Sx, bs = signals(g, c)
        p = plan_for(g, c, L, Sx, bs)
        out[sym] = S.run(c["b"], p, COSTS[level], **kw)[0]
    return out


def cells(T, c):
    """Per-fold arrays (n, wins, gross profit, gross loss, max drawdown) in USD for one instrument."""
    b = c["b"]
    k = np.zeros((8, 5))
    if len(T) == 0:
        return k
    f = c["fold"][T[:, 1].astype(np.int64)]
    net = T[:, 13] * b.pv
    ok = f >= 0
    k[:, 0] = np.bincount(f[ok], minlength=8)
    k[:, 1] = np.bincount(f[ok], T[ok, 17], minlength=8)
    k[:, 2] = np.bincount(f[ok], np.maximum(net[ok], 0), minlength=8)
    k[:, 3] = np.bincount(f[ok], np.maximum(-net[ok], 0), minlength=8)
    return k


def cell_score(k, nsess):
    n, w, gp, gl = k[0], k[1], k[2], k[3]
    if n < 1:
        return -0.2
    k0 = 10.0 * (gp + gl) / n
    pfs = (gp + k0) / (gl + k0)
    if pfs <= 1.0:
        return pfs - 1.0
    tpd = n / nsess
    return (pfs - 1.0) * min(1.0, tpd / 5.0) ** 0.5 * min(1.0, (100.0 * w / n) / 60.0)


def fitness(g, e, folds=DISCOVER):
    """Search fitness on the given folds only.  Returns (fitness, summary dict)."""
    Ts = run(g, e)
    sc = []
    agg = np.zeros(5)
    ns = 0
    per = {}
    for sym in SYMS:
        k = cells(Ts[sym], e[sym])
        for f in folds:
            sc.append(cell_score(k[f], e[sym]["nsess"][f]))
        a = k[list(folds)].sum(0)
        per[sym] = a
        agg += a
        ns += e[sym]["nsess"][list(folds)].sum()
    sc = np.array(sc)
    n = agg[0]
    summ = dict(n=int(n), tpd=float(n / ns), wr=float(100 * agg[1] / n) if n else 0.0,
                pf=float(agg[2] / agg[3]) if agg[3] > 0 else 0.0,
                pf_es=float(per["ES"][2] / per["ES"][3]) if per["ES"][3] > 0 else 0.0,
                pf_ym=float(per["YM"][2] / per["YM"][3]) if per["YM"][3] > 0 else 0.0,
                worst_cell=float(sc.min()))
    return float(sc.mean() - 0.5 * sc.std()), summ


# ------------------------------------------------------------------ genome generation
def rand_exit(rng):
    u = rng.random()
    if u < 0.6:
        return ("atr", float(rng.choice(STOPS)), float(rng.choice(RS)), int(rng.choice((0, 12, 24))))
    if u < 0.75:
        return ("bars", int(rng.choice(NBARS)))
    if u < 0.9:
        return ("trail", int(rng.choice((0, 12, 24))))
    return ("opp",)


def rand_genome(rng, V, ids):
    k = int(rng.choice((1, 2, 2, 3, 3, 4)))
    panel = []
    while len(panel) < k:
        v = int(rng.integers(V))
        if all(ids[v] != ids[p] for p in panel):
            panel.append(v)
    return dict(mode=str(rng.choice(("arrow", "regime"))), factor=float(rng.choice(FACTORS)), panel=panel,
                m=int(rng.integers(1, k + 1)), W=int(rng.integers(0, 5)), exit=rand_exit(rng),
                be=float(rng.choice((0.0, 0.0, 0.5, 1.0))), part=float(rng.choice((0.0, 0.0, 0.5))))


def step(seq, v, rng):
    i = seq.index(v) + int(rng.choice((-1, 1)))
    return seq[min(max(i, 0), len(seq) - 1)]


def mutate(g, rng, V, ids, other=None):
    g = json.loads(json.dumps(g))
    g["exit"] = tuple(g["exit"])
    u = rng.random()
    p = g["panel"]
    if u < 0.22:                                   # swap one voter
        i = int(rng.integers(len(p)))
        for _ in range(20):
            v = int(rng.integers(V))
            if all(ids[v] != ids[q] for j, q in enumerate(p) if j != i):
                p[i] = v
                break
    elif u < 0.32 and len(p) < 4:                  # add a voter
        for _ in range(20):
            v = int(rng.integers(V))
            if all(ids[v] != ids[q] for q in p):
                p.append(v)
                break
    elif u < 0.40 and len(p) > 1:                  # drop a voter
        p.pop(int(rng.integers(len(p))))
    elif u < 0.48:
        g["m"] = g["m"] + int(rng.choice((-1, 1)))
    elif u < 0.56:
        g["W"] = min(4, max(0, g["W"] + int(rng.choice((-1, 1)))))
    elif u < 0.64:
        g["factor"] = step(FACTORS, g["factor"], rng)
    elif u < 0.68:
        g["mode"] = "regime" if g["mode"] == "arrow" else "arrow"
    elif u < 0.84:                                 # exit parameter step
        ex = list(g["exit"])
        if ex[0] == "atr":
            j = int(rng.integers(1, 4))
            ex[j] = step((STOPS, RS, (0, 12, 24))[j - 1], ex[j], rng)
        elif ex[0] == "bars":
            ex[1] = step(NBARS, ex[1], rng)
        elif ex[0] == "trail":
            ex[1] = step((0, 12, 24), ex[1], rng)
        g["exit"] = tuple(ex)
    elif u < 0.90:
        g["exit"] = rand_exit(rng)
    elif u < 0.95:
        g["be"], g["part"] = float(rng.choice((0.0, 0.5, 1.0))), float(rng.choice((0.0, 0.5)))
    elif other is not None:                        # crossover: panel from one, exits from the other
        g["exit"], g["be"], g["part"] = tuple(other["exit"]), other["be"], other["part"]
    g["m"] = min(max(1, g["m"]), len(g["panel"]))
    return g
