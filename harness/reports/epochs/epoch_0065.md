# Epoch 65 report

- Generations completed: 32500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 32001 to 32500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 288, island B 301.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (392462 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 65086; effective independent trials (clustered): 39053.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 2309 | 213 | 0 | 5.4% |
| ATOM_DROP | 625 | 93 | 0 | 5.9% |
| ATOM_SWAP | 5188 | 414 | 1 | 13.2% |
| ENSEMBLE | 310 | 23 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 2860 | 363 | 0 | 7.6% |
| EXIT_TRANSPLANT | 2744 | 302 | 1 | 7.4% |
| INVERT | 1002 | 30 | 0 | 3.2% |
| LIBRARY_PROBE | 8230 | 593 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 4726 | 811 | 0 | 20.4% |
| SIMPLIFY | 560 | 87 | 0 | 6.0% |
| SLOT_CROSSOVER | 3917 | 499 | 3 | 11.5% |
