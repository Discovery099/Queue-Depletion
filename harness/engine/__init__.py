"""Backtest engine package: data access, order simulator, cost model, metrics.

ENGINE_VERSION is bumped on any change to engine, gates or audits (SPEC 19.7); a bump
requires re-running tests/engine and re-scoring the hall of fame (SPEC 7.8).
"""
import hashlib
import json
import os
import tempfile

ENGINE_VERSION = "1.0.0"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def path(*parts):
    return os.path.join(ROOT, *parts)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def canon(obj):
    """Canonical JSON text used for every content hash."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=_default)


def _default(o):
    import numpy as np
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(type(o))


def write_json(p, obj, indent=1):
    """Atomic JSON write: temporary file then rename (SPEC 19.1)."""
    d = os.path.dirname(p)
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
    with os.fdopen(fd, "w") as f:
        json.dump(obj, f, indent=indent, sort_keys=True, default=_default)
    os.replace(tmp, p)


def read_json(p):
    with open(p) as f:
        return json.load(f)


def write_text(p, s):
    d = os.path.dirname(p)
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
    with os.fdopen(fd, "w") as f:
        f.write(s)
    os.replace(tmp, p)


def frozen_hashes():
    """Hashes of the frozen files, verified at every start (SPEC 19.1, 19.6)."""
    return {
        "partition": sha256_file(path("config/partition.lock.json")),
        "costs": sha256_file(path("config/costs.lock.json")),
        "raw_ES": sha256_file(path("data/raw/ES_5min_RTH_6year.csv")),
        "raw_YM": sha256_file(path("data/raw/YM_5min_RTH_6year.csv")),
    }
