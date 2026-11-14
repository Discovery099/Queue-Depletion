# Epoch 106 report

- Generations completed: 53000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 52501 to 53000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 316, island B 309.
- Best composite score so far: A 0.7338, B 0.6280 (generation 52964).
- Honeypot genome voided: True. Ledger chain intact: True (639596 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 106086; effective independent trials (clustered): 63653.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3672 | 356 | 1 | 5.4% |
| ATOM_DROP | 1141 | 176 | 0 | 5.9% |
| ATOM_SWAP | 8399 | 629 | 1 | 13.0% |
| ENSEMBLE | 598 | 53 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 4708 | 602 | 6 | 7.6% |
| EXIT_TRANSPLANT | 4496 | 521 | 9 | 7.4% |
| INVERT | 1630 | 63 | 0 | 3.3% |
| LIBRARY_PROBE | 12763 | 863 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 7876 | 1413 | 1 | 20.5% |
| SIMPLIFY | 1027 | 163 | 0 | 6.0% |
| SLOT_CROSSOVER | 6661 | 948 | 5 | 11.6% |
