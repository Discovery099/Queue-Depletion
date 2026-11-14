"""Vault Keeper (SPEC 5.5-5.7, 16.3, 17.7).  Plain code with one entry point.

The ONLY program permitted to read data/vault.  Research code submits a frozen strategy package; the
keeper checks the request, the budget and the genome distance to every earlier request, runs the
package on vault data in the default engine at base costs, applies the answer rule of SPEC 5.6,
appends to the hash-chained ledger and returns.  It prints and stores nothing else: no equity curve,
no trade list, no dates, no per-month or per-instrument split.

    python vault/keeper.py --request vault/requests/request_001.json            # Vault-A query
    python vault/keeper.py --request vault/requests/request_001.json --exam B   # one-shot Vault-B exam
"""
import argparse
import json
import os
import stat
import sys

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import ENGINE_VERSION, path, read_json, sha256_bytes, write_json  # noqa: E402
from engine import metrics as M  # noqa: E402
from engine import sim  # noqa: E402
from engine.data import INSTRUMENTS, frame_to_bars, partition  # noqa: E402
from genome import compile_py, genome as GN  # noqa: E402
from genome.dsl import Ctx  # noqa: E402

GATES = yaml.safe_load(open(path("config/gates.yaml")))
COSTS = read_json(path("config/costs.lock.json"))["levels"]
BUDGET = {"A": 60, "B": 5}
MIN_GAP_GENERATIONS = 1500
MAX_PER_LINEAGE = 2
SAME_DISTANCE = 0.15
TOL = {"win_rate": 0.04, "profit_factor": 0.25, "trades_per_year": None, "dd_ratio": 0.05}   # None: 15% of the research value
BIN = {"win_rate": 0.01, "profit_factor": 0.05, "trades_per_year": 10.0, "dd_ratio": 0.05}
REQUIRED_ATTESTATIONS = ("stages_1_to_4_passed_at_gold_floors", "placebo_requirement_holds", "held_tier_through_epoch_reevaluation",
                         "red_team_budget_spent_unbroken", "pine_parity_verified", "expected_result_written")


class Refused(Exception):
    pass


class Keeper:
    def __init__(self, vault_dir=None, ledger_path=None, lock=None):
        self.vault_dir = vault_dir or path("data/vault")
        self.ledger_path = ledger_path or path("vault/ledger.jsonl")
        self.lock = lock or partition()

    # ---------------- hash-chained, append-only ledger
    def records(self):
        if not os.path.exists(self.ledger_path):
            return []
        out, prev = [], "0" * 64
        for line in open(self.ledger_path):
            o = json.loads(line)
            body = json.dumps(o["r"], sort_keys=True, separators=(",", ":"))
            if o["p"] != prev or sha256_bytes((prev + body).encode()) != o["h"]:
                raise Refused("vault ledger hash chain is broken; halt (SPEC 19.6)")
            prev = o["h"]
            out.append(o["r"])
        self._last = prev
        return out

    def append(self, rec):
        self.records()
        prev = getattr(self, "_last", "0" * 64)
        body = json.dumps(rec, sort_keys=True, separators=(",", ":"))
        h = sha256_bytes((prev + body).encode())
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        with open(self.ledger_path, "a") as f:
            f.write(json.dumps({"p": prev, "r": rec, "h": h}, sort_keys=True, separators=(",", ":")) + "\n")
        self._last = h

    # ---------------- request checks (SPEC 16.3, 5.7)
    def check(self, req, exam):
        recs = self.records()
        mine = [r for r in recs if r["exam"] == exam and r["status"] == "ANSWERED"]
        if len(mine) >= BUDGET[exam]:
            raise Refused(f"Vault-{exam} budget of {BUDGET[exam]} is spent")
        g = req["genome"]
        if GN.validate(g):
            raise Refused("package genome is invalid: " + "; ".join(GN.validate(g)[:3]))
        if req.get("engine_version") != ENGINE_VERSION:
            raise Refused("package was frozen under a different engine version")
        if req.get("genome_id") != GN.finalize(dict(g))["genome_id"]:
            raise Refused("genome hash does not match the frozen package")
        missing = [k for k in REQUIRED_ATTESTATIONS if not req.get("attestations", {}).get(k)]
        if missing:
            raise Refused("conditions of SPEC 16.3 not attested: " + ", ".join(missing))
        for k in ("win_rate", "profit_factor", "trades_per_year", "dd_ratio"):
            if k not in req.get("research_metrics", {}):
                raise Refused(f"research value for {k} missing from the package")
        if exam == "A":
            answered = [r for r in recs if r["status"] == "ANSWERED"]
            if answered and req["generation"] - max(r["generation"] for r in answered) < MIN_GAP_GENERATIONS:
                raise Refused(f"fewer than {MIN_GAP_GENERATIONS} generations since the last vault query")
            if sum(1 for r in mine if r["lineage_id"] == req["lineage_id"]) >= MAX_PER_LINEAGE:
                raise Refused("lineage has used its 2 Vault-A queries")
            retired = {r["lineage_id"] for r in recs if r["exam"] == "A" and r["status"] == "ANSWERED" and r["verdict"] == "FAIL"}
            if req["lineage_id"] in retired:
                raise Refused("lineage is retired from vault eligibility after a Vault-A fail")
            for r in recs:
                if r["status"] == "ANSWERED" and r["exam"] == "A":
                    dist = 0.0 if r["genome_id"] == req["genome_id"] else GN.distance(g, r["genome"])
                    if dist < SAME_DISTANCE:
                        raise Refused(f"within genome distance {SAME_DISTANCE} of a previously queried strategy "
                                      f"(distance {dist:.3f}, earlier verdict {r['verdict']}); no re-submission (SPEC 5.7)")
        else:
            passed_a = [r for r in recs if r["exam"] == "A" and r["status"] == "ANSWERED" and r["verdict"] == "PASS" and r["genome_id"] == req["genome_id"]]
            if not passed_a:
                raise Refused("Vault-B is only for a strategy that passed Vault-A")
            if any(r["exam"] == "B" and r["status"] == "ANSWERED" and
                   (r["genome_id"] == req["genome_id"] or GN.distance(g, r["genome"]) < SAME_DISTANCE) for r in recs):
                raise Refused("Vault-B is one shot: this strategy, or a near-identical one, has already sat the exam")

    # ---------------- vault access
    def _load(self, sym):
        d = self.vault_dir
        mode = stat.S_IMODE(os.stat(d).st_mode)
        os.chmod(d, 0o700)
        try:
            return pd.read_parquet(os.path.join(d, f"{sym}.parquet"))
        finally:
            os.chmod(d, mode)

    def _sessions(self, exam):
        v = self.lock["vault"]
        na = v["vault_a"]["sessions"]
        first = self.lock["research"]["sessions"] + self.lock["embargo"]["sessions"]
        return (first, first + na) if exam == "A" else (first + na, first + v["sessions"])

    def _run(self, g, exam, tf):
        lo, hi = self._sessions(exam)
        frames = {s: self._load(s) for s in INSTRUMENTS}
        frames = {s: f[f["sess"] < hi] for s, f in frames.items()}            # Vault-B features warm up on Vault-A
        bars = {s: frame_to_bars(frames[s], s, tf) for s in INSTRUMENTS}
        from orchestrator.evaluate import other_arrays, twin_runs
        out, tw = [], np.zeros((200, 5))
        for i, s in enumerate(INSTRUMENTS):
            b = bars[s]
            ctx = Ctx(b, other=other_arrays(b, bars["YM" if s == "ES" else "ES"]))
            plan, aux = compile_py.to_plan(g, ctx)
            T, eq, inpos, _ = sim.run(b, plan, COSTS["base"])
            df = M.trades_frame(T, b, entry_type=g["slots"]["entry"]["type"])
            df = df[(df["sess"] >= lo) & (df["sess"] < hi)]
            out.append(df)
            mask = (b.sess >= lo) & (b.sess < hi)
            tw += twin_runs({"bars": b, "plan": plan, "aux": aux, "T": T, "inpos": inpos}, mask, 200, 1000 + i)
        tr = pd.concat(out, ignore_index=True)
        tv = {s: self.lock["instruments"][s]["tick_value"] for s in INSTRUMENTS}
        m = M.evaluate(tr, np.arange(lo, hi), tv)
        with np.errstate(divide="ignore", invalid="ignore"):
            twr = np.where(tw[:, 1] > 0, tw[:, 0] / tw[:, 1], 0.0)
        m["alpha_pts"] = 100 * (m["win_rate"] - float(np.median(twr)))
        m["each_wr"] = min((M.basic(tr.loc[tr.instrument == s, "net_usd"].values, tv[s])["win_rate"] if (tr.instrument == s).any() else 0.0)
                           for s in INSTRUMENTS)
        return m

    # ---------------- verdict and answer rule
    def verdict(self, g, exam):
        from gates.stage1 import freq_floor
        gold = GATES["tiers"]["gold"]
        tf = g["primary_timeframe_min"]
        m = self._run(g, exam, tf)
        fl = freq_floor(tf)
        checks = [
            (m["win_rate"], gold["win_rate"], 1), (m["each_wr"], gold["win_rate_each"], 1), (m["wilson_lo"], gold["wilson_lo"], 1),
            (m["alpha_pts"], gold["alpha_pts"], 1), (m["profit_factor"], gold["pf"], 1), (m.get("payoff", 0.0), gold["payoff"], 1),
            (m.get("expectancy_costs", 0.0), gold["exp_costs"], 1), (m.get("largest_loss_in_avg_wins", 99.0), gold["largest_loss_avg_wins"], -1),
            (m.get("tail_share", 99.0), GATES["forensics"]["tail_share_max"], -1), (m["trades_per_year"], fl["trades_per_year"], 1),
            (m.get("session_share", 0.0), fl["session_share"], 1), (m.get("dd_ratio", 99.0), 0.20, -1),
            (m.get("underwater_sessions", 9999), 189, -1),
        ]
        core_pass = 0
        for ctf in (5, 10, 15, 30, 60):
            mm = m if ctf == tf else self._run(g, exam, ctf)
            f2 = freq_floor(ctf)
            core_pass += int(mm["win_rate"] >= gold["win_rate_each"] and mm["profit_factor"] >= gold["pf_worst_fold"]
                             and mm["trades_per_year"] >= f2["trades_per_year"] and mm["alpha_pts"] > 0)
        checks.append((core_pass, gold["core_tfs"], 1))
        ok = [(v >= t) if sgn > 0 else (v <= t) for v, t, sgn in checks]
        near = [(v >= 0.9 * t) if sgn > 0 else (v <= 1.1 * t) for v, t, sgn in checks]
        v = "PASS" if all(ok) else "MARGINAL" if all(near) else "FAIL"
        return v, {"win_rate": m["win_rate"], "profit_factor": m["profit_factor"], "trades_per_year": m["trades_per_year"],
                   "dd_ratio": min(m.get("dd_ratio", 99.0), 9.0)}

    @staticmethod
    def thresholdout(vault, research, rng):
        """If the vault value is within tolerance of the research value, return the research value;
        otherwise the vault value plus Laplace noise (scale: a quarter of the tolerance).  Coarse bins."""
        out = {}
        for k, v in vault.items():
            r = research[k]
            tol = TOL[k] if TOL[k] is not None else 0.15 * abs(r)
            x = r if abs(v - r) <= tol else v + rng.laplace(0.0, tol / 4.0)
            out[k] = round(round(x / BIN[k]) * BIN[k], 6)
        return out

    def query(self, req, exam="A"):
        """Answer one request.  Returns {'status', 'verdict', 'answer', 'queries_used'} and appends to the ledger."""
        try:
            self.check(req, exam)
        except Refused as e:
            self.append({"exam": exam, "status": "REFUSED", "reason": str(e), "generation": req.get("generation"),
                         "genome_id": req.get("genome_id"), "lineage_id": req.get("lineage_id"), "genome": req.get("genome")})
            return {"status": "REFUSED", "reason": str(e)}
        v, vault_vals = self.verdict(req["genome"], exam)
        used = sum(1 for r in self.records() if r["exam"] == exam and r["status"] == "ANSWERED") + 1
        seed = int(sha256_bytes((req["genome_id"] + exam + str(used)).encode())[:12], 16)
        ans = self.thresholdout(vault_vals, req["research_metrics"], np.random.default_rng(seed))
        rec = {"exam": exam, "status": "ANSWERED", "verdict": v, "answer": ans, "generation": req["generation"],
               "genome_id": req["genome_id"], "lineage_id": req["lineage_id"], "genome": req["genome"], "query_number": used,
               "engine_version": ENGINE_VERSION}
        self.append(rec)
        return {"status": "ANSWERED", "verdict": v, "answer": ans, "queries_used": used, "budget": BUDGET[exam]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--request", required=True)
    ap.add_argument("--exam", default="A", choices=["A", "B"])
    a = ap.parse_args()
    res = Keeper().query(read_json(a.request), a.exam)
    out = os.path.splitext(a.request)[0].replace("request_", "answer_") + f"_{a.exam}.json"
    write_json(out, res)
    print(json.dumps(res))


if __name__ == "__main__":
    main()
