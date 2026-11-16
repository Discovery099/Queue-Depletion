"""Phase 3: the one-time Holdout audit of three frozen candidates.  Run once."""
import json
import os
import sqlite3
import sys

os.environ["QUORUM_OPEN_HOLDOUT"] = "1"
import numpy as np
import pandas as pd

from .core import SYMS, N_SEARCH, plan_s1, trades, summ, line, ROOT
from engine import path
from orchestrator import evaluate as EV

OUT = os.path.join(ROOT, "reports", "phase3_holdout.json")
if os.path.exists(OUT):
    sys.exit("the Holdout audit has already been run; see reports/phase3_holdout.json")
NH = 168
res = {}


def show(name, df):
    r = {"pooled": summ(df, NH * 2)}
    r["pooled"]["tpd"] = len(df) / NH / 2
    print(f"\n=== {name}\n  pooled ", line(r["pooled"]))
    for s in SYMS:
        r[s] = summ(df[df.sym == s], NH)
        print(f"  {s}     ", line(r[s]))
    r["pass"] = bool(r["pooled"]["n"] and r["pooled"]["pf"] >= 1.15 and r["pooled"]["net"] > 0)
    print("  Holdout pass:", r["pass"])
    res[name] = r


db = sqlite3.connect("file:" + path("ledger/lineage.sqlite") + "?mode=ro", uri=True)
for name, gen in (("A generation 25968", 25968), ("B generation 44439", 44439)):
    g = json.loads(db.execute("SELECT genome FROM genomes WHERE generation=?", [gen]).fetchone()[0])
    rows = []
    for s in SYMS:
        r = EV.run(g, s, g["primary_timeframe_min"], scope="holdout")
        t = r["trades"]
        t = t[t["sess"] >= N_SEARCH]
        rows.append(pd.DataFrame({"sym": s, "ts": t["entry_ts"].values, "net": t["net_usd"].values, "win": t["is_win"].values.astype(bool)}))
    show(name, pd.concat(rows, ignore_index=True))
    EV.clear_caches()
df = trades(plan_s1, block="holdout")
df = df[df.sess >= N_SEARCH]
show("C noise-area momentum (published settings)", df[["sym", "ts", "net", "win"]])
json.dump(res, open(OUT, "w"), indent=1, default=float)
