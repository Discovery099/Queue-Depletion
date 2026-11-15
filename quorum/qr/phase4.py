"""Phase 4: shortlist from Discover, Confirm for the shortlist, finalist checks."""
import glob
import json
import os

import numpy as np

from . import search as Q
from .common import ROOT, SYMS, COSTS
from .consensus import twin
from .report import full, words, line

ALL = tuple(range(8))
rows = []
for fn in sorted(glob.glob(os.path.join(ROOT, "cache", "phase3_island*.jsonl"))):
    rows += [json.loads(x) for x in open(fn)]
print("evaluations:", len(rows), "distinct:", len({Q.gkey(r["g"]) for r in rows}))
fit = np.array([r["fit"] for r in rows])
pf = np.array([r["s"]["pf"] for r in rows])
wr = np.array([r["s"]["wr"] for r in rows])
tpd = np.array([r["s"]["tpd"] for r in rows])
n = np.array([r["s"]["n"] for r in rows])
ok = n >= 200
summary = {"evaluations": len(rows), "discover": {}}
print("Discover distribution (candidates with at least 200 trades):")
for lo, hi in ((0, 1), (1, 3), (3, 5), (5, 99)):
    m = ok & (tpd >= lo) & (tpd < hi)
    if m.any():
        d = dict(count=int(m.sum()), pf_median=float(np.median(pf[m])), pf_p99=float(np.quantile(pf[m], 0.99)), pf_max=float(pf[m].max()),
                 wr_median=float(np.median(wr[m])), n_goal=int((m & (pf >= 2.0) & (wr >= 60)).sum()))
        summary["discover"][f"{lo}-{hi}"] = d
        print(f"  {lo}-{hi} trades/day: {d['count']:6d} candidates, PF median {d['pf_median']:.2f}, 99th pct {d['pf_p99']:.2f}, max {d['pf_max']:.2f}; "
              f"win% median {d['wr_median']:.0f}; PF>=2 and win>=60%: {d['n_goal']}")

e = Q.env(5)
order = np.argsort(-fit)
cand = list(order[:300]) + [i for i in order if tpd[i] >= 3.0][:100]
short, sigs, seen = [], [], set()
for i in cand:
    g = rows[i]["g"]
    k = Q.gkey(g)
    if k in seen:
        continue
    seen.add(k)
    L, Sx, _ = Q.signals(g, e["ES"])
    s = set(np.flatnonzero(L | Sx).tolist())
    if not s or any(len(s & t) / min(len(s), len(t)) > 0.5 for t in sigs):
        continue
    short.append(i); sigs.append(s)
    if len(short) >= 60:
        break
print("shortlist:", len(short))

res = []
for i in short:
    g = rows[i]["g"]
    Ts = Q.run(g, e)
    d, c = full(g, e, Q.DISCOVER, Ts=Ts), full(g, e, Q.CONFIRM, Ts=Ts)
    cf, _ = Q.fitness(g, e, Q.CONFIRM)
    res.append(dict(i=int(i), g=g, fit=float(fit[i]), conf_fit=cf, disc=d, conf=c, words=words(g, e)))
dp = np.array([r["disc"]["pooled"]["pf"] for r in res]); cp = np.array([r["conf"]["pooled"]["pf"] for r in res])
dw = np.array([r["disc"]["pooled"]["wr"] for r in res]); cw = np.array([r["conf"]["pooled"]["wr"] for r in res])
print(f"shortlist PF: discover median {np.median(dp):.2f} -> confirm median {np.median(cp):.2f}; confirm PF > 1: {(cp > 1).sum()} of {len(cp)}; "
      f"> 1.2: {(cp > 1.2).sum()}; > 1.5: {(cp > 1.5).sum()}; >= 2: {(cp >= 2).sum()}")
print(f"shortlist win rate: discover median {np.median(dw):.0f}% -> confirm median {np.median(cw):.0f}%")
summary["shortlist"] = dict(n=len(res), disc_pf_median=float(np.median(dp)), conf_pf_median=float(np.median(cp)),
                            conf_pf_gt1=int((cp > 1).sum()), conf_pf_gt12=int((cp > 1.2).sum()), conf_pf_gt15=int((cp > 1.5).sum()),
                            conf_pf_ge2=int((cp >= 2).sum()), disc_wr_median=float(np.median(dw)), conf_wr_median=float(np.median(cw)))
# a random sample of all evaluated candidates, for the overall picture
rng = np.random.default_rng(5)
samp = rng.choice(np.flatnonzero(ok), 300, replace=False)
sd, sc = [], []
for i in samp:
    c = full(rows[i]["g"], e, Q.CONFIRM)["pooled"]
    sd.append(pf[i]); sc.append(c["pf"])
print(f"random 300 candidates: discover PF median {np.median(sd):.2f}, confirm PF median {np.median(sc):.2f}")
summary["random300"] = dict(disc_pf_median=float(np.median(sd)), conf_pf_median=float(np.median(sc)))

elig = [r for r in res if r["conf"]["ES"]["pf"] > 1.0 and r["conf"]["YM"]["pf"] > 1.0]
elig.sort(key=lambda r: -r["conf_fit"])
print("eligible for finalist (confirm PF > 1 on both instruments):", len(elig))
final = elig[:3]
print("\nShortlist, best 15 by Confirm fitness:  discover -> confirm (pooled, per instrument per day)")
for r in sorted(res, key=lambda r: -r["conf_fit"])[:15]:
    print(f"  D {line(r['disc']['pooled'])} | C {line(r['conf']['pooled'])} | C ES PF {r['conf']['ES']['pf']:.2f} YM PF {r['conf']['YM']['pf']:.2f}\n     {r['words']}")
print("\nShortlist members with the most trades (>= 3 a day on Discover):")
for r in sorted([r for r in res if r["disc"]["pooled"]["tpd"] >= 3], key=lambda r: -r["conf_fit"])[:8]:
    print(f"  D {line(r['disc']['pooled'])} | C {line(r['conf']['pooled'])}\n     {r['words']}")

for k, r in enumerate(final):
    g = r["g"]
    r["all"] = full(g, e, ALL)
    r["stress"] = full(g, e, ALL, level="stress")["pooled"]
    r["tf"] = {}
    for tf in (10, 15, 30):
        r["tf"][tf] = full(g, Q.env(tf), ALL)
    tw = []
    for sym in SYMS:
        c = e[sym]
        L, Sx, bs = Q.signals(g, c)
        p = Q.plan_for(g, c, L, Sx, bs)
        tw.append(twin(c["b"], p, np.random.default_rng(11), 60))
    r["twin_wr"] = float(np.median([np.mean([a["wr"], b["wr"]]) for a, b in zip(*tw)]))
    r["twin_pf"] = float(np.median([np.mean([a["pf"], b["pf"]]) for a, b in zip(*tw)]))
    nb = []
    rngn = np.random.default_rng(3)
    seenn = {Q.gkey(g)}
    for _ in range(200):
        h = Q.mutate(g, rngn, len(e["names"]), e["ids"])
        if Q.gkey(h) in seenn or sorted(h["panel"]) != sorted(g["panel"]) or h["mode"] != g["mode"] or h["exit"][0] != g["exit"][0]:
            continue
        seenn.add(Q.gkey(h))
        nb.append(full(h, e, ALL)["pooled"]["pf"])
    r["neighbours"] = dict(n=len(nb), pf_min=float(min(nb)), pf_median=float(np.median(nb)), pf_max=float(max(nb))) if nb else {}
    print(f"\nFINALIST {k + 1}: {r['words']}")
    print(f"  discover  {line(r['disc']['pooled'])}\n  confirm   {line(r['conf']['pooled'])}   ES {line(r['conf']['ES'])} | YM {line(r['conf']['YM'])}")
    print(f"  all folds {line(r['all']['pooled'])}; twin win {r['twin_wr']:.0f}% PF {r['twin_pf']:.2f}; stress costs PF {r['stress']['pf']:.2f}")
    print("  timeframes: " + "; ".join(f"{tf}m {line(r['tf'][tf]['pooled'])}" for tf in (10, 15, 30)))
    print(f"  neighbours: {r['neighbours']}")
json.dump(dict(summary=summary, shortlist=res, finalists=final), open("reports/phase4.json", "w"), indent=1, default=float)
