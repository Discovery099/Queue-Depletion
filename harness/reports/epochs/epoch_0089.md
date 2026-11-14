# Epoch 89 report

- Generations completed: 44500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 44001 to 44500.

| Outcome | Count |
|---|---|
| HOME_ONLY | 3 |
| STAGE1_FAIL | 497 |

- Stage 1 pass rate: 0.60%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 305, island B 307.
- Best composite score so far: A 0.6862, B 0.5468 (generation 43033).
- Honeypot genome voided: True. Ledger chain intact: True (536720 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 89086; effective independent trials (clustered): 53453.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3086 | 292 | 1 | 5.4% |
| ATOM_DROP | 892 | 132 | 0 | 5.9% |
| ATOM_SWAP | 7072 | 542 | 1 | 13.1% |
| ENSEMBLE | 498 | 38 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 3964 | 518 | 2 | 7.6% |
| EXIT_TRANSPLANT | 3770 | 426 | 4 | 7.4% |
| INVERT | 1365 | 53 | 0 | 3.3% |
| LIBRARY_PROBE | 10903 | 761 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 6546 | 1163 | 1 | 20.5% |
| SIMPLIFY | 846 | 135 | 0 | 6.0% |
| SLOT_CROSSOVER | 5529 | 752 | 4 | 11.6% |
