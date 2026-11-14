# Epoch 17 report

- Generations completed: 8500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 8001 to 8500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 210, island B 178.
- Best composite score so far: A 0.5158, B 0.5468 (generation 8403).
- Honeypot genome voided: True. Ledger chain intact: True (103324 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 17100; effective independent trials (clustered): 10261.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 531 | 71 | 0 | 5.9% |
| ATOM_DROP | 161 | 21 | 0 | 5.9% |
| ATOM_SWAP | 1277 | 121 | 0 | 13.8% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 678 | 90 | 0 | 7.8% |
| EXIT_TRANSPLANT | 599 | 67 | 0 | 7.6% |
| INVERT | 264 | 10 | 0 | 3.3% |
| LIBRARY_PROBE | 3093 | 251 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 948 | 144 | 0 | 20.2% |
| SIMPLIFY | 128 | 20 | 0 | 6.1% |
| SLOT_CROSSOVER | 811 | 111 | 0 | 11.8% |
