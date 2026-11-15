# Epoch 144 report

- Generations completed: 72000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 71501 to 72000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 325, island B 316.
- Best composite score so far: A 0.7610, B 0.7245 (generation 70498).
- Honeypot genome voided: True. Ledger chain intact: True (868068 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 144086; effective independent trials (clustered): 86452.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4852 | 475 | 1 | 5.4% |
| ATOM_DROP | 1742 | 300 | 0 | 6.1% |
| ATOM_SWAP | 11202 | 833 | 6 | 12.9% |
| ENSEMBLE | 780 | 70 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 6479 | 876 | 9 | 7.6% |
| EXIT_TRANSPLANT | 6111 | 806 | 13 | 7.6% |
| INVERT | 2222 | 96 | 0 | 3.3% |
| LIBRARY_PROBE | 16912 | 1070 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 10822 | 1972 | 1 | 20.5% |
| SIMPLIFY | 1520 | 224 | 0 | 5.8% |
| SLOT_CROSSOVER | 9329 | 1396 | 9 | 11.7% |
