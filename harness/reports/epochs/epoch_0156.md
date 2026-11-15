# Epoch 156 report

- Generations completed: 78000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 77501 to 78000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 326, island B 316.
- Best composite score so far: A 0.7610, B 0.7655 (generation 73770).
- Honeypot genome voided: True. Ledger chain intact: True (940236 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 156086; effective independent trials (clustered): 93653.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 5247 | 518 | 1 | 5.4% |
| ATOM_DROP | 1917 | 342 | 1 | 6.1% |
| ATOM_SWAP | 12140 | 905 | 8 | 12.9% |
| ENSEMBLE | 826 | 74 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 7032 | 958 | 9 | 7.6% |
| EXIT_TRANSPLANT | 6595 | 904 | 14 | 7.6% |
| INVERT | 2397 | 108 | 0 | 3.3% |
| LIBRARY_PROBE | 18255 | 1138 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 11730 | 2162 | 1 | 20.5% |
| SIMPLIFY | 1671 | 242 | 0 | 5.8% |
| SLOT_CROSSOVER | 10161 | 1554 | 9 | 11.7% |
