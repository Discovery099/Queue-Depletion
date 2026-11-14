"""Audit of the auditors (SPEC 14.9, 7.8 item 3, 15.2): deliberately broken strategies, one per hazard
tag in SPEC 8.4 plus a selection leak, an intrabar-optimistic strategy and a full-series
normalisation.  Every audit run starts by confirming that all planted defects are still caught.
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from audit import canary, static_audit, truncation  # noqa: E402
from engine import features as F  # noqa: E402
from genome import compile_py, genome as GN  # noqa: E402
from genome.dsl import B, C, H, L, Ctx, ext, shift, sma  # noqa: E402
from genome.genome import A, new_genome  # noqa: E402
from orchestrator import evaluate as EV  # noqa: E402

canary.install()


@pytest.fixture(scope="module")
def bars():
    b = EV.bars_for("ES", 5)
    return EV.subset(b, b.sess >= EV.N_SEARCH - 40)


# ---- planted dynamic defects: each is a store series that uses the future in the way the tag describes
def _defects(b):
    n = b.n
    sess_hi = np.empty(n)
    sess_cl = np.empty(n)
    starts = np.flatnonzero(b.first)
    ends = np.r_[starts[1:], n]
    for s, e in zip(starts, ends):
        sess_hi[s:e] = b.h[s:e].max()          # the session's FINAL high, known only at the close
        sess_cl[s:e] = b.c[e - 1]              # the session's FINAL close
    piv = np.zeros(n)
    for i in range(3, n - 3):
        if b.h[i] == b.h[i - 3:i + 4].max():
            piv[i] = 1.0                       # pivot marked AT the pivot bar: needs 3 future bars
    zz = np.empty(n)
    for i in range(n):                         # regression over a window that includes later bars
        zz[i] = b.c[max(0, i - 10):min(n, i + 11)].mean()
    fut = np.r_[b.c[2:], b.c[-1], b.c[-1]]     # plot/series shifted backwards in time
    win = np.zeros(n)                          # a signal kept only if the NEXT bars proved it right
    win[:-5] = (b.c[5:] > b.c[:-5]).astype(float)
    rt = np.zeros(n)                           # "realtime" value: differs on the last (live) bar
    rt[-1] = 1.0
    htf = np.empty(n)                          # security with lookahead on: the unfinished 12-bar bar's close
    cnt = F.sess_count(b.first).astype(int)
    for i in range(n):
        j = min(ends[np.searchsorted(starts, i, side="right") - 1] - 1, i + (11 - cnt[i] % 12))
        htf[i] = b.c[j]
    z = (b.c - b.c.mean()) / b.c.std()         # full-series normalisation
    intra = np.where(b.c > b.o, b.h, b.l)      # depends on intrabar order the data does not contain; also future-free
    return {"SECURITY_LOOKAHEAD": htf, "PIVOT_UNCONFIRMED": piv, "REALTIME_REPAINT": rt, "FUTURE_OFFSET": fut,
            "ZIGZAG_RECALC": zz, "HTF_CLOSE_INTRABAR": sess_cl, "SESSION_VALUE_LEAK": sess_hi,
            "REPEATED_SIGNAL_DELETE": win, "FULL_SERIES_NORMALISATION": z, "SELECTION_LEAK": np.full(n, np.percentile(b.c, 80))}


DYNAMIC = ["SECURITY_LOOKAHEAD", "PIVOT_UNCONFIRMED", "REALTIME_REPAINT", "FUTURE_OFFSET", "ZIGZAG_RECALC", "HTF_CLOSE_INTRABAR",
           "SESSION_VALUE_LEAK", "REPEATED_SIGNAL_DELETE", "FULL_SERIES_NORMALISATION", "SELECTION_LEAK"]


@pytest.mark.parametrize("tag", DYNAMIC)
def test_truncation_audit_catches_planted_defect(bars, tag):
    prov = lambda b: {"defect": _defects(b)[tag]}   # noqa: E731
    r = truncation.audit_expr(ext("defect"), bars, None, prov, n=60, seed=1)   # the audit compares the value itself
    assert not r["clean"], tag


def test_truncation_audit_passes_a_causal_feature(bars):
    assert truncation.audit_expr(C > sma(C, B(20)), bars, None, None, n=60, seed=1)["clean"]
    assert truncation.audit_expr(shift(H, 3) > shift(L, 5), bars, None, None, n=60, seed=1)["clean"]


def test_leaked_next_close_feature_is_detected_in_a_full_genome(bars):
    """SPEC 7.8 item 3: a strategy using next bar's close is detected by the truncation audit."""
    g = new_genome([A("tr_ema_cross")], regime=[{"atom": canary.HONEYPOT_ID, "params": {"band": 0}}])
    r = truncation.audit(g, bars, None, canary.provider, n=40, seed=2)
    assert not r["clean"] and canary.HONEYPOT_ID in r["first_divergence"]["feature"]


def test_clean_genome_passes_truncation(bars):
    g = new_genome([A("tr_sweep_prior_day")], regime=[A("st_htf_bar_dir")], location=[A("loc_vwap_band")],
                   stop=A("r_stop_swing"), exits=[A("x_target_vwap"), A("x_invalidate_ema")])
    full = EV.bars_for("ES", 5)
    ob = EV.bars_for("YM", 5)
    m = full.sess >= EV.N_SEARCH - 40
    oth = {k: v[m] for k, v in EV.other_arrays(full, ob).items()}
    r = truncation.audit(g, bars, oth, canary.provider, n=40, seed=3)
    assert r["clean"], r


def test_dsl_cannot_express_a_negative_shift():
    with pytest.raises(ValueError):
        shift(C, -1)
    with pytest.raises(ValueError):
        F.shift(np.arange(5.0), -1)


# ---- static audit
def test_honeypot_genome_is_voided_by_the_static_audit():
    g = new_genome([A("tr_ema_cross")], regime=[{"atom": canary.HONEYPOT_ID, "params": {"band": 0}}])
    a = static_audit.audit(g, compile_py.python_source(g))
    assert not a["clean"] and any(h["rule"] == "hazard_tagged_atom" for h in a["hits"])


def test_clean_genome_passes_static_audit():
    g = new_genome([A("tr_rsi_hook")], location=[A("loc_vwap_band")])
    a = static_audit.audit(g, compile_py.python_source(g))
    assert a["clean"], a["hits"]


@pytest.mark.parametrize("src,rule", [
    ("x = close.shift(-1)", "negative_shift"),
    ("y = shift(c, -2)", "negative_shift"),
    ("m = s.rolling(5, center=True).mean()", "centred_window"),
    ("v = c[i + 1]", "forward_index"),
    ("z = (c - c.mean()) / c.std()", "whole_series_statistic"),
    ("thr = np.percentile(c, 80)", "whole_series_statistic"),
    ("df = pd.read_parquet('data/vault/ES.parquet')", "vault_reference"),
    ("if date == 20200316: skip = True", "date_literal"),
    ("if close > 4350.25: go = True", "price_level_literal"),
])
def test_static_python_rules(src, rule):
    assert rule in [h["rule"] for h in static_audit.scan_python(src)]


@pytest.mark.parametrize("src,rule", [
    ('x = request.security(syminfo.tickerid, "60", close, lookahead = barmerge.lookahead_on)', "security_lookahead_on"),
    ('x = request.security(syminfo.tickerid, "60", close)', "security_without_lookahead_off"),
    ("if barstate.isrealtime\n    a = 1", "realtime_branch"),
    ('strategy("s", calc_on_every_tick=true)', "calc_on_every_tick"),
    ('strategy("s", calc_on_order_fills=true)', "calc_on_order_fills"),
    ("plot(close, offset=-5)", "negative_offset"),
    ("varip int n = 0", "varip"),
    ('strategy("s", use_bar_magnifier=true)', "bar_magnifier"),
    ('ok = timeframe.period == "5"', "timeframe_condition"),
    ('if cond\n    strategy.entry("L", strategy.long)', "orders_without_isconfirmed"),
    ('x = barstate.islast ? 1 : 0', "islast_outside_display"),
])
def test_static_pine_rules(src, rule):
    assert rule in [h["rule"] for h in static_audit.scan_pine(src)]


def test_parameter_precision_and_grid_rules():
    g = new_genome([A("tr_rsi_hook")])
    g["slots"]["trigger"]["atoms"][0]["params"]["lvl"] = 31.4159
    hits = [h["rule"] for h in static_audit.scan_genome(GN.finalize(g))]
    assert "genome_invalid" in hits and "parameter_over_4_significant_digits" in hits


def test_complexity_ceiling_enforced():
    g = new_genome([A("tr_rsi_hook"), A("tr_sweep_swing")], regime=[A("st_adx_trend"), A("st_ema_stack")],
                   location=[A("loc_bollinger_outer"), A("loc_keltner_outer")], filters=[A("f_relative_volume_high"), A("f_atr_rank_high")])
    assert g["complexity"] > 22 and any(h["rule"] in ("complexity_over_budget", "genome_invalid") for h in static_audit.scan_genome(g))


# ---- intrabar-optimistic strategy: a tight target inside a wide stop depends on the unknown intrabar order
def test_intrabar_optimism_is_measurable():
    g = new_genome([A("tr_momentum_bar", k=1.5)], stop=A("r_stop_atr", k=0.5), exits=[A("x_target_atr", k=0.5)])
    pes = EV.run(g, "ES", 5)["trades"]
    opt = EV.run(g, "ES", 5, optimistic=True)["trades"]
    assert len(pes) > 200
    assert opt["is_win"].mean() - pes["is_win"].mean() > 0.02     # the audit's gap is real and one-sided
    assert (opt["is_win"].mean() >= pes["is_win"].mean())


# ---- canaries carry no forward information and are stable under truncation
def test_canary_series_do_not_depend_on_loaded_data_length(bars):
    full = canary.provider(bars)
    cut = canary.provider(truncation.truncate(bars, bars.n // 2))
    for aid in canary.canary_ids():
        k = "cx_" + aid
        assert np.allclose(full[k][: bars.n // 2 + 1], cut[k], equal_nan=True), aid
    assert len(canary.canary_ids()) == 12
