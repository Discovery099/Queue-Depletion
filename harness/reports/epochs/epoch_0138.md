# Epoch 138 report

- Generations completed: 69000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 68501 to 69000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 325, island B 313.
- Best composite score so far: A 0.7610, B 0.7138 (generation 66118).
- Honeypot genome voided: True. Ledger chain intact: True (831980 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 138086; effective independent trials (clustered): 82853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4665 | 460 | 1 | 5.4% |
| ATOM_DROP | 1644 | 283 | 0 | 6.1% |
| ATOM_SWAP | 10774 | 806 | 5 | 13.0% |
| ENSEMBLE | 751 | 65 | 1 | 2.6% |
| ENTRY_TRANSPLANT | 6203 | 831 | 9 | 7.6% |
| EXIT_TRANSPLANT | 5872 | 761 | 10 | 7.6% |
| INVERT | 2122 | 91 | 0 | 3.3% |
| LIBRARY_PROBE | 16262 | 1039 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 10356 | 1888 | 1 | 20.5% |
| SIMPLIFY | 1433 | 215 | 0 | 5.9% |
| SLOT_CROSSOVER | 8889 | 1323 | 9 | 11.7% |
