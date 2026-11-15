# Epoch 186 report

- Generations completed: 93000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 92501 to 93000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 326, island B 320.
- Best composite score so far: A 0.7640, B 0.7879 (generation 88594).
- Honeypot genome voided: True. Ledger chain intact: True (1120656 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 186086; effective independent trials (clustered): 111653.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 6233 | 612 | 1 | 5.4% |
| ATOM_DROP | 2432 | 459 | 1 | 6.2% |
| ATOM_SWAP | 14528 | 1053 | 10 | 12.9% |
| ENSEMBLE | 909 | 84 | 2 | 2.7% |
| ENTRY_TRANSPLANT | 8416 | 1163 | 13 | 7.6% |
| EXIT_TRANSPLANT | 7811 | 1123 | 20 | 7.7% |
| INVERT | 2843 | 138 | 0 | 3.3% |
| LIBRARY_PROBE | 21698 | 1310 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 12.9% |
| PARAM_STEP | 13923 | 2493 | 2 | 20.3% |
| SIMPLIFY | 1984 | 284 | 0 | 5.8% |
| SLOT_CROSSOVER | 12194 | 1927 | 10 | 11.8% |
