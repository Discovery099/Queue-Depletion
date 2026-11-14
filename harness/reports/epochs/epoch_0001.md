# Epoch 1 report

- Generations completed: 500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 1 to 500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 57, island B 58.
- Best composite score so far: A 0.3053, B 0.3267 (generation 100).
- Honeypot genome voided: True. Ledger chain intact: True (7216 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 1100; effective independent trials (clustered): 658.
- Hall of fame: {'bronze': 0, 'silver': 0, 'gold': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 10 | 2 | 0 | 5.8% |
| ATOM_DROP | 5 | 2 | 0 | 7.2% |
| ATOM_SWAP | 29 | 4 | 0 | 12.8% |
| ENSEMBLE | 0 | 0 | 0 | 3.9% |
| ENTRY_TRANSPLANT | 25 | 3 | 0 | 6.7% |
| EXIT_TRANSPLANT | 18 | 2 | 0 | 6.7% |
| INVERT | 8 | 1 | 0 | 3.6% |
| LIBRARY_PROBE | 384 | 29 | 0 | 3.0% |
| LLM_HYPOTHESIS | 0 | 0 | 0 | 10.3% |
| PARAM_STEP | 1 | 0 | 0 | 21.6% |
| SIMPLIFY | 0 | 0 | 0 | 7.8% |
| SLOT_CROSSOVER | 20 | 3 | 0 | 10.6% |
