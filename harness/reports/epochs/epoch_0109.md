# Epoch 109 report

- Generations completed: 54500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 54001 to 54500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 316, island B 310.
- Best composite score so far: A 0.7610, B 0.6280 (generation 53323).
- Honeypot genome voided: True. Ledger chain intact: True (657608 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 109086; effective independent trials (clustered): 65453.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3765 | 376 | 1 | 5.4% |
| ATOM_DROP | 1186 | 188 | 0 | 6.0% |
| ATOM_SWAP | 8613 | 643 | 1 | 13.0% |
| ENSEMBLE | 613 | 54 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 4831 | 625 | 6 | 7.6% |
| EXIT_TRANSPLANT | 4627 | 540 | 9 | 7.4% |
| INVERT | 1672 | 64 | 0 | 3.3% |
| LIBRARY_PROBE | 13098 | 884 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 8149 | 1463 | 1 | 20.5% |
| SIMPLIFY | 1059 | 170 | 0 | 6.0% |
| SLOT_CROSSOVER | 6858 | 987 | 6 | 11.7% |
