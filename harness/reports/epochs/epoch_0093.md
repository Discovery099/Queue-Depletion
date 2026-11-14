# Epoch 93 report

- Generations completed: 46500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 46001 to 46500.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 311, island B 307.
- Best composite score so far: A 0.7050, B 0.5468 (generation 45871).
- Honeypot genome voided: True. Ledger chain intact: True (560784 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 93086; effective independent trials (clustered): 55853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3207 | 306 | 1 | 5.4% |
| ATOM_DROP | 943 | 144 | 0 | 5.9% |
| ATOM_SWAP | 7394 | 561 | 1 | 13.1% |
| ENSEMBLE | 524 | 44 | 0 | 2.7% |
| ENTRY_TRANSPLANT | 4130 | 534 | 3 | 7.6% |
| EXIT_TRANSPLANT | 3957 | 447 | 5 | 7.4% |
| INVERT | 1417 | 55 | 0 | 3.3% |
| LIBRARY_PROBE | 11348 | 790 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 6859 | 1221 | 1 | 20.5% |
| SIMPLIFY | 893 | 143 | 0 | 6.0% |
| SLOT_CROSSOVER | 5799 | 807 | 4 | 11.6% |
