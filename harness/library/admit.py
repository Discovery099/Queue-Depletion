"""Atom admission (SPEC 8.1 steps 5-8, 8.4, 8.5, 8.6).

For every atom: (1) truncation audit of its own conditions, proving the re-implementation is free of
the hazards found in its source scripts; (2) the standalone information test on the first half of the
Research block, each logged as a trial; (3) supporting-script count and up to 10 citations from the
mined inventory.  Writes library/ontology.json and library/citations.jsonl.

Library files are read as text only.  Nothing from them is executed.
"""
import csv
import gzip
import json
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import path, write_json, sha256_file  # noqa: E402
from engine.data import INSTRUMENTS, partition  # noqa: E402
from genome.dsl import Ctx  # noqa: E402
from library.atoms import catalog as K  # noqa: E402
from audit import canary, truncation  # noqa: E402
from orchestrator import evaluate as EV  # noqa: E402
from orchestrator.ledger import Ledger  # noqa: E402

HORIZONS = (3, 12, 39)
PERMISSIVE = ("MPL-2.0", "MIT", "Apache-2.0")
RESTRICTED = ("CC-BY-NC-SA-4.0", "CC-BY-NC", "CC-BY-SA", "GPL")


def load_inventory():
    with gzip.open(path("library/inventory.csv.gz"), "rt", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["callset"] = set(r["calls"].split("|")) if r["calls"] else set()
    return rows


def citations(rows, texts):
    out = {}
    for aid, a in K.ATOMS.items():
        calls, kw = a.ev
        pat = re.compile(kw) if kw else None
        hits = []
        for i, r in enumerate(rows):
            if calls and not calls <= r["callset"]:
                continue
            if pat is not None:
                t = texts.get(i)
                if t is None or not pat.search(t):
                    continue
            elif not calls:
                continue
            hits.append(i)
        lic = {}
        for i in hits:
            lic[rows[i]["licence"]] = lic.get(rows[i]["licence"], 0) + 1
        ordered = sorted(hits, key=lambda i: (0 if rows[i]["licence"] in PERMISSIVE else 1 if rows[i]["licence"] == "unspecified" else 2,
                                              -int(rows[i]["version"]), rows[i]["path"]))
        hz = {}
        for i in hits:
            for h in filter(None, rows[i]["hazards"].split("|")):
                hz[h] = hz.get(h, 0) + 1
        out[aid] = {"supporting_scripts": len(hits), "licence_counts": lic,
                    "only_restricted_licences": bool(hits) and all(rows[i]["licence"] in RESTRICTED for i in hits),
                    "hazards_in_sources": dict(sorted(hz.items(), key=lambda kv: -kv[1])),
                    "citations": [{"path": rows[i]["path"], "licence": rows[i]["licence"]} for i in ordered[:10]]}
    return out


def standalone(ctxs, o, first_half):
    """Signed forward return in ATR units when the atom is active, minus the mean at matched times of day.
    Block bootstrap by session (500 draws).  Returns {horizon: {effect, lo, hi, n}}."""
    res = {}
    rng = np.random.default_rng(12345)
    per_h = {h: [] for h in HORIZONS}
    for c in ctxs:
        b = c.b
        m = b.sess < first_half
        L, S = c.ev(o["long"]) & m, c.ev(o["short"]) & m
        a = c.ev(K.A)
        bucket = b.slot // 6
        for h in HORIZONS:
            fwd = np.full(b.n, np.nan)
            same = b.sess[h:] == b.sess[:-h]
            fwd[:-h] = np.where(same, (b.c[h:] - b.c[:-h]) / np.where(a[:-h] > 0, a[:-h], np.nan), np.nan)
            base = np.zeros(b.n)
            for k in np.unique(bucket):
                sel = m & (bucket == k) & ~np.isnan(fwd)
                base[bucket == k] = fwd[sel].mean() if sel.any() else 0.0
            ex = np.where(L, fwd - base, 0.0) + np.where(S, -(fwd - base), 0.0)
            act = (L | S) & ~np.isnan(fwd)
            ex = np.where(act, ex, 0.0)
            ns = int(b.sess.max()) + 1
            per_h[h].append((np.bincount(b.sess, weights=ex, minlength=ns)[:first_half],
                             np.bincount(b.sess, weights=act.astype(float), minlength=ns)[:first_half]))
    for h in HORIZONS:
        s = sum(x[0] for x in per_h[h])
        n = sum(x[1] for x in per_h[h])
        tot = n.sum()
        if tot < 30:
            res[h] = {"effect": 0.0, "lo": 0.0, "hi": 0.0, "n": int(tot)}
            continue
        idx = rng.integers(0, len(s), (500, len(s)))
        bs = s[idx].sum(1) / np.maximum(1.0, n[idx].sum(1))
        res[h] = {"effect": float(s.sum() / tot), "lo": float(np.percentile(bs, 2.5)), "hi": float(np.percentile(bs, 97.5)),
                  "n": int(tot), "t": float((s.sum() / tot) / max(1e-12, bs.std()))}
    return res


def main():
    canary.install()
    rows = load_inventory()
    need_text = any(a.ev[1] for a in K.ATOMS.values())
    texts = {}
    if need_text:
        raw = path("library/raw")
        for i, r in enumerate(rows):
            try:
                texts[i] = open(os.path.join(raw, r["path"]), "rb").read().decode("utf-8", "replace").lower()
            except OSError:
                pass
    cites = citations(rows, texts)
    texts.clear()
    led = Ledger()
    first_half = partition()["research"]["sessions"] // 2
    ctxs = [EV.ctx_for(s, 5) for s in INSTRUMENTS]
    # admission slice for the truncation audit: the last 80 search sessions of each instrument
    slices = []
    for c in ctxs:
        b = c.b
        m = b.sess >= EV.N_SEARCH - 80
        sb = EV.subset(b, m)
        sb.key = b.key + "|admit"
        slices.append((sb, {k: v[m] for k, v in c.other.items()}))
    onto = {"note": "All code is an original re-implementation of concepts. Hazard tags list what the SOURCE scripts did; "
                    "'hazard_free' is the truncation-audit result for this re-implementation.", "atoms": {}}
    admitted = 0
    for aid, a in K.ATOMS.items():
        rec = {"id": aid, "type": a.typ, "family": a.fam, "family_name": K.FAMILIES[a.fam], "description": a.desc,
               "inputs": a.grid, "defaults": a.default, "session_time_window": bool(a.tw),
               "hazard_tags_in_sources": list(a.hz), **cites[aid]}
        if getattr(a, "blocked", False):
            rec.update({"hazard_free": False, "admitted": False, "blocked_reason": "hazard-tagged: " + ",".join(a.hz)})
            onto["atoms"][aid] = rec
            continue
        if a.typ == "EXIT":
            rec.update({"hazard_free": True, "admitted": True, "kind": a.kind, "prior_weight": 1.0,
                        "note": "exit and stop rules are audited inside every genome's truncation audit"})
            admitted += 1
            onto["atoms"][aid] = rec
            continue
        o = a.build()
        clean = True
        for sb, oth in slices[:1]:
            for name in ("long", "short", "lvl_long", "lvl_short"):
                if o[name] is not None:
                    r = truncation.audit_expr(o[name], sb, oth, EV.EXT_PROVIDER, n=30, seed=len(aid))
                    clean = clean and r["clean"]
        tid = led.open(generation=0, stage="atom_info", genome_id=aid, lineage_id="atoms", operator="STANDALONE_TEST",
                       data_slice="research_first_half", instrument="ES+YM", timeframe_min=5, cost_level="none",
                       stress_mode="forward_return", seed=12345, code_hash=sha256_file(path("library/atoms/catalog.py")),
                       data_hash=partition()["blocks"]["ES"]["research_sha256"][:16])
        led.commit()
        info = standalone(ctxs, o, first_half)
        led.close(tid, n_trades=info[12]["n"], score=info[12].get("t"))
        best_t = max(info[h].get("t", 0.0) for h in HORIZONS)
        rec.update({"hazard_free": bool(clean), "admitted": bool(clean), "standalone": info,
                    "prior_weight": float(min(3.0, max(0.25, 1.0 + best_t / 2.0)))})
        admitted += int(clean)
        onto["atoms"][aid] = rec
    led.commit()
    fams = {}
    for r in onto["atoms"].values():
        if r["admitted"]:
            fams[r["family"]] = fams.get(r["family"], 0) + 1
    onto["summary"] = {"atoms": len(onto["atoms"]), "admitted": admitted, "admitted_by_family": fams,
                       "families_with_admitted_atoms": len(fams)}
    write_json(path("library/ontology.json"), onto)
    with open(path("library/citations.jsonl"), "w") as f:
        for aid, r in onto["atoms"].items():
            f.write(json.dumps({"atom": aid, "supporting_scripts": r["supporting_scripts"], "citations": r["citations"],
                                "only_restricted_licences": r["only_restricted_licences"]}) + "\n")
    print(json.dumps(onto["summary"], indent=1))
    bad = [k for k, r in onto["atoms"].items() if not r["admitted"]]
    print("not admitted:", bad)
    z = sorted(((r["standalone"][12].get("t", 0), k) for k, r in onto["atoms"].items() if "standalone" in r), reverse=True)
    print("largest standalone t (12 bars):", [(k, round(t, 1)) for t, k in z[:8]])
    print("smallest:", [(k, round(t, 1)) for t, k in z[-5:]])
    print("zero-support atoms:", [k for k, r in onto["atoms"].items() if r["supporting_scripts"] == 0])


if __name__ == "__main__":
    main()
