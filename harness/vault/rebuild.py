"""Rebuild the sealed vault files in a fresh checkout (keeper-side tool).

data/vault is not in version control.  This re-creates it from the raw CSVs using the frozen
partition, checks every block against the hashes in config/partition.lock.json, and seals the
directory again.  It prints nothing about vault prices: only whether the hashes match.

    python vault/rebuild.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import path, read_json  # noqa: E402
from tools.prepare_data import RAW, load, sha_rows, to_store  # noqa: E402


def main():
    lock = read_json(path("config/partition.lock.json"))
    vdir = path("data/vault")
    os.makedirs(vdir, exist_ok=True)
    os.chmod(vdir, 0o700)
    frames = {s: load(s) for s in RAW}
    common = sorted(set(frames["ES"].date) & set(frames["YM"].date))
    assert len(common) == lock["common_sessions"], "raw files do not match the frozen partition"
    sess_index = {d: i for i, d in enumerate(common)}
    first = lock["research"]["sessions"] + lock["embargo"]["sessions"]
    vdates = set(common[first:])
    ok = True
    for s, df in frames.items():
        v = df[df.date.isin(vdates)]
        same = sha_rows(v) == lock["blocks"][s]["vault_sha256"] and len(v) == lock["blocks"][s]["vault_rows"]
        ok = ok and same
        if same:
            to_store(v, sess_index).to_parquet(os.path.join(vdir, f"{s}.parquet"), compression="zstd", index=False)
        print(f"{s}: vault block matches the frozen hash: {same}")
    os.chmod(vdir, 0o000)
    if not ok:
        sys.exit("HALT: vault rows do not match config/partition.lock.json (SPEC 19.6)")


if __name__ == "__main__":
    main()
