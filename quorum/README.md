# Quorum: Smart Trend as base, library strategies as voters

Question: does taking a trade only when Smart Trend V1 and one or more other strategies agree within 0 to 4 candles
give 5+ trades a day, 60%+ wins and a profit factor of 2+? Answer on ES/YM 5-minute data: no. See `reports/REPORT.md`.

| File | What |
|---|---|
| `PROTOCOL.md` | Rules fixed before results: splits, acceptance levels, selection rule |
| `reports/REPORT.md` | Findings |
| `deliverables/SmartTrend_Quorum.pine` | TradingView strategy: Smart Trend base + 16 switchable voters + Lorentzian + agreement window + webhook group |
| `deliverables/CHECK_SHEET.md` | Ten trades per instrument to compare against the chart |
| `reports/phase1.json`, `phase2_tf5.json.gz`, `phase3_evaluations.jsonl.gz`, `phase4.json` | Raw results |

Run (needs `harness/` data restored, see `harness/README.md`):

    python3 -m qr.phase1          # owner's hypothesis as written
    python3 -m qr.voters          # voter event matrices
    python3 -m qr.phase2 5        # census of voters and agreeing pairs
    python3 -m qr.phase3 25000    # 4 islands x 25,000 evaluations on Discover
    python3 -m qr.phase4          # shortlist, Confirm, finalist checks
    python3 -m qr.export_pine     # Pine file and check sheet

Uses the frozen partition, cost model and simulator of `harness/`. The Holdout and the vault were not opened.
