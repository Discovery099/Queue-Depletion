# Epoch 23 report

- Generations completed: 11500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 11001 to 11500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 235, island B 216.
- Best composite score so far: A 0.5290, B 0.5468 (generation 8637).
- Honeypot genome voided: True. Ledger chain intact: True (139324 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 23100; effective independent trials (clustered): 13861.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 755 | 92 | 0 | 5.8% |
| ATOM_DROP | 224 | 31 | 0 | 5.9% |
| ATOM_SWAP | 1774 | 168 | 0 | 13.8% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 946 | 125 | 0 | 7.8% |
| EXIT_TRANSPLANT | 868 | 90 | 0 | 7.5% |
| INVERT | 357 | 11 | 0 | 3.3% |
| LIBRARY_PROBE | 3777 | 309 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 1422 | 244 | 0 | 20.7% |
| SIMPLIFY | 198 | 27 | 0 | 5.9% |
| SLOT_CROSSOVER | 1169 | 165 | 0 | 11.9% |
