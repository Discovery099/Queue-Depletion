# Epoch 31 report

- Generations completed: 15500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 15001 to 15500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 257, island B 252.
- Best composite score so far: A 0.5593, B 0.5468 (generation 15441).
- Honeypot genome voided: True. Ledger chain intact: True (187364 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 31100; effective independent trials (clustered): 18661.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1075 | 121 | 0 | 5.7% |
| ATOM_DROP | 296 | 39 | 0 | 5.9% |
| ATOM_SWAP | 2470 | 234 | 0 | 13.8% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 1271 | 163 | 0 | 7.8% |
| EXIT_TRANSPLANT | 1204 | 134 | 0 | 7.6% |
| INVERT | 483 | 15 | 0 | 3.3% |
| LIBRARY_PROBE | 4662 | 374 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 2075 | 366 | 0 | 20.9% |
| SIMPLIFY | 254 | 35 | 0 | 5.9% |
| SLOT_CROSSOVER | 1700 | 228 | 0 | 11.8% |
