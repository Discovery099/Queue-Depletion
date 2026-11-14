# Epoch 127 report

- Generations completed: 63500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 63001 to 63500.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 323, island B 311.
- Best composite score so far: A 0.7610, B 0.6980 (generation 63398).
- Honeypot genome voided: True. Ledger chain intact: True (765888 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 127086; effective independent trials (clustered): 76252.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4341 | 427 | 1 | 5.4% |
| ATOM_DROP | 1469 | 240 | 0 | 6.0% |
| ATOM_SWAP | 9972 | 745 | 5 | 13.0% |
| ENSEMBLE | 699 | 60 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 5674 | 741 | 8 | 7.6% |
| EXIT_TRANSPLANT | 5434 | 687 | 10 | 7.5% |
| INVERT | 1943 | 80 | 0 | 3.3% |
| LIBRARY_PROBE | 15022 | 979 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 9532 | 1737 | 1 | 20.5% |
| SIMPLIFY | 1287 | 203 | 0 | 5.9% |
| SLOT_CROSSOVER | 8098 | 1194 | 9 | 11.7% |
