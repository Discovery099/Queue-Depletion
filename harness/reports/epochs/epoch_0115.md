# Epoch 115 report

- Generations completed: 57500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 57001 to 57500.

| Outcome | Count |
|---|---|
| HOME_ONLY | 2 |
| STAGE1_FAIL | 498 |

- Stage 1 pass rate: 0.40%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 316, island B 311.
- Best composite score so far: A 0.7610, B 0.6785 (generation 57412).
- Honeypot genome voided: True. Ledger chain intact: True (693760 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 115086; effective independent trials (clustered): 69053.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3973 | 395 | 1 | 5.4% |
| ATOM_DROP | 1273 | 199 | 0 | 5.9% |
| ATOM_SWAP | 9084 | 677 | 4 | 13.0% |
| ENSEMBLE | 644 | 57 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 5098 | 653 | 6 | 7.6% |
| EXIT_TRANSPLANT | 4906 | 597 | 10 | 7.5% |
| INVERT | 1755 | 66 | 0 | 3.2% |
| LIBRARY_PROBE | 13751 | 914 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 8601 | 1556 | 1 | 20.5% |
| SIMPLIFY | 1122 | 179 | 0 | 6.0% |
| SLOT_CROSSOVER | 7264 | 1043 | 8 | 11.7% |
