# Epoch 197 report

- Generations completed: 98500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 98001 to 98500.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 327, island B 322.
- Best composite score so far: A 0.7640, B 0.7879 (generation 88594).
- Honeypot genome voided: True. Ledger chain intact: True (1186820 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 197086; effective independent trials (clustered): 118254.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 6563 | 643 | 1 | 5.4% |
| ATOM_DROP | 2602 | 488 | 1 | 6.2% |
| ATOM_SWAP | 15365 | 1110 | 10 | 12.8% |
| ENSEMBLE | 929 | 87 | 2 | 2.7% |
| ENTRY_TRANSPLANT | 8920 | 1243 | 16 | 7.7% |
| EXIT_TRANSPLANT | 8247 | 1198 | 22 | 7.7% |
| INVERT | 2995 | 146 | 0 | 3.3% |
| LIBRARY_PROBE | 22942 | 1374 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 12.9% |
| PARAM_STEP | 14780 | 2647 | 4 | 20.3% |
| SIMPLIFY | 2106 | 308 | 0 | 5.8% |
| SLOT_CROSSOVER | 13022 | 2063 | 10 | 11.8% |
