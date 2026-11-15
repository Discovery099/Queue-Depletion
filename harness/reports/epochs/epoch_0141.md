# Epoch 141 report

- Generations completed: 70500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 70001 to 70500.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 100.00% (1 genomes).
- Occupied archive cells: island A 324, island B 315.
- Best composite score so far: A 0.7610, B 0.7245 (generation 70498).
- Honeypot genome voided: True. Ledger chain intact: True (850056 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 141086; effective independent trials (clustered): 84652.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4760 | 468 | 1 | 5.4% |
| ATOM_DROP | 1682 | 287 | 0 | 6.0% |
| ATOM_SWAP | 10968 | 818 | 6 | 13.0% |
| ENSEMBLE | 768 | 67 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 6346 | 859 | 9 | 7.6% |
| EXIT_TRANSPLANT | 5999 | 787 | 12 | 7.6% |
| INVERT | 2174 | 95 | 0 | 3.3% |
| LIBRARY_PROBE | 16579 | 1055 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 10593 | 1939 | 1 | 20.5% |
| SIMPLIFY | 1475 | 219 | 0 | 5.8% |
| SLOT_CROSSOVER | 9127 | 1362 | 9 | 11.7% |

## Monitor notes

- canary adoption above 2%: promotion halted for this epoch pending tightening (SPEC 15.1)
