# Epoch 35 report

- Generations completed: 17500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 17001 to 17500.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 264, island B 265.
- Best composite score so far: A 0.6311, B 0.5468 (generation 17057).
- Honeypot genome voided: True. Ledger chain intact: True (211376 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 35100; effective independent trials (clustered): 21062.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1227 | 135 | 0 | 5.7% |
| ATOM_DROP | 323 | 45 | 0 | 5.9% |
| ATOM_SWAP | 2814 | 255 | 0 | 13.7% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 1448 | 184 | 0 | 7.8% |
| EXIT_TRANSPLANT | 1384 | 150 | 0 | 7.5% |
| INVERT | 539 | 17 | 0 | 3.3% |
| LIBRARY_PROBE | 5105 | 407 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 2421 | 424 | 0 | 20.9% |
| SIMPLIFY | 292 | 46 | 0 | 6.1% |
| SLOT_CROSSOVER | 1937 | 256 | 1 | 11.7% |
