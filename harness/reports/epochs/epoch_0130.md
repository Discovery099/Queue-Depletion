# Epoch 130 report

- Generations completed: 65000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 64501 to 65000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 324, island B 311.
- Best composite score so far: A 0.7610, B 0.6980 (generation 63398).
- Honeypot genome voided: True. Ledger chain intact: True (783928 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 130086; effective independent trials (clustered): 78053.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4428 | 436 | 1 | 5.4% |
| ATOM_DROP | 1537 | 254 | 0 | 6.0% |
| ATOM_SWAP | 10193 | 762 | 5 | 13.0% |
| ENSEMBLE | 712 | 63 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 5820 | 766 | 8 | 7.6% |
| EXIT_TRANSPLANT | 5550 | 704 | 10 | 7.5% |
| INVERT | 2003 | 81 | 0 | 3.3% |
| LIBRARY_PROBE | 15349 | 996 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 9738 | 1783 | 1 | 20.5% |
| SIMPLIFY | 1327 | 209 | 0 | 5.9% |
| SLOT_CROSSOVER | 8314 | 1228 | 9 | 11.7% |
