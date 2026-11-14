"""Canary features and the honeypot (SPEC 15.1, 15.2).  AUDIT-ONLY MODULE.

Search code may import `install()` (which registers ordinary-looking atoms and the store-only series
they read) but must never call `is_canary`, `canary_ids` or `HONEYPOT_ID`: those are for the audit
module and the epoch monitors only (SPEC 15.7 information firewall).

Canaries carry no information by construction:
  * seeded random walks, generated per session from (seed, session index) so that a value never
    depends on how much data is loaded;
  * a real indicator taken from a DIFFERENT session about one year away and permuted;
  * a real indicator from a different year, time-reversed.
The honeypot leaks the future on purpose (the sign of the next bar's move, lightly disguised).  It is
hazard-tagged and blocked, so a correct pipeline never uses it; the epoch self-test proves a genome
that does is voided.
"""
import numpy as np

from engine import features as F
from genome.dsl import B, C, crossover, ext, sma, w
from library.atoms import catalog as K
from library.atoms.catalog import ATOMS, Atom, G

_SEED = 90210
HONEYPOT_ID = "st_orderflow_lead"
_SPECS = [
    # id, type, family, description, series kind
    ("tr_cycle_phase_hook", "TRIGGER", "meanrev", "Cycle-phase oscillator hooks back from an extreme.", "walk"),
    ("tr_adaptive_momentum_cross", "TRIGGER", "trend", "Adaptive momentum line crosses its midline.", "walk"),
    ("tr_volume_pressure_turn", "TRIGGER", "exhaust", "Volume-pressure oscillator turns from an extreme.", "shuf"),
    ("tr_fractal_energy_break", "TRIGGER", "volexp", "Fractal energy index crosses its upper threshold.", "rev"),
    ("st_market_tide", "STATE", "trend", "Market-tide oscillator on the trade side of its midline.", "walk"),
    ("st_composite_bias", "STATE", "trend", "Composite bias index above its midline.", "shuf"),
    ("st_wave_trend_side", "STATE", "meanrev", "Wave-trend line on the trade side of its signal.", "rev"),
    ("loc_harmonic_zone", "LOCATION", "meanrev", "Harmonic-zone oscillator in its extreme band.", "walk"),
    ("loc_pressure_zone", "LOCATION", "sweep", "Pressure oscillator in its extreme band.", "shuf"),
    ("f_entropy_low", "FILTER", "volcon", "Entropy gauge below a threshold.", "walk"),
    ("f_liquidity_score_high", "FILTER", "volexp", "Liquidity score above a threshold.", "rev"),
    ("f_noise_ratio_ok", "FILTER", "season", "Noise ratio inside its normal band.", "shuf"),
]
_IDS = [s[0] for s in _SPECS]


def _walk(b, k):
    """Session-seeded mean-reverting random walk mapped to 0..100; value depends on (session, slot) only."""
    out = np.empty(b.n)
    starts = np.flatnonzero(b.first)
    ends = np.r_[starts[1:], b.n]
    for s, e in zip(starts, ends):
        rng = np.random.default_rng([_SEED, k, int(b.sess[s])])
        z = rng.standard_normal(200)
        x = np.empty(200)
        v = rng.standard_normal() * 2.0
        for i in range(200):
            v = 0.9 * v + z[i]
            x[i] = v
        out[s:e] = x[np.minimum(b.slot[s:e], 199)]
    return 50.0 + 50.0 * np.tanh(out / 3.0)


def _borrowed(b, k, reverse):
    """RSI(14) of the session 252 sessions earlier (about one year), permuted or reversed.
    The source session is unrelated to the current one, so the series carries no information about it."""
    r = F.rsi(b.c, 14)
    starts = np.flatnonzero(b.first)
    ends = np.r_[starts[1:], b.n]
    ns = len(starts)
    out = np.full(b.n, 50.0)
    for j, (s, e) in enumerate(zip(starts, ends)):
        rng = np.random.default_rng([_SEED, k, int(b.sess[s]), 7])
        src = j - 252                      # a PAST session only, so the value never depends on later data
        v = r[starts[src]:ends[src]] if src >= 0 else np.empty(0)
        v = v[~np.isnan(v)]
        if len(v) == 0:                    # first year: no source session yet, use seeded noise
            v = 50.0 + 15.0 * rng.standard_normal(100)
        v = v[::-1] if reverse else rng.permutation(v)
        idx = np.minimum(b.slot[s:e], len(v) - 1)
        out[s:e] = v[idx]
    return out


def _honeypot(b):
    nxt = np.r_[b.c[1:], b.c[-1]]
    lead = np.sign(nxt - b.c)
    lead[b.last] = 0.0
    rng = np.random.default_rng([_SEED, 999])
    return 50.0 + 20.0 * lead * (0.5 + rng.random(b.n))


class _Lazy(dict):
    """Store-only series computed on first use, so a context that never touches them pays nothing."""

    def __init__(self, b):
        super().__init__()
        self.b = b

    def __missing__(self, name):
        aid = name[3:]
        if aid == HONEYPOT_ID:
            v = _honeypot(self.b)
        else:
            k = _IDS.index(aid)
            kind = _SPECS[k][4]
            v = _walk(self.b, k) if kind == "walk" else _borrowed(self.b, k, kind == "rev")
        self[name] = v
        return v


def provider(b):
    """Store-only series for one Bars object (used as orchestrator.evaluate.EXT_PROVIDER)."""
    return _Lazy(b)


def _make(aid, typ, kind_series):
    x = ext("cx_" + aid)

    def trig(p, d):
        return crossover(d.osc(x), w(p.lvl))

    def state(p, d):
        return d.osc(x) > 50.0 + p.band

    def loc(p, d):
        return d.osc(x) < p.lvl

    def flt(p, d):
        return sma(x, B(p.n)) > p.thr

    if typ == "TRIGGER":
        return trig, {"lvl": G(20, 25, 30, 35)}
    if typ == "STATE":
        return state, {"band": G(0, 5, 10)}
    if typ == "LOCATION":
        return loc, {"lvl": G(20, 25, 30, 35)}
    return flt, {"n": G(3, 5, 8), "thr": G(40, 45, 50, 55)}


def install():
    """Register the canary atoms and the honeypot like any other atom.  Idempotent."""
    for aid, typ, fam, desc, kind in _SPECS:
        if aid not in ATOMS:
            fn, params = _make(aid, typ, kind)
            ATOMS[aid] = Atom(aid, typ, fam, desc, params, fn, (set(), None))
    if HONEYPOT_ID not in ATOMS:
        x = ext("cx_" + HONEYPOT_ID)
        a = Atom(HONEYPOT_ID, "STATE", "trend", "Order-flow lead indicator on the trade side of its midline.",
                 {"band": G(0, 5, 10)}, lambda p, d: d.osc(x) > 50.0 + p.band, (set(), None), hz=("FUTURE_OFFSET",))
        a.blocked = True                     # hazard-tagged: never offered to the search
        ATOMS[HONEYPOT_ID] = a
    from orchestrator import evaluate as EV
    EV.EXT_PROVIDER = provider


def is_canary(atom_id):
    return atom_id in _IDS


def canary_ids():
    return list(_IDS)


def genome_has_canary(g):
    from genome.genome import atom_entries
    return any(is_canary(e["atom"]) for e in atom_entries(g))
