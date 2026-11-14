# Epoch 90 report

- Generations completed: 45000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 44501 to 45000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 306, island B 307.
- Best composite score so far: A 0.6862, B 0.5468 (generation 43033).
- Honeypot genome voided: True. Ledger chain intact: True (542760 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 90086; effective independent trials (clustered): 54054.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3114 | 296 | 1 | 5.4% |
| ATOM_DROP | 907 | 134 | 0 | 5.9% |
| ATOM_SWAP | 7146 | 543 | 1 | 13.1% |
| ENSEMBLE | 503 | 38 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 4015 | 521 | 2 | 7.6% |
| EXIT_TRANSPLANT | 3803 | 430 | 4 | 7.4% |
| INVERT | 1378 | 53 | 0 | 3.3% |
| LIBRARY_PROBE | 11011 | 770 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 6635 | 1175 | 1 | 20.5% |
| SIMPLIFY | 858 | 135 | 0 | 6.0% |
| SLOT_CROSSOVER | 5601 | 769 | 4 | 11.6% |
