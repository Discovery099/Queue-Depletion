# Epoch 3 report

- Generations completed: 1500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 1001 to 1500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 67, island B 77.
- Best composite score so far: A 0.4187, B 0.3441 (generation 1040).
- Honeypot genome voided: True. Ledger chain intact: True (19216 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 3100; effective independent trials (clustered): 1860.
- Hall of fame: {'bronze': 0, 'silver': 0, 'gold': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 25 | 4 | 0 | 6.0% |
| ATOM_DROP | 13 | 3 | 0 | 6.7% |
| ATOM_SWAP | 95 | 11 | 0 | 13.7% |
| ENSEMBLE | 0 | 0 | 0 | 4.4% |
| ENTRY_TRANSPLANT | 56 | 6 | 0 | 7.3% |
| EXIT_TRANSPLANT | 47 | 8 | 0 | 8.0% |
| INVERT | 25 | 2 | 0 | 3.6% |
| LIBRARY_PROBE | 1158 | 95 | 0 | 3.4% |
| LLM_HYPOTHESIS | 0 | 0 | 0 | 11.7% |
| PARAM_STEP | 5 | 0 | 0 | 18.8% |
| SIMPLIFY | 13 | 1 | 0 | 5.6% |
| SLOT_CROSSOVER | 63 | 7 | 0 | 10.9% |
