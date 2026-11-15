# Epoch 143 report

- Generations completed: 71500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 71001 to 71500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 325, island B 315.
- Best composite score so far: A 0.7610, B 0.7245 (generation 70498).
- Honeypot genome voided: True. Ledger chain intact: True (862068 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 143086; effective independent trials (clustered): 64391.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4829 | 474 | 1 | 5.4% |
| ATOM_DROP | 1721 | 290 | 0 | 6.0% |
| ATOM_SWAP | 11115 | 825 | 6 | 12.9% |
| ENSEMBLE | 776 | 67 | 1 | 2.6% |
| ENTRY_TRANSPLANT | 6431 | 870 | 9 | 7.6% |
| EXIT_TRANSPLANT | 6077 | 799 | 13 | 7.6% |
| INVERT | 2207 | 95 | 0 | 3.3% |
| LIBRARY_PROBE | 16804 | 1063 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 10747 | 1963 | 1 | 20.5% |
| SIMPLIFY | 1506 | 223 | 0 | 5.8% |
| SLOT_CROSSOVER | 9258 | 1385 | 9 | 11.7% |
