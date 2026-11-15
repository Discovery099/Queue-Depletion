"""Phase 1: the owner's hypothesis exactly as written (Smart Trend arrows x Lorentzian signals, sync 0-4 bars)."""
import json
import sys

import numpy as np

from .common import SYMS, bars, atr14, stats
from . import lc
from .consensus import owner_sync, make_plan, backtest, event_study, twin

EXITS = {"after 4 bars": ("bars", 4), "opposite match (flat at close)": ("opp",), "1 ATR stop, 2R target": ("atr", 1.0, 2.0)}
out = {}
for tf in (5, 10, 15, 30):
    for sym in SYMS:
        b = bars(sym, tf)
        a = atr14(b)
        r = lc.lorentzian(b)
        _, reg, sL, sS = lc.smart_arrows(b)
        sets = {"Smart Trend alone": (sL, sS), "Lorentzian alone": (r["lc_long"], r["lc_short"])}
        for w in range(5):
            sets[f"both agree, window {w}"] = owner_sync(sL, sS, r["lc_long"], r["lc_short"], w)
        for name, (L, Sx) in sets.items():
            rec = {"event": event_study(b, L, Sx, a)}
            for ex_name, ex in EXITS.items():
                p = make_plan(b, L, Sx, ex, a, entry_until=330)
                st = stats(backtest(b, p), b)
                rec[ex_name] = st
                if tf == 5 and (name.startswith("both") and name.endswith(("2", "4")) or "alone" in name):
                    tw = twin(b, p, np.random.default_rng(7), 60)
                    rec[ex_name]["twin_wr"] = float(np.nanmedian([x["wr"] for x in tw]))
                    rec[ex_name]["twin_pf"] = float(np.nanmedian([x["pf"] for x in tw]))
            out[f"{tf}|{sym}|{name}"] = rec
        print(tf, sym, "done", flush=True)
json.dump(out, open("reports/phase1.json", "w"), indent=1, default=float)

for tf in (5, 10, 15, 30):
    print(f"\n=== {tf} min ===")
    for sym in SYMS:
        print(f"-- {sym}: signal set | events/day | fwd move ATR (t) at 2, 4, 8 bars | cost ATR || per exit: trades/day, win%, PF, $/trade [twin win%, PF]")
        for key, rec in out.items():
            t, s, name = key.split("|")
            if int(t) != tf or s != sym:
                continue
            e = rec["event"]
            line = f"{name:26s} {e['per_day']:5.2f} | " + " ".join(f"{e[k][0]:+.3f}({e[k][1]:+.1f})" for k in (2, 4, 8)) + f" | {e['cost_atr']:.3f} ||"
            for ex in EXITS:
                st = rec[ex]
                tw = f" [{st['twin_wr']:.0f}%,{st['twin_pf']:.2f}]" if "twin_wr" in st else ""
                line += f" {st['tpd']:.2f}/d {st['wr']:.0f}% {st['pf']:.2f} ${st['exp_usd']:+.0f}{tw} |"
            print(line)
