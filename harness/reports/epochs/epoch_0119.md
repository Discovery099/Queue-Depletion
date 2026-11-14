# Epoch 119 report

- Generations completed: 59500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 59001 to 59500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 319, island B 311.
- Best composite score so far: A 0.7610, B 0.6853 (generation 58054).
- Honeypot genome voided: True. Ledger chain intact: True (717772 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 119086; effective independent trials (clustered): 71454.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4090 | 407 | 1 | 5.4% |
| ATOM_DROP | 1340 | 210 | 0 | 5.9% |
| ATOM_SWAP | 9394 | 703 | 4 | 13.0% |
| ENSEMBLE | 660 | 57 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 5326 | 689 | 6 | 7.6% |
| EXIT_TRANSPLANT | 5068 | 627 | 10 | 7.5% |
| INVERT | 1826 | 73 | 0 | 3.3% |
| LIBRARY_PROBE | 14180 | 930 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 8893 | 1616 | 1 | 20.6% |
| SIMPLIFY | 1174 | 185 | 0 | 6.0% |
| SLOT_CROSSOVER | 7520 | 1091 | 9 | 11.7% |
