# Epoch 169 report

- Generations completed: 84500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 84001 to 84500.

| Outcome | Count |
|---|---|
| HOME_ONLY | 2 |
| STAGE1_FAIL | 498 |

- Stage 1 pass rate: 0.40%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 327, island B 318.
- Best composite score so far: A 0.7610, B 0.7660 (generation 80566).
- Honeypot genome voided: True. Ledger chain intact: True (1018448 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 169086; effective independent trials (clustered): 101453.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 5662 | 555 | 1 | 5.4% |
| ATOM_DROP | 2148 | 401 | 1 | 6.2% |
| ATOM_SWAP | 13170 | 976 | 9 | 12.9% |
| ENSEMBLE | 863 | 78 | 2 | 2.7% |
| ENTRY_TRANSPLANT | 7664 | 1051 | 12 | 7.6% |
| EXIT_TRANSPLANT | 7138 | 993 | 19 | 7.7% |
| INVERT | 2583 | 120 | 0 | 3.3% |
| LIBRARY_PROBE | 19732 | 1207 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 12658 | 2305 | 1 | 20.4% |
| SIMPLIFY | 1820 | 259 | 0 | 5.8% |
| SLOT_CROSSOVER | 11033 | 1718 | 10 | 11.8% |
