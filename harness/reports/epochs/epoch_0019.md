# Epoch 19 report

- Generations completed: 9500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 9001 to 9500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 221, island B 193.
- Best composite score so far: A 0.5290, B 0.5468 (generation 8637).
- Honeypot genome voided: True. Ledger chain intact: True (115324 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 19100; effective independent trials (clustered): 11462.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 608 | 82 | 0 | 5.9% |
| ATOM_DROP | 190 | 26 | 0 | 5.9% |
| ATOM_SWAP | 1426 | 138 | 0 | 13.8% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 771 | 100 | 0 | 7.8% |
| EXIT_TRANSPLANT | 687 | 74 | 0 | 7.5% |
| INVERT | 297 | 11 | 0 | 3.3% |
| LIBRARY_PROBE | 3308 | 269 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 1109 | 180 | 0 | 20.5% |
| SIMPLIFY | 158 | 21 | 0 | 5.9% |
| SLOT_CROSSOVER | 936 | 130 | 0 | 11.8% |
