# Epoch 193 report

- Generations completed: 96500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 96001 to 96500.

| Outcome | Count |
|---|---|
| HOME_ONLY | 2 |
| STAGE1_FAIL | 498 |

- Stage 1 pass rate: 0.40%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 327, island B 322.
- Best composite score so far: A 0.7640, B 0.7879 (generation 88594).
- Honeypot genome voided: True. Ledger chain intact: True (1162768 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 193086; effective independent trials (clustered): 115853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 6447 | 634 | 1 | 5.4% |
| ATOM_DROP | 2543 | 479 | 1 | 6.2% |
| ATOM_SWAP | 15061 | 1085 | 10 | 12.8% |
| ENSEMBLE | 920 | 86 | 2 | 2.7% |
| ENTRY_TRANSPLANT | 8733 | 1210 | 15 | 7.6% |
| EXIT_TRANSPLANT | 8076 | 1162 | 22 | 7.7% |
| INVERT | 2948 | 146 | 0 | 3.3% |
| LIBRARY_PROBE | 22466 | 1351 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 12.9% |
| PARAM_STEP | 14483 | 2597 | 4 | 20.3% |
| SIMPLIFY | 2064 | 301 | 0 | 5.8% |
| SLOT_CROSSOVER | 12730 | 2019 | 10 | 11.8% |
