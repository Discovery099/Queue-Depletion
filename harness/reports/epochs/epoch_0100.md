# Epoch 100 report

- Generations completed: 50000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 49501 to 50000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 3 |
| STAGE1_FAIL | 497 |

- Stage 1 pass rate: 0.60%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 314, island B 308.
- Best composite score so far: A 0.7338, B 0.5741 (generation 48034).
- Honeypot genome voided: True. Ledger chain intact: True (602924 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 100086; effective independent trials (clustered): 60053.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3462 | 338 | 1 | 5.4% |
| ATOM_DROP | 1058 | 163 | 0 | 5.9% |
| ATOM_SWAP | 7924 | 593 | 1 | 13.0% |
| ENSEMBLE | 563 | 51 | 0 | 2.7% |
| ENTRY_TRANSPLANT | 4418 | 571 | 5 | 7.6% |
| EXIT_TRANSPLANT | 4244 | 477 | 8 | 7.4% |
| INVERT | 1529 | 57 | 0 | 3.3% |
| LIBRARY_PROBE | 12120 | 825 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 7411 | 1324 | 1 | 20.5% |
| SIMPLIFY | 971 | 155 | 0 | 6.0% |
| SLOT_CROSSOVER | 6271 | 878 | 4 | 11.6% |
