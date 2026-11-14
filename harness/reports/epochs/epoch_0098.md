# Epoch 98 report

- Generations completed: 49000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 48501 to 49000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 312, island B 307.
- Best composite score so far: A 0.7338, B 0.5741 (generation 48034).
- Honeypot genome voided: True. Ledger chain intact: True (590848 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 98086; effective independent trials (clustered): 58854.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3381 | 329 | 1 | 5.4% |
| ATOM_DROP | 1019 | 152 | 0 | 5.9% |
| ATOM_SWAP | 7775 | 584 | 1 | 13.1% |
| ENSEMBLE | 549 | 48 | 0 | 2.7% |
| ENTRY_TRANSPLANT | 4332 | 558 | 4 | 7.6% |
| EXIT_TRANSPLANT | 4165 | 467 | 6 | 7.4% |
| INVERT | 1494 | 56 | 0 | 3.3% |
| LIBRARY_PROBE | 11917 | 816 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 7253 | 1300 | 1 | 20.6% |
| SIMPLIFY | 953 | 153 | 0 | 6.0% |
| SLOT_CROSSOVER | 6133 | 855 | 4 | 11.6% |
