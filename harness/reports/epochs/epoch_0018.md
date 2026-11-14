# Epoch 18 report

- Generations completed: 9000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 8501 to 9000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 214, island B 184.
- Best composite score so far: A 0.5290, B 0.5468 (generation 8637).
- Honeypot genome voided: True. Ledger chain intact: True (109324 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 18100; effective independent trials (clustered): 10862.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 567 | 76 | 0 | 5.9% |
| ATOM_DROP | 177 | 25 | 0 | 6.0% |
| ATOM_SWAP | 1356 | 131 | 0 | 13.8% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 731 | 97 | 0 | 7.8% |
| EXIT_TRANSPLANT | 644 | 71 | 0 | 7.5% |
| INVERT | 279 | 10 | 0 | 3.3% |
| LIBRARY_PROBE | 3198 | 258 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 1025 | 160 | 0 | 20.3% |
| SIMPLIFY | 139 | 21 | 0 | 6.1% |
| SLOT_CROSSOVER | 874 | 121 | 0 | 11.8% |
