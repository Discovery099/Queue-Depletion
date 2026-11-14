"""Stage 2 robustness (SPEC 10.2 step 7; 12.4, 12.6, 12.8, 13.3-13.5, 14.3-14.6, 15.3, 7.5).

Runs for candidates that passed stage 1 on their home folds AND the all-folds confirmation.  Order:
canary check, dynamic audits (a failure voids the generation), then the robustness gates.
Everything here uses the search sessions of the Research block only.
"""
import copy
import math

import numpy as np
import pandas as pd

from audit import canary, truncation
from engine import decoys
from engine import metrics as M
from engine.data import CORE_TFS, INSTRUMENTS
from gates import stats
from gates.stage1 import BR, evaluate_slice, gate
from genome import genome as GN
from orchestrator import evaluate as EV

G = EV.GATES
TF = EV.TEST_FOLDS


def runs_for(g, tf, **kw):
    return {s: EV.run(g, s, tf, **kw) for s in INSTRUMENTS}


def pooled(runs, folds=TF):
    tr = pd.concat([runs[s]["trades"] for s in INSTRUMENTS], ignore_index=True)
    tr = tr[tr["fold"].isin(folds)]
    return tr, M.evaluate(tr, EV.fold_sessions(folds), EV.TV)


# ------------------------------------------------------------------ frame transforms (research data only)
def mirror_frames():
    """Inverted market (SPEC 12.8): prices reflected around the first price, highs and lows swapped."""
    out = {}
    for s in INSTRUMENTS:
        df = EV._frame(s, "search").copy()
        k = 2.0 * df["open"].values[0]
        o, h, l, c = df["open"].values, df["high"].values, df["low"].values, df["close"].values
        df["open"], df["high"], df["low"], df["close"] = k - o, k - l, k - h, k - c
        out[s] = df
    return out


def drift_neutral_frames():
    """Each session's open-to-close drift removed proportionally along the session (SPEC 12.8).
    Overnight gaps are kept, so the offset accumulates across sessions."""
    out = {}
    for s in INSTRUMENTS:
        df = EV._frame(s, "search").copy()
        tick = EV.partition()["instruments"][s]["tick"]
        sess = df["sess"].values
        starts = np.flatnonzero(np.r_[True, sess[1:] != sess[:-1]])
        ends = np.r_[starts[1:], len(df)]
        o, h, l, c = (df[k].values.astype(float).copy() for k in ("open", "high", "low", "close"))
        off = 0.0
        for a, z in zip(starts, ends):
            n = z - a
            drift = c[z - 1] - o[a]
            fo = np.arange(n) / n
            fc = (np.arange(n) + 1.0) / n
            o[a:z] -= off + drift * fo
            c[a:z] -= off + drift * fc
            h[a:z] -= off + drift * (fo + fc) / 2
            l[a:z] -= off + drift * (fo + fc) / 2
            off += drift
        r = lambda x: np.round(x / tick) * tick   # noqa: E731
        o, c = r(o), r(c)
        df["open"], df["close"] = o, c
        df["high"], df["low"] = np.maximum(r(h), np.maximum(o, c)), np.minimum(r(l), np.minimum(o, c))
        out[s] = df
    return out


def regime_shuffle_frames(seed):
    """Sessions recombined in random order within each regime cell (SPEC 13.5 synthetic relative 3)."""
    rng = np.random.default_rng([31337, seed])
    cells = EV.regime_cells("ES")
    order = np.arange(EV.N_SEARCH)
    for c in np.unique(cells):
        idx = np.flatnonzero(cells == c)
        order[idx] = rng.permutation(idx)
    out = {}
    for s in INSTRUMENTS:
        df = EV._frame(s, "search").reset_index(drop=True)
        lo, lh, ll, lc, p0 = decoys._logparts(df)
        out[s] = decoys._assemble(df, lo, lh, ll, lc, p0, EV.partition()["instruments"][s]["tick"], order)
    return out


def blended_frames():
    """Equal-volatility-weighted average of ES and YM returns, rescaled to each price level
    (SPEC 13.5 synthetic relative 1).  Not a new market."""
    fr = {s: EV._frame(s, "search").reset_index(drop=True) for s in INSTRUMENTS}
    parts = {s: decoys._logparts(fr[s]) for s in INSTRUMENTS}
    sd = {s: parts[s][3].std() for s in INSTRUMENTS}
    key = {s: pd.Index(fr[s]["ts_utc_ns"].values) for s in INSTRUMENTS}
    out = {}
    for s in INSTRUMENTS:
        o = "YM" if s == "ES" else "ES"
        j = key[o].get_indexer(key[s])
        ok = j >= 0
        jj = np.maximum(j, 0)
        mix = []
        for k in range(4):
            a, b = parts[s][k], parts[o][k]
            mix.append(np.where(ok, 0.5 * (a + b[jj] * sd[s] / sd[o]), a))
        lo, lh, ll, lc = mix
        top, bot = np.maximum(lo, lc), np.minimum(lo, lc)
        out[s] = decoys._assemble(fr[s], lo, np.maximum(lh, top), np.minimum(ll, bot), lc, parts[s][4], EV.partition()["instruments"][s]["tick"])
    return out


class frames:
    """Context manager: evaluate on a transformed market, then restore the research data."""

    def __init__(self, fr):
        self.fr = fr

    def __enter__(self):
        self.prev = dict(EV.FRAME_OVERRIDE)
        EV.set_frames(self.fr)

    def __exit__(self, *a):
        EV.set_frames(self.prev or None)


# ------------------------------------------------------------------ the stage
def stage2(g, seed, tier_name="bronze", quick=False, log=None):
    """Returns a result dict with 'gates', 'passed', 'void', 'tier_ok' and detailed sections.
    `log(stage_label, n_backtests)` is called before each block of backtests so the caller can open ledger rows."""
    log = log or (lambda *a, **k: None)
    tier = G["tiers"][tier_name]
    tf0 = g["primary_timeframe_min"]
    out = {"gates": [], "sections": {}, "void": False, "flags": []}
    gates = out["gates"]

    # ---- canary (15.1)
    if canary.genome_has_canary(g):
        out.update({"passed": False, "failed_reason": "CANARY"})
        gates.append(gate("s2.no_canary_atoms", 0, 1))
        return out
    gates.append(gate("s2.no_canary_atoms", 1, 1))

    # ---- dynamic truncation audit (14.3): decisive, performance-blind
    aud = {}
    for s in INSTRUMENTS:
        ctx = EV.ctx_for(s, tf0)
        aud[s] = truncation.audit(g, ctx.b, ctx.other, EV.EXT_PROVIDER, n=60 if quick else 300, seed=seed)
    out["sections"]["truncation"] = aud
    clean = all(a["clean"] for a in aud.values())
    gates.append(gate("s2.truncation_audit_clean", int(clean), 1))
    if not clean:
        out.update({"passed": False, "void": True, "failed_reason": "LOOKAHEAD: " + str(next(a["first_divergence"] for a in aud.values() if not a["clean"]))})
        return out

    # ---- base record on all six folds, nominal
    log("s2.nominal", 2)
    base_runs = runs_for(g, tf0)
    nominal = evaluate_slice(g, base_runs, TF, G["twins"]["n"], seed, tier=BR, full_thresholds=True)
    tr0, m0 = pooled(base_runs)
    out["sections"]["nominal"] = {k: nominal[k] for k in ("pooled", "twin", "score", "wf")}

    # ---- intrabar sensitivity (14.5) and selection leak (14.6)
    log("s2.intrabar_optimistic", 2)
    _, mo = pooled(runs_for(g, tf0, optimistic=True))
    gap = 100 * (mo["win_rate"] - m0["win_rate"])
    out["sections"]["intrabar"] = {"pessimistic_win_rate": m0["win_rate"], "optimistic_win_rate": mo["win_rate"], "gap_pts": gap,
                                   "same_bar_share": m0.get("same_bar_share", 0.0)}
    gates.append(gate("s2.intrabar_win_rate_gap_pts", gap, G["robustness"]["intrabar_wr_gap_pts"], "<=", "above the limit caps the strategy at Bronze"))
    if m0.get("same_bar_share", 0.0) > G["robustness"]["same_bar_share_flag"]:
        out["flags"].append("SAME_BAR_TRADES")
    out["sections"]["selection_leak"] = {
        "data_derived_constants": [], "note": "Every numeric value in the genome is a grid parameter chosen by the search on walk-forward "
        "folds; thresholds that depend on data (percentile ranks, regime terciles, volatility scalers) are rolling or expanding "
        "estimates computed inside the strategy. No constant was computed on data overlapping a test fold."}
    gates.append(gate("s2.selection_leak_constants", 0, 0, "<="))

    # ---- pine parity mode difference (7.4): never a gate input, reported
    log("s2.fill_at_signal_close", 2)
    _, mc = pooled(runs_for(g, tf0, fill_at_close=True))
    out["sections"]["parity_mode"] = {"default_expectancy_costs": m0["expectancy_costs"], "signal_close_expectancy_costs": mc["expectancy_costs"]}
    gates.append(gate("s2.edge_survives_next_bar_fill", m0["expectancy_costs"], 0, ">", "edge must not exist only when filling at the signal close"))

    # ---- core timeframes (13.3)
    tfs = {}
    for tf in CORE_TFS:
        log(f"s2.timeframe_{tf}", 2)
        r = base_runs if tf == tf0 else runs_for(g, tf)
        e = nominal if tf == tf0 else evaluate_slice(g, r, TF, 100, seed + tf, tier=BR, full_thresholds=True, tf=tf)
        m = e["pooled"]
        ok = (m["win_rate"] >= tier["win_rate_each"] and m["profit_factor"] >= tier["pf_worst_fold"] and m["payoff"] >= tier["payoff"]
              and e["trades_per_year_per_instrument"] >= e_floor(tf, tier_name) and not [x for x in e["failed_gates"] if x.startswith("wr.")])
        tfs[tf] = {"win_rate": m["win_rate"], "profit_factor": m["profit_factor"], "n": m["n"], "alpha_pts": e["twin"]["win_rate_alpha_pts"],
                   "alpha_above_p95": m["win_rate"] > e["twin"]["p95_win_rate"], "trades_per_year": e["trades_per_year_per_instrument"],
                   "expectancy_costs": m["expectancy_costs"], "passes_tier_floors": bool(ok), "score": e["score"]}
    out["sections"]["timeframes"] = tfs
    pf = [v["profit_factor"] for v in tfs.values()]
    wr = [v["win_rate"] for v in tfs.values()]
    n_pass = sum(v["passes_tier_floors"] for v in tfs.values())
    gates.append(gate("s2.core_timeframes_passing", n_pass, tier["core_tfs"]))
    gates.append(gate("s2.worst_timeframe_pf", min(pf), G["timeframes"]["worst_pf_min"]))
    gates.append(gate("s2.timeframe_win_rate_spread_pts", 100 * (max(wr) - min(wr)), G["timeframes"]["wr_spread_pts"], "<="))
    gates.append(gate("s2.alpha_positive_every_timeframe", min(v["alpha_pts"] for v in tfs.values()), 0, ">"))
    gates.append(gate("s2.alpha_above_twin_p95_every_timeframe", int(all(v["alpha_above_p95"] for v in tfs.values())), 1))
    gates.append(gate("s2.timeframe_pf_cv", float(np.std(pf) / np.mean(pf)) if np.mean(pf) > 0 else 9.0, G["timeframes"]["pf_cv_max"], "<="))
    two_worst = sorted(v["score"] for v in tfs.values())[:2]
    out["two_worst_timeframe_score"] = float(np.mean(two_worst))

    # ---- bar alignment (13.4)
    align = {}
    worst_ratio, worst_gap = 9.0, 0.0
    for tf in CORE_TFS:
        if tf == 5 or quick:
            continue
        for off in range(1, tf // 5):
            log(f"s2.alignment_{tf}_{off}", 2)
            _, m = pooled(runs_for(g, tf, offset=off))
            ratio = m["profit_factor"] / tfs[tf]["profit_factor"] if tfs[tf]["profit_factor"] > 0 else 0.0
            wgap = 100 * abs(m["win_rate"] - tfs[tf]["win_rate"])
            align[f"{tf}m+{5 * off}"] = {"pf_ratio": ratio, "wr_gap_pts": wgap}
            worst_ratio, worst_gap = min(worst_ratio, ratio), max(worst_gap, wgap)
    out["sections"]["alignment"] = align
    if align:
        gates.append(gate("s2.alignment_pf_ratio", worst_ratio, G["timeframes"]["alignment_pf_ratio"]))
        gates.append(gate("s2.alignment_win_rate_gap_pts", worst_gap, G["timeframes"]["alignment_wr_pts"], "<="))

    # ---- stress costs (7.5)
    log("s2.stress_costs", 2)
    _, ms = pooled(runs_for(g, tf0, cost="stress"))
    out["sections"]["stress_costs"] = {"profit_factor": ms["profit_factor"], "net_usd": ms["net_usd"], "win_rate": ms["win_rate"]}
    gates.append(gate("s2.stress_cost_pf", ms["profit_factor"], G["costs"]["stress_pf_min"]))

    # ---- drift and direction (12.8)
    lg, sh = tr0[tr0["direction"] > 0], tr0[tr0["direction"] < 0]
    bl = M.basic(lg["net_usd"].values, lg["instrument"].map(EV.TV).values.astype(float)) if len(lg) else M.basic(np.array([]), 1.0)
    bs = M.basic(sh["net_usd"].values, sh["instrument"].map(EV.TV).values.astype(float)) if len(sh) else M.basic(np.array([]), 1.0)
    out["sections"]["long_short"] = {"long": {k: bl[k] for k in ("n", "win_rate", "profit_factor")}, "short": {k: bs[k] for k in ("n", "win_rate", "profit_factor")}}
    if g["direction"] == "both_mirrored":
        gates.append(gate("s2.weaker_side_pf", min(bl["profit_factor"], bs["profit_factor"]), G["robustness"]["side_pf_min"]))
        gates.append(gate("s2.long_short_win_rate_gap_pts", 100 * abs(bl["win_rate"] - bs["win_rate"]), G["robustness"]["side_wr_gap_pts"], "<="))
    log("s2.drift_neutral", 2)
    with frames(drift_neutral_frames()):
        _, md = pooled(runs_for(g, tf0))
    keep = md["expectancy_costs"] / m0["expectancy_costs"] if m0["expectancy_costs"] > 0 else 0.0
    out["sections"]["drift_neutral"] = {"expectancy_costs": md["expectancy_costs"], "retention": keep, "win_rate": md["win_rate"]}
    gates.append(gate("s2.drift_neutral_expectancy_retention", keep, G["robustness"]["drift_neutral_retention"]))
    log("s2.inverted_market", 2)
    with frames(mirror_frames()):
        _, mi = pooled(runs_for(g, tf0))
    out["sections"]["inverted_market"] = {"profit_factor": mi["profit_factor"], "win_rate": mi["win_rate"], "expectancy_costs": mi["expectancy_costs"]}
    if g["direction"] == "both_mirrored":
        gates.append(gate("s2.inverted_market_pf", mi["profit_factor"], 1.0, ">"))
        gates.append(gate("s2.inverted_market_expectancy_retention", mi["expectancy_costs"] / m0["expectancy_costs"] if m0["expectancy_costs"] > 0 else 0.0, 0.5))

    # ---- cross-instrument (13.5)
    per = nominal["by_instrument"]
    gates.append(gate("s2.each_instrument_win_rate", min(per[s]["win_rate"] for s in INSTRUMENTS), tier["win_rate_each"]))
    gates.append(gate("s2.each_instrument_pf", min(per[s]["profit_factor"] for s in INSTRUMENTS), tier["pf_worst_fold"]))
    nb1 = GN.one_step_neighbours(g, 1)
    nb2 = [] if quick else GN.one_step_neighbours(g, 2)
    neigh = {"one": [], "two": []}
    cfg_daily = [daily_blocks(base_runs)]
    exp_by_inst = {s: [per[s]["expectancy_costs"]] for s in INSTRUMENTS}
    for name, lst in (("one", nb1), ("two", nb2)):
        for h in lst:
            log(f"s2.neighbour_{name}", 2)
            r = runs_for(h, tf0)
            e = evaluate_slice(h, r, TF, 100, seed + 13, tier=BR, full_thresholds=True)
            neigh[name].append({"passed": e["passed"], "score": e["score"], "pf": e["pooled"]["profit_factor"], "win_rate": e["pooled"]["win_rate"]})
            cfg_daily.append(daily_blocks(r))
            for s in INSTRUMENTS:
                exp_by_inst[s].append(e["by_instrument"][s]["expectancy_costs"])
    # zero-shot transfer: choose among {candidate + neighbours} on one instrument, evaluate on the other
    transfer = {}
    for a, b in (("ES", "YM"), ("YM", "ES")):
        pick = int(np.argmax(exp_by_inst[a]))
        native = max(exp_by_inst[b])
        transfer[f"{a}_to_{b}"] = exp_by_inst[b][pick] / native if native > 0 else 0.0
    out["sections"]["transfer"] = transfer
    gates.append(gate("s2.zero_shot_transfer_retention", min(transfer.values()), G["robustness"]["transfer_retention"]))
    # divergence days (reported)
    dES = M.daily_series(base_runs["ES"]["trades"], np.arange(EV.N_SEARCH))
    bE, bY = EV.bars_for("ES", 5), EV.bars_for("YM", 5)
    rE = pd.Series(bE.c[bE.last] / bE.o[bE.first] - 1, index=bE.sess[bE.last])
    rY = pd.Series(bY.c[bY.last] / bY.o[bY.first] - 1, index=bY.sess[bY.last])
    spread = (rE - rY).abs()
    div = set(spread.index[(np.sign(rE) != np.sign(rY)) | (spread > spread.expanding(60).quantile(0.8).shift(1))])
    td = tr0[tr0["sess"].isin(div)]
    bd = M.basic(td["net_usd"].values, td["instrument"].map(EV.TV).values.astype(float)) if len(td) else M.basic(np.array([]), 1.0)
    out["sections"]["divergence_days"] = {"sessions": len(div), "n": bd["n"], "win_rate": bd["win_rate"], "profit_factor": bd["profit_factor"],
                                          "note": "ES and YM are highly correlated; these are the sessions where they give partly independent evidence."}
    # synthetic relatives
    rel = {}
    for name, fr in (("blended_returns", blended_frames), ("regime_shuffle", lambda: regime_shuffle_frames(seed))):
        log(f"s2.relative_{name}", 2)
        with frames(fr()):
            _, mr = pooled(runs_for(g, tf0))
        rel[name] = {"profit_factor": mr["profit_factor"], "net_usd": mr["net_usd"], "win_rate": mr["win_rate"]}
    out["sections"]["synthetic_relatives"] = {**rel, "note": "Derived from ES and YM; these are not new markets."}
    gates.append(gate("s2.synthetic_relatives_profitable", min(v["net_usd"] for v in rel.values()), 0, ">"))

    # ---- parameter robustness (12.6)
    one_ok = np.mean([x["passed"] for x in neigh["one"]]) if neigh["one"] else 1.0
    two_ok = np.mean([x["passed"] for x in neigh["two"]]) if neigh["two"] else 1.0
    med = float(np.median([x["score"] for x in neigh["one"] + neigh["two"]])) if (neigh["one"] or neigh["two"]) else nominal["score"]
    gates.append(gate("s2.plateau_one_step_pass_share", one_ok, G["robustness"]["plateau_one_step"]))
    if neigh["two"]:
        gates.append(gate("s2.plateau_two_step_pass_share", two_ok, G["robustness"]["plateau_two_step"]))
    gates.append(gate("s2.peak_excess_over_neighbourhood", nominal["score"] / med - 1.0 if med > 0 else 9.0, G["robustness"]["plateau_peak_excess"], "<="))
    nfog = 30 if quick else 200
    rng = np.random.default_rng([seed, 99])
    fog = []
    for _ in range(nfog):
        h = GN.fog_variant(rng, g)
        log("s2.fog", 2)
        fog.append(evaluate_slice(h, runs_for(h, tf0), TF, 40, seed + 17, tier=BR)["score"])
    fog25 = float(np.percentile(fog, 25))
    out["fog_score_p25"] = fog25
    out["sections"]["parameter_robustness"] = {"one_step": neigh["one"], "two_step_pass_share": float(two_ok), "neighbourhood_median_score": med,
                                               "fog_p25": fog25, "fog_retention": fog25 / nominal["score"] if nominal["score"] > 0 else 0.0, "fog_variants": nfog}
    # ablation: an atom whose removal does not hurt is deleted (the simplified genome becomes a new proposal)
    abl = []
    for slot in ("regime", "location", "filter"):
        for i in range(len(g["slots"][slot])):
            h = copy.deepcopy(g)
            h["slots"][slot].pop(i)
            h = GN.finalize(h)
            log("s2.ablation", 2)
            e = evaluate_slice(h, runs_for(h, tf0), TF, 100, seed + 19, tier=BR)
            abl.append({"removed": g["slots"][slot][i]["atom"], "score_without": e["score"], "delta": nominal["score"] - e["score"],
                        "noise_band": float(np.std(fog)), "removable": bool(nominal["score"] - e["score"] < np.std(fog)), "genome": h})
    out["sections"]["ablation"] = [{k: v for k, v in a.items() if k != "genome"} for a in abl]
    out["simplified"] = next((a["genome"] for a in sorted(abl, key=lambda a: a["delta"]) if a["removable"]), None)

    # ---- probability of backtest overfitting over the neighbourhood (12.4)
    pb = stats.pbo_cscv(np.vstack(cfg_daily), 16, 300 if quick else 2000, seed)
    out["sections"]["pbo"] = pb
    if tier_name != "bronze" and pb["pbo"] is not None:
        gates.append(gate("s2.probability_of_backtest_overfitting", pb["pbo"], tier.get("pbo_max", 0.30), "<="))
        gates.append(gate("s2.degradation_slope", pb["slope"], 0, ">="))

    # ---- combinatorial purged cross-validation (5.3 scheme B): distribution of test-pair results
    groups = EV.SEARCH["cpcv_groups"]
    edges = np.linspace(0, EV.N_SEARCH, groups + 1).round().astype(int)
    cp = []
    for i in range(groups):
        for j in range(i + 1, groups):
            sel = tr0["sess"].between(edges[i], edges[i + 1] - 1) | tr0["sess"].between(edges[j], edges[j + 1] - 1)
            t = tr0[sel]
            if len(t) >= 10:
                cp.append(M.basic(t["net_usd"].values, t["instrument"].map(EV.TV).values.astype(float))["profit_factor"])
    out["sections"]["cpcv"] = {"combinations": len(cp), "pf_p5": float(np.percentile(cp, 5)) if cp else 0.0, "pf_median": float(np.median(cp)) if cp else 0.0,
                               "share_pf_above_1": float(np.mean(np.array(cp) > 1.0)) if cp else 0.0}

    # ---- decoy markets (15.3)
    dpf, dalpha = [], []
    for kind, i in decoys.sample(8 if quick else G["decoys"]["sample"], seed):
        log(f"s2.decoy_{kind}_{i}", 2)
        with frames(decoys.decoy(kind, i)):
            r = runs_for(g, tf0)
            e = evaluate_slice(g, r, TF, 40, seed + 23, tier=BR)
        dpf.append(e["pooled"]["profit_factor"])
        dalpha.append(e["twin"]["win_rate_alpha_pts"])
    out["sections"]["decoys"] = {"n": len(dpf), "median_pf": float(np.median(dpf)), "median_alpha_pts": float(np.median(dalpha)),
                                 "max_pf": float(np.max(dpf)), "real_alpha_pts": nominal["twin"]["win_rate_alpha_pts"]}
    gates.append(gate("s2.median_decoy_pf", float(np.median(dpf)), tier["decoy_pf_max"], "<"))
    gates.append(gate("s2.alpha_gap_real_minus_decoy_pts", nominal["twin"]["win_rate_alpha_pts"] - float(np.median(dalpha)), G["decoys"]["alpha_gap_pts"]))

    out["passed"] = all(x["pass"] for x in gates)
    out["failed_gates"] = [x["gate"] for x in gates if not x["pass"]]
    integrity = {"s2.no_canary_atoms", "s2.truncation_audit_clean", "s2.selection_leak_constants", "s2.median_decoy_pf", "s2.core_timeframes_passing",
                 "s2.edge_survives_next_bar_fill"}
    out["bronze_ok"] = not (set(out["failed_gates"]) & integrity)
    out["nominal_score"] = nominal["score"]
    return out


def e_floor(tf, tier_name):
    from gates.stage1 import freq_floor
    return freq_floor(tf)["trades_per_year"] * (0.75 if tier_name == "bronze" else 1.0)


def daily_blocks(runs, n_blocks=16):
    """Per-block mean daily net (pooled instruments) over the six test folds, for CSCV."""
    sess = EV.fold_sessions(TF)
    d = sum(M.daily_series(runs[s]["trades"], sess) for s in INSTRUMENTS).values
    edges = np.linspace(0, len(d), n_blocks + 1).round().astype(int)
    return np.array([d[edges[i]:edges[i + 1]].mean() for i in range(n_blocks)])
