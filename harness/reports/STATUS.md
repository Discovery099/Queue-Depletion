# Status: run complete at generation 100,000

- Generations completed: 100,000 of 100,000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B). The vault and the inner holdout were never opened.
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1,000 placebo generations (four runs, three decoy types)

`OUTCOME: NONE` — no strategy met Bronze. Read `reports/FINAL.md` first; `deliverables/DOSSIER.md` covers the leading candidate.

## In one screen

| Measure | Value |
|---|---|
| Passed the stage 1 screen on their island's folds | 66 |
| Confirmed on all six test folds | 0 |
| Closest approach | Generation 44439: 69.3% wins, twin 61.7%, profit factor 1.51 on 915 trades; failed one gate (35.9% of profit from one fold; limit 35%) |
| Most consistent | Generation 25968: 73.2% wins, twin 66.0%, profit factor 1.19 on 2,281 trades, about 400 trades a year per instrument |
| Leaders on unseen folds at the end | 69.6% wins, profit factor 1.27 (1.77 on the folds they were selected on) |
| Stage 1 candidate backtests | 200,156; about 120,000 effective independent trials |
| Canary adoption; honeypot | 0%; voided at all 200 epoch checks |
| Reproducibility | 80 of 80 re-runs identical |
| Ledger | 602,419 rows, hash chain intact |
| Tests | 134 passing |

## What the run established

1. The owner's target (80% wins, high profit factor, 200 trades a year, robust across timeframes and instruments) is not supported
   by this data with the techniques in the library. Nothing came close to Gold; nothing reached Bronze.
2. A small real edge exists in momentum-thrust and trend-flip entries on trend days: 4 to 8 points of win rate beyond the exits'
   geometry, a profit factor of about 1.2 to 1.3 on unseen folds, weaker on YM than ES and fading through 2023.
3. Mean-reversion, sweep, exhaustion and ES/YM lead-lag triggers perform like the no-information canaries after costs.
4. Selection overfits fast. Every safeguard that fired (twin, island exchange, all-folds confirmation, placebo) fired on something real.

## Where things are

| What | Where |
|---|---|
| Final report, charts | `reports/FINAL.md`, `reports/charts/` |
| Leading-candidate dossier | `deliverables/DOSSIER.md` |
| Candidate Pine files (NOT CERTIFIED), parity results, TradingView check sheets, robustness runs | `reports/candidates/` |
| Frontier tables | `reports/frontier.md` |
| Island exchanges | `reports/exchange_*.md` |
| Strategist reviews | `reports/reviews/` |
| Lessons, graveyard | `ledger/lessons.md`, `ledger/snapshots/graveyard_*.jsonl.xz` |
| Gate changes (tightenings only) | `reports/gate_changes.md` |
| Errata (15 items) | `reports/ERRATA.md` |
| Generation 0 checklist and what was not built | `reports/milestones/bootstrap.md` |
| How to restore and resume | `README.md` |

## What the owner decides next

The loop has ended and will not extend past 100,000 without written instruction. Options, recorded in `OWNER_OVERRIDES.md` if taken:

- Paper-trade a candidate through the existing webhook in paper mode (no certification implied).
- Add a less correlated instrument (NQ, RTY, CL or GC) as pure out-of-sample data. This is the most valuable extra evidence.
- Relax a requirement (profit-factor floor, frequency floor) and say which; the frontier shows what each buys.
- Supply finer data to remove the intrabar ambiguity.

## Housekeeping

- Pushed to GitHub on branch `claude/dazzling-rubin-wc3b48`.
- `runs/` (one folder per generation; 13 GB, older shards packed as `runs/NNN.tar.gz`) and `library/raw/` exist only on the machine
  that ran them. The ledgers are in the repository as compressed snapshots (`python3 tools/snapshot.py restore`).
- Nothing here connects to a broker or a webhook. Nothing here is financial advice.
