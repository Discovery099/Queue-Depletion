# Epoch 51 report

- Generations completed: 25500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 25001 to 25500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 278, island B 289.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (307750 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 51086; effective independent trials (clustered): 30653.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1830 | 168 | 0 | 5.5% |
| ATOM_DROP | 484 | 66 | 0 | 5.9% |
| ATOM_SWAP | 4102 | 337 | 0 | 13.6% |
| ENSEMBLE | 152 | 12 | 0 | 2.7% |
| ENTRY_TRANSPLANT | 2211 | 273 | 0 | 7.7% |
| EXIT_TRANSPLANT | 2112 | 229 | 0 | 7.6% |
| INVERT | 787 | 24 | 0 | 3.3% |
| LIBRARY_PROBE | 6747 | 505 | 0 | 3.6% |
| LLM_HYPOTHESIS | 19 | 8 | 0 | 11.5% |
| PARAM_STEP | 3653 | 619 | 0 | 20.8% |
| SIMPLIFY | 419 | 62 | 0 | 6.0% |
| SLOT_CROSSOVER | 2984 | 387 | 2 | 11.7% |
