"""Vault Keeper tests against a DUMMY vault made from research data (SPEC 10.1 item 8).
The real vault is never read by these tests.
"""
import copy
import json
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import ENGINE_VERSION  # noqa: E402
from engine.data import INSTRUMENTS, load_frame, partition  # noqa: E402
from genome.genome import A, new_genome  # noqa: E402
from vault.keeper import BUDGET, Keeper  # noqa: E402

ATT = {k: True for k in ("stages_1_to_4_passed_at_gold_floors", "placebo_requirement_holds", "held_tier_through_epoch_reevaluation",
                         "red_team_budget_spent_unbroken", "pine_parity_verified", "expected_result_written")}


@pytest.fixture()
def keeper(tmp_path):
    d = tmp_path / "vault"
    d.mkdir()
    for s in INSTRUMENTS:
        f = load_frame(s)
        f[(f["sess"] >= 700) & (f["sess"] < 900)].to_parquet(d / f"{s}.parquet", index=False)
    os.chmod(d, 0o000)                                  # sealed, like the real one
    lock = {"research": {"sessions": 700}, "embargo": {"sessions": 0},
            "vault": {"sessions": 200, "vault_a": {"sessions": 133}}, "instruments": partition()["instruments"]}
    yield Keeper(str(d), str(tmp_path / "ledger.jsonl"), lock)
    os.chmod(d, 0o700)


def request(g, generation=20000, lineage="L000001", metrics=None):
    return {"genome": g, "genome_id": g["genome_id"], "engine_version": ENGINE_VERSION, "generation": generation, "lineage_id": lineage,
            "attestations": dict(ATT), "research_metrics": metrics or {"win_rate": 0.5, "profit_factor": 1.0, "trades_per_year": 400.0, "dd_ratio": 0.5}}


G1 = new_genome([A("tr_sweep_prior_day")], stop=A("r_stop_signal_bar"), exits=[A("x_target_r", k=1.0)])
G2 = new_genome([A("tr_rsi_hook")], location=[A("loc_vwap_band")], stop=A("r_stop_atr"), exits=[A("x_target_vwap")])
G1_NEAR = new_genome([A("tr_sweep_prior_day")], stop=A("r_stop_signal_bar", buf=0.5), exits=[A("x_target_r", k=1.0)])


def test_answer_contains_only_the_permitted_fields_and_ledger_chains(keeper):
    r = keeper.query(request(G1))
    assert r["status"] == "ANSWERED" and r["verdict"] in ("PASS", "MARGINAL", "FAIL")
    assert set(r) == {"status", "verdict", "answer", "queries_used", "budget"}
    assert set(r["answer"]) == {"win_rate", "profit_factor", "trades_per_year", "dd_ratio"}
    assert r["verdict"] == "FAIL"                         # an unremarkable strategy does not meet the Gold vector
    recs = keeper.records()
    assert len(recs) == 1 and recs[0]["query_number"] == 1
    assert oct(os.stat(keeper.vault_dir).st_mode & 0o777) == "0o0"     # sealed again after the read


def test_thresholdout_returns_research_value_when_results_agree():
    rng = np.random.default_rng(0)
    research = {"win_rate": 0.70, "profit_factor": 1.60, "trades_per_year": 300.0, "dd_ratio": 0.20}
    close = {"win_rate": 0.72, "profit_factor": 1.45, "trades_per_year": 320.0, "dd_ratio": 0.22}
    assert Keeper.thresholdout(close, research, rng) == {"win_rate": 0.70, "profit_factor": 1.60, "trades_per_year": 300.0, "dd_ratio": 0.20}
    far = {"win_rate": 0.50, "profit_factor": 0.90, "trades_per_year": 100.0, "dd_ratio": 0.90}
    a = Keeper.thresholdout(far, research, rng)
    assert abs(a["win_rate"] - 0.50) < 0.08 and a["win_rate"] != 0.70      # noisy vault value, coarse bin
    assert round(a["win_rate"] * 100) == pytest.approx(a["win_rate"] * 100)
    assert abs(a["profit_factor"] - 0.90) < 0.5


def test_refuses_without_attestations_or_with_wrong_hash(keeper):
    q = request(G1)
    q["attestations"]["red_team_budget_spent_unbroken"] = False
    assert keeper.query(q)["status"] == "REFUSED"
    q = request(G1)
    q["genome_id"] = "0" * 64
    assert keeper.query(q)["status"] == "REFUSED"
    q = request(G1)
    q["engine_version"] = "0.0.0"
    assert keeper.query(q)["status"] == "REFUSED"
    assert all(r["status"] == "REFUSED" for r in keeper.records())


def test_minimum_gap_lineage_retirement_and_distance_check(keeper):
    assert keeper.query(request(G1, generation=20000))["status"] == "ANSWERED"            # verdict FAIL
    r = keeper.query(request(G2, generation=20500, lineage="L000002"))
    assert r["status"] == "REFUSED" and "1500" in r["reason"]                             # minimum gap
    r = keeper.query(request(G2, generation=22000, lineage="L000001"))
    assert r["status"] == "REFUSED" and "retired" in r["reason"]                          # lineage retired after a fail
    r = keeper.query(request(G1_NEAR, generation=22000, lineage="L000003"))
    assert r["status"] == "REFUSED" and "distance" in r["reason"]                         # tweak-and-retry refused
    r = keeper.query(request(G1, generation=22000, lineage="L000004"))
    assert r["status"] == "REFUSED" and "distance" in r["reason"]                         # same strategy, new lineage name
    assert keeper.query(request(G2, generation=22000, lineage="L000002"))["status"] == "ANSWERED"


def test_vault_b_requires_a_vault_a_pass(keeper):
    r = keeper.query(request(G1), exam="B")
    assert r["status"] == "REFUSED" and "Vault-A" in r["reason"]


def test_budget_is_enforced(keeper):
    for i in range(BUDGET["A"]):
        keeper.append({"exam": "A", "status": "ANSWERED", "verdict": "MARGINAL", "generation": 1000 * i, "genome_id": f"x{i}",
                       "lineage_id": f"Lx{i}", "genome": G2, "answer": {}, "query_number": i + 1})
    r = keeper.query(request(G1, generation=10 ** 6))
    assert r["status"] == "REFUSED" and "budget" in r["reason"]


def test_tampering_with_the_ledger_is_detected(keeper):
    keeper.query(request(G1))
    lines = open(keeper.ledger_path).read().splitlines()
    o = json.loads(lines[0])
    o["r"]["verdict"] = "PASS"
    open(keeper.ledger_path, "w").write(json.dumps(o) + "\n")
    with pytest.raises(Exception):
        keeper.records()


def test_research_loader_cannot_open_the_real_vault():
    from engine.data import _check_research_path
    from engine import path
    with pytest.raises(PermissionError):
        _check_research_path(path("data/vault/ES.parquet"))
    assert oct(os.stat(path("data/vault")).st_mode & 0o777) == "0o0"
    assert not os.path.exists(path("vault/ledger.jsonl")) or open(path("vault/ledger.jsonl")).read() == ""   # real vault never queried
