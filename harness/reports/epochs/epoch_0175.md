# Epoch 175 report

- Generations completed: 87500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 87001 to 87500.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 327, island B 318.
- Best composite score so far: A 0.7640, B 0.7660 (generation 86275).
- Honeypot genome voided: True. Ledger chain intact: True (1054540 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 175086; effective independent trials (clustered): 105053.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 5851 | 573 | 1 | 5.4% |
| ATOM_DROP | 2228 | 415 | 1 | 6.2% |
| ATOM_SWAP | 13639 | 1010 | 9 | 12.9% |
| ENSEMBLE | 877 | 82 | 2 | 2.7% |
| ENTRY_TRANSPLANT | 7939 | 1090 | 13 | 7.6% |
| EXIT_TRANSPLANT | 7355 | 1026 | 19 | 7.7% |
| INVERT | 2674 | 132 | 0 | 3.3% |
| LIBRARY_PROBE | 20450 | 1245 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 13135 | 2370 | 1 | 20.4% |
| SIMPLIFY | 1885 | 269 | 0 | 5.8% |
| SLOT_CROSSOVER | 11438 | 1790 | 10 | 11.8% |
