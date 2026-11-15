# Epoch 182 report

- Generations completed: 91000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 90501 to 91000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 327, island B 320.
- Best composite score so far: A 0.7640, B 0.7879 (generation 88594).
- Honeypot genome voided: True. Ledger chain intact: True (1096604 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 182086; effective independent trials (clustered): 109253.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 6095 | 599 | 1 | 5.4% |
| ATOM_DROP | 2356 | 436 | 1 | 6.2% |
| ATOM_SWAP | 14218 | 1039 | 10 | 12.9% |
| ENSEMBLE | 895 | 83 | 2 | 2.7% |
| ENTRY_TRANSPLANT | 8231 | 1137 | 13 | 7.6% |
| EXIT_TRANSPLANT | 7638 | 1083 | 20 | 7.7% |
| INVERT | 2779 | 137 | 0 | 3.3% |
| LIBRARY_PROBE | 21233 | 1285 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 13634 | 2453 | 1 | 20.4% |
| SIMPLIFY | 1950 | 278 | 0 | 5.8% |
| SLOT_CROSSOVER | 11942 | 1884 | 10 | 11.8% |
