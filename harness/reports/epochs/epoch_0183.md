# Epoch 183 report

- Generations completed: 91500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 91001 to 91500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 327, island B 320.
- Best composite score so far: A 0.7640, B 0.7879 (generation 88594).
- Honeypot genome voided: True. Ledger chain intact: True (1102604 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 183086; effective independent trials (clustered): 109853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 6128 | 601 | 1 | 5.4% |
| ATOM_DROP | 2370 | 441 | 1 | 6.2% |
| ATOM_SWAP | 14283 | 1042 | 10 | 12.9% |
| ENSEMBLE | 898 | 83 | 2 | 2.7% |
| ENTRY_TRANSPLANT | 8278 | 1148 | 13 | 7.7% |
| EXIT_TRANSPLANT | 7676 | 1091 | 20 | 7.7% |
| INVERT | 2798 | 138 | 0 | 3.3% |
| LIBRARY_PROBE | 21381 | 1294 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 12.9% |
| PARAM_STEP | 13696 | 2462 | 1 | 20.4% |
| SIMPLIFY | 1959 | 280 | 0 | 5.8% |
| SLOT_CROSSOVER | 12004 | 1892 | 10 | 11.8% |
