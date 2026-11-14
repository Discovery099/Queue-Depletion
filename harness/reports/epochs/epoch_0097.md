# Epoch 97 report

- Generations completed: 48500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 48001 to 48500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 312, island B 307.
- Best composite score so far: A 0.7338, B 0.5741 (generation 48034).
- Honeypot genome voided: True. Ledger chain intact: True (584848 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 97086; effective independent trials (clustered): 58254.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3343 | 326 | 1 | 5.4% |
| ATOM_DROP | 1004 | 150 | 0 | 5.9% |
| ATOM_SWAP | 7700 | 581 | 1 | 13.1% |
| ENSEMBLE | 544 | 47 | 0 | 2.7% |
| ENTRY_TRANSPLANT | 4288 | 553 | 4 | 7.6% |
| EXIT_TRANSPLANT | 4125 | 464 | 6 | 7.4% |
| INVERT | 1473 | 56 | 0 | 3.3% |
| LIBRARY_PROBE | 11822 | 808 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 7177 | 1283 | 1 | 20.5% |
| SIMPLIFY | 939 | 151 | 0 | 6.0% |
| SLOT_CROSSOVER | 6056 | 844 | 4 | 11.6% |
