# Epoch 148 report

- Generations completed: 74000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 73501 to 74000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 325, island B 316.
- Best composite score so far: A 0.7610, B 0.7655 (generation 73770).
- Honeypot genome voided: True. Ledger chain intact: True (892156 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 148086; effective independent trials (clustered): 88853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4979 | 486 | 1 | 5.4% |
| ATOM_DROP | 1802 | 314 | 1 | 6.1% |
| ATOM_SWAP | 11530 | 860 | 8 | 12.9% |
| ENSEMBLE | 791 | 72 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 6659 | 908 | 9 | 7.6% |
| EXIT_TRANSPLANT | 6263 | 835 | 14 | 7.6% |
| INVERT | 2279 | 99 | 0 | 3.3% |
| LIBRARY_PROBE | 17375 | 1098 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 11122 | 2042 | 1 | 20.5% |
| SIMPLIFY | 1573 | 228 | 0 | 5.8% |
| SLOT_CROSSOVER | 9598 | 1440 | 9 | 11.7% |
