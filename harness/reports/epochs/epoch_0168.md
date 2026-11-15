# Epoch 168 report

- Generations completed: 84000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 83501 to 84000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 327, island B 318.
- Best composite score so far: A 0.7610, B 0.7660 (generation 80566).
- Honeypot genome voided: True. Ledger chain intact: True (1012424 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 168086; effective independent trials (clustered): 100853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 5635 | 554 | 1 | 5.4% |
| ATOM_DROP | 2133 | 396 | 1 | 6.2% |
| ATOM_SWAP | 13090 | 967 | 9 | 12.9% |
| ENSEMBLE | 860 | 78 | 2 | 2.7% |
| ENTRY_TRANSPLANT | 7613 | 1045 | 10 | 7.6% |
| EXIT_TRANSPLANT | 7093 | 988 | 19 | 7.7% |
| INVERT | 2573 | 120 | 0 | 3.3% |
| LIBRARY_PROBE | 19613 | 1204 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 12.9% |
| PARAM_STEP | 12588 | 2295 | 1 | 20.4% |
| SIMPLIFY | 1811 | 258 | 0 | 5.8% |
| SLOT_CROSSOVER | 10962 | 1710 | 10 | 11.8% |
