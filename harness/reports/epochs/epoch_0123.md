# Epoch 123 report

- Generations completed: 61500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 61001 to 61500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 321, island B 311.
- Best composite score so far: A 0.7610, B 0.6891 (generation 61032).
- Honeypot genome voided: True. Ledger chain intact: True (741824 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 123086; effective independent trials (clustered): 73853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4222 | 419 | 1 | 5.4% |
| ATOM_DROP | 1404 | 225 | 0 | 6.0% |
| ATOM_SWAP | 9687 | 733 | 5 | 13.0% |
| ENSEMBLE | 678 | 59 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 5497 | 719 | 6 | 7.6% |
| EXIT_TRANSPLANT | 5242 | 650 | 10 | 7.5% |
| INVERT | 1881 | 75 | 0 | 3.3% |
| LIBRARY_PROBE | 14594 | 957 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 9215 | 1685 | 1 | 20.6% |
| SIMPLIFY | 1239 | 195 | 0 | 5.9% |
| SLOT_CROSSOVER | 7812 | 1141 | 9 | 11.7% |
