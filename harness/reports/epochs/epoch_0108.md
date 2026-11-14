# Epoch 108 report

- Generations completed: 54000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 53501 to 54000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 316, island B 310.
- Best composite score so far: A 0.7610, B 0.6280 (generation 53323).
- Honeypot genome voided: True. Ledger chain intact: True (651608 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 108086; effective independent trials (clustered): 64853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3734 | 371 | 1 | 5.4% |
| ATOM_DROP | 1168 | 187 | 0 | 6.0% |
| ATOM_SWAP | 8552 | 637 | 1 | 13.0% |
| ENSEMBLE | 605 | 53 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 4795 | 620 | 6 | 7.6% |
| EXIT_TRANSPLANT | 4584 | 533 | 9 | 7.4% |
| INVERT | 1656 | 63 | 0 | 3.3% |
| LIBRARY_PROBE | 12984 | 877 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 8043 | 1443 | 1 | 20.5% |
| SIMPLIFY | 1053 | 168 | 0 | 6.0% |
| SLOT_CROSSOVER | 6797 | 977 | 6 | 11.7% |
