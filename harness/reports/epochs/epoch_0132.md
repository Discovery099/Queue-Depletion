# Epoch 132 report

- Generations completed: 66000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 65501 to 66000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 324, island B 311.
- Best composite score so far: A 0.7610, B 0.6980 (generation 63398).
- Honeypot genome voided: True. Ledger chain intact: True (795940 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 132086; effective independent trials (clustered): 79252.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4490 | 446 | 1 | 5.4% |
| ATOM_DROP | 1560 | 259 | 0 | 6.0% |
| ATOM_SWAP | 10326 | 772 | 5 | 13.0% |
| ENSEMBLE | 729 | 63 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 5918 | 784 | 9 | 7.6% |
| EXIT_TRANSPLANT | 5631 | 717 | 10 | 7.5% |
| INVERT | 2043 | 83 | 0 | 3.3% |
| LIBRARY_PROBE | 15586 | 1007 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 9891 | 1812 | 1 | 20.5% |
| SIMPLIFY | 1357 | 211 | 0 | 5.9% |
| SLOT_CROSSOVER | 8440 | 1247 | 9 | 11.7% |
