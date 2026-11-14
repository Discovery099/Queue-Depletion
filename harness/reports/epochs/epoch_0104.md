# Epoch 104 report

- Generations completed: 52000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 51501 to 52000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 315, island B 309.
- Best composite score so far: A 0.7338, B 0.5931 (generation 51720).
- Honeypot genome voided: True. Ledger chain intact: True (627532 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 104086; effective independent trials (clustered): 62452.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3601 | 349 | 1 | 5.4% |
| ATOM_DROP | 1110 | 166 | 0 | 5.9% |
| ATOM_SWAP | 8242 | 614 | 1 | 13.0% |
| ENSEMBLE | 585 | 52 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 4617 | 592 | 6 | 7.6% |
| EXIT_TRANSPLANT | 4416 | 511 | 8 | 7.4% |
| INVERT | 1589 | 59 | 0 | 3.3% |
| LIBRARY_PROBE | 12538 | 848 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 7726 | 1383 | 1 | 20.5% |
| SIMPLIFY | 1006 | 162 | 0 | 6.0% |
| SLOT_CROSSOVER | 6541 | 935 | 4 | 11.7% |
