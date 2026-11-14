# Epoch 15 report

- Generations completed: 7500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 7001 to 7500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 200, island B 166.
- Best composite score so far: A 0.4434, B 0.5468 (generation 5480).
- Honeypot genome voided: True. Ledger chain intact: True (91228 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 15100; effective independent trials (clustered): 9063.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 459 | 62 | 0 | 5.9% |
| ATOM_DROP | 142 | 21 | 0 | 6.1% |
| ATOM_SWAP | 1104 | 99 | 0 | 13.7% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 584 | 79 | 0 | 7.9% |
| EXIT_TRANSPLANT | 521 | 61 | 0 | 7.7% |
| INVERT | 232 | 9 | 0 | 3.4% |
| LIBRARY_PROBE | 2891 | 234 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 763 | 110 | 0 | 20.0% |
| SIMPLIFY | 111 | 16 | 0 | 6.0% |
| SLOT_CROSSOVER | 683 | 92 | 0 | 11.8% |
