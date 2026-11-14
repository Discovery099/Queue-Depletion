# Epoch 118 report

- Generations completed: 59000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 58501 to 59000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 319, island B 311.
- Best composite score so far: A 0.7610, B 0.6853 (generation 58054).
- Honeypot genome voided: True. Ledger chain intact: True (711772 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 118086; effective independent trials (clustered): 70853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4065 | 403 | 1 | 5.4% |
| ATOM_DROP | 1329 | 210 | 0 | 6.0% |
| ATOM_SWAP | 9307 | 698 | 4 | 13.0% |
| ENSEMBLE | 657 | 57 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 5279 | 681 | 6 | 7.6% |
| EXIT_TRANSPLANT | 5036 | 619 | 10 | 7.5% |
| INVERT | 1807 | 71 | 0 | 3.3% |
| LIBRARY_PROBE | 14071 | 927 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 8806 | 1596 | 1 | 20.5% |
| SIMPLIFY | 1161 | 183 | 0 | 6.0% |
| SLOT_CROSSOVER | 7453 | 1083 | 9 | 11.7% |
