# Epoch 136 report

- Generations completed: 68000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 67501 to 68000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 323, island B 312.
- Best composite score so far: A 0.7610, B 0.7138 (generation 66118).
- Honeypot genome voided: True. Ledger chain intact: True (819980 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 136086; effective independent trials (clustered): 81653.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4608 | 455 | 1 | 5.4% |
| ATOM_DROP | 1617 | 277 | 0 | 6.1% |
| ATOM_SWAP | 10636 | 794 | 5 | 13.0% |
| ENSEMBLE | 743 | 65 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 6123 | 816 | 9 | 7.6% |
| EXIT_TRANSPLANT | 5789 | 749 | 10 | 7.6% |
| INVERT | 2096 | 91 | 0 | 3.3% |
| LIBRARY_PROBE | 16021 | 1029 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 10192 | 1859 | 1 | 20.5% |
| SIMPLIFY | 1415 | 215 | 0 | 5.9% |
| SLOT_CROSSOVER | 8731 | 1294 | 9 | 11.7% |
