"""Trial ledger (SPEC 6.4, A.4, Article 13).

One row per backtest, written BEFORE the result is read.  The sqlite table is the working copy;
ledger/trials.jsonl is an append-only, hash-chained mirror so deletion or reordering is detectable.
Only the Orchestrator process writes here.
"""
import datetime
import json
import os
import sqlite3

from engine import ENGINE_VERSION, path, sha256_bytes

FIELDS = ["generation", "stage", "genome_id", "lineage_id", "operator", "data_slice", "instrument",
          "timeframe_min", "cost_level", "stress_mode", "seed", "code_hash", "engine_version", "data_hash"]
RESULT = ["n_trades", "win_rate", "profit_factor", "expectancy_ticks", "score"]


def utcnow():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class Ledger:
    def __init__(self, directory=None):
        self.dir = directory or path("ledger")
        os.makedirs(self.dir, exist_ok=True)
        self.db = sqlite3.connect(os.path.join(self.dir, "trials.sqlite"))
        self.db.execute("""CREATE TABLE IF NOT EXISTS trials (
            trial_id INTEGER PRIMARY KEY, generation INTEGER, stage TEXT, genome_id TEXT, lineage_id TEXT,
            operator TEXT, data_slice TEXT, instrument TEXT, timeframe_min INTEGER, cost_level TEXT,
            stress_mode TEXT, seed INTEGER, opened_utc TEXT, closed_utc TEXT, status TEXT,
            n_trades INTEGER, win_rate REAL, profit_factor REAL, expectancy_ticks REAL, score REAL,
            code_hash TEXT, engine_version TEXT, data_hash TEXT)""")
        self.db.execute("CREATE INDEX IF NOT EXISTS ix_gen ON trials(generation)")
        self.db.commit()
        self.jsonl = os.path.join(self.dir, "trials.jsonl")
        self.last_hash = self._tail_hash()

    def _tail_hash(self):
        if not os.path.exists(self.jsonl) or os.path.getsize(self.jsonl) == 0:
            return "0" * 64
        with open(self.jsonl, "rb") as f:
            f.seek(max(0, os.path.getsize(self.jsonl) - 8192))
            last = f.read().splitlines()[-1]
        return json.loads(last)["h"]

    def _append(self, rec):
        body = json.dumps(rec, sort_keys=True, separators=(",", ":"))
        h = sha256_bytes((self.last_hash + body).encode())
        with open(self.jsonl, "a") as f:
            f.write(json.dumps({"p": self.last_hash, "r": rec, "h": h}, sort_keys=True, separators=(",", ":")) + "\n")
        self.last_hash = h

    def open(self, **kw):
        """Insert an OPEN row and return its trial_id.  Call before running the backtest."""
        kw.setdefault("engine_version", ENGINE_VERSION)
        vals = [kw.get(k) for k in FIELDS]
        now = utcnow()
        cur = self.db.execute(
            f"INSERT INTO trials ({','.join(FIELDS)},opened_utc,status) VALUES ({','.join('?' * len(FIELDS))},?,?)",
            vals + [now, "OPEN"])
        tid = cur.lastrowid
        self._append({"ev": "open", "trial_id": tid, "t": now, **{k: kw.get(k) for k in FIELDS}})
        return tid

    def open_many(self, rows):
        ids = [self.open(**r) for r in rows]
        self.db.commit()
        return ids

    def close(self, trial_id, status="DONE", **res):
        now = utcnow()
        self.db.execute(
            "UPDATE trials SET closed_utc=?, status=?, n_trades=?, win_rate=?, profit_factor=?, expectancy_ticks=?, score=? "
            "WHERE trial_id=?",
            [now, status] + [res.get(k) for k in RESULT] + [trial_id])
        self._append({"ev": "close", "trial_id": trial_id, "t": now, "status": status,
                      **{k: res.get(k) for k in RESULT}})

    def commit(self):
        self.db.commit()

    def abort_open(self, generation):
        """Mark rows left OPEN by an interrupted generation as ABORTED (never deleted, SPEC 19.1)."""
        rows = self.db.execute("SELECT trial_id FROM trials WHERE generation=? AND status='OPEN'", [generation]).fetchall()
        for (tid,) in rows:
            self.close(tid, status="ABORTED")
        self.db.commit()
        return len(rows)

    def count(self, where="1=1", args=()):
        return self.db.execute(f"SELECT COUNT(*) FROM trials WHERE {where}", args).fetchone()[0]

    def verify_chain(self):
        """Re-walk the jsonl mirror; returns (ok, number of records)."""
        prev = "0" * 64
        n = 0
        if not os.path.exists(self.jsonl):
            return True, 0
        with open(self.jsonl) as f:
            for line in f:
                o = json.loads(line)
                body = json.dumps(o["r"], sort_keys=True, separators=(",", ":"))
                if o["p"] != prev or sha256_bytes((prev + body).encode()) != o["h"]:
                    return False, n
                prev = o["h"]
                n += 1
        return True, n
