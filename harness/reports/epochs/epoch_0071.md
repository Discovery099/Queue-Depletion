# Epoch 71 report

- Generations completed: 35500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 35001 to 35500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 289, island B 302.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (428516 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 71086; effective independent trials (clustered): 42653.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 2512 | 233 | 0 | 5.4% |
| ATOM_DROP | 703 | 101 | 0 | 5.9% |
| ATOM_SWAP | 5624 | 436 | 1 | 13.2% |
| ENSEMBLE | 377 | 27 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 3143 | 403 | 0 | 7.6% |
| EXIT_TRANSPLANT | 2992 | 334 | 2 | 7.4% |
| INVERT | 1077 | 36 | 0 | 3.2% |
| LIBRARY_PROBE | 8919 | 637 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 5210 | 901 | 0 | 20.5% |
| SIMPLIFY | 624 | 101 | 0 | 6.0% |
| SLOT_CROSSOVER | 4290 | 549 | 3 | 11.5% |
