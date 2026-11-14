# Epoch 117 report

- Generations completed: 58500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 58001 to 58500.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 318, island B 311.
- Best composite score so far: A 0.7610, B 0.6853 (generation 58054).
- Honeypot genome voided: True. Ledger chain intact: True (705772 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 117086; effective independent trials (clustered): 70253.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4035 | 399 | 1 | 5.4% |
| ATOM_DROP | 1311 | 208 | 0 | 6.0% |
| ATOM_SWAP | 9236 | 692 | 4 | 13.0% |
| ENSEMBLE | 650 | 57 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 5216 | 670 | 6 | 7.6% |
| EXIT_TRANSPLANT | 4986 | 610 | 10 | 7.5% |
| INVERT | 1785 | 70 | 0 | 3.3% |
| LIBRARY_PROBE | 13969 | 919 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 8744 | 1584 | 1 | 20.5% |
| SIMPLIFY | 1152 | 183 | 0 | 6.0% |
| SLOT_CROSSOVER | 7387 | 1067 | 9 | 11.7% |
