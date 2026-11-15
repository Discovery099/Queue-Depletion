# Epoch 154 report

- Generations completed: 77000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 76501 to 77000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 326, island B 316.
- Best composite score so far: A 0.7610, B 0.7655 (generation 73770).
- Honeypot genome voided: True. Ledger chain intact: True (928196 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 154086; effective independent trials (clustered): 92453.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 5185 | 511 | 1 | 5.4% |
| ATOM_DROP | 1887 | 335 | 1 | 6.1% |
| ATOM_SWAP | 11995 | 891 | 8 | 12.9% |
| ENSEMBLE | 817 | 72 | 1 | 2.6% |
| ENTRY_TRANSPLANT | 6940 | 948 | 9 | 7.6% |
| EXIT_TRANSPLANT | 6519 | 894 | 14 | 7.6% |
| INVERT | 2360 | 107 | 0 | 3.3% |
| LIBRARY_PROBE | 18041 | 1127 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 11571 | 2128 | 1 | 20.5% |
| SIMPLIFY | 1645 | 241 | 0 | 5.8% |
| SLOT_CROSSOVER | 10011 | 1522 | 9 | 11.7% |
