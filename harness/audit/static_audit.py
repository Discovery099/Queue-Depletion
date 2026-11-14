"""Static audit (SPEC 14.2): run on every generation before any backtest.  A failure voids it.

Three scans:
  genome  - atoms registered, admitted and not hazard-tagged; parameters on their grids; within budget;
  python  - the generated strategy source and the signal-layer modules it relies on;
  pine    - the exported Pine source (stage 2 and above).
The auditor does not look at performance.
"""
import functools
import re

from engine import path, sha256_file
from genome import genome as GN
from library.atoms.catalog import ATOMS

PY_RULES = [
    ("negative_shift", r"shift\s*\(\s*[^,()]*,\s*-\s*\d|\.shift\s*\(\s*-"),
    ("centred_window", r"center\s*=\s*True"),
    ("forward_index", r"\[\s*[a-z_]\w*\s*\+\s*[1-9a-z_]"),
    ("whole_series_statistic", r"\.(mean|std|var|max|min|quantile|rank|median)\s*\(\s*\)|np\.(mean|std|var|nanmean|nanstd|quantile|percentile|median)\s*\("),
    ("vault_reference", r"data/vault|vault\.keeper|from\s+vault|import\s+vault"),
    ("date_literal", r"(?<![\w.])(19|20)\d{2}[-/]?(0[1-9]|1[0-2])[-/]?(0[1-9]|[12]\d|3[01])(?![\w.])"),
    ("price_level_literal", r"(?<![\w.])(?:[2-7]\d{3}|[2-5]\d{4})(?:\.\d+)?(?![\w.])"),
]
PINE_RULES = [
    ("security_lookahead_on", r"lookahead\s*=\s*(barmerge\.lookahead_on|true)"),
    ("realtime_branch", r"barstate\.isrealtime|barstate\.isnew"),
    ("calc_on_every_tick", r"calc_on_every_tick\s*=\s*true"),
    ("calc_on_order_fills", r"calc_on_order_fills\s*=\s*true"),
    ("negative_offset", r"offset\s*=\s*-|\[\s*-\s*\d"),
    ("varip", r"\bvarip\b"),
    ("bar_magnifier", r"use_bar_magnifier\s*=\s*true|security_lower_tf"),
    ("process_orders_on_close", r"process_orders_on_close\s*=\s*true"),
]
# modules whose text forms the signal layer; whole-series statistics are forbidden in them
SIGNAL_LAYER = ["library/atoms/catalog.py", "genome/compile_py.py"]


def _strip_comments_py(src):
    src = re.sub(r'"""[\s\S]*?"""', '""', src)
    return re.sub(r"#.*", "", src)


def scan_python(src, whole_series=True):
    code = _strip_comments_py(src)
    code = re.sub(r"r'''[\s\S]*?'''", "''", code)          # the embedded genome JSON is audited by scan_genome
    hits = []
    for name, pat in PY_RULES:
        if name == "whole_series_statistic" and not whole_series:
            continue
        m = re.search(pat, code)
        if m:
            hits.append({"rule": name, "match": m.group(0)[:60]})
    return hits


@functools.lru_cache(maxsize=4)
def _signal_layer_scan(key):
    hits = []
    for rel in SIGNAL_LAYER:
        for h in scan_python(open(path(rel)).read()):
            if h["rule"] in ("price_level_literal",):     # grids of indicator lengths are not price levels
                continue
            hits.append({**h, "file": rel})
    return tuple((h["file"], h["rule"], h["match"]) for h in hits)


def signal_layer_hash():
    return "|".join(sha256_file(path(r))[:16] for r in SIGNAL_LAYER)


def scan_genome(g, ceiling=GN.CEILING, admitted=None):
    hits = [{"rule": "genome_invalid", "match": p} for p in GN.validate(g)]
    for e in GN.atom_entries(g):
        a = ATOMS.get(e["atom"])
        if a is None:
            continue
        if getattr(a, "blocked", False):
            hits.append({"rule": "hazard_tagged_atom", "match": e["atom"]})
        if admitted is not None and e["atom"] not in admitted and not getattr(a, "blocked", False):
            hits.append({"rule": "atom_not_admitted", "match": e["atom"]})
        for k, v in e["params"].items():
            if isinstance(v, float) and len(f"{v:.10g}".replace(".", "").replace("-", "").lstrip("0")) > 4:
                hits.append({"rule": "parameter_over_4_significant_digits", "match": f"{e['atom']}.{k}={v}"})
    if g["complexity"] > ceiling:
        hits.append({"rule": "complexity_over_budget", "match": f"{g['complexity']} > {ceiling}"})
    return hits


def scan_pine(src):
    code = re.sub(r"//.*", "", src)
    hits = []
    for name, pat in PINE_RULES:
        m = re.search(pat, code)
        if m:
            hits.append({"rule": name, "match": m.group(0)[:60]})
    for m in re.finditer(r"request\.security\s*\(([^\n]*)\)", code):
        if "lookahead_off" not in m.group(1):
            hits.append({"rule": "security_without_lookahead_off", "match": m.group(0)[:60]})
    for line in code.splitlines():
        if "timeframe.period" in line and "request.security" not in line:
            hits.append({"rule": "timeframe_condition", "match": line.strip()[:60]})
        if "barstate.islast" in line and not line.strip().startswith("if barstate.islast"):
            hits.append({"rule": "islast_outside_display", "match": line.strip()[:60]})
    # every order call must sit under a barstate.isconfirmed guard
    if re.search(r"strategy\.(entry|order|exit|close|close_all|cancel)\s*\(", code):
        if "barstate.isconfirmed" not in code:
            hits.append({"rule": "orders_without_isconfirmed", "match": "no barstate.isconfirmed guard"})
        lines = code.splitlines()
        guard_indent = None
        for ln in lines:
            if not ln.strip():
                continue
            ind = len(ln) - len(ln.lstrip())
            if guard_indent is not None and ind <= guard_indent:
                guard_indent = None
            if re.match(r"\s*if\s+.*(barstate\.isconfirmed|canTrade)", ln):
                guard_indent = ind if guard_indent is None else guard_indent
            if re.search(r"strategy\.(entry|order|exit|close|close_all|cancel)\s*\(", ln) and guard_indent is None:
                hits.append({"rule": "order_outside_confirmed_block", "match": ln.strip()[:60]})
    return hits


def audit(g, py_src, pine_src=None, ceiling=GN.CEILING, admitted=None):
    """Full static audit.  Returns {'clean': bool, 'hits': [...]}."""
    hits = [{"where": "genome", **h} for h in scan_genome(g, ceiling, admitted)]
    hits += [{"where": "strategy.py", **h} for h in scan_python(py_src)]
    hits += [{"where": f, "rule": r, "match": m} for f, r, m in _signal_layer_scan(signal_layer_hash())]
    if pine_src is not None:
        hits += [{"where": "strategy.pine", **h} for h in scan_pine(pine_src)]
    return {"clean": not hits, "hits": hits, "signal_layer_hash": signal_layer_hash()}
