# Epoch 121 report

- Generations completed: 60500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 60001 to 60500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 320, island B 311.
- Best composite score so far: A 0.7610, B 0.6853 (generation 58054).
- Honeypot genome voided: True. Ledger chain intact: True (729824 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 121086; effective independent trials (clustered): 72653.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4149 | 410 | 1 | 5.4% |
| ATOM_DROP | 1374 | 217 | 0 | 5.9% |
| ATOM_SWAP | 9526 | 714 | 5 | 13.0% |
| ENSEMBLE | 673 | 59 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 5425 | 712 | 6 | 7.6% |
| EXIT_TRANSPLANT | 5165 | 641 | 10 | 7.5% |
| INVERT | 1852 | 74 | 0 | 3.3% |
| LIBRARY_PROBE | 14382 | 941 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 9051 | 1654 | 1 | 20.6% |
| SIMPLIFY | 1201 | 189 | 0 | 5.9% |
| SLOT_CROSSOVER | 7673 | 1120 | 9 | 11.7% |
