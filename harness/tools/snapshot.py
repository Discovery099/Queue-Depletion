"""Ledger snapshots for version control.

The working ledgers (ledger/trials.jsonl, trials.sqlite, lineage.sqlite, graveyard.jsonl) grow past
GitHub's 100 MB file limit, so they are not committed.  This tool writes them as compressed shards
under ledger/snapshots/ (complete shards never change again, so each commit adds little), and
restores the working files from the shards in a fresh checkout.

    python tools/snapshot.py save       # before committing
    python tools/snapshot.py restore    # in a new session, before resuming the loop
    python tools/snapshot.py verify     # snapshot equals the working ledgers

Nothing is ever deleted from the working ledgers; the trial ledger's hash chain is re-verified after
a restore.
"""
import json
import lzma
import os
import sqlite3
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import path, read_json, sha256_file, write_json  # noqa: E402

SNAP = path("ledger/snapshots")
LINES = 100_000        # trial-ledger records per shard
GENS = 5_000           # generations per lineage / graveyard shard
TRIAL_COLS = ["trial_id", "generation", "stage", "genome_id", "lineage_id", "operator", "data_slice", "instrument", "timeframe_min",
              "cost_level", "stress_mode", "seed", "opened_utc", "closed_utc", "status", "n_trades", "win_rate", "profit_factor",
              "expectancy_ticks", "score", "code_hash", "engine_version", "data_hash"]


def _write_xz(p, data):
    tmp = p + ".tmp"
    with lzma.open(tmp, "wb", preset=6) as f:
        f.write(data)
    os.replace(tmp, p)


def save():
    os.makedirs(SNAP, exist_ok=True)
    man = read_json(os.path.join(SNAP, "MANIFEST.json")) if os.path.exists(os.path.join(SNAP, "MANIFEST.json")) else {"files": {}}
    done = man["files"]
    # ---- trial ledger (append-only jsonl): fixed-size shards of whole lines
    with open(path("ledger/trials.jsonl"), "rb") as f:
        k, buf, n = 0, [], 0
        for line in f:
            buf.append(line)
            n += 1
            if len(buf) == LINES:
                name = f"trials_{k:04d}.jsonl.xz"
                if done.get(name, {}).get("lines") != LINES:
                    _write_xz(os.path.join(SNAP, name), b"".join(buf))
                    done[name] = {"lines": LINES, "complete": True}
                k, buf = k + 1, []
        if buf:
            name = f"trials_{k:04d}.jsonl.xz"
            _write_xz(os.path.join(SNAP, name), b"".join(buf))
            done[name] = {"lines": len(buf), "complete": False}
    # ---- lineage database: one parquet shard per 5,000 generations
    db = sqlite3.connect(path("ledger/lineage.sqlite"))
    top = db.execute("SELECT MAX(generation) FROM genomes").fetchone()[0] or 0
    for lo in range(0, top + 1, GENS):
        name = f"lineage_{lo:06d}.parquet"
        full = top >= lo + GENS
        if done.get(name, {}).get("complete"):
            continue
        df = pd.read_sql_query("SELECT * FROM genomes WHERE generation >= ? AND generation < ? ORDER BY generation", db, params=[lo, lo + GENS])
        df.to_parquet(os.path.join(SNAP, name), compression="zstd", compression_level=15, index=False)
        done[name] = {"rows": int(len(df)), "complete": bool(full)}
    # ---- graveyard: shards by generation
    shards = {}
    with open(path("ledger/graveyard.jsonl"), "rb") as f:
        for line in f:
            g = json.loads(line)["generation"]
            shards.setdefault(g // GENS * GENS, []).append(line)
    for lo, lines in sorted(shards.items()):
        name = f"graveyard_{lo:06d}.jsonl.xz"
        full = top >= lo + GENS
        if done.get(name, {}).get("complete"):
            continue
        _write_xz(os.path.join(SNAP, name), b"".join(lines))
        done[name] = {"lines": len(lines), "complete": bool(full)}
    man.update({"trial_records": n, "lineage_rows": db.execute("SELECT COUNT(*) FROM genomes").fetchone()[0], "top_generation": top,
                "trials_jsonl_sha256": sha256_file(path("ledger/trials.jsonl")), "graveyard_sha256": sha256_file(path("ledger/graveyard.jsonl"))})
    write_json(os.path.join(SNAP, "MANIFEST.json"), man)
    size = sum(os.path.getsize(os.path.join(SNAP, x)) for x in os.listdir(SNAP))
    big = max(os.path.getsize(os.path.join(SNAP, x)) for x in os.listdir(SNAP))
    print(f"snapshot saved: {len(done)} files, {size / 1e6:.1f} MB in total, largest {big / 1e6:.1f} MB; {n} trial records, top generation {top}")


def _names(prefix):
    return sorted(x for x in os.listdir(SNAP) if x.startswith(prefix))


def restore(force=False):
    for f in ("ledger/trials.jsonl", "ledger/trials.sqlite", "ledger/lineage.sqlite", "ledger/graveyard.jsonl"):
        if os.path.exists(path(f)) and not force:
            sys.exit(f"{f} already exists; refusing to overwrite a working ledger (use 'restore --force' in a fresh checkout only)")
    with open(path("ledger/trials.jsonl"), "wb") as out:
        for name in _names("trials_"):
            with lzma.open(os.path.join(SNAP, name), "rb") as f:
                out.write(f.read())
    with open(path("ledger/graveyard.jsonl"), "wb") as out:
        for name in _names("graveyard_"):
            with lzma.open(os.path.join(SNAP, name), "rb") as f:
                out.write(f.read())
    for f in ("ledger/trials.sqlite", "ledger/lineage.sqlite"):
        if os.path.exists(path(f)):
            os.remove(path(f))
    # the sqlite trial table is a mirror of the jsonl events: replay them
    from orchestrator.ledger import Ledger
    led = Ledger()
    rows = {}
    for line in open(path("ledger/trials.jsonl")):
        r = json.loads(line)["r"]
        if r["ev"] == "open":
            rows[r["trial_id"]] = {**{c: r.get(c) for c in TRIAL_COLS}, "opened_utc": r["t"], "status": "OPEN"}
        else:
            x = rows[r["trial_id"]]
            x.update({"closed_utc": r["t"], "status": r["status"], **{c: r.get(c) for c in ("n_trades", "win_rate", "profit_factor", "expectancy_ticks", "score")}})
    led.db.executemany(f"INSERT INTO trials ({','.join(TRIAL_COLS)}) VALUES ({','.join('?' * len(TRIAL_COLS))})",
                       [[x.get(c) for c in TRIAL_COLS] for x in rows.values()])
    led.db.commit()
    db = sqlite3.connect(path("ledger/lineage.sqlite"))
    db.execute("""CREATE TABLE IF NOT EXISTS genomes (generation INTEGER PRIMARY KEY, genome_id TEXT, lineage_id TEXT,
        island TEXT, operator TEXT, parents TEXT, tf INTEGER, complexity INTEGER, status TEXT, stage INTEGER, tier TEXT,
        score REAL, n_trades INTEGER, win_rate REAL, pf REAL, alpha REAL, cell TEXT, trig_key TEXT, genome TEXT, daily BLOB)""")
    for name in _names("lineage_"):
        df = pd.read_parquet(os.path.join(SNAP, name))
        db.executemany("INSERT OR REPLACE INTO genomes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                       df.astype(object).where(df.notna(), None).values.tolist())
    db.execute("CREATE INDEX IF NOT EXISTS ix_gid ON genomes(genome_id)")
    db.execute("CREATE INDEX IF NOT EXISTS ix_trig ON genomes(trig_key)")
    db.commit()
    verify()


def verify():
    man = read_json(os.path.join(SNAP, "MANIFEST.json"))
    from orchestrator.ledger import Ledger
    led = Ledger()
    ok, n = led.verify_chain()
    db = sqlite3.connect(path("ledger/lineage.sqlite"))
    rows = db.execute("SELECT COUNT(*) FROM genomes").fetchone()[0]
    same = (sha256_file(path("ledger/trials.jsonl")) == man["trials_jsonl_sha256"] and sha256_file(path("ledger/graveyard.jsonl")) == man["graveyard_sha256"]
            and n == man["trial_records"] and rows == man["lineage_rows"] and led.count() * 2 >= n)
    print(f"hash chain intact: {ok} ({n} records); lineage rows {rows}; trial rows {led.count()}; snapshot equals working ledgers: {same}")
    if not (ok and same):
        sys.exit(1)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "save"
    {"save": save, "verify": verify, "restore": lambda: restore("--force" in sys.argv)}[cmd]()
