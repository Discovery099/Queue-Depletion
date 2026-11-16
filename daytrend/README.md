# Daytrend: published intraday rules, ML combiner, one-time Holdout audit

Result: nothing profitable. See `reports/REPORT.md`; rules in `PROTOCOL.md` (amendment committed before the Holdout
was opened). Run: `python3 -m dt.phase1`, `python3 -m dt.phase2`; `dt.phase3` refuses to run a second time.
Uses the frozen data partition, costs and simulator of `harness/` via `quorum/qr/common.py`.
