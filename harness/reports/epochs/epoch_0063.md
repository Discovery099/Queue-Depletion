# Epoch 63 report

- Generations completed: 31500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 31001 to 31500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 287, island B 299.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (380410 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 63086; effective independent trials (clustered): 37853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 2245 | 203 | 0 | 5.4% |
| ATOM_DROP | 601 | 89 | 0 | 5.9% |
| ATOM_SWAP | 5050 | 400 | 1 | 13.2% |
| ENSEMBLE | 297 | 22 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 2777 | 345 | 0 | 7.6% |
| EXIT_TRANSPLANT | 2650 | 294 | 1 | 7.4% |
| INVERT | 972 | 30 | 0 | 3.2% |
| LIBRARY_PROBE | 7991 | 580 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.2% |
| PARAM_STEP | 4578 | 785 | 0 | 20.4% |
| SIMPLIFY | 537 | 84 | 0 | 6.0% |
| SLOT_CROSSOVER | 3773 | 482 | 2 | 11.5% |
