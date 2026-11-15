# Epoch 188 report

- Generations completed: 94000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 93501 to 94000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 2 |
| STAGE1_FAIL | 498 |

- Stage 1 pass rate: 0.40%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 326, island B 320.
- Best composite score so far: A 0.7640, B 0.7879 (generation 88594).
- Honeypot genome voided: True. Ledger chain intact: True (1132692 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 188086; effective independent trials (clustered): 112852.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 6304 | 623 | 1 | 5.4% |
| ATOM_DROP | 2465 | 464 | 1 | 6.2% |
| ATOM_SWAP | 14670 | 1058 | 10 | 12.9% |
| ENSEMBLE | 911 | 86 | 2 | 2.7% |
| ENTRY_TRANSPLANT | 8518 | 1174 | 14 | 7.6% |
| EXIT_TRANSPLANT | 7878 | 1134 | 22 | 7.7% |
| INVERT | 2873 | 141 | 0 | 3.3% |
| LIBRARY_PROBE | 21904 | 1319 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 12.9% |
| PARAM_STEP | 14093 | 2528 | 2 | 20.3% |
| SIMPLIFY | 2008 | 290 | 0 | 5.8% |
| SLOT_CROSSOVER | 12347 | 1953 | 10 | 11.8% |
