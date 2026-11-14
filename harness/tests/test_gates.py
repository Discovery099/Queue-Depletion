"""Gate unit tests (SPEC 10.1 item 6): a known-null strategy fails, a known-overfit strategy fails,
a geometry-only high win rate fails, and a strategy with genuine (planted) foresight clears the twin
gates, which shows the gates can tell earned win rate from manufactured win rate in both directions.

The planted-foresight strategies read a store series that leaks the future; they exist only to test
the gate arithmetic and would be voided by the audits in a real generation.
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from audit import canary  # noqa: E402
from gates import stage1 as S1  # noqa: E402
from genome.dsl import ext  # noqa: E402
from genome.genome import A, new_genome  # noqa: E402
from library.atoms.catalog import ATOMS, Atom, G  # noqa: E402
from orchestrator import evaluate as EV  # noqa: E402

canary.install()
_base = EV.EXT_PROVIDER


class _Prov(dict):
    def __init__(self, b):
        super().__init__()
        self.b, self.base = b, _base(b)

    def __missing__(self, name):
        if name not in ("t_foresight", "t_overfit"):
            return self.base[name]
        b = self.b
        n, k = b.n, 6
        fut = np.zeros(n)
        same = b.sess[k:] == b.sess[:-k]
        fut[:-k] = np.where(same, b.c[k:] - b.c[:-k], 0.0)
        rng = np.random.default_rng(5)
        noise = rng.standard_normal(n)
        sig = np.sign(fut) * (rng.random(n) < 0.12)              # sparse, correct direction of the next 30 minutes
        early = EV.FOLD_OF[np.minimum(b.sess, EV.N_SEARCH - 1)] <= 2
        self["t_foresight"] = sig
        self["t_overfit"] = np.where(early, sig, np.sign(noise) * (rng.random(n) < 0.12))   # works only in folds 1-2
        return self[name]


def _prov(b):
    return _Prov(b)


@pytest.fixture(scope="module", autouse=True)
def planted():
    for name in ("t_foresight", "t_overfit"):
        x = ext(name)
        ATOMS["tr_" + name] = Atom("tr_" + name, "TRIGGER", "trend", "test-only planted series", {"z": G(0.5,)},
                                   (lambda xx: (lambda p, d: d.sg(xx) > p.z))(x), (set(), None))
    EV.EXT_PROVIDER = _prov
    EV.clear_caches()
    yield
    EV.EXT_PROVIDER = _base
    EV.clear_caches()
    for name in ("t_foresight", "t_overfit"):
        ATOMS.pop("tr_" + name)


def failed(res, prefix):
    return [g for g in res["failed_gates"] if g.startswith(prefix)]


def test_known_null_strategy_fails():
    g = new_genome([A("tr_cycle_phase_hook")], stop=A("r_stop_atr", k=1.0), exits=[A("x_target_r", k=1.0)])
    res, _ = S1.stage1(g, "A", 1)
    assert not res["passed"]
    assert abs(res["twin"]["win_rate_alpha_pts"]) < 4.0                     # a canary has no alpha
    assert "twin.win_rate_alpha_pts" in res["failed_gates"] and "floor.profit_factor_pooled" in res["failed_gates"]
    assert res["pooled"]["expectancy_costs"] < 0                            # a null strategy earns minus costs


def test_geometry_only_high_win_rate_fails_the_twin_test():
    g = new_genome([A("tr_ema_cross")], stop=A("r_stop_atr", k=2.5), exits=[A("x_target_r", k=0.4)])
    res, _ = S1.stage1(g, "A", 1)
    assert res["pooled"]["win_rate"] > 0.62                                 # headline looks good...
    assert res["twin"]["median_win_rate"] > 0.60                            # ...but the random-entry twin wins as often
    assert not res["passed"] and "twin.win_rate_alpha_pts" in res["failed_gates"]
    assert res["score"] < 0.2


def test_known_overfit_strategy_fails_out_of_sample():
    g = new_genome([A("tr_t_overfit")], stop=A("r_stop_atr", k=1.0), exits=[A("x_target_r", k=1.0), A("x_time_stop", m=30)])
    res, runs = S1.stage1(g, "A", 1)
    assert res["wf"]["in_sample_expectancy_costs"] > 1.0                    # strong in the folds it was 'fitted' on
    assert res["wf"]["oos_expectancy_costs"] < 0.5
    assert not res["passed"] and "wf.efficiency" in res["failed_gates"]
    assert res["score"] < 0.1


def test_planted_foresight_clears_the_twin_gates():
    g = new_genome([A("tr_t_foresight")], stop=A("r_stop_atr", k=1.0), exits=[A("x_target_r", k=1.0), A("x_time_stop", m=30)])
    res, runs = S1.stage1(g, "A", 1)
    tw = res["twin"]
    assert tw["win_rate_alpha_pts"] > 12 and not failed(res, "twin.")
    assert tw["random_exit_wilson_lo"] > 0.5                                # the entries themselves carry the skill
    assert res["pooled"]["profit_factor"] > 1.4 and res["score"] > 0.3
    conf = S1.stage1_confirm(g, runs, 1)
    assert conf["twin"]["n_twins"] == 200 and not failed(conf, "twin.")


def test_islands_score_disjoint_folds_and_confirmation_uses_all_six():
    assert set(EV.ISLAND_FOLDS["A"]) | set(EV.ISLAND_FOLDS["B"]) == set(EV.TEST_FOLDS)
    assert not set(EV.ISLAND_FOLDS["A"]) & set(EV.ISLAND_FOLDS["B"])
    g = new_genome([A("tr_sweep_prior_day")])
    ra, _ = S1.stage1(g, "A", 1)
    rb, _ = S1.stage1(g, "B", 1)
    assert ra["folds"] == [3, 5, 7] and rb["folds"] == [4, 6, 8] and ra["pooled"]["n"] != rb["pooled"]["n"]


def test_inner_holdout_is_invisible_to_search_stages():
    b = EV.bars_for("ES", 5)
    assert b.sess.max() == EV.N_SEARCH - 1                                   # the holdout bars are not even loaded
    with pytest.raises(PermissionError):
        from engine.data import _check_research_path
        _check_research_path(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data/vault/ES.parquet"))


def test_structural_limits_hold_on_every_trade():
    g = new_genome([A("tr_rsi_hook")], stop=A("r_stop_swing", n=12, buf=0.5), exits=[A("x_target_r", k=0.4)])
    r = EV.run(g, "ES", 5)
    t = r["trades"]
    b = r["bars"]
    atr = r["aux"]["atr"][t["sig_idx"].values]
    ref = b.c[t["sig_idx"].values]
    risk = np.abs(ref - t["initial_stop"].values)
    assert len(t) > 100
    assert np.all(risk <= 2.5 * atr + b.tick) and np.all(risk <= 0.006 * ref + b.tick) and np.all(risk >= 0.3 * atr - b.tick)
    assert np.all((t["initial_stop"].values / b.tick) % 1 == 0) and np.all((t["initial_target"].values / b.tick) % 1 == 0)
    tdist = np.abs(t["initial_target"].values - ref)
    assert np.all(risk / tdist <= 2.5 + 1e-9)                                # stop-to-target at most 2.5, on the rounded prices
    assert np.all(tdist >= 3 * 0.55 - b.tick)                                # at least three round-trip costs (ES: 0.55 points)
