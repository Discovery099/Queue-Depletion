# Epoch 198 report

- Generations completed: 99000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 98501 to 99000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 327, island B 322.
- Best composite score so far: A 0.7640, B 0.7879 (generation 88594).
- Honeypot genome voided: True. Ledger chain intact: True (1192820 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 198086; effective independent trials (clustered): 118853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 6589 | 646 | 1 | 5.4% |
| ATOM_DROP | 2616 | 488 | 1 | 6.2% |
| ATOM_SWAP | 15445 | 1114 | 10 | 12.8% |
| ENSEMBLE | 932 | 87 | 2 | 2.7% |
| ENTRY_TRANSPLANT | 8962 | 1251 | 16 | 7.7% |
| EXIT_TRANSPLANT | 8282 | 1209 | 22 | 7.7% |
| INVERT | 3017 | 147 | 0 | 3.3% |
| LIBRARY_PROBE | 23059 | 1381 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 12.9% |
| PARAM_STEP | 14856 | 2663 | 4 | 20.3% |
| SIMPLIFY | 2120 | 309 | 0 | 5.8% |
| SLOT_CROSSOVER | 13093 | 2071 | 10 | 11.8% |
