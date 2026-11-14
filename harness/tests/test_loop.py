"""Orchestrator tests in an isolated folder: folder contents and order, resumability, determinism,
and the promotion path.  Nothing here writes to the real ledger, archive or runs."""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import read_json, sha256_file  # noqa: E402
from gates import stage1 as S1  # noqa: E402
from genome.genome import A, new_genome  # noqa: E402
from orchestrator import evaluate as EV, promote  # noqa: E402
from orchestrator.loop import Run  # noqa: E402

REQUIRED = ["hypothesis.md", "hypothesis.sha256", "genome.json", "lineage.json", "strategy.py", "config.lock.json", "env.txt",
            "audit_static.json", "metrics_stage1.json", "trades.parquet", "equity.parquet", "winrate_integrity.json", "gates.json",
            "prediction_score.json", "SUMMARY.md", "MANIFEST.sha256"]


@pytest.fixture(scope="module")
def run(tmp_path_factory):
    root = str(tmp_path_factory.mktemp("iso"))
    r = Run(root=root, workers=2, batch=4, quiet=True)
    r.run(8)
    return r


def test_generation_folder_is_complete_and_hypothesis_precedes_results(run):
    for n in range(1, 9):
        d = run.gen_dir(n)
        files = os.listdir(d)
        for f in REQUIRED:
            assert f in files, (n, f)
        assert os.path.getmtime(os.path.join(d, "hypothesis.sha256")) <= os.path.getmtime(os.path.join(d, "metrics_stage1.json"))
        h = open(os.path.join(d, "hypothesis.sha256")).read().split()[0]
        from engine import sha256_bytes
        assert h == sha256_bytes(open(os.path.join(d, "hypothesis.md"), "rb").read())
        for line in open(os.path.join(d, "MANIFEST.sha256")).read().splitlines():
            digest, name = line.split("  ")
            assert sha256_file(os.path.join(d, name)) == digest
        assert "WIN-RATE STATEMENT" in open(os.path.join(d, "SUMMARY.md")).read()


def test_every_backtest_has_a_ledger_row_opened_before_it_closed(run):
    rows = run.ledger.db.execute("SELECT generation, status, opened_utc, closed_utc FROM trials").fetchall()
    assert len(rows) == 8 * 6 and all(r[1] == "DONE" and r[2] <= r[3] for r in rows)
    ok, n = run.ledger.verify_chain()
    assert ok and n == 2 * len(rows)


def test_resume_continues_from_the_checkpoint(run):
    r2 = Run(root=run.root, workers=2, batch=4, quiet=True)
    assert r2.st["next_generation"] == 9
    r2.run(4)
    assert r2.st["next_generation"] == 13 and os.path.exists(r2.gen_dir(12))


def test_same_seed_gives_the_same_genomes_and_metrics(run, tmp_path):
    r = Run(root=str(tmp_path), workers=2, batch=4, quiet=True)
    r.run(8)
    for n in range(1, 9):
        a, b = read_json(os.path.join(run.gen_dir(n), "genome.json")), read_json(os.path.join(r.gen_dir(n), "genome.json"))
        assert a["genome_id"] == b["genome_id"]
        ma, mb = read_json(os.path.join(run.gen_dir(n), "metrics_stage1.json")), read_json(os.path.join(r.gen_dir(n), "metrics_stage1.json"))
        assert ma["pooled"]["n"] == mb["pooled"]["n"] and ma["score"] == pytest.approx(mb["score"], rel=1e-12)


def test_stop_file_and_frozen_hash_guards(run, tmp_path):
    st = read_json(os.path.join(run.root, "state/checkpoint.json"))
    st["frozen"]["partition"] = "0" * 64
    bad = str(tmp_path / "bad")
    os.makedirs(bad + "/state")
    json.dump(st, open(bad + "/state/checkpoint.json", "w"))
    with pytest.raises(SystemExit):
        Run(root=bad, workers=1, quiet=True)
    assert "frozen file" in open(bad + "/reports/HALT.md").read()


def test_honeypot_check_voids(run):
    assert run.honeypot_check()


def test_promotion_path_writes_evidence_and_autopsy(run):
    g = new_genome([A("tr_sweep_prior_day")], regime=[A("st_vwap_side")], stop=A("r_stop_signal_bar"), exits=[A("x_target_r", k=1.0)], tf=15)
    n = 9000
    d = run.gen_dir(n)
    os.makedirs(d, exist_ok=True)
    from engine import write_json
    write_json(os.path.join(d, "gates.json"), {"stage1": []})
    runs = {s: EV.run(g, s, 15) for s in ("ES", "YM")}
    conf = S1.stage1_confirm(g, runs, 1)
    run.quick_stages = True
    status, tier, reason, stage = promote.process(run, {"generation": n, "genome": g, "seed": 1, "lineage_id": "Ltest", "operator": "TEST", "code_hash": "x"}, conf)
    assert status == "STAGE2_FAIL" and tier is None and stage == 2
    for f in ("audit_dynamic.json", "autopsy.md", "robustness/timeframes.json", "robustness/decoys.json", "robustness/parameter_robustness.json"):
        assert os.path.exists(os.path.join(d, f)), f
    assert "stage2" in read_json(os.path.join(d, "gates.json"))
    assert run.ledger.count("generation=9000 AND status='OPEN'") == 0 and run.ledger.count("generation=9000") > 50
