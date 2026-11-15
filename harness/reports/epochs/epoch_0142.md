# Epoch 142 report

- Generations completed: 71000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 70501 to 71000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 324, island B 315.
- Best composite score so far: A 0.7610, B 0.7245 (generation 70498).
- Honeypot genome voided: True. Ledger chain intact: True (856068 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 142086; effective independent trials (clustered): 85253.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4792 | 470 | 1 | 5.4% |
| ATOM_DROP | 1704 | 290 | 0 | 6.0% |
| ATOM_SWAP | 11036 | 823 | 6 | 12.9% |
| ENSEMBLE | 776 | 67 | 1 | 2.6% |
| ENTRY_TRANSPLANT | 6387 | 862 | 9 | 7.6% |
| EXIT_TRANSPLANT | 6040 | 798 | 13 | 7.6% |
| INVERT | 2194 | 95 | 0 | 3.3% |
| LIBRARY_PROBE | 16687 | 1057 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 10667 | 1954 | 1 | 20.5% |
| SIMPLIFY | 1490 | 221 | 0 | 5.8% |
| SLOT_CROSSOVER | 9198 | 1378 | 9 | 11.7% |
