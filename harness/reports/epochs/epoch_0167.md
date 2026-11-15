# Epoch 167 report

- Generations completed: 83500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 83001 to 83500.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 327, island B 318.
- Best composite score so far: A 0.7610, B 0.7660 (generation 80566).
- Honeypot genome voided: True. Ledger chain intact: True (1006424 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 167086; effective independent trials (clustered): 100253.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 5609 | 551 | 1 | 5.4% |
| ATOM_DROP | 2115 | 390 | 1 | 6.2% |
| ATOM_SWAP | 13020 | 966 | 9 | 12.9% |
| ENSEMBLE | 858 | 76 | 2 | 2.6% |
| ENTRY_TRANSPLANT | 7565 | 1039 | 10 | 7.6% |
| EXIT_TRANSPLANT | 7058 | 983 | 19 | 7.7% |
| INVERT | 2553 | 117 | 0 | 3.3% |
| LIBRARY_PROBE | 19496 | 1194 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 12516 | 2285 | 1 | 20.5% |
| SIMPLIFY | 1797 | 258 | 0 | 5.8% |
| SLOT_CROSSOVER | 10884 | 1694 | 10 | 11.8% |
