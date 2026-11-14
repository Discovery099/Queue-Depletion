"""Promotion ladder beyond stage 1 (SPEC 10.2 steps 7-11, 16.2, 16.3, 16.5).

Runs in the Orchestrator process for the rare candidates that pass stage 1 and its all-folds
confirmation.  Every block of backtests is opened in the trial ledger before it runs.
"""
import json
import os
import shutil

import numpy as np

from engine import ENGINE_VERSION, path, read_json, sha256_file, write_json, write_text
from engine.data import INSTRUMENTS
from gates import stats
from genome import genome as GN
from orchestrator import evaluate as EV
from orchestrator.ledger import utcnow

G = EV.GATES
TIER_ORDER = ["bronze", "silver", "gold"]


def target_tier(m, alpha):
    """Highest tier whose headline floors the confirmed walk-forward record meets."""
    best = "bronze"
    for t in ("silver", "gold"):
        f = G["tiers"][t]
        if m["win_rate"] >= f["win_rate"] and m["profit_factor"] >= f["pf"] and alpha >= f["alpha_pts"] and m["payoff"] >= f["payoff"]:
            best = t
    return best


def trial_info(run, lineage_id, exclude_generation=None):
    """Effective number of independent trials from the stored daily series of all stage 1 trials (SPEC 12.3)."""
    rows = run.db.execute("SELECT generation, daily FROM genomes WHERE daily IS NOT NULL").fetchall()
    sess = EV.fold_sessions(EV.TEST_FOLDS)
    series = [np.frombuffer(b, np.float32)[sess] for g, b in rows if g != exclude_generation]
    raw = run.ledger.count("stage='1' AND stress_mode='candidate' AND status='DONE'")
    if len(series) >= 10:
        e = stats.effective_trials(np.vstack(series), seed=run.st["master_seed"])
        scale = raw / max(1, len(series))
        n_eff = int(np.ceil(e["n_eff"] * max(1.0, scale)))
        var_sr = e["var_sharpe"]
    else:
        n_eff, var_sr, e = max(1, raw), 0.01, {}
    debt = run.db.execute("SELECT COUNT(*) FROM genomes WHERE lineage_id=?", [lineage_id]).fetchone()[0]
    fam = np.vstack(series)[-200:] if len(series) else None
    return {"raw": raw, "n_eff": n_eff, "var_sharpe": var_sr, "lineage_debt": debt,
            "lineage_debt_clusters": int(np.ceil(debt * n_eff / max(1, raw))), "family_daily": fam, "detail": e}


def process(run, prop, res_confirm):
    """Take one confirmed candidate through stages 2-4.  Returns (status, tier, reason)."""
    from gates import stage2 as S2, stage3 as S3
    n, g = prop["generation"], prop["genome"]
    d = run.gen_dir(n)
    rob = os.path.join(d, "robustness")
    os.makedirs(rob, exist_ok=True)
    m, alpha = res_confirm["pooled"], res_confirm["twin"]["win_rate_alpha_pts"]
    aim = target_tier(m, alpha)
    open_ids = []

    def log(label, k):
        for _ in range(max(1, k // 2)):
            for s in INSTRUMENTS if k >= 2 else INSTRUMENTS[:1]:
                open_ids.append(run.ledger.open(generation=n, stage=label.split(".")[0][1:], genome_id=g["genome_id"], lineage_id=prop["lineage_id"],
                                                operator=prop["operator"], data_slice="search_all_folds", instrument=s,
                                                timeframe_min=g["primary_timeframe_min"], cost_level="base", stress_mode=label, seed=prop["seed"],
                                                code_hash=prop["code_hash"], data_hash=run.st["frozen"]["partition"][:16]))
        run.ledger.commit()

    def close_all(status="DONE"):
        for tid in open_ids:
            run.ledger.close(tid, status=status)
        open_ids.clear()
        run.ledger.commit()

    gates_path = os.path.join(d, "gates.json")
    gates = read_json(gates_path)
    tier, stage, status, reason = None, 2, "STAGE2_FAIL", ""
    try:
        r2 = S2.stage2(g, prop["seed"], aim, log=log, quick=getattr(run, "quick_stages", False))
    except Exception as e:                                             # one strategy's failure never stops the loop
        close_all("ABORTED")
        return "ERROR", None, f"stage 2 error: {type(e).__name__}: {e}", 2
    close_all()
    gates["stage2"] = r2["gates"]
    gates["stage2_target_tier"] = aim
    write_json(os.path.join(d, "audit_dynamic.json"), {k: r2["sections"].get(k) for k in ("truncation", "intrabar", "selection_leak", "parity_mode")
                                                       if k in r2["sections"]} | {"replay_and_persistence": pine_audit(g, d, rob)})
    for k, v in r2["sections"].items():
        if k not in ("truncation", "intrabar", "selection_leak", "parity_mode"):
            write_json(os.path.join(rob, f"{k}.json"), v)
    if r2.get("void"):
        write_json(gates_path, gates)
        return "VOID", None, r2["failed_reason"], 2
    if r2.get("failed_reason") == "CANARY":
        write_json(gates_path, gates)
        return "STAGE2_FAIL", None, "CANARY", 2
    if r2.get("simplified"):
        with open(run.p("state/hypothesis_queue.jsonl"), "a") as f:
            f.write(json.dumps({"genome": r2["simplified"], "hypothesis": f"Ablation of generation {n}: one atom's removal changed the score "
                                "by less than the fog noise band, so the simpler genome is proposed in its place (SPEC 12.6)."}) + "\n")
    if r2["bronze_ok"]:
        tier = "bronze"
    if r2["passed"] and aim != "bronze":
        stage = 3
        info = trial_info(run, prop["lineage_id"], n)
        try:
            r3 = S3.stage3(g, prop["seed"], aim, info, log=log, quick=getattr(run, "quick_stages", False))
        except Exception as e:
            close_all("ABORTED")
            write_json(gates_path, gates)
            return "ERROR", tier, f"stage 3 error: {type(e).__name__}: {e}", 3
        close_all()
        gates["stage3"] = r3["gates"]
        gates["trial_count_used"] = {"raw": info["raw"], "n_eff": info["n_eff"], "lineage_debt": info["lineage_debt"]}
        for k, v in r3["sections"].items():
            if k != "red_team":
                write_json(os.path.join(rob, f"s3_{k}.json"), v)
        rt = r3["sections"]["red_team"]
        write_text(os.path.join(d, "redteam.md"), redteam_md(n, rt))
        with open(run.p("ledger/stage3_candidates.jsonl"), "a") as f:
            f.write(json.dumps({"generation": n, "p_value": r3["p_value"], "tier_aim": aim}) + "\n")
        if r3["passed"]:
            tier = "silver"
            stage = 4
            used = run.st.setdefault("holdout_queries", {}).get(prop["lineage_id"], 0)
            if used >= 3:
                reason = "inner-holdout budget of 3 queries for this lineage is spent"
            else:
                run.st["holdout_queries"][prop["lineage_id"]] = used + 1
                log("s4.inner_holdout", 2)
                r4 = S3.stage4(g, prop["seed"], aim, r3["wf_expectancy_costs"])
                close_all()
                gates["stage4_inner_holdout"] = r4["gates"]
                write_json(os.path.join(rob, "inner_holdout.json"), {k: r4[k] for k in ("pooled", "twin_median_win_rate", "alpha_pts", "sessions")})
                if r4["passed"]:
                    status = "STAGE4_PASS"
                    reason = "passed the inner holdout" + (
                        "; eligible for a Vault-A request once every condition of SPEC 16.3 holds" if aim == "gold" else
                        "; Silver floors only, so no vault request (Gold floors are required)")
                else:
                    status, reason = "STAGE4_FAIL", "inner holdout: " + ", ".join(r4["failed_gates"][:4])
        else:
            status, reason = "STAGE3_FAIL", ", ".join(r3["failed_gates"][:5])
            if rt["broken"]:
                reason = "red team break: " + "; ".join(rt["findings"][:2])
    elif not r2["passed"]:
        reason = ", ".join(r2["failed_gates"][:5])
    else:
        status, reason = "STAGE2_PASS", "all stage 2 gates pass at Bronze floors; Silver needs Silver floors on the walk-forward record"
    write_json(gates_path, gates)
    if status.endswith("FAIL") or status == "ERROR":
        write_text(os.path.join(d, "autopsy.md"), autopsy_md(n, g, status, reason, gates))
    if tier:
        hof = run.p("archive/hall_of_fame", tier, f"gen_{n:06d}")
        if os.path.exists(hof):
            shutil.rmtree(hof)
        shutil.copytree(d, hof)
        run.st["tier_counts"][tier] = run.st["tier_counts"].get(tier, 0) + 1
        first = run.st["tier_counts"][tier] == 1
        write_text(run.p("reports/milestones", f"{'first_' if first else ''}{tier}_gen_{n:06d}.md"),
                   "# " + ("First " if first else "") + f"{tier.capitalize()} member: generation {n}\n\n" + "\n".join(run.header()) +
                   f"\n- Status: {status}. {reason}\n- Evidence folder: archive/hall_of_fame/{tier}/gen_{n:06d}\n"
                   "- Limits of the evidence: two highly correlated instruments, regular hours only, 5-minute bars with unknown intrabar order, "
                   "research data only (no vault result), no live fills.\n")
    return status, tier, reason, stage


def pine_audit(g, d, rob):
    """Pine export, static Pine audit, and the independent replay/parity check (SPEC 14.4, 14.7, 18)."""
    try:
        from genome import compile_pine
        from audit import static_audit
        src = compile_pine.export(g)
        write_text(os.path.join(d, "strategy.pine"), src)
        hits = static_audit.scan_pine(src)
        out = {"pine_exported": True, "static_pine_hits": hits}
        try:
            from audit import pine_replay
            par = pine_replay.parity(g, src)
            write_json(os.path.join(rob, "pine_parity.json"), par)
            out.update({"replay_trades_match": par["match"], "signals_vanished": par.get("vanished", None), "signals_late": par.get("late", None)})
        except ImportError:
            out["replay_trades_match"] = None
            out["note"] = "independent Pine replay interpreter not available in this build; parity NOT verified"
        return out
    except ImportError:
        return {"pine_exported": False, "note": "Pine exporter not available in this build"}
    except Exception as e:
        return {"pine_exported": False, "error": f"{type(e).__name__}: {e}"}


def redteam_md(n, rt):
    L = [f"# Red team log, generation {n}", "", f"Budget: {rt['backtests']} of {rt['budget']} research backtests used. "
         f"Outcome: {'BROKEN' if rt['broken'] else 'not broken'}.", "", "| Attack | Result | Broke it |", "|---|---|---|"]
    for a in rt["attacks"]:
        L.append(f"| {a['attack']} | {a['detail'] or a['value']} | {'yes' if a['broke'] else 'no'} |")
    if rt["findings"]:
        L += ["", "## Findings", ""] + [f"- {f}" for f in rt["findings"]]
    return "\n".join(L) + "\n"


def autopsy_md(n, g, status, reason, gates):
    L = [f"# Autopsy, generation {n}", "", f"- Outcome: {status}", f"- Cause: {reason}", "", "```", GN.describe(g), "```", "", "## Failed gates", ""]
    for stage in ("stage2", "stage3", "stage4_inner_holdout"):
        for x in gates.get(stage, []):
            if not x["pass"]:
                L.append(f"- {x['gate']}: value {x['value']} against {x['op']} {x['threshold']}" + (f" ({x['note']})" if x.get("note") else ""))
    L += ["", "## Lesson", "", "Added to the graveyard; distilled into ledger/lessons.md at the next 1,000-generation review."]
    return "\n".join(L) + "\n"
