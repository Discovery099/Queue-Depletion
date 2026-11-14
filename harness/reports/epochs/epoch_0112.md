# Epoch 112 report

- Generations completed: 56000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 55501 to 56000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 315, island B 310.
- Best composite score so far: A 0.7610, B 0.6430 (generation 55510).
- Honeypot genome voided: True. Ledger chain intact: True (675684 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 112086; effective independent trials (clustered): 67253.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3851 | 385 | 1 | 5.4% |
| ATOM_DROP | 1226 | 192 | 0 | 5.9% |
| ATOM_SWAP | 8838 | 662 | 3 | 13.0% |
| ENSEMBLE | 632 | 54 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 4963 | 643 | 6 | 7.6% |
| EXIT_TRANSPLANT | 4758 | 563 | 10 | 7.5% |
| INVERT | 1713 | 64 | 0 | 3.2% |
| LIBRARY_PROBE | 13440 | 899 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 8387 | 1514 | 1 | 20.5% |
| SIMPLIFY | 1095 | 176 | 0 | 6.0% |
| SLOT_CROSSOVER | 7068 | 1014 | 6 | 11.7% |
