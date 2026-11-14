# Epoch 125 report

- Generations completed: 62500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 62001 to 62500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 323, island B 311.
- Best composite score so far: A 0.7610, B 0.6892 (generation 62036).
- Honeypot genome voided: True. Ledger chain intact: True (753876 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 125086; effective independent trials (clustered): 75053.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4273 | 422 | 1 | 5.4% |
| ATOM_DROP | 1438 | 236 | 0 | 6.0% |
| ATOM_SWAP | 9818 | 736 | 5 | 13.0% |
| ENSEMBLE | 688 | 59 | 1 | 2.6% |
| ENTRY_TRANSPLANT | 5586 | 732 | 7 | 7.6% |
| EXIT_TRANSPLANT | 5342 | 666 | 10 | 7.5% |
| INVERT | 1917 | 79 | 0 | 3.3% |
| LIBRARY_PROBE | 14819 | 967 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 9370 | 1707 | 1 | 20.5% |
| SIMPLIFY | 1260 | 200 | 0 | 6.0% |
| SLOT_CROSSOVER | 7960 | 1166 | 9 | 11.7% |
