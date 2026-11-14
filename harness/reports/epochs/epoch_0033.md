# Epoch 33 report

- Generations completed: 16500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 16001 to 16500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 261, island B 260.
- Best composite score so far: A 0.5974, B 0.5468 (generation 15525).
- Honeypot genome voided: True. Ledger chain intact: True (199364 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 33100; effective independent trials (clustered): 19862.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1161 | 127 | 0 | 5.6% |
| ATOM_DROP | 311 | 41 | 0 | 5.9% |
| ATOM_SWAP | 2653 | 245 | 0 | 13.7% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 1353 | 172 | 0 | 7.8% |
| EXIT_TRANSPLANT | 1288 | 141 | 0 | 7.5% |
| INVERT | 513 | 16 | 0 | 3.3% |
| LIBRARY_PROBE | 4882 | 388 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 2248 | 403 | 0 | 21.0% |
| SIMPLIFY | 273 | 40 | 0 | 6.0% |
| SLOT_CROSSOVER | 1808 | 240 | 0 | 11.7% |
