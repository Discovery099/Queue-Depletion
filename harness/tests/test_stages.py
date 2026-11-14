"""Mechanics of stages 2, 3 and 4 (quick settings).  These tests check that every gate is produced and
that integrity failures are routed correctly; they do not select or rank any strategy.
Stage 4 is exercised on a decoy market so the real inner holdout is not opened by a test."""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from audit import canary  # noqa: E402
from engine import decoys  # noqa: E402
from gates import stage2 as S2, stage3 as S3, stats  # noqa: E402
from genome.genome import A, new_genome  # noqa: E402
from orchestrator import evaluate as EV  # noqa: E402

canary.install()
G_PLAIN = new_genome([A("tr_sweep_prior_day")], regime=[A("st_vwap_side")], stop=A("r_stop_signal_bar"), exits=[A("x_target_r", k=1.0)], tf=15)


def test_stage2_fails_a_canary_genome_first():
    g = new_genome([A("tr_cycle_phase_hook")])
    r = S2.stage2(g, 1, quick=True)
    assert not r["passed"] and r["failed_reason"] == "CANARY" and len(r["gates"]) == 1


def test_stage2_voids_a_lookahead_genome():
    g = new_genome([A("tr_ema_cross")], regime=[{"atom": canary.HONEYPOT_ID, "params": {"band": 0}}])
    r = S2.stage2(g, 1, quick=True)
    assert r["void"] and r["failed_reason"].startswith("LOOKAHEAD")


@pytest.fixture(scope="module")
def s2():
    calls = []
    r = S2.stage2(G_PLAIN, 1, quick=True, log=lambda label, n: calls.append((label, n)))
    return r, calls


def test_stage2_produces_every_gate_and_section(s2):
    r, calls = s2
    names = {x["gate"] for x in r["gates"]}
    for need in ("s2.truncation_audit_clean", "s2.intrabar_win_rate_gap_pts", "s2.core_timeframes_passing", "s2.worst_timeframe_pf",
                 "s2.timeframe_pf_cv", "s2.stress_cost_pf", "s2.weaker_side_pf", "s2.drift_neutral_expectancy_retention",
                 "s2.inverted_market_pf", "s2.zero_shot_transfer_retention", "s2.synthetic_relatives_profitable",
                 "s2.plateau_one_step_pass_share", "s2.peak_excess_over_neighbourhood", "s2.median_decoy_pf", "s2.alpha_gap_real_minus_decoy_pts"):
        assert need in names, need
    for sec in ("truncation", "intrabar", "selection_leak", "timeframes", "stress_costs", "long_short", "drift_neutral", "inverted_market",
                "transfer", "divergence_days", "synthetic_relatives", "parameter_robustness", "ablation", "pbo", "cpcv", "decoys"):
        assert sec in r["sections"], sec
    assert set(r["sections"]["timeframes"]) == {5, 10, 15, 30, 60}
    assert r["sections"]["truncation"]["ES"]["clean"] and not r["passed"]        # an ordinary rule set does not pass
    assert sum(n for _, n in calls) > 100                                         # every backtest block was announced for the ledger
    assert not EV.FRAME_OVERRIDE                                                  # research data restored after decoys


def test_stage3_and_red_team_mechanics():
    info = {"n_eff": 50, "var_sharpe": 0.01, "raw": 1000, "family_daily": np.random.default_rng(0).normal(0, 100, (5, len(EV.fold_sessions(EV.TEST_FOLDS))))}
    r = S3.stage3(G_PLAIN, 1, "silver", info, quick=True)
    names = {x["gate"] for x in r["gates"]}
    for need in ("s3.red_team_unbroken", "s3.deflated_sharpe_probability", "s3.deflated_win_rate_alpha", "s3.reality_check_p_value",
                 "s3.bootstrap_pf_p5", "s3.entry_permutation_above_p99", "s3.session_shuffle_relative_change", "s3.start_point_pf_cv",
                 "s3.profitable_rolling_6_month_windows", "s3.worst_regime_cell_pf", "s3.hidden_timeframes_passing", "s3.shock_cost_net"):
        assert need in names, need
    rt = r["sections"]["red_team"]
    assert rt["backtests"] <= rt["budget"] and len(rt["attacks"]) >= 10 and not r["passed"]
    assert len(S3.hidden_timeframes(G_PLAIN)) == 3 and S3.hidden_timeframes(G_PLAIN) == S3.hidden_timeframes(G_PLAIN)


def test_stage4_runs_on_a_decoy_holdout_and_clears_caches():
    with S2.frames(decoys.decoy("model", 1)):
        r = S3.stage4(G_PLAIN, 1, "bronze", 1.0)
    assert r["sessions"] == 168 and not r["passed"] and "s4.win_rate_alpha_pts" in r["failed_gates"]
    assert abs(r["alpha_pts"]) < 6                       # no edge on a decoy


def test_statistics():
    rng = np.random.default_rng(1)
    noise = rng.normal(0, 1, (40, 16))
    assert 0.3 < stats.pbo_cscv(noise, seed=1)["pbo"] < 0.7                       # pure noise: best in-sample is a coin flip out of sample
    skill = noise + np.linspace(0, 3, 40)[:, None]
    assert stats.pbo_cscv(skill, seed=1)["pbo"] < 0.1
    d = rng.normal(0.02, 1, 700)
    assert stats.deflated_sharpe(d, 1000, 0.002)[0] < 0.6 < stats.deflated_sharpe(rng.normal(0.25, 1, 700), 1000, 0.002)[0]
    assert stats.benjamini_hochberg([0.001, 0.2, 0.004, 0.9], 0.10) == [0, 2]
    x = rng.normal(0, 1, (300, 400))
    x[100:200] = x[0] + 0.05 * rng.normal(0, 1, (100, 400))                       # 100 near-copies count as about one trial
    e = stats.effective_trials(x, seed=1)
    assert e["raw"] == 300 and e["n_eff"] < 290
