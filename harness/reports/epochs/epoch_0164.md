# Epoch 164 report

- Generations completed: 82000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 81501 to 82000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 327, island B 318.
- Best composite score so far: A 0.7610, B 0.7660 (generation 80566).
- Honeypot genome voided: True. Ledger chain intact: True (988360 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 164086; effective independent trials (clustered): 98453.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 5501 | 543 | 1 | 5.4% |
| ATOM_DROP | 2068 | 373 | 1 | 6.1% |
| ATOM_SWAP | 12812 | 957 | 9 | 12.9% |
| ENSEMBLE | 849 | 76 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 7420 | 1021 | 10 | 7.6% |
| EXIT_TRANSPLANT | 6922 | 954 | 18 | 7.6% |
| INVERT | 2512 | 116 | 0 | 3.3% |
| LIBRARY_PROBE | 19153 | 1179 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 12292 | 2256 | 1 | 20.5% |
| SIMPLIFY | 1761 | 251 | 0 | 5.8% |
| SLOT_CROSSOVER | 10681 | 1648 | 10 | 11.8% |
