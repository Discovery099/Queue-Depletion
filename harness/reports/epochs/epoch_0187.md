# Epoch 187 report

- Generations completed: 93500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 93001 to 93500.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 326, island B 320.
- Best composite score so far: A 0.7640, B 0.7879 (generation 88594).
- Honeypot genome voided: True. Ledger chain intact: True (1126668 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 187086; effective independent trials (clustered): 112253.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 6266 | 615 | 1 | 5.4% |
| ATOM_DROP | 2447 | 461 | 1 | 6.2% |
| ATOM_SWAP | 14601 | 1054 | 10 | 12.9% |
| ENSEMBLE | 910 | 85 | 2 | 2.7% |
| ENTRY_TRANSPLANT | 8458 | 1169 | 13 | 7.6% |
| EXIT_TRANSPLANT | 7845 | 1127 | 21 | 7.7% |
| INVERT | 2857 | 139 | 0 | 3.3% |
| LIBRARY_PROBE | 21793 | 1313 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 12.9% |
| PARAM_STEP | 14023 | 2512 | 2 | 20.3% |
| SIMPLIFY | 1993 | 285 | 0 | 5.8% |
| SLOT_CROSSOVER | 12278 | 1941 | 10 | 11.8% |
