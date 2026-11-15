# Epoch 155 report

- Generations completed: 77500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 77001 to 77500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 326, island B 316.
- Best composite score so far: A 0.7610, B 0.7655 (generation 73770).
- Honeypot genome voided: True. Ledger chain intact: True (934236 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 155086; effective independent trials (clustered): 93053.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 5223 | 515 | 1 | 5.4% |
| ATOM_DROP | 1903 | 340 | 1 | 6.1% |
| ATOM_SWAP | 12071 | 897 | 8 | 12.9% |
| ENSEMBLE | 821 | 74 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 6987 | 955 | 9 | 7.6% |
| EXIT_TRANSPLANT | 6554 | 898 | 14 | 7.6% |
| INVERT | 2375 | 107 | 0 | 3.3% |
| LIBRARY_PROBE | 18137 | 1131 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 11641 | 2139 | 1 | 20.5% |
| SIMPLIFY | 1658 | 242 | 0 | 5.8% |
| SLOT_CROSSOVER | 10101 | 1542 | 9 | 11.7% |
