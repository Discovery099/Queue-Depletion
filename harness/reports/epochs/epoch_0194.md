# Epoch 194 report

- Generations completed: 97000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 96501 to 97000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 327, island B 322.
- Best composite score so far: A 0.7640, B 0.7879 (generation 88594).
- Honeypot genome voided: True. Ledger chain intact: True (1168768 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 194086; effective independent trials (clustered): 116453.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 6480 | 637 | 1 | 5.4% |
| ATOM_DROP | 2556 | 482 | 1 | 6.2% |
| ATOM_SWAP | 15138 | 1093 | 10 | 12.9% |
| ENSEMBLE | 922 | 86 | 2 | 2.7% |
| ENTRY_TRANSPLANT | 8788 | 1218 | 15 | 7.6% |
| EXIT_TRANSPLANT | 8114 | 1172 | 22 | 7.7% |
| INVERT | 2958 | 146 | 0 | 3.3% |
| LIBRARY_PROBE | 22588 | 1355 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 12.9% |
| PARAM_STEP | 14545 | 2604 | 4 | 20.3% |
| SIMPLIFY | 2073 | 302 | 0 | 5.8% |
| SLOT_CROSSOVER | 12809 | 2030 | 10 | 11.8% |
