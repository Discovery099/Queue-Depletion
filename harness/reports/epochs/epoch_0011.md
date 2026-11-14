# Epoch 11 report

- Generations completed: 5500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 5001 to 5500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 168, island B 136.
- Best composite score so far: A 0.4434, B 0.5468 (generation 5480).
- Honeypot genome voided: True. Ledger chain intact: True (67228 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 11100; effective independent trials (clustered): 6660.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 333 | 50 | 0 | 6.0% |
| ATOM_DROP | 89 | 15 | 0 | 6.2% |
| ATOM_SWAP | 734 | 68 | 0 | 13.7% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 408 | 55 | 0 | 7.8% |
| EXIT_TRANSPLANT | 362 | 45 | 0 | 7.7% |
| INVERT | 146 | 6 | 0 | 3.4% |
| LIBRARY_PROBE | 2431 | 202 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.2% |
| PARAM_STEP | 453 | 66 | 0 | 19.9% |
| SIMPLIFY | 76 | 11 | 0 | 6.0% |
| SLOT_CROSSOVER | 458 | 59 | 0 | 11.7% |
