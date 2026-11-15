# Epoch 173 report

- Generations completed: 86500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 86001 to 86500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 327, island B 318.
- Best composite score so far: A 0.7640, B 0.7660 (generation 86275).
- Honeypot genome voided: True. Ledger chain intact: True (1042488 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 173086; effective independent trials (clustered): 103852.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 5782 | 566 | 1 | 5.4% |
| ATOM_DROP | 2206 | 413 | 1 | 6.2% |
| ATOM_SWAP | 13471 | 997 | 9 | 12.9% |
| ENSEMBLE | 875 | 82 | 2 | 2.7% |
| ENTRY_TRANSPLANT | 7854 | 1083 | 12 | 7.6% |
| EXIT_TRANSPLANT | 7287 | 1016 | 19 | 7.7% |
| INVERT | 2640 | 123 | 0 | 3.3% |
| LIBRARY_PROBE | 20219 | 1238 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 12981 | 2348 | 1 | 20.4% |
| SIMPLIFY | 1864 | 264 | 0 | 5.8% |
| SLOT_CROSSOVER | 11292 | 1765 | 10 | 11.8% |
