"""Data and charts for the final report (SPEC 20.4): closest approaches, per-technique statistics,
exchange history, frontier charts.  Research data only.  Writes reports/final_data.json and two PNG
charts under reports/charts/.  The prose of reports/FINAL.md is written from these numbers."""
import collections
import glob
import json
import os
import sqlite3
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from audit import canary  # noqa: E402
from engine import path, read_json, write_json  # noqa: E402
from library.atoms.catalog import ATOMS, FAMILIES  # noqa: E402

canary.install()
CAN = set(canary.canary_ids())
# chart tokens (validated default palette of the data-viz method)
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE = "#2a78d6", "#eb6834"
SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]


def home_only(db):
    rows = []
    for gen, js in db.execute("SELECT generation, genome FROM genomes WHERE status='HOME_ONLY'"):
        d = path("runs", f"{gen // 1000:03d}", f"gen_{gen:06d}")
        f = os.path.join(d, "metrics_stage1_confirmation.json")
        if not os.path.exists(f):
            continue
        c, g = read_json(f), json.loads(js)
        gates = read_json(os.path.join(d, "gates.json"))["stage1_confirmation_all_folds"]
        fails = [{"gate": x["gate"], "value": x["value"], "threshold": x["threshold"]} for x in gates if not x["pass"]]
        m = c["pooled"]
        rows.append({"generation": gen, "tf": g["primary_timeframe_min"], "complexity": g["complexity"], "n": m["n"], "win_rate": m["win_rate"],
                     "wilson_lo": m["wilson_lo"], "profit_factor": m["profit_factor"], "payoff": m["payoff"], "expectancy_costs": m["expectancy_costs"],
                     "alpha": c["twin"]["win_rate_alpha_pts"], "twin": c["twin"]["median_win_rate"], "fold_pf": [x["profit_factor"] for x in c["by_fold"]],
                     "failed": fails, "n_failed": len(fails), "genome": g})
    rows.sort(key=lambda r: (r["n_failed"], -r["profit_factor"]))
    return rows


def atom_stats(db):
    by = collections.defaultdict(list)
    for gen, js, n, wr, pf, alpha in db.execute("SELECT generation, genome, n_trades, win_rate, pf, alpha FROM genomes WHERE generation > 2000 AND n_trades >= 150"):
        g = json.loads(js)
        s = g["slots"]
        atoms = {e["atom"] for k in ("regime", "location", "filter", "exit") for e in s[k]} | {e["atom"] for e in s["trigger"]["atoms"]} | {s["risk"]["stop"]["atom"]}
        for a in atoms:
            by[a].append((wr or 0, pf or 0, alpha or 0))
    out = []
    for a, v in by.items():
        x = np.array(v)
        if a not in ATOMS:
            continue
        out.append({"atom": a, "type": ATOMS[a].typ, "family": ATOMS[a].fam, "canary": a in CAN, "genomes": len(x),
                    "median_pf": float(np.median(x[:, 1])), "median_alpha": float(np.median(x[:, 2])), "median_wr": float(np.median(x[:, 0])),
                    "share_pf_above_1": float((x[:, 1] > 1.0).mean()), "share_strong": float(((x[:, 0] >= 0.65) & (x[:, 1] >= 1.2)).mean())})
    return sorted(out, key=lambda r: -r["share_strong"])


def solo_triggers(db):
    """Each trigger's own evidence: single-trigger genomes proposed by LIBRARY_PROBE after generation 2,000
    (geometry-matched twins), at least 150 out-of-sample trades.  Canary triggers give the no-information baseline."""
    by = collections.defaultdict(list)
    for js, wr, pf, alpha in db.execute("SELECT genome, win_rate, pf, alpha FROM genomes WHERE generation > 2000 AND operator='LIBRARY_PROBE' AND n_trades >= 150"):
        g = json.loads(js)
        t = g["slots"]["trigger"]["atoms"]
        if len(t) == 1 and not g.get("ensemble"):
            by[t[0]["atom"]].append((wr or 0, pf or 0, alpha or 0))
    out = []
    for a, v in by.items():
        x = np.array(v)
        if a in ATOMS and len(x) >= 15:
            out.append({"atom": a, "family": ATOMS[a].fam, "canary": a in CAN, "genomes": len(x), "median_alpha": float(np.median(x[:, 2])),
                        "median_pf": float(np.median(x[:, 1])), "share_pf_above_1_1": float((x[:, 1] > 1.1).mean())})
    return sorted(out, key=lambda r: -r["median_pf"])


def exchanges():
    out = []
    for f in sorted(glob.glob(path("reports", "exchange_*.json"))):
        s = read_json(f)["summary"]
        out.append({k: s.get(k) for k in ("generation", "leaders", "retention", "mean_home_pf", "mean_away_pf", "mean_home_wr", "mean_away_wr", "survivors")})
    return out


def charts(db, ho, ex):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker  # noqa: F401
    from matplotlib.colors import BoundaryNorm, ListedColormap
    os.makedirs(path("reports/charts"), exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                         "xtick.color": INK2, "ytick.color": INK2, "text.color": INK, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE})
    # ---- 1. where 100,000 strategies landed: win rate against profit factor (counts, one sequential hue)
    r = np.array(db.execute("SELECT win_rate, pf FROM genomes WHERE n_trades >= 150 AND win_rate IS NOT NULL").fetchall())
    fig, ax = plt.subplots(figsize=(9, 5.6), dpi=200)
    xe, ye = np.arange(30, 92, 2), np.arange(0.5, 2.55, 0.05)
    h, _, _ = np.histogram2d(100 * r[:, 0], np.clip(r[:, 1], 0.5, 2.5), bins=[xe, ye])
    bounds = [1, 5, 20, 60, 150, 400, 1000, 1e9]
    hm = np.ma.masked_where(h.T < 1, h.T)
    pc = ax.pcolormesh(xe, ye, hm, cmap=ListedColormap(SEQ), norm=BoundaryNorm(bounds, len(SEQ)), edgecolors=SURFACE, linewidth=0.4)
    box = dict(facecolor=SURFACE, edgecolor="none", alpha=0.9, pad=1.5)
    for (x0, y0, lab, lx, ly) in ((65, 1.4, "Bronze floor: 65% wins, profit factor 1.4", 65.5, 2.42), (80, 1.8, "Gold floor: 80%, 1.8", 80.5, 1.83)):
        ax.plot([x0, 90], [y0, y0], color=INK2, lw=1, ls=(0, (4, 3)))
        ax.plot([x0, x0], [y0, 2.5], color=INK2, lw=1, ls=(0, (4, 3)))
        ax.text(lx, ly, lab, fontsize=8.5, color=INK2, va="bottom", bbox=box, zorder=6)
    for k, c in enumerate(ho[:2]):
        ax.scatter([100 * c["win_rate"]], [c["profit_factor"]], s=90, facecolor=ORANGE, edgecolor=SURFACE, linewidth=2, zorder=5)
        ax.annotate(f"generation {c['generation']} on all six folds\n{100 * c['win_rate']:.1f}% wins, profit factor {c['profit_factor']:.2f}",
                    (100 * c["win_rate"], c["profit_factor"]), xytext=(34, 2.2 - 0.28 * k), fontsize=8.5, color=INK,
                    arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
    ax.set_xlim(30, 90)
    ax.set_ylim(0.5, 2.5)
    ax.set_xlabel("Win rate on the island's home test folds (%)")
    ax.set_ylabel("Profit factor")
    ax.set_title(f"Where {len(r):,} evaluated strategies landed (at least 150 out-of-sample trades)", loc="left", fontsize=11, color=INK)
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    cb = fig.colorbar(pc, ax=ax, ticks=bounds[:-1], pad=0.02)
    cb.set_label("Strategies per cell", color=INK2)
    cb.outline.set_visible(False)
    fig.text(0.01, 0.01, "Cells show home-fold screening results (the folds the search selects on). Orange points are the two closest approaches, "
             "re-scored on all six test folds.", fontsize=7.5, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path("reports/charts/frontier_win_rate_profit_factor.png"))
    plt.close(fig)
    # ---- 2. leaders at home and on unseen folds, across the island exchanges
    fig, ax = plt.subplots(figsize=(9, 4.6), dpi=200)
    gx = [e["generation"] for e in ex]
    for key, col, lab in (("mean_home_pf", BLUE, "on the folds they were selected on"), ("mean_away_pf", ORANGE, "on folds that never influenced them")):
        y = [e[key] for e in ex]
        ax.plot(gx, y, color=col, lw=2, marker="o", ms=5, mec=SURFACE, mew=1.2, label=lab)
        ax.text(gx[-1] + 900, y[-1], f"{y[-1]:.2f}", color=INK, fontsize=9, va="center")
    ax.axhline(1.0, color=INK2, lw=1)
    ax.text(60000, 1.012, "break-even", fontsize=8.5, color=INK2)
    ax.axhline(1.4, color=INK2, lw=1, ls=(0, (4, 3)))
    ax.text(60000, 1.412, "Bronze floor (1.4)", fontsize=8.5, color=INK2)
    ax.axvline(20008, color=GRID, lw=1.2)
    ax.text(20600, 0.84, "anti-overfit changes\nat generation 20,009", fontsize=8.5, color=INK2, va="bottom")
    ax.set_xlim(gx[0] - 2500, gx[-1] + 7000)
    ax.set_ylim(0.8, 1.75)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _p: f"{int(v):,}"))
    ax.set_xlabel("Generation of the island exchange")
    ax.set_ylabel("Mean profit factor of the 20 leaders")
    ax.set_title("The leading strategies' profit factor: selected folds against unseen folds", loc="left", fontsize=11, color=INK)
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(frameon=False, loc="upper left", fontsize=9, labelcolor=INK)
    fig.tight_layout()
    fig.savefig(path("reports/charts/leaders_home_vs_unseen.png"))
    plt.close(fig)


def main():
    st = read_json(path("state/checkpoint.json"))
    db = sqlite3.connect("file:" + path("ledger/lineage.sqlite") + "?mode=ro", uri=True)
    ho = home_only(db)
    at = atom_stats(db)
    ex = exchanges()
    solo = solo_triggers(db)
    by_status = dict(db.execute("SELECT status, COUNT(*) FROM genomes GROUP BY status").fetchall())
    fam = collections.defaultdict(list)
    for a in at:
        if a["type"] == "TRIGGER" and not a["canary"]:
            fam[a["family"]].append(a)
    fams = [{"family": FAMILIES[f], "trigger_atoms": len(v), "genomes": sum(x["genomes"] for x in v),
             "median_pf": float(np.median([x["median_pf"] for x in v])), "best_share_strong": max(x["share_strong"] for x in v)} for f, v in fam.items()]
    out = {"generations": st["next_generation"] - 1, "counts": st["counts"], "tier_counts": st["tier_counts"], "by_status": by_status,
           "n_eff": st.get("n_eff"), "vault": st["vault"], "home_only": [{k: v for k, v in r.items() if k != "genome"} for r in ho],
           "leading_generation": ho[0]["generation"] if ho else None, "atoms": at, "families": sorted(fams, key=lambda r: -r["best_share_strong"]),
           "canary_summary": {"genomes": sum(a["genomes"] for a in at if a["canary"]),
                              "max_share_strong": max([a["share_strong"] for a in at if a["canary"]] or [0.0]),
                              "median_pf": float(np.median([a["median_pf"] for a in at if a["canary"]] or [0.0]))},
           "exchanges": ex, "operator_stats": st["operator_stats"], "solo_triggers": solo}
    write_json(path("reports/final_data.json"), out)
    charts(db, ho, ex)
    print("generations", out["generations"], "| home-only", len(ho), "| leading", out["leading_generation"])
    for r in ho[:8]:
        print(f"  gen {r['generation']} tf{r['tf']} n={r['n']} wr={100 * r['win_rate']:.1f} pf={r['profit_factor']:.2f} alpha={r['alpha']:+.1f} fails={r['n_failed']} "
              f"{[x['gate'] for x in r['failed']][:3]}")
    can = [x for x in solo if x["canary"]]
    print("canary triggers alone (baseline):", [(x["atom"], x["genomes"], round(x["median_pf"], 2), round(x["median_alpha"], 1)) for x in can])
    real = [x for x in solo if not x["canary"]]
    print("best triggers alone:", [(x["atom"], x["genomes"], round(x["median_pf"], 2), round(x["median_alpha"], 1), round(100 * x["share_pf_above_1_1"])) for x in real[:12]])
    print("worst triggers alone:", [(x["atom"], round(x["median_pf"], 2)) for x in real[-10:]])
    fa = collections.defaultdict(list)
    for x in real:
        fa[x["family"]].append(x["median_pf"])
    print("family median of trigger medians:", sorted(((FAMILIES[k], round(float(np.median(v)), 2), len(v)) for k, v in fa.items()), key=lambda t: -t[1]))


if __name__ == "__main__":
    main()
