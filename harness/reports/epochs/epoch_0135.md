# Epoch 135 report

- Generations completed: 67500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 67001 to 67500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 325, island B 312.
- Best composite score so far: A 0.7610, B 0.7138 (generation 66118).
- Honeypot genome voided: True. Ledger chain intact: True (813980 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 135086; effective independent trials (clustered): 81052.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4576 | 452 | 1 | 5.4% |
| ATOM_DROP | 1600 | 270 | 0 | 6.0% |
| ATOM_SWAP | 10558 | 789 | 5 | 13.0% |
| ENSEMBLE | 742 | 64 | 1 | 2.6% |
| ENTRY_TRANSPLANT | 6070 | 805 | 9 | 7.6% |
| EXIT_TRANSPLANT | 5750 | 740 | 10 | 7.6% |
| INVERT | 2080 | 87 | 0 | 3.3% |
| LIBRARY_PROBE | 15924 | 1026 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 10120 | 1848 | 1 | 20.5% |
| SIMPLIFY | 1398 | 214 | 0 | 5.9% |
| SLOT_CROSSOVER | 8653 | 1281 | 9 | 11.7% |
