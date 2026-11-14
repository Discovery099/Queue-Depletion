"""Script-library mining, deterministic steps (SPEC 8.1 steps 1-3 and the hazard scan of 8.4).

Every library file is untrusted text: it is read, tokenised with regular expressions and counted.
Nothing from the library is ever executed or imported.

The supplied archive has no index, provenance or licence folders (only <type>/<version>/<name>.pine),
so the inventory is built from the files themselves: declaration type and version from the path and
the //@version line, licence and author from the header comments.

Outputs (library/):
  inventory.csv.gz   one row per script
  call_stats.json    how many scripts call each function
  clusters.json      fingerprint clusters with representative scripts
  hazards.json       scripts per hazard tag
  mining_summary.json
"""
import collections
import csv
import gzip
import hashlib
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

LICENCES = [
    ("CC-BY-NC-SA-4.0", r"NonCommercial-ShareAlike|BY-NC-SA|by-nc-sa"),
    ("CC-BY-NC", r"Attribution-NonCommercial|BY-NC\b|by-nc\b"),
    ("CC-BY-SA", r"Attribution-ShareAlike|BY-SA\b|by-sa\b"),
    ("MPL-2.0", r"Mozilla Public License|mozilla\.org/MPL"),
    ("GPL", r"GNU General Public|GPL-?[23]|gnu\.org/licenses"),
    ("MIT", r"\bMIT License\b|opensource\.org/licenses/MIT"),
    ("Apache-2.0", r"Apache License"),
]
NON_COMMERCIAL_OR_SHAREALIKE = {"CC-BY-NC-SA-4.0", "CC-BY-NC", "CC-BY-SA", "GPL"}

# pre-v5 names that became ta.* / request.* / math.* later, so one technique maps to one token
LEGACY = set("""sma ema rma wma vwma swma alma hma linreg rsi atr tr stoch cci mfi macd bb bbw kc kcw dmi adx
supertrend sar highest lowest highestbars lowestbars crossover crossunder cross change mom roc barssince valuewhen
pivothigh pivotlow stdev variance dev correlation percentrank percentile_linear_interpolation
percentile_nearest_rank cum vwap obv tsi cmo cog wpr rising falling median mode range""".split())
LEGACY_REQ = {"security": "request.security"}
LEGACY_MATH = set("abs max min round floor ceil sqrt pow log exp sign avg sum".split())

CALL = re.compile(r"(?<![\w.])((?:ta|math|request|strategy|array|matrix|str|timeframe|session|ticker|color|line|label|box|table|input|syminfo|barstate|chart|map|polyline|linefill|log|runtime)\.[A-Za-z_][\w.]*|[A-Za-z_]\w*)\s*\(")
COMMENT = re.compile(r"//.*?$", re.M)
STRING = re.compile(r"\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'")
INPUT = re.compile(r"(\w+)\s*=\s*input(?:\.(\w+))?\s*\(\s*(?:defval\s*=\s*)?([-+]?\d+\.?\d*|true|false)")
COND = re.compile(r"(?:alertcondition|strategy\.entry|strategy\.order|plotshape|plotarrow)\s*\((.*)$", re.M)

HAZARDS = {
    "SECURITY_LOOKAHEAD": re.compile(r"lookahead\s*=\s*(?:barmerge\.lookahead_on|true)"),
    "PIVOT_UNCONFIRMED": re.compile(r"pivot(?:high|low)[\s\S]{0,4000}?(?:offset\s*=\s*-|bar_index\s*-\s*\w+|bar_index\s*\[)"),
    "REALTIME_REPAINT": re.compile(r"barstate\.isrealtime|calc_on_every_tick\s*=\s*true|\bvarip\b"),
    "FUTURE_OFFSET": re.compile(r"offset\s*=\s*-\s*\w|\[\s*-\s*\d+\s*\]"),
    "ZIGZAG_RECALC": re.compile(r"zig\s*-?zag|line\.set_xy[12]?\s*\(|line\.set_y[12]\s*\(|regression channel", re.I),
    "HTF_CLOSE_INTRABAR": re.compile(r"(?:request\.)?security\s*\([^\n]*?[\"'](?:D|1D|W|1W|M|1M)[\"'][^\n]*?\bclose\b(?!\s*\[)"),
    "SESSION_VALUE_LEAK": re.compile(r"(?:request\.)?security\s*\([^\n]*?[\"'](?:D|1D|W|1W)[\"'][^\n]*?\b(?:high|low|volume)\b(?!\s*\[)[^\n]*?lookahead\s*=\s*(?:barmerge\.lookahead_on|true)"),
    "REPEATED_SIGNAL_DELETE": re.compile(r"label\.delete\s*\(\s*\w+\s*\[\s*1\s*\]|label\.set_x(?:y|loc)?\s*\("),
    "BAR_MAGNIFIER_DEPENDENCE": re.compile(r"use_bar_magnifier\s*=\s*true|security_lower_tf|calc_on_order_fills\s*=\s*true"),
}


def norm_call(name, version):
    if "." in name:
        return name
    if name in LEGACY_REQ:
        return LEGACY_REQ[name]
    if name in LEGACY and version <= 4:
        return "ta." + name
    if name in LEGACY_MATH and version <= 4:
        return "math." + name
    if name == "study":
        return "indicator"
    return name


def skeleton(expr):
    """Normalised expression skeleton: identifiers -> I, numbers -> N, strings dropped."""
    e = STRING.sub("S", expr)
    e = re.sub(r"\d+\.?\d*", "N", e)
    e = re.sub(r"[A-Za-z_][\w.]*", lambda m: m.group(0) if m.group(0) in ("and", "or", "not") or "." in m.group(0) else "I", e)
    return re.sub(r"\s+", "", e)[:120]


def scan():
    rows, feats = [], []
    seen_exact, seen_ws = {}, {}
    n_files = dup_exact = dup_ws = parse_fail = 0
    for dirpath, _, files in sorted(os.walk(RAW)):
        for fn in sorted(files):
            if not fn.endswith(".pine"):
                continue
            n_files += 1
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, RAW)
            try:
                raw = open(p, "rb").read()
                text = raw.decode("utf-8", errors="replace")
            except OSError:
                parse_fail += 1
                continue
            h = hashlib.sha256(raw).hexdigest()
            hw = hashlib.sha256(re.sub(r"\s+", "", text).encode()).hexdigest()
            if h in seen_exact:
                dup_exact += 1
                continue
            seen_exact[h] = rel
            if hw in seen_ws:
                dup_ws += 1
                continue
            seen_ws[hw] = rel
            parts = rel.split(os.sep)
            decl_dir, ver_dir = parts[0], parts[1]
            mv = re.search(r"//\s*@version\s*=\s*(\d)", text)
            version = int(mv.group(1)) if mv else (int(ver_dir[1]) if ver_dir[1:].isdigit() else 0)
            head = text[:3000]
            lic = "unspecified"
            for name, pat in LICENCES:
                if re.search(pat, head):
                    lic = name
                    break
            ma = re.search(r"//\s*©\s*([^\n\r]{1,60})", head)
            author = ma.group(1).strip() if ma else ""
            code = COMMENT.sub("", text)
            nostr = STRING.sub('""', code)
            try:
                calls = collections.Counter(norm_call(m.group(1), version) for m in CALL.finditer(nostr))
                for kw in ("if", "for", "while", "switch", "and", "or", "not"):
                    calls.pop(kw, None)
                inputs = INPUT.findall(nostr)
                conds = [skeleton(m.group(1)) for m in COND.finditer(nostr)]
                hz = sorted(k for k, pat in HAZARDS.items() if pat.search(code))
            except RecursionError:
                parse_fail += 1
                continue
            builtin = sorted(k for k in calls if "." in k)
            rows.append({"path": rel, "declaration": decl_dir, "version": version, "licence": lic, "author": author,
                         "bytes": len(raw), "lines": text.count("\n") + 1, "sha256": h, "n_inputs": len(inputs),
                         "n_security": calls.get("request.security", 0), "n_ta_calls": sum(v for k, v in calls.items() if k.startswith("ta.")),
                         "hazards": "|".join(hz), "calls": "|".join(builtin)})
            feats.append((set(builtin), conds, [v for _, _, v in inputs]))
    summary = {"files": n_files, "exact_duplicates_dropped": dup_exact, "whitespace_duplicates_dropped": dup_ws,
               "parse_failures": parse_fail, "scripts_kept": len(rows)}
    return rows, feats, summary


def cluster(rows, feats, seed=17):
    """Cluster by fingerprint: TF-IDF over called functions and condition skeletons, reduced by SVD,
    grouped with k-means.  Deterministic for a fixed seed."""
    from sklearn.cluster import MiniBatchKMeans
    from sklearn.decomposition import TruncatedSVD
    from sklearn.feature_extraction.text import TfidfVectorizer
    docs = []
    for calls, conds, defaults in feats:
        toks = list(calls) + ["sk:" + hashlib.md5(c.encode()).hexdigest()[:8] for c in conds[:20]]
        toks += ["dv:" + d for d in defaults[:12]]
        docs.append(" ".join(t.replace(" ", "") for t in toks) or "empty")
    X = TfidfVectorizer(token_pattern=r"\S+", min_df=3, sublinear_tf=True).fit_transform(docs)
    Z = TruncatedSVD(n_components=min(96, X.shape[1] - 1), random_state=seed).fit_transform(X)
    Z /= np.maximum(np.linalg.norm(Z, axis=1, keepdims=True), 1e-12)
    k = max(50, min(2500, len(rows) // 6))
    km = MiniBatchKMeans(n_clusters=k, random_state=seed, n_init=3, batch_size=4096).fit(Z)
    lab = km.labels_
    out = []
    for cid in range(k):
        idx = np.flatnonzero(lab == cid)
        if len(idx) == 0:
            continue
        d = np.linalg.norm(Z[idx] - km.cluster_centers_[cid], axis=1)
        rep = idx[np.argsort(d)[:3]]
        common = collections.Counter()
        for i in idx:
            common.update(feats[i][0])
        top = [f for f, c in common.most_common(12) if c >= 0.5 * len(idx)]
        out.append({"cluster": int(cid), "size": int(len(idx)), "representatives": [rows[i]["path"] for i in rep],
                    "common_calls": top})
    out.sort(key=lambda c: -c["size"])
    return out, lab


def main():
    if not os.path.isdir(RAW):
        sys.exit("library/raw is missing: unzip library/raw_zips/*.zip into library/raw first")
    rows, feats, summary = scan()
    stats = collections.Counter()
    for calls, _, _ in feats:
        stats.update(calls)
    clusters, lab = cluster(rows, feats)
    for r, c in zip(rows, lab):
        r["cluster"] = int(c)
    with gzip.open(os.path.join(HERE, "inventory.csv.gz"), "wt", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    hz = collections.defaultdict(int)
    for r in rows:
        for h in filter(None, r["hazards"].split("|")):
            hz[h] += 1
    summary.update({
        "by_declaration": dict(collections.Counter(r["declaration"] for r in rows)),
        "by_version": dict(sorted(collections.Counter(r["version"] for r in rows).items())),
        "by_licence": dict(collections.Counter(r["licence"] for r in rows).most_common()),
        "clusters": len(clusters), "scripts_with_any_hazard": sum(1 for r in rows if r["hazards"]),
        "hazard_counts": dict(sorted(hz.items(), key=lambda kv: -kv[1])),
        "distinct_builtin_functions": len(stats),
    })
    json.dump(dict(stats.most_common()), open(os.path.join(HERE, "call_stats.json"), "w"), indent=0)
    json.dump(clusters, open(os.path.join(HERE, "clusters.json"), "w"), indent=0)
    json.dump(summary, open(os.path.join(HERE, "mining_summary.json"), "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
