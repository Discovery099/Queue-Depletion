"""Stage 3 adversarial (SPEC 10.2 step 8; 12.5, 12.7, 12.10, 13.1 hidden timeframes, 7.5 shock costs,
15.5 red team) and stage 4 inner holdout (SPEC 5.4, 16.2).
"""
import copy
import math

import numpy as np
import pandas as pd
from scipy import stats as ss

from audit import truncation
from engine import metrics as M
from engine import sim
from engine.data import HIDDEN_TFS, INSTRUMENTS
from gates import stats
from gates.stage1 import BR, evaluate_slice, freq_floor, gate
from gates.stage2 import frames, pooled, runs_for
from genome import genome as GN
from orchestrator import evaluate as EV

G = EV.GATES
TF = EV.TEST_FOLDS
RED_TEAM_BUDGET = 200


def _expect(tr):
    return float((tr["net_usd"].values / tr["instrument"].map(M.RT_COST_USD).values.astype(float)).mean()) if len(tr) else 0.0


def hidden_timeframes(g):
    """Three off-grid timeframes drawn from the genome's hash, so the lineage cannot know them in advance."""
    rng = np.random.default_rng(int(g["genome_id"][:12], 16))
    return sorted(int(x) for x in rng.choice(np.array(HIDDEN_TFS), 3, replace=False))


def dropped_bar_frames(seed, share=0.005):
    rng = np.random.default_rng([555, seed])
    out = {}
    for s in INSTRUMENTS:
        df = EV._frame(s, "search")
        out[s] = df[rng.random(len(df)) >= share]
    return out


def start_offset_frames(k):
    return {s: EV._frame(s, "search")[lambda d: d["sess"] >= k] for s in INSTRUMENTS}


def session_shuffle_frames(seed):
    from engine import decoys
    rng = np.random.default_rng([8088, seed])
    order = rng.permutation(EV.N_SEARCH)
    out = {}
    for s in INSTRUMENTS:
        df = EV._frame(s, "search").reset_index(drop=True)
        lo, lh, ll, lc, p0 = decoys._logparts(df)
        out[s] = decoys._assemble(df, lo, lh, ll, lc, p0, EV.partition()["instruments"][s]["tick"], order)
    return out


def shift_entries(plan, aux, b, k):
    """Entry signals moved k bars later, wrapping inside the session; exits, stops and targets are those
    of the new bar, and the structural limits must hold there (SPEC 12.7 entry permutation)."""
    idx = np.arange(b.n)
    ln = b.sess_end - b.sess_start + 1
    new = b.sess_start + (idx - b.sess_start + k) % ln
    p = plan.copy()
    for name, valid in (("sigL", aux["validL"]), ("sigS", aux["validS"])):
        z = np.zeros(b.n, np.bool_)
        src = getattr(plan, name)
        z[new[src]] = True
        setattr(p, name, z & valid & ~b.last)
    return p


def red_team(g, seed, base_runs, tr0, m0, nominal_score, quick=False, log=None):
    """Try to break the candidate within a budget of 200 research backtests (SPEC 15.5).
    Returns {'broken': bool, 'findings': [...], 'attacks': [...], 'backtests': n}."""
    log = log or (lambda *a, **k: None)
    tf0 = g["primary_timeframe_min"]
    attacks, findings = [], []
    used = [0]

    def spend(n, label):
        if used[0] + n > RED_TEAM_BUDGET:
            return False
        log("s3.redteam_" + label, n)
        used[0] += n
        return True

    def record(name, value, broken, detail=""):
        attacks.append({"attack": name, "value": value, "broke": bool(broken), "detail": detail})
        if broken:
            findings.append(f"{name}: {detail or value}")

    base_net = m0["net_usd"]
    # 1. stress switches of SPEC 7.6: does any setting turn the strategy unprofitable?
    for k in (1, 2):
        if spend(2, f"entry_delay_{k}"):
            _, m = pooled(runs_for(g, tf0, transform=lambda p, b, k=k: sim.delay_entries(p, b, k)))
            record(f"entry delayed {k} bar(s)", m["net_usd"], m["net_usd"] <= 0, f"net ${m['net_usd']:.0f}, win rate {100 * m['win_rate']:.1f}%")
    if spend(2, "exit_delay"):
        _, m = pooled(runs_for(g, tf0, transform=lambda p, b: sim.delay_exits(p, b, 1)))
        record("discretionary exits delayed 1 bar", m["net_usd"], m["net_usd"] <= 0, f"net ${m['net_usd']:.0f}")
    for i in range(3 if quick else 10):
        if spend(2, "missed_fills"):
            rng = np.random.default_rng([seed, 41, i])
            tr, m = pooled(runs_for(g, tf0, transform=lambda p, b, rng=rng: sim.drop_entries(p, rng, 0.10)))
            if g["slots"]["entry"]["type"] == "limit" and len(tr):       # also lose a random 10% of the limit fills that won
                w = tr.index[tr["is_win"]]
                drop = rng.choice(w, int(0.1 * len(w)), replace=False) if len(w) else []
                net = tr["net_usd"].sum() - tr.loc[drop, "net_usd"].sum()
            else:
                net = m["net_usd"]
            record(f"10% of entries missed (seed {i})", net, net <= 0, f"net ${net:.0f}")
    for i in range(3 if quick else 10):
        if spend(2, "price_jitter"):
            rng = np.random.default_rng([seed, 43, i])
            out = {}
            for s in INSTRUMENTS:
                r = base_runs[s]
                T, *_ = sim.run(sim.jitter_bars(r["bars"], rng), r["plan"], EV.COSTS["base"])
                out[s] = {"trades": M.trades_frame(T, r["bars"], fold_of_sess=EV.FOLD_OF)}
            _, m = pooled(out)
            record(f"1-tick jitter on highs and lows (seed {i})", m["net_usd"], m["net_usd"] <= 0, f"net ${m['net_usd']:.0f}")
    for i in range(2 if quick else 6):
        if spend(2, "bar_drop"):
            with frames(dropped_bar_frames(seed + i)):
                _, m = pooled(runs_for(g, tf0))
            record(f"0.5% of bars deleted (seed {i})", m["net_usd"], m["net_usd"] <= 0, f"net ${m['net_usd']:.0f}")
    if spend(2, "stress_cost"):
        _, m = pooled(runs_for(g, tf0, cost="stress"))
        record("stress costs", m["net_usd"], m["net_usd"] <= 0, f"net ${m['net_usd']:.0f}, profit factor {m['profit_factor']:.2f}")
    # 2. a contiguous 60-session window losing more than 25% of total profit
    sess = EV.fold_sessions(TF)
    d = sum(M.daily_series(base_runs[s]["trades"], sess) for s in INSTRUMENTS).values
    cs = np.r_[0.0, d.cumsum()]
    w60 = (cs[60:] - cs[:-60]).min() if len(d) > 60 else 0.0
    record("worst 60-session window", float(w60), base_net > 0 and -w60 > 0.25 * base_net, f"${w60:.0f} against total ${base_net:.0f}")
    # 3. a parameter move of at most 2 grid steps that halves the profit factor
    worst = None
    for step in (1, 2):
        for h in GN.one_step_neighbours(g, step):
            if not spend(2, "param_move"):
                break
            _, m = pooled(runs_for(h, tf0))
            if worst is None or m["profit_factor"] < worst[0]:
                worst = (m["profit_factor"], step)
    if worst:
        record("worst parameter move within 2 grid steps", worst[0], worst[0] < 0.5 * m0["profit_factor"],
               f"profit factor {worst[0]:.2f} against {m0['profit_factor']:.2f} ({worst[1]} step)")
    # 4. dependence on fewer than 5% of sessions for more than 40% of profit
    top = np.sort(d)[::-1][: max(1, int(0.05 * len(d)))].sum()
    record("profit share of the best 5% of sessions", float(top / base_net) if base_net > 0 else 9.0, base_net > 0 and top > 0.40 * base_net,
           f"{100 * top / base_net:.0f}% of profit" if base_net > 0 else "no profit")
    # 5. a repaint or lookahead path the audits missed: other seeds, other timeframe
    for tf in sorted({tf0, 15, 30}):
        ctx = EV.ctx_for("YM", tf)
        a = truncation.audit(g, ctx.b, ctx.other, EV.EXT_PROVIDER, n=40 if quick else 150, seed=seed + 1000 + tf)
        record(f"truncation re-audit at {tf} minutes (fresh bars)", a["mismatches"], not a["clean"], str(a["first_divergence"]))
    # 6. a simpler genome, at least 30% lower complexity, within 10% of the score
    simpler = None
    cands = []
    for slot in ("regime", "location", "filter"):
        for i in range(len(g["slots"][slot])):
            h = copy.deepcopy(g)
            h["slots"][slot].pop(i)
            cands.append(GN.finalize(h))
    if len(g["slots"]["exit"]) > 1:
        for i in range(len(g["slots"]["exit"])):
            h = copy.deepcopy(g)
            h["slots"]["exit"].pop(i)
            cands.append(GN.finalize(h))
    h = copy.deepcopy(g)
    for slot in ("regime", "location", "filter"):
        h["slots"][slot] = []
    cands.append(GN.finalize(h))
    for h in cands:
        if h["complexity"] <= 0.7 * g["complexity"] and not GN.validate(h) and spend(2, "simpler"):
            e = evaluate_slice(h, runs_for(h, tf0), TF, 100, seed + 5, tier=BR)
            if e["score"] >= 0.9 * nominal_score and (simpler is None or e["score"] > simpler[1]):
                simpler = (h, e["score"])
    record("simpler genome within 10% of the score", simpler[1] if simpler else None, simpler is not None,
           f"complexity {simpler[0]['complexity']} against {g['complexity']}" if simpler else "none found")
    hard = [f for f in findings if not f.startswith("simpler genome")]
    return {"broken": bool(hard), "findings": findings, "attacks": attacks, "backtests": used[0], "budget": RED_TEAM_BUDGET,
            "simpler_genome": simpler[0] if simpler else None}


def stage3(g, seed, tier_name, trial_info, quick=False, log=None):
    """trial_info: {'n_eff', 'var_sharpe', 'raw', 'lineage_debt', 'family_daily': array or None}."""
    log = log or (lambda *a, **k: None)
    tier = G["tiers"][tier_name]
    tf0 = g["primary_timeframe_min"]
    out = {"gates": [], "sections": {}, "flags": []}
    gates = out["gates"]
    log("s3.nominal", 2)
    base = runs_for(g, tf0)
    nominal = evaluate_slice(g, base, TF, G["twins"]["n"], seed, tier=BR, full_thresholds=True)
    tr0, m0 = pooled(base)
    sess = EV.fold_sessions(TF)
    daily = sum(M.daily_series(base[s]["trades"], sess) for s in INSTRUMENTS).values

    # ---- red team (15.5)
    rt = red_team(g, seed, base, tr0, m0, nominal["score"], quick, log)
    out["sections"]["red_team"] = {k: rt[k] for k in ("broken", "findings", "attacks", "backtests", "budget")}
    out["simpler_genome"] = rt["simpler_genome"]
    gates.append(gate("s3.red_team_unbroken", int(not rt["broken"]), 1))

    # ---- deflated statistics with the full trial count (12.5)
    n_trials = max(trial_info["n_eff"], trial_info.get("lineage_debt_clusters", 1))
    dsr, sr, sr0 = stats.deflated_sharpe(daily, n_trials, trial_info["var_sharpe"])
    tw = nominal["twin"]
    twin_sd = max(1e-6, (tw["p95_win_rate"] - tw["median_win_rate"]) / 1.645)
    null_max = tw["median_win_rate"] + twin_sd * ss.norm.ppf(0.95 ** (1.0 / max(2, n_trials)))
    p_sr = float(1 - ss.norm.cdf(sr * math.sqrt(len(daily)))) if sr > 0 else 1.0
    out["sections"]["deflated"] = {"trials_used": n_trials, "raw_trials": trial_info["raw"], "n_eff": trial_info["n_eff"],
                                   "deflated_sharpe_probability": dsr, "sharpe_per_session": sr, "expected_max_sharpe_of_null": sr0,
                                   "win_rate": m0["win_rate"], "null_max_win_rate_p95": float(null_max), "p_value": p_sr}
    out["p_value"] = p_sr
    if tier_name != "bronze":
        gates.append(gate("s3.deflated_sharpe_probability", dsr, tier["dsr_min"]))
    gates.append(gate("s3.deflated_win_rate_alpha", m0["win_rate"] - null_max, 0, ">",
                      "win rate must exceed the 95th percentile of the best of N_eff random-entry twins"))
    fam = trial_info.get("family_daily")
    if fam is not None and len(fam):
        log("s3.reality_check", 0)
        p_rc = stats.reality_check(daily, np.zeros(len(daily)), fam, n=300 if quick else 2000, seed=seed)
        out["sections"]["reality_check"] = {"p_value": p_rc, "family_size": len(fam), "benchmark": "flat (no position)"}
        gates.append(gate("s3.reality_check_p_value", p_rc, 0.05, "<="))

    # ---- resampling (12.7)
    tv = tr0["instrument"].map(EV.TV).values.astype(float)
    order = np.argsort(tr0["entry_ts"].values)
    bs = stats.block_bootstrap(tr0["net_usd"].values[order], tv[order], 10, 500 if quick else 5000, seed)
    out["sections"]["trade_bootstrap"] = bs
    gates.append(gate("s3.bootstrap_pf_p5", bs["pf_p5"], G["resampling"]["bootstrap_pf_p5"]))
    gates.append(gate("s3.bootstrap_win_rate_p5", bs["wr_p5"], tier["win_rate"] - G["resampling"]["bootstrap_wr_margin_pts"] / 100.0))
    nperm = 100 if quick else 1000
    rng = np.random.default_rng([seed, 71])
    perm_exp = np.zeros(nperm)
    log("s3.entry_permutation", 2 * nperm)
    for i in range(nperm):
        tot, cnt = 0.0, 0
        for s in INSTRUMENTS:
            r = base[s]
            b = r["bars"]
            k = max(2, int(round(int(rng.integers(20, 201)) * 5.0 / b.tf)))
            p = shift_entries(r["plan"], r["aux"], b, k)
            T, *_ = sim.run(b, p, EV.COSTS["base"])
            keep = np.isin(EV.FOLD_OF[b.sess[T[:, sim.C["entry_idx"]].astype(int)]], TF) if len(T) else np.zeros(0, bool)
            tot += (T[keep, sim.C["net_pts"]] * b.pv / M.RT_COST_USD[s]).sum()
            cnt += int(keep.sum())
        perm_exp[i] = tot / cnt if cnt else 0.0
    p99 = float(np.percentile(perm_exp, G["resampling"]["permutation_percentile"]))
    out["sections"]["entry_permutation"] = {"candidate_expectancy_costs": m0["expectancy_costs"], "shifted_p99": p99, "shifted_median": float(np.median(perm_exp)), "n": nperm}
    gates.append(gate("s3.entry_permutation_above_p99", m0["expectancy_costs"] - p99, 0, ">"))
    log("s3.session_shuffle", 2)
    with frames(session_shuffle_frames(seed)):
        _, msh = pooled(runs_for(g, tf0))
    chg = abs(msh["expectancy_costs"] / m0["expectancy_costs"] - 1.0) if m0["expectancy_costs"] > 0 else 9.0
    out["sections"]["session_shuffle"] = {"expectancy_costs": msh["expectancy_costs"], "relative_change": chg}
    gates.append(gate("s3.session_shuffle_relative_change", chg, 0.30, "<="))
    pfs = []
    for k in (range(1, 21, 5) if quick else range(1, 21)):
        log("s3.start_offset", 2)
        with frames(start_offset_frames(k)):
            _, mk = pooled(runs_for(g, tf0))
        pfs.append(mk["profit_factor"])
    out["sections"]["start_point"] = {"pf_min": float(min(pfs)), "pf_max": float(max(pfs)), "pf_cv": float(np.std(pfs) / np.mean(pfs)) if np.mean(pfs) > 0 else 9.0}
    gates.append(gate("s3.start_point_pf_cv", out["sections"]["start_point"]["pf_cv"], 0.10, "<="))

    # ---- stability (12.10)
    r6, n6 = M.rolling_window_share(tr0, sess, 126)
    r3, n3 = M.rolling_window_share(tr0, sess, 63)
    gates.append(gate("s3.profitable_rolling_6_month_windows", r6, tier["roll6m"]))
    gates.append(gate("s3.profitable_rolling_3_month_windows", r3, G["stability"]["roll3m"]))
    x = (tr0["net_usd"].values / tr0["instrument"].map(M.RT_COST_USD).values.astype(float))[order]
    decay = {"flag": False}
    if len(x) >= 500:
        roll = pd.Series(x).rolling(250).mean().dropna().values
        t = np.arange(len(roll)) / (len(x) / (len(sess) / 252.0))          # years
        sl, ic, rv, pv, se = ss.linregress(t, roll)
        rel = sl / roll.mean() if roll.mean() > 0 else 0.0
        decay = {"slope_per_year_relative": float(rel), "p_value": float(pv), "flag": bool(rel < -0.30 and pv < 0.05)}
    out["sections"]["stability"] = {"rolling_6m": r6, "windows_6m": n6, "rolling_3m": r3, "windows_3m": n3, "edge_decay": decay}
    if decay["flag"]:
        out["flags"].append("DECAYING: capped at Silver")
    worst_cell = 9.0
    cells = {}
    for c, t in tr0.groupby("regime_cell"):
        if c >= 0 and len(t) >= 50:
            pf = M.basic(t["net_usd"].values, t["instrument"].map(EV.TV).values.astype(float))["profit_factor"]
            cells[int(c)] = {"n": int(len(t)), "profit_factor": pf}
            worst_cell = min(worst_cell, pf)
    out["sections"]["regime_cells"] = cells
    gates.append(gate("s3.worst_regime_cell_pf", worst_cell, 1.0))

    # ---- hidden off-grid timeframes (13.1) and shock costs (7.5)
    hid = {}
    for tf in hidden_timeframes(g):
        log(f"s3.hidden_tf_{tf}", 2)
        e = evaluate_slice(g, runs_for(g, tf), TF, 100, seed + tf, tier=BR, tf=tf)
        m = e["pooled"]
        hid[tf] = {"win_rate": m["win_rate"], "profit_factor": m["profit_factor"], "alpha_pts": e["twin"]["win_rate_alpha_pts"],
                   "passes": bool(m["win_rate"] >= tier["win_rate_each"] and m["profit_factor"] >= tier["pf_worst_fold"] and e["twin"]["win_rate_alpha_pts"] > 0
                                  and e["trades_per_year_per_instrument"] >= freq_floor(tf)["trades_per_year"] * (0.75 if tier_name == "bronze" else 1.0))}
    out["sections"]["hidden_timeframes"] = hid
    gates.append(gate("s3.hidden_timeframes_passing", sum(v["passes"] for v in hid.values()), tier.get("hidden_tfs", 2)))
    log("s3.shock_costs", 2)
    _, mk = pooled(runs_for(g, tf0, cost="shock"))
    out["sections"]["shock_costs"] = {"net_usd": mk["net_usd"], "profit_factor": mk["profit_factor"]}
    gates.append(gate("s3.shock_cost_net", mk["net_usd"], 0, ">"))
    _, mnsd = pooled(runs_for(g, tf0, loss_standdown=0))
    out["sections"]["loss_guard_effect"] = {"with_guard": {"win_rate": m0["win_rate"], "profit_factor": m0["profit_factor"], "n": m0["n"]},
                                            "without_guard": {"win_rate": mnsd["win_rate"], "profit_factor": mnsd["profit_factor"], "n": mnsd["n"]}}
    # tier floors at this stage
    for name, val, thr in (("win_rate_pooled", m0["win_rate"], tier["win_rate"]), ("profit_factor_pooled", m0["profit_factor"], tier["pf"]),
                           ("payoff_ratio", m0["payoff"], tier["payoff"]), ("expectancy_costs", m0["expectancy_costs"], tier["exp_costs"]),
                           ("win_rate_alpha_pts", nominal["twin"]["win_rate_alpha_pts"], tier["alpha_pts"]),
                           ("wilson_lower", m0["wilson_lo"], tier["wilson_lo"])):
        gates.append(gate(f"s3.floor_{tier_name}.{name}", val, thr))
    gates.append(gate(f"s3.floor_{tier_name}.largest_loss_in_average_wins", m0.get("largest_loss_in_avg_wins", 99.0), tier["largest_loss_avg_wins"], "<="))
    out["passed"] = all(x["pass"] for x in gates)
    out["failed_gates"] = [x["gate"] for x in gates if not x["pass"]]
    out["wf_expectancy_costs"] = m0["expectancy_costs"]
    return out


def stage4(g, seed, tier_name, wf_expectancy_costs):
    """Inner holdout (SPEC 5.4): the final 15% of Research sessions, opened only here.  Features warm up
    on the search sessions; only holdout trades are scored."""
    tier = G["tiers"][tier_name]
    tf0 = g["primary_timeframe_min"]
    lo, hi = EV.N_SEARCH, EV.partition()["research"]["sessions"]
    trs, tw = [], np.zeros((G["twins"]["n"], 5))
    for i, s in enumerate(INSTRUMENTS):
        r = EV.run(g, s, tf0, scope="holdout")
        b = r["bars"]
        trs.append(r["trades"][r["trades"]["sess"] >= lo])
        tw += EV.twin_runs(r, b.sess >= lo, G["twins"]["n"], seed + 97 * (i + 1))
    EV.clear_caches()                                   # nothing computed on holdout bars stays in memory
    tr = pd.concat(trs, ignore_index=True)
    m = M.evaluate(tr, np.arange(lo, hi), EV.TV)
    with np.errstate(divide="ignore", invalid="ignore"):
        twr = np.where(tw[:, 1] > 0, tw[:, 0] / tw[:, 1], 0.0)
    alpha = 100 * (m["win_rate"] - float(np.median(twr)))
    fl = freq_floor(tf0)
    gates = [gate("s4.win_rate", m["win_rate"], tier["win_rate"]), gate("s4.profit_factor", m["profit_factor"], tier["pf"]),
             gate("s4.win_rate_alpha_pts", alpha, tier["alpha_pts"]), gate("s4.payoff_ratio", m.get("payoff", 0.0), tier["payoff"]),
             gate("s4.expectancy_retention", m.get("expectancy_costs", 0.0) / wf_expectancy_costs if wf_expectancy_costs > 0 else 0.0,
                  1.0 - G["inner_holdout"]["max_degradation"]),
             gate("s4.trades_per_year", m["trades_per_year"], fl["trades_per_year"] * (0.75 if tier_name == "bronze" else 1.0)),
             gate("s4.wilson_lower", m["wilson_lo"], tier["wilson_lo"] - 0.04, ">=", "holdout sample is small: floor minus 4 points")]
    return {"gates": gates, "passed": all(x["pass"] for x in gates), "failed_gates": [x["gate"] for x in gates if not x["pass"]],
            "pooled": {k: m.get(k) for k in ("n", "win_rate", "wilson_lo", "wilson_hi", "profit_factor", "payoff", "expectancy_costs", "trades_per_year",
                                             "session_share", "largest_loss_in_avg_wins")},
            "twin_median_win_rate": float(np.median(twr)), "alpha_pts": alpha, "sessions": hi - lo}
