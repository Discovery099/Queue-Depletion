# Epoch 91 report

- Generations completed: 45500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 45001 to 45500.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 310, island B 307.
- Best composite score so far: A 0.6862, B 0.5468 (generation 43033).
- Honeypot genome voided: True. Ledger chain intact: True (548772 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 91086; effective independent trials (clustered): 54653.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3140 | 300 | 1 | 5.4% |
| ATOM_DROP | 924 | 138 | 0 | 5.9% |
| ATOM_SWAP | 7235 | 552 | 1 | 13.1% |
| ENSEMBLE | 511 | 41 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 4053 | 528 | 2 | 7.6% |
| EXIT_TRANSPLANT | 3854 | 435 | 5 | 7.4% |
| INVERT | 1394 | 54 | 0 | 3.3% |
| LIBRARY_PROBE | 11106 | 777 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 6720 | 1195 | 1 | 20.5% |
| SIMPLIFY | 866 | 139 | 0 | 6.0% |
| SLOT_CROSSOVER | 5668 | 785 | 4 | 11.6% |
