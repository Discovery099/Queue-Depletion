# Epoch 140 report

- Generations completed: 70000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 69501 to 70000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 325, island B 315.
- Best composite score so far: A 0.7610, B 0.7138 (generation 66118).
- Honeypot genome voided: True. Ledger chain intact: True (844044 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 140086; effective independent trials (clustered): 84053.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4727 | 464 | 1 | 5.4% |
| ATOM_DROP | 1674 | 286 | 0 | 6.1% |
| ATOM_SWAP | 10904 | 816 | 6 | 13.0% |
| ENSEMBLE | 762 | 67 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 6298 | 849 | 9 | 7.6% |
| EXIT_TRANSPLANT | 5955 | 777 | 11 | 7.6% |
| INVERT | 2151 | 93 | 0 | 3.3% |
| LIBRARY_PROBE | 16462 | 1050 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 10523 | 1925 | 1 | 20.5% |
| SIMPLIFY | 1462 | 218 | 0 | 5.9% |
| SLOT_CROSSOVER | 9053 | 1347 | 9 | 11.7% |
