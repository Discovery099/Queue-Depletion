"""Reproducibility self-test (SPEC 19.5, Article 21): re-run randomly chosen past generations from their
folders alone and confirm identical metrics.  Only generations sealed under the current engine version
are eligible; a mismatch is a halt condition.  Usage: python tools/repro_check.py [count]"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from audit import canary  # noqa: E402
from engine import ENGINE_VERSION, path, read_json, write_json  # noqa: E402
from gates import stage1 as S1  # noqa: E402

canary.install()
k = int(sys.argv[1]) if len(sys.argv) > 1 else 20
st = read_json(path("state/checkpoint.json"))
lo = int(sys.argv[2]) if len(sys.argv) > 2 else 1
rng = random.Random(st["next_generation"])
cands = list(range(lo, st["next_generation"]))
rng.shuffle(cands)
out, bad = [], []
for n in cands:
    d = path("runs", f"{n // 1000:03d}", f"gen_{n:06d}")
    mf = os.path.join(d, "metrics_stage1.json")
    if not os.path.exists(mf) or read_json(os.path.join(d, "config.lock.json"))["engine_version"] != ENGINE_VERSION:
        continue
    lock, m = read_json(os.path.join(d, "config.lock.json")), read_json(mf)
    res, _ = S1.stage1(read_json(os.path.join(d, "genome.json")), lock["island"], lock["generation_seed"], generation=n)
    same = (res["pooled"]["n"] == m["pooled"]["n"] and abs(res["pooled"]["net_usd"] - m["pooled"]["net_usd"]) < 1e-6
            and abs(res["score"] - m["score"]) < 1e-9 * max(1.0, abs(m["score"])))
    out.append({"generation": n, "identical": bool(same), "trades": m["pooled"]["n"], "score": m["score"], "score_rerun": res["score"]})
    if not same:
        bad.append(n)
    if len(out) >= k:
        break
write_json(path("reports/repro_check_latest.json"), {"engine_version": ENGINE_VERSION, "checked": len(out), "mismatches": bad, "results": out})
print(f"{len(out)} generations re-run from their folders under engine {ENGINE_VERSION}; mismatches: {bad or 'none'}")
