# Epoch 124 report

- Generations completed: 62000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 61501 to 62000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 322, island B 311.
- Best composite score so far: A 0.7610, B 0.6891 (generation 61032).
- Honeypot genome voided: True. Ledger chain intact: True (747836 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 124086; effective independent trials (clustered): 74454.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4246 | 421 | 1 | 5.4% |
| ATOM_DROP | 1418 | 229 | 0 | 6.0% |
| ATOM_SWAP | 9750 | 733 | 5 | 13.0% |
| ENSEMBLE | 681 | 59 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 5551 | 729 | 7 | 7.6% |
| EXIT_TRANSPLANT | 5285 | 656 | 10 | 7.5% |
| INVERT | 1900 | 77 | 0 | 3.3% |
| LIBRARY_PROBE | 14694 | 962 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 9300 | 1697 | 1 | 20.5% |
| SIMPLIFY | 1249 | 196 | 0 | 5.9% |
| SLOT_CROSSOVER | 7897 | 1158 | 9 | 11.7% |
