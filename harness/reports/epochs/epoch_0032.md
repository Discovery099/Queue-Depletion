# Epoch 32 report

- Generations completed: 16000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 15501 to 16000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 258, island B 255.
- Best composite score so far: A 0.5974, B 0.5468 (generation 15525).
- Honeypot genome voided: True. Ledger chain intact: True (193364 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 32100; effective independent trials (clustered): 19262.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1119 | 122 | 0 | 5.6% |
| ATOM_DROP | 303 | 40 | 0 | 5.9% |
| ATOM_SWAP | 2562 | 238 | 0 | 13.7% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 1311 | 167 | 0 | 7.8% |
| EXIT_TRANSPLANT | 1251 | 139 | 0 | 7.6% |
| INVERT | 498 | 16 | 0 | 3.3% |
| LIBRARY_PROBE | 4772 | 378 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 2164 | 382 | 0 | 20.9% |
| SIMPLIFY | 265 | 37 | 0 | 6.0% |
| SLOT_CROSSOVER | 1745 | 236 | 0 | 11.8% |
