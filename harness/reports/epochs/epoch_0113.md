# Epoch 113 report

- Generations completed: 56500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 56001 to 56500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 315, island B 310.
- Best composite score so far: A 0.7610, B 0.6613 (generation 56366).
- Honeypot genome voided: True. Ledger chain intact: True (681684 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 113086; effective independent trials (clustered): 67853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3890 | 388 | 1 | 5.4% |
| ATOM_DROP | 1240 | 196 | 0 | 6.0% |
| ATOM_SWAP | 8914 | 665 | 3 | 13.0% |
| ENSEMBLE | 637 | 55 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 5008 | 647 | 6 | 7.6% |
| EXIT_TRANSPLANT | 4804 | 575 | 10 | 7.5% |
| INVERT | 1723 | 64 | 0 | 3.2% |
| LIBRARY_PROBE | 13553 | 904 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 8467 | 1528 | 1 | 20.5% |
| SIMPLIFY | 1103 | 177 | 0 | 6.0% |
| SLOT_CROSSOVER | 7132 | 1024 | 6 | 11.7% |
