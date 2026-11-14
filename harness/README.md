# Strategy Evolution Harness

Built from `SPEC.md` (text of `SPEC.pdf`, the owner's specification, unchanged). Start with `reports/STATUS.md` for where things
stand; `reports/milestones/understanding.md` for how the specification was read; `reports/ERRATA.md` for every deviation.

## Run and resume

```bash
cd harness
python3 -m pytest tests -q                       # 124 tests: engine, audits, gates, keeper, loop
python3 -m orchestrator.loop --generations 5000  # continue the search from state/checkpoint.json
touch STOP                                       # finishes the current batch, checkpoints and halts; delete STOP to resume
python3 -m orchestrator.loop --placebo 1000 --tag my_run --decoy phase:3   # placebo pipeline on a decoy market
```

A new session should read, in order: `SPEC.md`, `state/checkpoint.json`, the latest file in `reports/epochs/`, `ledger/lessons.md`,
`reports/STATUS.md`. Nothing needed to continue lives only in a conversation.

`library/raw/` (the extracted scripts) and `runs/` (one folder per generation) are not committed because of their size. Re-create
`library/raw/` with `cd library/raw && for z in ../raw_zips/*.zip; do unzip -q -o $z; done`.

## Layout

| Path | What |
|---|---|
| `config/` | Frozen partition and costs; gate thresholds (tighten only); search settings |
| `data/` | Raw CSVs, research block, sealed vault, data-quality report |
| `baseline/` | The owner's Smart Trend V1, its Python reproduction and reference metrics |
| `library/` | Script inventory, clusters, the atom catalogue (`atoms/catalog.py`), ontology and citations |
| `engine/` | Data access, order simulator, features, metrics, decoy markets |
| `genome/` | Expression language (Python and Pine back ends), genome, compiler to a simulator plan and to Pine |
| `gates/` | Stage 1 screen and score, stage 2 robustness, stage 3 adversarial and stage 4 holdout, statistics |
| `audit/` | Static audit, truncation audit, canaries and honeypot |
| `vault/` | Vault Keeper (the only code that may read `data/vault`) and its ledger |
| `orchestrator/` | The loop, trial ledger, promotion ladder, lessons |
| `ledger/` | Trials (sqlite and hash-chained jsonl), lineage, graveyard, lessons |
| `archive/` | Quality-diversity grid and hall of fame |
| `reports/` | Status, epochs, reviews, milestones, errata, gate changes |

Nothing here connects to a broker or a webhook. Nothing here is financial advice, and no backtest result is a promise of live
performance.
