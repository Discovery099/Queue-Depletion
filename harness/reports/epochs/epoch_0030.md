# Epoch 30 report

- Generations completed: 15000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 14501 to 15000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 257, island B 246.
- Best composite score so far: A 0.5347, B 0.5468 (generation 14703).
- Honeypot genome voided: True. Ledger chain intact: True (181324 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 30100; effective independent trials (clustered): 18061.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1036 | 116 | 0 | 5.7% |
| ATOM_DROP | 288 | 37 | 0 | 5.9% |
| ATOM_SWAP | 2379 | 226 | 0 | 13.8% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 1238 | 161 | 0 | 7.8% |
| EXIT_TRANSPLANT | 1162 | 127 | 0 | 7.5% |
| INVERT | 459 | 14 | 0 | 3.3% |
| LIBRARY_PROBE | 4555 | 366 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 1996 | 349 | 0 | 20.9% |
| SIMPLIFY | 248 | 32 | 0 | 5.9% |
| SLOT_CROSSOVER | 1629 | 222 | 0 | 11.8% |
