"""Phase 1: the three published rules at their published settings on the 947 search sessions."""
import json

import numpy as np

from .core import SYMS, N_SEARCH, plan_s1, plan_s2, plan_s3, trades, summ, line

RULES = {"S1 noise-area momentum": plan_s1, "S2 last-half-hour momentum": plan_s2, "S3 5-minute opening-range breakout": plan_s3}
out = {}
for name, fn in RULES.items():
    df = trades(fn)
    st = trades(fn, level="stress")
    print(f"\n=== {name}")
    r = {"pooled": summ(df, N_SEARCH * 2)}
    r["pooled"]["tpd"] = len(df) / N_SEARCH / 2
    print("  pooled      ", line(r["pooled"]))
    for sym in SYMS:
        r[sym] = summ(df[df.sym == sym], N_SEARCH)
        print(f"  {sym}          ", line(r[sym]))
    r["stress"] = summ(st, N_SEARCH * 2)
    print("  2x costs    ", line(r["stress"]))
    r["folds"] = [summ(df[df.fold == k], 1)["pf"] for k in range(8)]
    print("  PF by fold  ", " ".join(f"{x:.2f}" for x in r["folds"]), "| folds profitable:", sum(x > 1 for x in r["folds"]))
    df["year"] = df["date"] // 10000
    r["years"] = {int(y): summ(g, 1)["pf"] for y, g in df.groupby("year")}
    print("  PF by year  ", {y: round(v, 2) for y, v in r["years"].items()})
    r["long"], r["short"] = summ(df[df.dir > 0], 1)["pf"], summ(df[df.dir < 0], 1)["pf"]
    print(f"  long PF {r['long']:.2f}  short PF {r['short']:.2f}")
    out[name] = r
json.dump(out, open("reports/phase1.json", "w"), indent=1, default=float)
