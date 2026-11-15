"""Orchestrator (SPEC 10, 17.1, 19): the resumable generation loop.  Plain code, no language model.

It routes work and enforces order.  It never starts a backtest without a hashed hypothesis and an
open ledger row, and it commits results in generation order so that the ledger and the archive are
deterministic for a given seed, batch size and worker count.

Run:   python -m orchestrator.loop --generations 50            (from the harness directory)
       python -m orchestrator.loop --placebo 1000 --tag gen0   (decoy markets only, SPEC 15.4)
"""
import argparse
import copy
import datetime
import json
import multiprocessing as mp
import os
import platform
import shutil
import sqlite3
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import ENGINE_VERSION, canon, frozen_hashes, path, read_json, sha256_bytes, sha256_file, write_json, write_text  # noqa: E402
from engine import metrics as M  # noqa: E402
from engine.data import INSTRUMENTS, partition  # noqa: E402
from audit import canary, static_audit  # noqa: E402
from genome import compile_py, genome as GN  # noqa: E402
from library.atoms.catalog import ATOMS, FAMILIES  # noqa: E402
from orchestrator import evaluate as EV  # noqa: E402
from orchestrator.ledger import Ledger, utcnow  # noqa: E402

SEARCH = EV.SEARCH
TIERS = ("bronze", "silver", "gold")
STAGE1_TRIALS = [("candidate", s) for s in INSTRUMENTS] + [("twin_entry", s) for s in INSTRUMENTS] + [("twin_exit", s) for s in INSTRUMENTS]


# ---------------------------------------------------------------------------------------------- workers
def _init_worker(decoy_spec):
    canary.install()
    if decoy_spec:
        from engine import decoys
        EV.set_frames(decoys.decoy(*decoy_spec))


def _stage1_job(job):
    """Runs in a worker process.  Writes trades and equity into the generation folder, returns metrics."""
    from gates import stage1 as S1
    g, island, seed, gen, folder = job["genome"], job["island"], job["seed"], job["generation"], job["folder"]
    t0 = time.time()
    try:
        res, runs = S1.stage1(g, island, seed, generation=gen)
        confirm = None
        if res["passed"]:
            res["needs_confirmation"] = True
        tr = pd.concat([runs[s]["trades"] for s in INSTRUMENTS], ignore_index=True)
        _compact(tr).to_parquet(os.path.join(folder, "trades.parquet"), compression="zstd", compression_level=12, index=False)
        daily = pd.DataFrame({s: M.daily_series(runs[s]["trades"], np.arange(EV.N_SEARCH)).values for s in INSTRUMENTS})
        daily.to_parquet(os.path.join(folder, "equity.parquet"), compression="zstd", index=False)
        res["daily_pooled"] = (daily.sum(axis=1).values).astype(np.float32).tobytes()
        res["liq_miss"] = {s: runs[s]["liq_miss"] for s in INSTRUMENTS}
        res["n_trades_all_folds"] = {s: int(len(runs[s]["trades"])) for s in INSTRUMENTS}
        res["seconds"] = time.time() - t0
        return {"generation": gen, "ok": True, "result": res, "confirm": confirm}
    except Exception as e:   # one strategy's failure never stops the loop (SPEC 19.6)
        import traceback
        return {"generation": gen, "ok": False, "error": f"{type(e).__name__}: {e}", "trace": traceback.format_exc()[-1500:]}


def _compact(tr):
    """Smaller on-disk types for the trade record (SPEC 6.3 storage budget); prices stay float64."""
    tr = tr.copy()
    for c in ("mae_ticks", "mfe_ticks", "mae_pct_of_stop", "gross_ticks", "cost_ticks", "net_ticks", "stop_to_target_ratio"):
        tr[c] = tr[c].astype("float32")
    for c in ("trade_id", "generation", "timeframe_min", "fold", "regime_cell", "bars_held", "minutes_held", "minutes_since_open",
              "session_date", "sess", "sig_idx", "entry_idx", "exit_idx"):
        tr[c] = tr[c].astype("int32")
    for c in ("instrument", "entry_order_type", "exit_reason"):
        tr[c] = tr[c].astype("category")
    return tr


def _confirm_job(job):
    from gates import stage1 as S1
    g, seed, gen = job["genome"], job["seed"], job["generation"]
    try:
        runs = {s: EV.run(g, s, g["primary_timeframe_min"], generation=gen) for s in INSTRUMENTS}
        res = S1.stage1_confirm(g, runs, seed)
        return {"generation": gen, "ok": True, "result": res}
    except Exception as e:
        return {"generation": gen, "ok": False, "error": f"{type(e).__name__}: {e}"}


# ---------------------------------------------------------------------------------------------- run
class Run:
    def __init__(self, root=None, decoy_spec=None, workers=None, batch=None, quiet=False):
        self.root = root or path()
        self.decoy_spec = decoy_spec
        self.workers = workers or min(SEARCH["budgets"]["max_cores"], os.cpu_count() or 1)
        self.batch = batch or self.workers * 4
        self.quiet = quiet
        for d in ("state", "ledger", "archive/hall_of_fame", "runs", "reports/epochs", "reports/milestones"):
            os.makedirs(self.p(d), exist_ok=True)
        canary.install()
        if decoy_spec:
            from engine import decoys
            EV.set_frames(decoys.decoy(*decoy_spec))
        self.ledger = Ledger(self.p("ledger"))
        self.db = sqlite3.connect(self.p("ledger/lineage.sqlite"))
        self.db.execute("""CREATE TABLE IF NOT EXISTS genomes (generation INTEGER PRIMARY KEY, genome_id TEXT, lineage_id TEXT,
            island TEXT, operator TEXT, parents TEXT, tf INTEGER, complexity INTEGER, status TEXT, stage INTEGER, tier TEXT,
            score REAL, n_trades INTEGER, win_rate REAL, pf REAL, alpha REAL, cell TEXT, trig_key TEXT, genome TEXT, daily BLOB)""")
        self.db.execute("CREATE INDEX IF NOT EXISTS ix_gid ON genomes(genome_id)")
        self.db.execute("CREATE INDEX IF NOT EXISTS ix_trig ON genomes(trig_key)")
        self.db.commit()
        self.admitted = self._admitted()
        self.weights = self._weights()
        self.pool = None
        self.load_state()

    def p(self, *a):
        return os.path.join(self.root, *a)

    # ---------------- state
    def _admitted(self):
        f = path("library/ontology.json")
        if not os.path.exists(f):
            return None
        o = read_json(f)["atoms"]
        return {k for k, r in o.items() if r.get("admitted")}

    def _weights(self):
        f = path("library/ontology.json")
        if not os.path.exists(f):
            return {}
        return {k: r.get("prior_weight", 1.0) for k, r in read_json(f)["atoms"].items()}

    def load_state(self):
        f = self.p("state/checkpoint.json")
        if os.path.exists(f):
            self.st = read_json(f)
            fh = frozen_hashes()
            if self.st["frozen"] != fh:
                self.halt("A frozen file's hash changed (partition, costs or raw data).", {"expected": self.st["frozen"], "found": fh})
            ok, n = self.ledger.verify_chain()
            if not ok:
                self.halt("Trial ledger hash chain is broken.", {"records_verified": n})
            for (tid,) in self.ledger.db.execute("SELECT trial_id FROM trials WHERE status='OPEN' AND generation>=?",
                                                 [self.st["next_generation"]]).fetchall():
                self.ledger.close(tid, status="ABORTED")          # through the ledger, so the hash-chained mirror records it too
            self.ledger.commit()
        else:
            ops = dict(SEARCH["operators"])
            self.st = {"next_generation": 1, "frozen": frozen_hashes(), "engine_version": ENGINE_VERSION, "master_seed": SEARCH["master_seed"],
                       "batch": self.batch, "workers": self.workers, "operator_share": ops,
                       "operator_stats": {k: {"uses": 0, "improved": 0, "passed": 0} for k in ops},
                       "vault": {"a_used": 0, "b_used": 0, "last_query_generation": None},
                       "counts": {"void": 0, "stage1_fail": 0, "stage1_pass": 0, "confirmed": 0, "error": 0},
                       "void_streak": [], "best_score": {"A": 0.0, "B": 0.0}, "best_generation": 0,
                       "complexity_ceiling": SEARCH["complexity_ceiling"], "tier_counts": {t: 0 for t in TIERS},
                       "epoch": 0, "survey_cursor": 0, "started_utc": utcnow(), "placebo": bool(self.decoy_spec),
                       "decoy": list(self.decoy_spec) if self.decoy_spec else None, "seconds_stage1": 0.0}
        self.archive = read_json(self.p("archive/map_elites.json")) if os.path.exists(self.p("archive/map_elites.json")) else {"A": {}, "B": {}}
        self.ids = {r[0] for r in self.db.execute("SELECT genome_id FROM genomes")}
        self.beh = {(r[0], r[1], r[2], round(r[3] or 0, 6), round(r[4] or 0, 6))
                    for r in self.db.execute("SELECT island, tf, n_trades, win_rate, pf FROM genomes WHERE n_trades > 0")}

    def checkpoint(self):
        self.st["ledger_last_hash"] = self.ledger.last_hash
        self.st["updated_utc"] = utcnow()
        write_json(self.p("state/checkpoint.json"), self.st)
        write_json(self.p("archive/map_elites.json"), self.archive)

    def heartbeat(self, state, last_error=None):
        el = max(1e-9, time.time() - self.t_start)
        write_json(self.p("state/heartbeat.json"), {"utc": utcnow(), "generation": self.st["next_generation"] - 1, "state": state,
                                                    "generations_per_hour_this_run": round(3600 * self.done_this_run / el, 1),
                                                    "last_error": last_error})

    def halt(self, cause, detail=None):
        os.makedirs(self.p("reports"), exist_ok=True)
        write_text(self.p("reports/HALT.md"), f"# HALT\n\n- UTC: {utcnow()}\n- Cause: {cause}\n- Generation: "
                   f"{getattr(self, 'st', {}).get('next_generation', '?')}\n\n```\n{json.dumps(detail, indent=1, default=str)}\n```\n\n"
                   "The loop stopped and waits for the owner (SPEC 19.6).\n")
        raise SystemExit(f"HALT: {cause}")

    # ---------------- helpers
    def gen_dir(self, n):
        return self.p("runs", f"{n // 1000:03d}", f"gen_{n:06d}")

    def phase(self, n):
        ph = SEARCH["phases"]
        return "survey" if n <= ph["survey_until"] else "assembly" if n <= ph["assembly_until"] else \
            "refinement" if n <= ph["refinement_until"] else "hardening" if n <= ph["hardening_until"] else "certification"

    def ceiling(self, n):
        c = self.st["complexity_ceiling"]
        return min(c, SEARCH["survey_complexity_ceiling"]) if self.phase(n) == "survey" else c

    def trig_key(self, g):
        t = [e["atom"] for e in g["slots"]["trigger"]["atoms"]] + [e["atom"] for m in g.get("ensemble", []) for e in m["trigger"]["atoms"]]
        return "+".join(sorted(t))

    def novel(self, g):
        if g["genome_id"] in self.ids:
            return False
        for (js,) in self.db.execute("SELECT genome FROM genomes WHERE trig_key=? ORDER BY generation DESC LIMIT 400", [self.trig_key(g)]):
            if GN.distance(g, json.loads(js)) < SEARCH["novelty_min_distance"] - 1e-9:
                return False
        return True

    def draw_tf(self, rng):
        r = rng.random()
        acc = 0.0
        for tf, pr in GN.PRIMARY_TF:
            acc += pr
            if r <= acc:
                return tf
        return 5

    def parent(self, rng, island):
        """70% from the grid (uniform over occupied cells, so sparse cells are favoured), 20% from the
        leaders, 10% uniformly from everything evaluated on this island (SPEC 10.2 step 1)."""
        cells = self.archive[island]
        if not cells:
            return None
        ps = SEARCH["parent_selection"]
        r = rng.random()
        if r < ps["grid"]:
            c = cells[sorted(cells)[int(rng.integers(len(cells)))]]
            return c["best"] if rng.random() < 0.7 or "simplest" not in c else c["simplest"]
        if r < ps["grid"] + ps["leaders"]:
            top = sorted((c["best"] for c in cells.values()), key=lambda e: -e["score"])[:10]
            return top[int(rng.integers(len(top)))]
        row = self.db.execute("SELECT generation, genome, score, tf, lineage_id, win_rate, pf, n_trades FROM genomes WHERE island=? AND status!='VOID' "
                              "ORDER BY RANDOM() LIMIT 1", [island]).fetchone() if False else None
        top = self.st["next_generation"] - 1
        r = None
        for _ in range(8):                               # a uniformly random generation of this island (index lookup, not a full scan)
            r = self.db.execute("SELECT generation, genome, score, tf, lineage_id FROM genomes WHERE generation>=? AND island=? "
                                "AND status NOT IN ('VOID','ERROR') ORDER BY generation LIMIT 1", [int(rng.integers(1, max(2, top + 1))), island]).fetchone()
            if r:
                break
        if not r:
            return None
        gen, js, score, tf, lin = r
        return {"generation": gen, "genome": json.loads(js), "score": score or 0.0, "lineage_id": lin, "metrics": None}

    def survey_item(self, k):
        """Deterministic survey order: every trigger atom alone, then one trigger per ordered pair of
        mechanism families with a context atom from the second family (SPEC 10.4)."""
        trig = sorted(a.id for a in ATOMS.values() if a.typ == "TRIGGER" and not getattr(a, "blocked", False))
        if k < len(trig):
            return ("single", trig[k])
        fams = sorted(FAMILIES)
        pairs = [(a, b) for a in fams for b in fams if a != b]
        j = k - len(trig)
        return ("pair", pairs[j]) if j < len(pairs) else None

    # ---------------- proposal
    def propose(self, n):
        rng = np.random.default_rng([self.st["master_seed"], n])
        island = "A" if n % 2 else "B"
        ceiling = self.ceiling(n)
        share = self.st["operator_share"]
        names = sorted(share)
        probs = np.array([share[k] for k in names])
        probs = probs / probs.sum()
        phase = self.phase(n)
        note = ""
        for attempt in range(30):
            op = names[int(rng.choice(len(names), p=probs))]
            if phase == "survey" and rng.random() < 0.6:
                op = "LIBRARY_PROBE"
            par = self.parent(rng, island)
            g, parents = None, []
            if op == "LLM_HYPOTHESIS":
                g = self.next_llm_hypothesis()
                if g is None:
                    op, note = "LIBRARY_PROBE", "LLM_HYPOTHESIS queue empty; share given to LIBRARY_PROBE"
            if op == "ENSEMBLE":
                other = self.parent(rng, island) if par is not None and phase != "survey" else None
                if other is not None and other["generation"] != par["generation"]:
                    fa = ATOMS[par["genome"]["slots"]["trigger"]["atoms"][0]["atom"]].fam
                    fb = ATOMS[other["genome"]["slots"]["trigger"]["atoms"][0]["atom"]].fam
                    if fa != fb and self.entry_overlap(par["genome"], other["genome"]) < 0.30:     # SPEC 15.11
                        g = GN.op_ensemble(rng, par["genome"], other["genome"])
                        if g is not None:
                            parents = [par["generation"], other["generation"]]
                if g is None:
                    op, note = "LIBRARY_PROBE", "no pair with different mechanism families and trade overlap below 30% was drawn; share given to LIBRARY_PROBE"
            if op == "LIBRARY_PROBE" or (par is None and op != "LLM_HYPOTHESIS"):
                item = self.survey_item(self.st["survey_cursor"]) if phase == "survey" else None
                tf = self.draw_tf(rng)
                if item and item[0] == "single":
                    g = GN.minimal_genome(rng, trigger_id=item[1], weights=self.weights, tf=tf, with_context=False)
                    self.st["survey_cursor"] += 1
                elif item and item[0] == "pair":
                    fa, fb = item[1]
                    ta = [a.id for a in ATOMS.values() if a.typ == "TRIGGER" and a.fam == fa and not getattr(a, "blocked", False)]
                    cb = [a for a in ATOMS.values() if a.typ in ("STATE", "LOCATION", "FILTER") and a.fam == fb and not getattr(a, "blocked", False)]
                    self.st["survey_cursor"] += 1
                    if ta and cb:
                        c = cb[int(rng.integers(len(cb)))]
                        slot = {"STATE": "regime", "LOCATION": "location", "FILTER": "filters"}[c.typ]
                        g = GN.new_genome([GN.A(ta[int(rng.integers(len(ta)))])], stop=GN.rand_atom(rng, "EXIT", "stop", weights=self.weights),
                                          exits=[GN.rand_atom(rng, "EXIT", "target", weights=self.weights)], tf=tf, **{slot: [GN.A(c.id)]})
                if g is None:
                    usage = dict(self.db.execute("SELECT trig_key, COUNT(*) FROM genomes GROUP BY trig_key").fetchall())
                    w = {a: self.weights.get(a, 1.0) / (1.0 + usage.get(a, 0)) for a in ATOMS}
                    g = GN.minimal_genome(rng, weights=w, tf=tf)
                op = "LIBRARY_PROBE" if op != "LLM_HYPOTHESIS" else op
            elif op != "LLM_HYPOTHESIS":
                pg = par["genome"]
                if op == "ENSEMBLE":
                    pass                                          # built above
                elif op in ("SLOT_CROSSOVER", "EXIT_TRANSPLANT", "ENTRY_TRANSPLANT"):
                    parents = [par["generation"]]
                    other = self.parent(rng, island)
                    if other is None or other["generation"] == par["generation"]:
                        continue
                    parents.append(other["generation"])
                    g = {"SLOT_CROSSOVER": GN.op_slot_crossover, "EXIT_TRANSPLANT": GN.op_exit_transplant,
                         "ENTRY_TRANSPLANT": GN.op_entry_transplant}[op](rng, pg, other["genome"])
                else:
                    parents = [par["generation"]]
                    fn = {"PARAM_STEP": GN.op_param_step, "ATOM_SWAP": GN.op_atom_swap, "ATOM_ADD": GN.op_atom_add,
                          "ATOM_DROP": GN.op_atom_drop, "INVERT": GN.op_invert, "SIMPLIFY": GN.op_simplify}[op]
                    g = fn(rng, pg, self.weights)
                    if op == "ATOM_ADD" and g is not None and rng.random() < 0.15:
                        g = GN.op_entry_type(rng, g)
                if g is not None:
                    g["primary_timeframe_min"] = pg["primary_timeframe_min"]
            if g is None:
                continue
            g = GN.finalize(g)
            if GN.validate(g) and not any(getattr(ATOMS.get(e["atom"]), "blocked", False) for e in GN.atom_entries(g)):
                continue
            if g["complexity"] > ceiling or not self.novel(g):
                continue
            lineage = f"L{n:06d}" if not parents else par.get("lineage_id") or f"L{par['generation']:06d}"
            return {"generation": n, "genome": g, "operator": op, "parents": parents, "island": island, "lineage_id": lineage,
                    "parent": par if parents else None, "note": note, "attempts": attempt + 1, "phase": phase,
                    "seed": int(np.random.default_rng([self.st["master_seed"], n, 1]).integers(2 ** 31))}
        return None

    def entry_overlap(self, g1, g2):
        """Share of the rarer genome's entry-signal bars that coincide with the other's (ES, primary timeframe of g1)."""
        try:
            ctx = EV.ctx_for("ES", g1["primary_timeframe_min"])
            sigs = []
            for g in (g1, g2):
                x = compile_py.build(g)
                sigs.append(ctx.ev(x["raw"]["long"]) | ctx.ev(x["raw"]["short"]))
            return float((sigs[0] & sigs[1]).sum() / max(1, min(sigs[0].sum(), sigs[1].sum())))
        except Exception:
            return 1.0

    def next_llm_hypothesis(self):
        f = self.p("state/hypothesis_queue.jsonl")
        if not os.path.exists(f):
            return None
        lines = open(f).read().splitlines()
        done = self.st.get("llm_queue_cursor", 0)
        while done < len(lines):
            try:
                item = json.loads(lines[done])
                done += 1
                self.st["llm_queue_cursor"] = done
                g = GN.finalize(item["genome"])
                g["_hypothesis_text"] = item.get("hypothesis", "")
                return g
            except Exception:
                done += 1
        self.st["llm_queue_cursor"] = done
        return None

    # ---------------- pre-registration and compile
    def hypothesis(self, prop):
        g, par = prop["genome"], prop["parent"]
        text = g.pop("_hypothesis_text", "")
        atoms = [e["atom"] for e in GN.atom_entries(g)]
        st = self.st["operator_stats"].get(prop["operator"], {"uses": 0, "improved": 0})
        rate = st["improved"] / st["uses"] if st["uses"] else None
        stop = g["slots"]["risk"]["stop"]
        tgt = next((e for e in g["slots"]["exit"] if ATOMS[e["atom"]].kind == "target"), None)
        if par and par.get("metrics"):
            pm = par["metrics"]
            wr = [max(0.0, pm["win_rate"] - 0.06), min(1.0, pm["win_rate"] + 0.06)]
            pf = [0.8 * pm["pf"], 1.25 * pm["pf"]]
            tpy = [0.6 * pm["tpy"], 1.6 * pm["tpy"]]
            basis = f"parent generation {par['generation']} (win rate {100 * pm['win_rate']:.1f}%, profit factor {pm['pf']:.2f}, {pm['tpy']:.0f} trades/yr)"
        else:
            geo = 0.5
            if tgt is not None and tgt["atom"] == "x_target_r":
                geo = 1.0 / (1.0 + tgt["params"]["k"])
            wr = [max(0.0, geo - 0.12), min(1.0, geo + 0.08)]
            pf = [0.7, 1.15]
            tpy = [40.0, 1500.0]
            basis = f"exit geometry alone (about {100 * geo:.0f}% for a random entry) because no parent exists"
        pred = {"win_rate": wr, "profit_factor": pf, "trades_per_year": tpy}
        mech = text or "; ".join(f"{a}: {ATOMS[a].desc}" for a in atoms)
        md = (f"# Hypothesis, generation {prop['generation']}\n\n"
              f"- Operator: {prop['operator']}" + (f" ({prop['note']})" if prop["note"] else "") + "\n"
              f"- Parents: {prop['parents'] or 'none'}; lineage {prop['lineage_id']}; island {prop['island']}; phase {prop['phase']}\n"
              f"- Primary timeframe: {g['primary_timeframe_min']} minutes\n\n"
              f"## Mechanism\n\n{mech}\n\n## Structure\n\n```\n{GN.describe(g)}\n```\n\n"
              f"## Why it might win often\n\n"
              + ("Written by the Strategist (see mechanism above).\n" if text else
                 f"Programmatic proposal. The operator {prop['operator']} has improved on its parent in "
                 + (f"{100 * rate:.0f}% of {st['uses']} uses so far" if rate is not None else "an unknown share of uses (none yet)")
                 + ". No claim of skill is made in advance: the random-entry twin decides whether any win rate is earned.\n")
              + f"\n## Library atoms used\n\n" + "\n".join(f"- {a} ({ATOMS[a].typ}, {FAMILIES[ATOMS[a].fam]})" for a in atoms)
              + f"\n\n## Predictions (ranges, before any backtest)\n\nBasis: {basis}.\n\n"
              f"- Win rate: {100 * wr[0]:.0f}% to {100 * wr[1]:.0f}%\n- Profit factor: {pf[0]:.2f} to {pf[1]:.2f}\n"
              f"- Trades per year per instrument: {tpy[0]:.0f} to {tpy[1]:.0f}\n\n"
              "## Falsifier\n\nThe idea is falsified if, out of sample, the win-rate alpha over the random-entry twin is not positive, "
              "or the profit factor is at or below 1.0, or the candidate's win rate is not above the twins' 99th percentile.\n")
        return md, pred

    def prepare(self, prop):
        """States PRE-REGISTER, COMPILE and LEDGER-OPEN.  Returns a job for the worker or None if VOID."""
        n, g = prop["generation"], prop["genome"]
        d = self.gen_dir(n)
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)
        md, pred = self.hypothesis(prop)
        write_text(os.path.join(d, "hypothesis.md"), md)
        h = sha256_bytes(md.encode())
        write_text(os.path.join(d, "hypothesis.sha256"), f"{h}  hypothesis.md\nutc {utcnow()}\n")
        prop["prediction"] = pred
        write_json(os.path.join(d, "genome.json"), g)
        dist = [round(GN.distance(g, prop["parent"]["genome"]), 4)] if prop["parent"] else []
        debt = self.db.execute("SELECT COUNT(*) FROM genomes WHERE lineage_id=?", [prop["lineage_id"]]).fetchone()[0]
        write_json(os.path.join(d, "lineage.json"), {"generation": n, "parents": prop["parents"], "operator": prop["operator"],
                                                     "lineage_id": prop["lineage_id"], "island": prop["island"],
                                                     "distance_to_parents": dist, "inherited_trial_debt": debt, "proposal_attempts": prop["attempts"]})
        src = compile_py.python_source(g)
        write_text(os.path.join(d, "strategy.py"), src)
        prop["code_hash"] = sha256_bytes(src.encode())
        write_json(os.path.join(d, "config.lock.json"), {
            "engine_version": ENGINE_VERSION, "frozen": self.st["frozen"], "gates_sha256": sha256_file(path("config/gates.yaml")),
            "search_sha256": sha256_file(path("config/search.yaml")), "signal_layer": static_audit.signal_layer_hash(),
            "master_seed": self.st["master_seed"], "generation_seed": prop["seed"], "island": prop["island"],
            "data": {s: partition()["blocks"][s]["research_sha256"] for s in INSTRUMENTS} if not self.decoy_spec else {"decoy": list(self.decoy_spec)},
            "stage1_folds": list(EV.ISLAND_FOLDS[prop["island"]]), "batch": self.st["batch"], "workers": self.st["workers"]})
        write_text(os.path.join(d, "env.txt"), ENV_TXT)
        aud = static_audit.audit(g, src, ceiling=self.ceiling(n), admitted=self.admitted)
        write_json(os.path.join(d, "audit_static.json"), aud)
        if not aud["clean"]:
            return None
        ids = []
        for mode, s in STAGE1_TRIALS:
            ids.append(self.ledger.open(generation=n, stage="1", genome_id=g["genome_id"], lineage_id=prop["lineage_id"], operator=prop["operator"],
                                        data_slice="wf_folds_" + "".join(map(str, EV.ISLAND_FOLDS[prop["island"]])), instrument=s,
                                        timeframe_min=g["primary_timeframe_min"], cost_level="base", stress_mode=mode, seed=prop["seed"],
                                        code_hash=prop["code_hash"], data_hash=self.st["frozen"]["partition"][:16]))
        prop["trial_ids"] = ids
        return {"genome": g, "island": prop["island"], "seed": prop["seed"], "generation": n, "folder": d}

    # ---------------- verdict
    def commit(self, prop, out, confirm=None):
        n, g, d = prop["generation"], prop["genome"], self.gen_dir(prop["generation"])
        st = self.st
        status, stage, tier, reason = "VOID", 0, None, ""
        res = None
        if out is None:
            aud = read_json(os.path.join(d, "audit_static.json"))
            reason = "STATIC_AUDIT: " + "; ".join(f"{h['rule']} ({h['match']})" for h in aud["hits"][:3])
            st["counts"]["void"] += 1
            st["void_streak"] = (st["void_streak"] + [aud["hits"][0]["rule"]])[-3:]
            if len(st["void_streak"]) == 3 and len(set(st["void_streak"])) == 1:
                self.finish(prop, status, stage, tier, reason, None)
                self.halt("Three consecutive VOID generations with the same cause.", {"cause": st["void_streak"][0]})
        elif not out["ok"]:
            status, stage, reason = "ERROR", 1, out["error"]
            st["counts"]["error"] += 1
            st["void_streak"] = []
            for tid in prop["trial_ids"]:
                self.ledger.close(tid, status="ABORTED")
            write_text(os.path.join(d, "error.txt"), out.get("trace", out["error"]))
        else:
            st["void_streak"] = []
            res = out["result"]
            m = res["pooled"]
            for tid, (mode, s) in zip(prop["trial_ids"], STAGE1_TRIALS):
                pm = res["by_instrument"][s]
                if mode == "candidate":
                    self.ledger.close(tid, n_trades=pm["n"], win_rate=pm["win_rate"], profit_factor=pm["profit_factor"],
                                      expectancy_ticks=pm.get("expectancy_ticks", 0.0), score=res["score"])
                elif mode == "twin_entry":
                    self.ledger.close(tid, n_trades=int(res["twin"]["median_trades"]), win_rate=res["twin"]["median_win_rate"],
                                      profit_factor=res["twin"]["median_profit_factor"], score=None)
                else:
                    self.ledger.close(tid, n_trades=res["twin"]["random_exit_n"], win_rate=res["twin"]["random_exit_win_rate"], score=None)
            st["seconds_stage1"] += res.get("seconds", 0.0)
            daily = res.pop("daily_pooled")
            prop["daily"] = daily
            write_json(os.path.join(d, "metrics_stage1.json"), {k: res[k] for k in ("island", "folds", "timeframe_min", "pooled", "by_instrument",
                                                                                   "by_fold", "wf", "score", "score_components", "score_factors",
                                                                                   "descriptors", "flags", "liq_miss", "trades_per_year_per_instrument")})
            write_json(os.path.join(d, "winrate_integrity.json"), {"twin": res["twin"], "forensics": {
                k: m.get(k) for k in ("payoff", "largest_loss_in_avg_wins", "tail_share", "skew", "loss_streak", "loss_streak_p99",
                                      "mae_winner_median_pct_stop", "scratch_share", "time_asymmetry", "session_exit_profit_share", "same_bar_share")},
                "frequency": {"trades_per_year_per_instrument": res["trades_per_year_per_instrument"], "session_share": m.get("session_share"),
                              "max_gap_sessions": m.get("max_gap_sessions")}})
            trial_n = self.ledger.count("stage='1' AND stress_mode='candidate' AND status='DONE'")
            gates = {"stage1": res["gates"], "trial_count_used": trial_n}
            pscore = self.prediction_score(prop, res)
            write_json(os.path.join(d, "prediction_score.json"), pscore)
            if res["passed"]:
                stage, status = 1, "STAGE1_PASS"
                st["counts"]["stage1_pass"] += 1
                if confirm is not None and confirm["ok"]:
                    cr = confirm["result"]
                    gates["stage1_confirmation_all_folds"] = cr["gates"]
                    write_json(os.path.join(d, "metrics_stage1_confirmation.json"), {k: cr[k] for k in ("folds", "pooled", "by_instrument", "by_fold",
                                                                                                         "wf", "score", "twin")})
                    if cr["passed"]:
                        status = "CONFIRMED"
                        st["counts"]["confirmed"] += 1
                        prop["confirm"] = cr
                        write_json(os.path.join(d, "gates.json"), gates)
                        from orchestrator import promote
                        status, tier, reason, stage = promote.process(self, prop, cr)
                        gates = read_json(os.path.join(d, "gates.json"))
                        st["counts"][status.lower()] = st["counts"].get(status.lower(), 0) + 1
                    else:
                        status, reason = "HOME_ONLY", "passes only on its island's folds: " + ", ".join(cr["failed_gates"][:4])
                elif confirm is not None:
                    status, reason = "ERROR", confirm["error"]
            else:
                stage, status = 1, "STAGE1_FAIL"
                st["counts"]["stage1_fail"] += 1
                fg = res["failed_gates"]
                reason = ("WR_INTEGRITY: " if any(x.startswith(("wr.", "twin.")) for x in fg) else "") + ", ".join(fg[:4]) + \
                         (f" (+{len(fg) - 4} more)" if len(fg) > 4 else "")
            write_json(os.path.join(d, "gates.json"), gates)
        self.finish(prop, status, stage, tier, reason, res)

    def prediction_score(self, prop, res):
        pred, m = prop["prediction"], res["pooled"]
        act = {"win_rate": m["win_rate"], "profit_factor": m["profit_factor"], "trades_per_year": res["trades_per_year_per_instrument"]}
        inside = {k: bool(pred[k][0] <= act[k] <= pred[k][1]) for k in pred}
        surprise = bool(act["win_rate"] > pred["win_rate"][1] + 0.10 or act["profit_factor"] > pred["profit_factor"][1] * 1.5) and m["n"] >= 100
        return {"predicted": pred, "actual": act, "inside_range": inside, "calibration": sum(inside.values()) / 3.0,
                "flag": "SURPRISE" if surprise else None}

    def finish(self, prop, status, stage, tier, reason, res):
        """States VERDICT, AUTOPSY (graveyard line) and SEAL."""
        n, g, d = prop["generation"], prop["genome"], self.gen_dir(prop["generation"])
        st = self.st
        score = res["score"] if res else 0.0
        m = res["pooled"] if res else {}
        cell = res["descriptors"]["cell"] if res else None
        entry = None
        if res and m.get("n", 0) > 0 and status not in ("VOID", "ERROR"):
            entry = {"generation": n, "genome": g, "score": score, "lineage_id": prop["lineage_id"], "status": status,
                     "metrics": {"win_rate": m["win_rate"], "pf": m["profit_factor"], "tpy": res["trades_per_year_per_instrument"],
                                 "alpha": res["twin"]["win_rate_alpha_pts"], "n": m["n"]}, "complexity": g["complexity"]}
            cells = self.archive[prop["island"]]
            cur = cells.get(cell)
            bkey = (prop["island"], g["primary_timeframe_min"], m["n"], round(m["win_rate"], 6), round(m["profit_factor"], 6))
            if bkey in self.beh:                         # identical trades to an earlier genome: counted as a trial, kept out of the archive
                reason = (reason + "; " if reason else "") + "behavioural duplicate of an earlier genome"
            elif cur is None or score > cur["best"]["score"]:
                old = cur["best"] if cur else None
                cells[cell] = {"best": entry}
                if old and old["score"] >= 0.95 * score and old["complexity"] < g["complexity"]:
                    cells[cell]["simplest"] = old
            elif score >= 0.95 * cur["best"]["score"] and g["complexity"] < cur.get("simplest", cur["best"])["complexity"]:
                cur["simplest"] = entry
            self.beh.add(bkey)
            if score > st["best_score"][prop["island"]]:
                st["best_score"][prop["island"]] = score
                st["best_generation"] = n
        os_ = st["operator_stats"].setdefault(prop["operator"], {"uses": 0, "improved": 0, "passed": 0})
        os_["uses"] += 1
        if prop["parent"] and score > (prop["parent"].get("score") or 0.0):
            os_["improved"] += 1
        elif not prop["parent"] and score > 0.05:
            os_["improved"] += 1
        if stage >= 1 and status not in ("STAGE1_FAIL", "VOID", "ERROR"):
            os_["passed"] += 1
        self.db.execute("INSERT OR REPLACE INTO genomes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        [n, g["genome_id"], prop["lineage_id"], prop["island"], prop["operator"], json.dumps(prop["parents"]),
                         g["primary_timeframe_min"], g["complexity"], status, stage, tier, score, m.get("n", 0), m.get("win_rate"),
                         m.get("profit_factor"), res["twin"]["win_rate_alpha_pts"] if res else None, cell, self.trig_key(g),
                         json.dumps(g, sort_keys=True), prop.get("daily") if m.get("n", 0) >= 30 else None])
        self.ids.add(g["genome_id"])
        if tier is None:
            with open(self.p("ledger/graveyard.jsonl"), "a") as f:
                f.write(json.dumps({"generation": n, "genome_id": g["genome_id"][:16], "atoms": [e["atom"] for e in GN.atom_entries(g)],
                                    "structure": {"trigger": self.trig_key(g), "entry": g["slots"]["entry"]["type"], "tf": g["primary_timeframe_min"],
                                                  "families": sorted({ATOMS[e['atom']].fam for e in GN.atom_entries(g)})},
                                    "stage": stage, "status": status, "failed_gates": (res or {}).get("failed_gates", [])[:8],
                                    "cause": reason[:200], "win_rate": m.get("win_rate"), "alpha": res["twin"]["win_rate_alpha_pts"] if res else None,
                                    "pf": m.get("profit_factor"), "n": m.get("n", 0)}) + "\n")
        write_text(os.path.join(d, "SUMMARY.md"), self.summary(prop, status, stage, reason, res, tier))
        man = []
        for fn in sorted(os.listdir(d)):
            if fn != "MANIFEST.sha256":
                man.append(f"{sha256_file(os.path.join(d, fn))}  {fn}")
        write_text(os.path.join(d, "MANIFEST.sha256"), "\n".join(man) + "\n")
        st["next_generation"] = n + 1
        self.done_this_run += 1

    def summary(self, prop, status, stage, reason, res, tier=None):
        n, g = prop["generation"], prop["genome"]
        lines = [f"# Generation {n}: {status}", "",
                 f"- What: {prop['operator']} on island {prop['island']}, {g['primary_timeframe_min']}-minute primary timeframe, complexity {g['complexity']}.",
                 f"- Result: {status} at stage {stage}." + (f" Reason: {reason}." if reason else ""),
                 f"- Tier: {tier or 'none'}.", "", "```", GN.describe(g), "```", ""]
        if res:
            m, tw = res["pooled"], res["twin"]
            lo, hi = m.get("wilson_lo", 0.0), m.get("wilson_hi", 0.0)
            lines += ["```", "WIN-RATE STATEMENT" + ("" if res["passed"] else "  (stage 1 failed; shown for the record)"),
                      f"Headline win rate (net, flat-to-flat, OOS):   {100 * m['win_rate']:.1f} %   (n = {m['n']} trades)",
                      f"Wilson 95% interval:                          {100 * lo:.1f} % to {100 * hi:.1f} %",
                      f"Geometry baseline (random-entry twin median): {100 * tw['median_win_rate']:.1f} %   ({tw['n_twins']} twins)",
                      f"Win-rate alpha:                               {tw['win_rate_alpha_pts']:+.1f} points (twin p99 = {100 * tw['p99_win_rate']:.1f} %)",
                      f"Random-exit twin win rate:                    {100 * tw['random_exit_win_rate']:.1f} %",
                      f"Payoff ratio:                                 {m.get('payoff', 0.0):.2f}",
                      f"Profit factor:                                {m['profit_factor']:.2f}",
                      f"Expectancy per trade:                         {m.get('expectancy_ticks', 0.0):+.2f} ticks   ({m.get('expectancy_costs', 0.0):+.2f} x round-trip cost)",
                      f"Largest loss / average win:                   {m.get('largest_loss_in_avg_wins', 0.0):.2f}",
                      f"Trades per year per instrument:               {res['trades_per_year_per_instrument']:.0f}",
                      f"Sessions with a trade:                        {100 * m.get('session_share', 0.0):.0f} %", "```", "",
                      f"- Out-of-sample folds scored: {res['folds']} (island {res['island']}). Composite score {res['score']:.4f}.",
                      f"- Failed gates ({len(res['failed_gates'])}): {', '.join(res['failed_gates']) or 'none'}."]
            if res.get("flags"):
                lines.append(f"- Flags: {', '.join(res['flags'])}.")
        lines += ["", "- Next step: " + ("none; recorded in the graveyard." if tier is None else
                                         "held in the hall of fame; re-evaluated each epoch against the growing trial count.")]
        return "\n".join(lines) + "\n"

    # ---------------- epochs
    def epoch_boundary(self):
        st = self.st
        st["epoch"] += 1
        e = st["epoch"]
        lo = (e - 1) * SEARCH["epoch_size"] + 1
        hi = e * SEARCH["epoch_size"]
        rows = self.db.execute("SELECT status, score, alpha, win_rate, pf, n_trades, genome, operator FROM genomes WHERE generation BETWEEN ? AND ?",
                               [lo, hi]).fetchall()
        n = max(1, len(rows))
        cnt = {}
        for r in rows:
            cnt[r[0]] = cnt.get(r[0], 0) + 1
        passes = [r for r in rows if r[0] in ("STAGE1_PASS", "CONFIRMED", "HOME_ONLY")]
        can = sum(1 for r in passes if canary.genome_has_canary(json.loads(r[6])))
        adoption = can / len(passes) if passes else 0.0
        pass_rate = len(passes) / n
        # operator adaptation within the floor (SPEC 10.3)
        floor = SEARCH["operator_share_floor"]
        base = SEARCH["operators"]
        raw = {k: base[k] * (0.5 + (s["improved"] + 1.0) / (s["uses"] + 2.0)) for k, s in st["operator_stats"].items() if k in base}
        tot = sum(raw.values())
        share = {k: max(floor, v / tot) for k, v in raw.items()}
        tot = sum(share.values())
        st["operator_share"] = {k: v / tot for k, v in share.items()}
        occupied = {isl: len(c) for isl, c in self.archive.items()}
        top = sorted((c["best"] for isl in self.archive for c in self.archive[isl].values()), key=lambda x: -x["score"])[:100]
        dists = [GN.distance(top[i]["genome"], top[j]["genome"]) for i in range(len(top)) for j in range(i + 1, min(len(top), i + 12))]
        notes = []
        if pass_rate > 0.15:
            notes.append("stage 1 pass rate above 15%: the screen is too loose and must be tightened (SPEC 10.5)")
        if adoption > 0.02:
            notes.append("canary adoption above 2%: promotion halted for this epoch pending tightening (SPEC 15.1)")
        from orchestrator import promote
        ti = promote.trial_info(self, "none")
        st["n_eff"] = {"raw": ti["raw"], "n_eff": ti["n_eff"], "var_sharpe": ti["var_sharpe"]}
        demoted = []
        f3 = self.p("ledger/stage3_candidates.jsonl")
        if os.path.exists(f3):
            from gates import stats as _stats
            cands = [json.loads(x) for x in open(f3)]
            keep = set(_stats.benjamini_hochberg([c["p_value"] for c in cands], 0.10))
            demoted = [c["generation"] for i, c in enumerate(cands) if i not in keep]
        exch = self.exchange() if e % 5 == 0 else None    # every 2,500 generations (SPEC 15.9)
        hp = self.honeypot_check()
        chain_ok, chain_n = self.ledger.verify_chain()
        rep = {"epoch": e, "generations": [lo, hi], "counts": cnt, "stage1_pass_rate": pass_rate, "canary_adoption_rate": adoption,
               "canary_passes": can, "occupied_cells": occupied, "mean_pairwise_distance_top100": float(np.mean(dists)) if dists else None,
               "best_score": st["best_score"], "best_generation": st["best_generation"], "operator_share": st["operator_share"],
               "operator_stats": st["operator_stats"], "honeypot_voided": hp, "ledger_chain_ok": chain_ok, "ledger_records": chain_n,
               "frozen_ok": frozen_hashes() == st["frozen"], "notes": notes, "utc": utcnow(), "effective_trials": st["n_eff"],
               "outside_false_discovery_set": demoted, "tier_counts": st["tier_counts"], "exchange": exch,
               "raw_stage1_trials": self.ledger.count("stage='1' AND stress_mode='candidate' AND status='DONE'")}
        if e % 2 == 0:                                   # every 1,000 generations (SPEC 15.8)
            from orchestrator import lessons
            lessons.distil(self)
        write_json(self.p("reports/epochs", f"epoch_{e:04d}.json"), rep)
        write_text(self.p("reports/epochs", f"epoch_{e:04d}.md"), self.epoch_md(rep))
        if not hp:
            self.halt("The honeypot check passed a leaking genome.", rep)
        if not chain_ok or not rep["frozen_ok"]:
            self.halt("Ledger chain or frozen-file hash check failed at the epoch boundary.", rep)
        return rep

    def exchange(self, k=10):
        """Island exchange (SPEC 15.9): each island's leading distinct strategies are scored on the other island's
        folds, which never influenced them.  A leader that keeps less than half its score there, or whose profit
        factor there is at or below 1.0, is removed from the archive; survivors migrate to the other island."""
        from gates import stage1 as S1
        gen_now = self.st["next_generation"] - 1
        rows = []
        for isl in ("A", "B"):
            away = "B" if isl == "A" else "A"
            cells = self.archive[isl]
            lead = sorted(((c, v["best"]) for c, v in cells.items() if not v["best"].get("migrated_from")), key=lambda cv: -cv[1]["score"])[:k]
            for cell, e in lead:
                g = e["genome"]
                tid = self.ledger.open(generation=e["generation"], stage="1e", genome_id=g["genome_id"], lineage_id=e.get("lineage_id"),
                                       operator="ISLAND_EXCHANGE", data_slice=f"away_folds_island_{away}", instrument="ES+YM",
                                       timeframe_min=g["primary_timeframe_min"], cost_level="base", stress_mode="candidate+twins",
                                       seed=e["generation"], code_hash="n/a", data_hash=self.st["frozen"]["partition"][:16])
                self.ledger.commit()
                try:
                    res, _ = S1.stage1(g, away, e["generation"], n_twins=200)
                except Exception:
                    self.ledger.close(tid, status="ABORTED")
                    continue
                m = res["pooled"]
                self.ledger.close(tid, n_trades=m["n"], win_rate=m["win_rate"], profit_factor=m["profit_factor"], score=res["score"])
                keep = res["score"] >= 0.5 * e["score"] and m["profit_factor"] > 1.0
                rows.append({"generation": e["generation"], "home": isl, "tf": g["primary_timeframe_min"], "home_score": e["score"],
                             "home_wr": e["metrics"]["win_rate"], "home_pf": e["metrics"]["pf"], "away_score": res["score"], "away_wr": m["win_rate"],
                             "away_pf": m["profit_factor"], "away_alpha": res["twin"]["win_rate_alpha_pts"], "away_n": m["n"], "survived": bool(keep),
                             "strategy": GN.describe(g).split("\n")[1][:90]})
                if not keep:
                    if "simplest" in cells[cell] and cells[cell]["simplest"]["generation"] != e["generation"]:
                        cells[cell] = {"best": cells[cell]["simplest"]}
                    else:
                        del cells[cell]
                    self.db.execute("UPDATE genomes SET status='DEMOTED_EXCHANGE' WHERE generation=?", [e["generation"]])
                else:
                    tgt = self.archive[away]
                    if cell not in tgt or res["score"] > tgt[cell]["best"]["score"]:
                        mig = dict(e)
                        mig.update({"score": res["score"], "migrated_from": isl,
                                    "metrics": {"win_rate": m["win_rate"], "pf": m["profit_factor"], "tpy": res["trades_per_year_per_instrument"],
                                                "alpha": res["twin"]["win_rate_alpha_pts"], "n": m["n"]}})
                        tgt[cell] = {"best": mig}
        self.ledger.commit()
        self.db.commit()
        if not rows:
            return None
        hs, aw = np.array([r["home_score"] for r in rows]), np.array([r["away_score"] for r in rows])
        summ = {"generation": gen_now, "leaders": len(rows), "mean_home_score": float(hs.mean()), "mean_away_score": float(aw.mean()),
                "retention": float(aw.mean() / hs.mean()) if hs.mean() > 0 else 0.0, "mean_home_pf": float(np.mean([r["home_pf"] for r in rows])),
                "mean_away_pf": float(np.mean([r["away_pf"] for r in rows])), "mean_home_wr": float(np.mean([r["home_wr"] for r in rows])),
                "mean_away_wr": float(np.mean([r["away_wr"] for r in rows])), "survivors": int(sum(r["survived"] for r in rows)),
                "demoted": int(sum(not r["survived"] for r in rows))}
        write_json(self.p(f"reports/exchange_{gen_now:06d}.json"), {"summary": summ, "rows": rows})
        L = [f"# Island exchange at generation {gen_now}", "", f"The {k} leading distinct strategies of each island, re-scored on the other "
             "island's three test folds (200 geometry-matched twins). Research data only.", "",
             f"- Mean composite score: {summ['mean_home_score']:.3f} at home, {summ['mean_away_score']:.3f} away (retention {100 * summ['retention']:.0f}%).",
             f"- Mean win rate: {100 * summ['mean_home_wr']:.1f}% at home, {100 * summ['mean_away_wr']:.1f}% away.",
             f"- Mean profit factor: {summ['mean_home_pf']:.2f} at home, {summ['mean_away_pf']:.2f} away.",
             f"- Survivors (kept at least half their score and a profit factor above 1.0): {summ['survivors']} of {len(rows)}; "
             f"{summ['demoted']} removed from the archive.", "",
             "| Generation | Home | Timeframe | Home: score / win rate / PF | Away: score / win rate / PF / alpha / trades | Survived | Strategy |", "|---|---|---|---|---|---|---|"]
        for r in rows:
            L.append(f"| {r['generation']} | {r['home']} | {r['tf']} min | {r['home_score']:.3f} / {100 * r['home_wr']:.1f}% / {r['home_pf']:.2f} | "
                     f"{r['away_score']:.3f} / {100 * r['away_wr']:.1f}% / {r['away_pf']:.2f} / {r['away_alpha']:+.1f} / {r['away_n']} | "
                     f"{'yes' if r['survived'] else 'no'} | {r['strategy']} |")
        write_text(self.p(f"reports/exchange_{gen_now:06d}.md"), "\n".join(L) + "\n")
        return summ

    def honeypot_check(self):
        """A synthetic genome that uses the honeypot must be voided by the static audit (SPEC 15.2)."""
        g = GN.new_genome([GN.A("tr_ema_cross")], regime=[{"atom": canary.HONEYPOT_ID, "params": {"band": 0}}])
        aud = static_audit.audit(g, compile_py.python_source(g), admitted=self.admitted)
        return not aud["clean"] and any(h["rule"] == "hazard_tagged_atom" for h in aud["hits"])

    def header(self):
        st = self.st
        best = max(st["tier_counts"], key=lambda t: (st["tier_counts"][t] > 0, TIERS.index(t))) if any(st["tier_counts"].values()) else "none"
        fdr = "not yet run"
        f = path("reports/milestones/placebo_latest.json")
        if os.path.exists(f):
            pl = read_json(f)
            fdr = (f"{pl['promotions']['bronze']} Bronze, {pl['promotions']['silver']} Silver, {pl['promotions']['gold']} Gold "
                   f"in {pl['generations']} placebo generations")
        return [f"- Generations completed: {st['next_generation'] - 1}" + (" (PLACEBO RUN ON DECOY MARKETS)" if st.get("placebo") else ""),
                f"- Best certified tier: {best}", f"- Vault queries used: {st['vault']['a_used']} of 60 (Vault-A), {st['vault']['b_used']} of 5 (Vault-B)",
                f"- Pipeline false-discovery rate, latest placebo run: {fdr}", ""]

    def epoch_md(self, r):
        L = [f"# Epoch {r['epoch']} report", ""] + self.header()
        L += [f"Generations {r['generations'][0]} to {r['generations'][1]}.", "",
              "| Outcome | Count |", "|---|---|"] + [f"| {k} | {v} |" for k, v in sorted(r["counts"].items())]
        L += ["", f"- Stage 1 pass rate: {100 * r['stage1_pass_rate']:.2f}%.",
              f"- Canary adoption among stage 1 passes: {100 * r['canary_adoption_rate']:.2f}% ({r['canary_passes']} genomes).",
              f"- Occupied archive cells: island A {r['occupied_cells'].get('A', 0)}, island B {r['occupied_cells'].get('B', 0)}.",
              f"- Best composite score so far: A {r['best_score']['A']:.4f}, B {r['best_score']['B']:.4f} (generation {r['best_generation']}).",
              f"- Honeypot genome voided: {r['honeypot_voided']}. Ledger chain intact: {r['ledger_chain_ok']} ({r['ledger_records']} records). Frozen files unchanged: {r['frozen_ok']}.",
              f"- Raw stage 1 trials to date: {r['raw_stage1_trials']}; effective independent trials (clustered): {r['effective_trials']['n_eff']}.",
              f"- Hall of fame: {r['tier_counts']}. Stage 3 candidates outside the 10% false-discovery set: {r['outside_false_discovery_set'] or 'none'}.",
              "", "## Operators", "",
              "| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |", "|---|---|---|---|---|"]
        for k, s in sorted(r["operator_stats"].items()):
            L.append(f"| {k} | {s['uses']} | {s['improved']} | {s['passed']} | {100 * r['operator_share'].get(k, 0):.1f}% |")
        if r["notes"]:
            L += ["", "## Monitor notes", ""] + [f"- {x}" for x in r["notes"]]
        return "\n".join(L) + "\n"

    # ---------------- main loop
    def run(self, generations):
        self.t_start = time.time()
        self.done_this_run = 0
        target = min(SEARCH["generations_total"], self.st["next_generation"] - 1 + generations)
        ctx = mp.get_context("fork")
        self.pool = ctx.Pool(self.workers, initializer=_init_worker, initargs=(self.decoy_spec,))
        last_hb = 0.0
        try:
            while self.st["next_generation"] <= target:
                if os.path.exists(path("STOP")):
                    self.checkpoint()
                    write_text(self.p("reports/STOPPED.md"), "# Stopped\n\n" + "\n".join(self.header()) +
                               f"\nThe STOP file was found at {utcnow()}. The current batch was finished and a checkpoint written.\n")
                    print("STOP file found: halting after checkpoint.")
                    return
                n0 = self.st["next_generation"]
                nb = min(self.st["batch"], target - n0 + 1)
                eb = SEARCH["epoch_size"]
                nb = min(nb, eb - ((n0 - 1) % eb))                       # never straddle an epoch boundary
                props = []
                for n in range(n0, n0 + nb):
                    pr = self.propose(n)
                    if pr is None:
                        self.halt("Could not propose a novel genome after 30 attempts.", {"generation": n})
                    props.append(pr)
                    self.ids.add(pr["genome"]["genome_id"])              # novelty within the batch
                jobs = [(pr, self.prepare(pr)) for pr in props]
                self.ledger.commit()
                outs = dict()
                live = [j for _, j in jobs if j is not None]
                for o in self.pool.imap_unordered(_stage1_job, live, chunksize=1):
                    outs[o["generation"]] = o
                # stage 1 confirmation for home-fold passes: open the ledger rows first, then run
                conf_jobs = []
                for pr, j in jobs:
                    o = outs.get(pr["generation"])
                    if j is not None and o and o["ok"] and o["result"]["passed"]:
                        for s in INSTRUMENTS:
                            for mode in ("candidate", "twin_entry", "twin_exit"):
                                pr.setdefault("confirm_ids", []).append(self.ledger.open(
                                    generation=pr["generation"], stage="1x", genome_id=pr["genome"]["genome_id"], lineage_id=pr["lineage_id"],
                                    operator=pr["operator"], data_slice="wf_folds_345678", instrument=s, timeframe_min=pr["genome"]["primary_timeframe_min"],
                                    cost_level="base", stress_mode=mode, seed=pr["seed"] + 1, code_hash=pr["code_hash"],
                                    data_hash=self.st["frozen"]["partition"][:16]))
                        conf_jobs.append({"genome": pr["genome"], "seed": pr["seed"], "generation": pr["generation"]})
                self.ledger.commit()
                confs = {o["generation"]: o for o in self.pool.imap_unordered(_confirm_job, conf_jobs, chunksize=1)} if conf_jobs else {}
                for pr, j in jobs:                                       # commit in generation order
                    c = confs.get(pr["generation"])
                    if c is not None:
                        for tid in pr.get("confirm_ids", []):
                            self.ledger.close(tid, status="DONE" if c["ok"] else "ABORTED",
                                              n_trades=c["result"]["pooled"]["n"] if c["ok"] else None,
                                              win_rate=c["result"]["pooled"]["win_rate"] if c["ok"] else None,
                                              profit_factor=c["result"]["pooled"]["profit_factor"] if c["ok"] else None)
                    self.commit(pr, outs.get(pr["generation"]) if j is not None else None, c)
                self.ledger.commit()
                self.db.commit()
                if (self.st["next_generation"] - 1) % eb == 0:
                    rep = self.epoch_boundary()
                    if not self.quiet:
                        print(f"epoch {rep['epoch']}: pass rate {100 * rep['stage1_pass_rate']:.2f}%, cells {rep['occupied_cells']}, best {rep['best_score']}")
                self.checkpoint()
                if time.time() - last_hb > 300 or self.st["next_generation"] > target:
                    self.heartbeat("RUNNING")
                    last_hb = time.time()
        finally:
            self.pool.close()
            self.pool.join()
            self.heartbeat("IDLE")


ENV_TXT = (f"python {platform.python_version()}\nplatform {platform.platform()}\n" +
           "\n".join(f"{m} {__import__(m).__version__}" for m in ("numpy", "pandas", "numba", "pyarrow", "scipy", "sklearn", "yaml")) + "\n"
           f"engine {ENGINE_VERSION}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--generations", type=int, default=50)
    ap.add_argument("--placebo", type=int, default=0, help="run this many generations on a decoy market in an isolated folder")
    ap.add_argument("--tag", default="gen0")
    ap.add_argument("--decoy", default="bootstrap:0")
    ap.add_argument("--workers", type=int, default=None)
    a = ap.parse_args()
    if a.placebo:
        kind, i = a.decoy.split(":")
        r = Run(root=path("state", "placebo", a.tag), decoy_spec=(kind, int(i)), workers=a.workers)
        r.run(a.placebo)
    else:
        r = Run(workers=a.workers)
        r.run(a.generations)
    st = r.st
    el = time.time() - r.t_start
    print(json.dumps({"next_generation": st["next_generation"], "counts": st["counts"], "best_score": st["best_score"],
                      "seconds": round(el, 1), "generations_per_hour": round(3600 * r.done_this_run / max(1e-9, el))}, indent=1))


if __name__ == "__main__":
    main()
