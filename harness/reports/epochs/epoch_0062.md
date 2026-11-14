# Epoch 62 report

- Generations completed: 31000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 30501 to 31000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 287, island B 299.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (374410 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 62086; effective independent trials (clustered): 37254.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 2216 | 201 | 0 | 5.4% |
| ATOM_DROP | 588 | 86 | 0 | 5.9% |
| ATOM_SWAP | 4980 | 396 | 1 | 13.2% |
| ENSEMBLE | 282 | 21 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 2725 | 338 | 0 | 7.6% |
| EXIT_TRANSPLANT | 2612 | 286 | 1 | 7.4% |
| INVERT | 954 | 29 | 0 | 3.2% |
| LIBRARY_PROBE | 7879 | 573 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.2% |
| PARAM_STEP | 4494 | 769 | 0 | 20.4% |
| SIMPLIFY | 532 | 83 | 0 | 6.0% |
| SLOT_CROSSOVER | 3709 | 475 | 2 | 11.5% |
