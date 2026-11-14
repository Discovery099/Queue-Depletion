# Epoch 110 report

- Generations completed: 55000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 54501 to 55000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 2 |
| STAGE1_FAIL | 498 |

- Stage 1 pass rate: 0.40%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 316, island B 310.
- Best composite score so far: A 0.7610, B 0.6280 (generation 53323).
- Honeypot genome voided: True. Ledger chain intact: True (663672 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 110086; effective independent trials (clustered): 66053.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3791 | 379 | 1 | 5.4% |
| ATOM_DROP | 1196 | 189 | 0 | 6.0% |
| ATOM_SWAP | 8692 | 648 | 3 | 13.0% |
| ENSEMBLE | 621 | 54 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 4877 | 631 | 6 | 7.6% |
| EXIT_TRANSPLANT | 4668 | 550 | 9 | 7.5% |
| INVERT | 1687 | 64 | 0 | 3.3% |
| LIBRARY_PROBE | 13215 | 887 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 8223 | 1477 | 1 | 20.5% |
| SIMPLIFY | 1072 | 171 | 0 | 6.0% |
| SLOT_CROSSOVER | 6929 | 995 | 6 | 11.7% |
