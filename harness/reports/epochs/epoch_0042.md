# Epoch 42 report

- Generations completed: 21000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 20501 to 21000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 270, island B 285.
- Best composite score so far: A 0.6363, B 0.5468 (generation 18133).
- Honeypot genome voided: True. Ledger chain intact: True (253658 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 42086; effective independent trials (clustered): 25253.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1483 | 149 | 0 | 5.6% |
| ATOM_DROP | 395 | 57 | 0 | 6.0% |
| ATOM_SWAP | 3380 | 284 | 0 | 13.5% |
| ENSEMBLE | 29 | 1 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 1780 | 223 | 0 | 7.7% |
| EXIT_TRANSPLANT | 1717 | 192 | 0 | 7.6% |
| INVERT | 643 | 21 | 0 | 3.3% |
| LIBRARY_PROBE | 5835 | 455 | 0 | 3.6% |
| LLM_HYPOTHESIS | 19 | 8 | 0 | 11.5% |
| PARAM_STEP | 2964 | 528 | 0 | 21.0% |
| SIMPLIFY | 358 | 55 | 0 | 6.1% |
| SLOT_CROSSOVER | 2397 | 305 | 1 | 11.6% |
