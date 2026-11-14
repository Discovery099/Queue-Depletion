# Epoch 86 report

- Generations completed: 43000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 42501 to 43000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 301, island B 306.
- Best composite score so far: A 0.6785, B 0.5468 (generation 42505).
- Honeypot genome voided: True. Ledger chain intact: True (518684 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 86086; effective independent trials (clustered): 51653.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 2992 | 284 | 0 | 5.4% |
| ATOM_DROP | 856 | 128 | 0 | 5.9% |
| ATOM_SWAP | 6835 | 521 | 1 | 13.1% |
| ENSEMBLE | 476 | 35 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 3832 | 500 | 1 | 7.6% |
| EXIT_TRANSPLANT | 3659 | 408 | 3 | 7.4% |
| INVERT | 1311 | 51 | 0 | 3.3% |
| LIBRARY_PROBE | 10573 | 738 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 6319 | 1122 | 1 | 20.5% |
| SIMPLIFY | 806 | 126 | 0 | 6.0% |
| SLOT_CROSSOVER | 5312 | 717 | 4 | 11.6% |
