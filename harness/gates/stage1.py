"""Stage 1 screen (SPEC 10.2 step 6, 11, 12.1, 12.2, 16.1): walk-forward metrics on the primary
timeframe, both instruments, base costs; win-rate integrity; the composite robustness score.

Walk-forward reading adopted for fixed-rule genomes (SPEC 5.3): the genome is not re-fitted per
fold.  For test fold k the in-sample record is the genome's own trades in folds 1..k-1 minus a
3-session purge, and the out-of-sample record is fold k.  Selection happens at the level of the
search, which is why each island scores on only half of the test folds (SPEC 15.9): stage 1 uses the
island's home folds with sample thresholds scaled to that share, and a candidate that passes is
then confirmed on all six test folds at the full thresholds before it may enter stage 2.
"""
import math

import numpy as np
import pandas as pd

from engine import metrics as M
from engine.data import INSTRUMENTS
from orchestrator import evaluate as EV
from library.atoms.catalog import ATOMS

G = EV.GATES
S = EV.SEARCH
BR = G["tiers"]["bronze"]


def lin(x, lo, hi):
    """Fixed transform to 0..1: 0 at `lo`, 1 at `hi` (lo may exceed hi for 'smaller is better')."""
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return 0.0
    return float(min(1.0, max(0.0, (x - lo) / (hi - lo))))


def gate(name, value, thr, op=">=", note=""):
    v = float(value) if value is not None else float("nan")
    ok = {">=": v >= thr, "<=": v <= thr, ">": v > thr, "<": v < thr}[op] if not math.isnan(v) else False
    return {"gate": name, "value": None if math.isnan(v) else round(v, 6), "threshold": thr, "op": op, "pass": bool(ok), "note": note}


def freq_floor(tf):
    tab = G["frequency"]["by_timeframe"]
    keys = sorted(tab)
    k = min(keys, key=lambda x: abs(x - tf)) if tf not in tab else tf
    if tf not in tab:   # hidden timeframes: interpolate on the log of the bar size
        lo = max([x for x in keys if x <= tf] or [keys[0]])
        hi = min([x for x in keys if x >= tf] or [keys[-1]])
        if lo == hi:
            return dict(tab[lo])
        wgt = (math.log(tf) - math.log(lo)) / (math.log(hi) - math.log(lo))
        return {kk: tab[lo][kk] + wgt * (tab[hi][kk] - tab[lo][kk]) for kk in tab[lo]}
    return dict(tab[k])


def fold_table(tr, folds):
    rows = []
    for k in folds:
        t = tr[tr["fold"] == k]
        b = M.basic(t["net_usd"].values, t["instrument"].map(EV.TV).values.astype(float)) if len(t) else M.basic(np.array([]), 1.0)
        per_inst = {s: int((t["instrument"] == s).sum()) for s in INSTRUMENTS}
        rows.append({"fold": k, "n": b["n"], "win_rate": b["win_rate"], "profit_factor": b["profit_factor"],
                     "net_usd": b["net_usd"], "n_by_instrument": per_inst})
    return rows


def wf_efficiency(tr_all, folds):
    """Out-of-sample average trade (in round-trip costs) over the in-sample average, per test fold."""
    rc = tr_all["instrument"].map(M.RT_COST_USD).values.astype(float)
    x = tr_all["net_usd"].values / rc
    sess = tr_all["sess"].values.astype(np.int64)
    is_vals, oos_vals = [], []
    own = np.isin(EV.FOLD_OF[np.minimum(sess, EV.N_SEARCH - 1)], [1, 2] + list(folds))   # never the other island's folds
    for k in folds:
        lo, hi = EV.FOLDS[k - 1]
        i = (sess < lo - EV.PURGE) & own
        o = (sess >= lo) & (sess < hi)
        if i.sum() >= 20 and o.sum() >= 5:
            is_vals.append(x[i].mean())
            oos_vals.append(x[o].mean())
    if not is_vals:
        return 0.0, 0.0, 0.0
    i_m, o_m = float(np.mean(is_vals)), float(np.mean(oos_vals))
    eff = (o_m / i_m) if i_m > 0 else (1.0 if o_m > 0 else 0.0)
    return eff, i_m, o_m


def min_track_record(daily):
    """Minimum track record length in sessions for the observed Sharpe to differ from zero at 95%."""
    sd = daily.std(ddof=1)
    if sd <= 0 or daily.mean() <= 0:
        return float("inf")
    sr = daily.mean() / sd
    z = (daily - daily.mean()) / sd
    g3, g4 = float((z ** 3).mean()), float((z ** 4).mean())
    return 1.0 + (1.0 - g3 * sr + (g4 - 1.0) / 4.0 * sr * sr) * (1.645 / sr) ** 2


def evaluate_slice(g, runs, folds, n_twins, seed, tier=BR, full_thresholds=False, tf=None):
    """Metrics, gates and score for a set of test folds.  `runs` maps instrument -> evaluate.run() result."""
    tf = tf or g["primary_timeframe_min"]
    share = len(folds) / len(EV.TEST_FOLDS)
    sess_ids = EV.fold_sessions(folds)
    tr_all = pd.concat([runs[s]["trades"] for s in INSTRUMENTS], ignore_index=True)
    tr = tr_all[tr_all["fold"].isin(folds)].reset_index(drop=True)
    m = M.evaluate(tr, sess_ids, EV.TV)
    per = {s: M.evaluate(tr[tr["instrument"] == s], sess_ids, EV.TV) for s in INSTRUMENTS}
    ft = fold_table(tr, folds)
    gates = []
    cx = g["complexity"]
    fl = freq_floor(tf)
    n_years = len(sess_ids) / 252.0

    # ---- sample size (12.1)
    need_inst = math.ceil(G["sample"]["min_trades_per_instrument"] * share)
    n_inst = min(per[s]["n"] for s in INSTRUMENTS)
    gates.append(gate("sample.trades_per_instrument", n_inst, need_inst))
    gates.append(gate("sample.trades_per_fold_per_instrument", min(min(r["n_by_instrument"].values()) for r in ft),
                      G["sample"]["min_trades_per_fold"]))
    gates.append(gate("sample.trades_per_complexity_point", m["n"] / max(1, cx), G["sample"]["trades_per_complexity_point"] * share))
    gates.append(gate("sample.wilson_lower", m["wilson_lo"], tier["win_rate"] - G["sample"]["wilson_margin_pts"] / 100.0))
    daily = sum(M.daily_series(tr[tr["instrument"] == s], sess_ids) for s in INSTRUMENTS)
    mtrl = min_track_record(daily)
    gates.append(gate("sample.min_track_record_sessions", len(sess_ids) - mtrl if math.isfinite(mtrl) else -1e9, 0, ">=",
                      note=f"needs {mtrl:.0f} sessions, has {len(sess_ids)}"))

    # ---- tier floors
    gates.append(gate("floor.win_rate_pooled", m["win_rate"], tier["win_rate"]))
    gates.append(gate("floor.win_rate_each_instrument", min(per[s]["win_rate"] for s in INSTRUMENTS), tier["win_rate_each"]))
    gates.append(gate("floor.profit_factor_pooled", m["profit_factor"], tier["pf"]))
    gates.append(gate("floor.payoff_ratio", m["payoff"], tier["payoff"]))
    gates.append(gate("floor.expectancy_in_round_trip_costs", m["expectancy_costs"], tier["exp_costs"]))
    gates.append(gate("floor.largest_loss_in_average_wins", m.get("largest_loss_in_avg_wins", 99.0), tier["largest_loss_avg_wins"], "<="))

    # ---- walk-forward consistency (12.2)
    pfs = [r["profit_factor"] for r in ft]
    wrs = [r["win_rate"] for r in ft]
    need_folds = math.ceil(G["walk_forward"]["folds_pf_above_1"] * share)
    gates.append(gate("wf.folds_with_pf_above_1", sum(p > 1.0 for p in pfs), need_folds))
    gates.append(gate("wf.median_fold_pf", float(np.median(pfs)), G["walk_forward"]["median_fold_pf"]))
    gates.append(gate("wf.worst_fold_pf", min(pfs), tier["pf_worst_fold"]))
    gates.append(gate("wf.worst_fold_win_rate_gap_pts", 100 * (float(np.median(wrs)) - min(wrs)), G["walk_forward"]["worst_fold_wr_gap_pts"], "<="))
    eff, is_m, oos_m = wf_efficiency(tr_all, folds)
    gates.append(gate("wf.efficiency", eff, G["walk_forward"]["efficiency_min"]))
    gates.append(gate("wf.in_sample_expectancy_costs", is_m, 0, ">",
                      "tightening (generation 15,009): the record before each test fold, which the search did not select on, must be profitable"))
    tot = sum(r["net_usd"] for r in ft)
    max_share = max(r["net_usd"] for r in ft) / tot if tot > 0 else 9.0
    gates.append(gate("wf.max_fold_profit_share", max_share, min(0.99, G["walk_forward"]["max_fold_profit_share"] / share), "<="))

    # ---- trade-record forensics (11.3)
    F = G["forensics"]
    gates.append(gate("wr.tail_share", m.get("tail_share", 99.0), F["tail_share_max"], "<="))
    gates.append(gate("wr.skew", m.get("skew", -99.0), F["skew_min"]))
    gates.append(gate("wr.loss_streak_vs_expected", m.get("loss_streak", 0) / max(1.0, m.get("loss_streak_p99", 1.0)), F["loss_streak_multiple"], "<="))
    gates.append(gate("wr.mae_of_winners_pct_stop", m.get("mae_winner_median_pct_stop", 9.0), F["mae_winner_median_max"], "<"))
    gates.append(gate("wr.scratch_share", m.get("scratch_share", 1.0), F["scratch_share_max"], "<="))
    gates.append(gate("wr.time_asymmetry", m.get("time_asymmetry", 99.0), F["time_asymmetry_max"], "<="))
    flags = []
    if m.get("session_exit_profit_share", 0.0) > F["session_exit_profit_flag"]:
        flags.append("SESSION_DRIFT_DEPENDENT")
    if m.get("same_bar_share", 0.0) > G["robustness"]["same_bar_share_flag"]:
        flags.append("SAME_BAR_TRADES")

    # ---- frequency and participation (11.5, 13.3)
    tpy = min(per[s]["n"] for s in INSTRUMENTS) / max(1e-9, n_years)
    floor_tpy = fl["trades_per_year"] * (0.75 if tier is BR else 1.0)
    gates.append(gate("freq.trades_per_year_per_instrument", tpy, floor_tpy))
    gates.append(gate("freq.session_share", m["session_share"], fl["session_share"]))
    gap_lim = G["frequency"]["max_gap_sessions_5m"] * 0.55 / fl["session_share"]
    gap = 0
    for s in INSTRUMENTS:
        traded = set(tr.loc[tr["instrument"] == s, "sess"].unique())
        for k in folds:
            cur = 0
            for x in range(*EV.FOLDS[k - 1]):
                cur = 0 if x in traded else cur + 1
                gap = max(gap, cur)
    gates.append(gate("freq.max_gap_sessions", gap, gap_lim, "<="))
    cell_ratio = 9.0
    for s in INSTRUMENTS:
        rc = EV.regime_cells(s)[sess_ids]
        ts = tr.loc[tr["instrument"] == s]
        overall = len(ts) / max(1, len(sess_ids))
        for c in range(6):
            ns = int((rc == c).sum())
            if ns >= 20 and overall > 0:
                cell_ratio = min(cell_ratio, (ts["regime_cell"] == c).sum() / ns / overall)
    gates.append(gate("freq.worst_regime_cell_share", cell_ratio, G["frequency"]["regime_cell_min_share"]))

    # ---- twins (11.4): only meaningful with trades; fewer twins once another gate has already failed
    failed_already = not all(x["pass"] for x in gates)
    nt = G["twins"]["n_when_already_failed"] if (failed_already and not full_thresholds) else n_twins
    tw = np.zeros((nt, 5))
    rex_w = rex_n = 0
    if m["n"] >= 20:
        for i, s in enumerate(INSTRUMENTS):
            mask = EV.sessions_mask(runs[s]["bars"], folds)
            tw += EV.twin_runs(runs[s], mask, nt, seed + 7919 * (i + 1))
            a, b_ = EV.random_exit_twin(runs[s], mask)
            rex_w, rex_n = rex_w + a, rex_n + b_
    with np.errstate(divide="ignore", invalid="ignore"):
        t_wr = np.where(tw[:, 1] > 0, tw[:, 0] / tw[:, 1], 0.0)
        t_exp = np.where(tw[:, 1] > 0, tw[:, 2] / tw[:, 1], 0.0)
        t_pf = np.where(tw[:, 4] > 0, tw[:, 3] / tw[:, 4], 0.0)
    twin = {"n_twins": nt, "median_win_rate": float(np.median(t_wr)), "p95_win_rate": float(np.percentile(t_wr, 95)),
            "p99_win_rate": float(np.percentile(t_wr, 99)), "median_expectancy_costs": float(np.median(t_exp)),
            "p95_expectancy_costs": float(np.percentile(t_exp, 95)), "p99_expectancy_costs": float(np.percentile(t_exp, 99)),
            "median_profit_factor": float(np.median(t_pf)), "p95_profit_factor": float(np.percentile(t_pf, 95)),
            "median_trades": float(np.median(tw[:, 1])), "random_exit_win_rate": (rex_w / rex_n) if rex_n else 0.0,
            "random_exit_n": rex_n, "random_exit_wilson_lo": M.wilson(rex_w, rex_n)[0]}
    alpha = 100 * (m["win_rate"] - twin["median_win_rate"])
    exp_alpha = m["expectancy_costs"] - twin["median_expectancy_costs"]
    twin["win_rate_alpha_pts"], twin["expectancy_alpha_costs"] = alpha, exp_alpha
    gates.append(gate("twin.win_rate_alpha_pts", alpha, tier["alpha_pts"]))
    gates.append(gate("twin.win_rate_above_p99", m["win_rate"] - twin["p99_win_rate"], 0, ">"))
    gates.append(gate("twin.expectancy_alpha", exp_alpha, 0, ">"))
    gates.append(gate("twin.expectancy_above_p99", m["expectancy_costs"] - twin["p99_expectancy_costs"], 0, ">"))
    gates.append(gate("twin.random_exit_wilson_lower", twin["random_exit_wilson_lo"], 0.5, ">"))

    # ---- composite robustness score (16.1)
    sc = S["score"]
    cell_pf = []
    for r in ft:
        cell_pf.append(r["profit_factor"])
    for s in INSTRUMENTS:
        cell_pf.append(per[s]["profit_factor"])
    worst_pf = min(cell_pf) if cell_pf else 0.0
    roll, n_win = M.rolling_window_share(tr, sess_ids, 63)
    cv = float(np.std(pfs) / np.mean(pfs)) if np.mean(pfs) > 0 else 9.0
    comp = {
        "alpha": lin(alpha, *sc["alpha_pts"]),
        "worst_pf": lin(worst_pf, *sc["worst_pf"]),
        "expectancy": lin(m["expectancy_costs"], *sc["expectancy_costs"]),
        "tail": (lin(m.get("largest_loss_in_avg_wins", 99.0), *sc["largest_loss_avg_wins"]) + lin(m.get("tail_share", 99.0), *sc["tail_share"])
                 + lin(m.get("skew", -99.0), *sc["skew"])) / 3.0,
        "consistency": 0.5 * roll + 0.5 * lin(cv, *sc["fold_pf_cv"]),
        "frequency": lin(tpy, floor_tpy / 2.0, floor_tpy),
        "fog": sc["fog_retention_before_stage2"],
        "simplicity": 1.0 - cx / S["complexity_ceiling"],
    }
    base = sum(sc["weights"][k] * comp[k] for k in comp)
    wr = m["win_rate"]
    pen = sc["win_rate_penalty"]
    if wr >= pen["full"]:
        f_wr = 1.0
    elif wr >= pen["half"]:
        f_wr = 0.5 + 0.5 * (wr - pen["half"]) / (pen["full"] - pen["half"])
    else:
        f_wr = max(0.0, 0.5 * (wr - pen["zero"]) / (pen["half"] - pen["zero"]))
    # overfit gap, both directions: the test folds are what the search selects on, so a record far BETTER there
    # than before them is as suspect as one far worse (tightening, generation 20,009)
    f_gap = max(0.0, min(eff, 1.0 / eff)) if eff > 0 else 0.0
    f_n = min(1.0, n_inst / need_inst) if sc.get("sample_shrink") else 1.0
    score = base * f_wr * f_gap * f_n
    return {
        "folds": list(folds), "timeframe_min": tf, "pooled": m, "by_instrument": per, "by_fold": ft, "twin": twin,
        "gates": gates, "passed": all(x["pass"] for x in gates), "flags": flags,
        "failed_gates": [x["gate"] for x in gates if not x["pass"]],
        "score": float(score), "score_components": comp,
        "score_factors": {"base": base, "win_rate": f_wr, "overfit_gap": f_gap, "sample": f_n},
        "wf": {"efficiency": eff, "in_sample_expectancy_costs": is_m, "oos_expectancy_costs": oos_m,
               "rolling_3m_profitable_share": roll, "rolling_windows": n_win, "fold_pf_cv": cv, "worst_cell_pf": worst_pf},
        "trades_per_year_per_instrument": tpy,
    }


def descriptors(g, res):
    """Behavioural descriptors for the quality-diversity grid (SPEC 16.4)."""
    m = res["pooled"]
    hold = m.get("median_minutes_held", 0.0)
    hb = 0 if hold < 20 else 1 if hold < 60 else 2 if hold < 180 else 3
    tps = m["n"] / max(1, m["sessions"]) / len(INSTRUMENTS)
    fb = 0 if tps < 1 else 1 if tps <= 2 else 2
    fam = ATOMS[g["slots"]["trigger"]["atoms"][0]["atom"]].fam
    return {"family": fam, "hold_bucket": hb, "freq_bucket": fb, "entry_type": g["slots"]["entry"]["type"],
            "cell": f"{fam}|{hb}|{fb}|{g['slots']['entry']['type']}"}


def stage1(g, island, seed, generation=-1, n_twins=None):
    """Run the stage 1 screen on the island's home folds.  Returns (result, runs)."""
    tf = g["primary_timeframe_min"]
    runs = {s: EV.run(g, s, tf, generation=generation) for s in INSTRUMENTS}
    res = evaluate_slice(g, runs, EV.ISLAND_FOLDS[island], n_twins or G["twins"]["n"], seed)
    res["descriptors"] = descriptors(g, res)
    res["island"] = island
    return res, runs


def stage1_confirm(g, runs, seed):
    """All six test folds at the full thresholds (the other island's folds included)."""
    return evaluate_slice(g, runs, EV.TEST_FOLDS, G["twins"]["n"], seed + 1, full_thresholds=True)
