# Epoch 161 report

- Generations completed: 80500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 80001 to 80500.

| Outcome | Count |
|---|---|
| HOME_ONLY | 3 |
| STAGE1_FAIL | 497 |

- Stage 1 pass rate: 0.60%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 326, island B 318.
- Best composite score so far: A 0.7610, B 0.7655 (generation 73770).
- Honeypot genome voided: True. Ledger chain intact: True (970348 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 161086; effective independent trials (clustered): 96654.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 5394 | 528 | 1 | 5.4% |
| ATOM_DROP | 2012 | 365 | 1 | 6.1% |
| ATOM_SWAP | 12551 | 939 | 9 | 12.9% |
| ENSEMBLE | 838 | 75 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 7281 | 1003 | 10 | 7.6% |
| EXIT_TRANSPLANT | 6803 | 938 | 17 | 7.6% |
| INVERT | 2474 | 113 | 0 | 3.3% |
| LIBRARY_PROBE | 18816 | 1164 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 12080 | 2224 | 1 | 20.5% |
| SIMPLIFY | 1730 | 248 | 0 | 5.8% |
| SLOT_CROSSOVER | 10492 | 1616 | 10 | 11.8% |
