"""Pack old generation folders (SPEC 6.3): stage 1 failures, errors and voids older than 10,000 generations
go into one compressed archive per 1,000-generation shard.  Nothing is deleted without being archived
and verified first; folders of any generation that passed the stage 1 screen stay as folders.
Usage: python tools/pack_runs.py [keep_last_generations=10000]"""
import os
import shutil
import sqlite3
import sys
import tarfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import path, read_json  # noqa: E402

keep = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
top = read_json(path("state/checkpoint.json"))["next_generation"] - 1
db = sqlite3.connect("file:" + path("ledger/lineage.sqlite") + "?mode=ro", uri=True)
keepers = {r[0] for r in db.execute("SELECT generation FROM genomes WHERE status NOT IN ('STAGE1_FAIL','VOID','ERROR','DEMOTED_EXCHANGE')")}
freed = 0
for shard in sorted(os.listdir(path("runs"))):
    d = path("runs", shard)
    if not os.path.isdir(d) or (int(shard) + 1) * 1000 - 1 > top - keep:
        continue
    names = sorted(x for x in os.listdir(d) if int(x[4:]) not in keepers)
    if not names:
        continue
    arc = path("runs", f"{shard}.tar.gz")
    if os.path.exists(arc):
        continue
    with tarfile.open(arc + ".tmp", "w:gz", compresslevel=4) as t:
        for x in names:
            t.add(os.path.join(d, x), arcname=f"{shard}/{x}")
    with tarfile.open(arc + ".tmp") as t:                     # verify before removing anything
        packed = {m.name.split("/")[1] for m in t.getmembers() if m.isdir() and m.name.count("/") == 1}
    assert packed == set(names), f"archive of shard {shard} is incomplete"
    os.replace(arc + ".tmp", arc)
    before = sum(os.path.getsize(os.path.join(r, f)) for x in names for r, _, fs in os.walk(os.path.join(d, x)) for f in fs)
    for x in names:
        shutil.rmtree(os.path.join(d, x))
    freed += before - os.path.getsize(arc)
    print(f"shard {shard}: {len(names)} folders packed, {len(os.listdir(d))} kept as folders", flush=True)
print(f"done; about {freed / 1e9:.2f} GB of file content saved (block overhead not counted)")
