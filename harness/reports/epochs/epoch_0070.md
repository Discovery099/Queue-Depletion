# Epoch 70 report

- Generations completed: 35000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 34501 to 35000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 289, island B 303.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (422516 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 70086; effective independent trials (clustered): 42052.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 2478 | 229 | 0 | 5.4% |
| ATOM_DROP | 692 | 101 | 0 | 5.9% |
| ATOM_SWAP | 5551 | 430 | 1 | 13.2% |
| ENSEMBLE | 366 | 25 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 3095 | 395 | 0 | 7.6% |
| EXIT_TRANSPLANT | 2950 | 330 | 2 | 7.4% |
| INVERT | 1067 | 35 | 0 | 3.2% |
| LIBRARY_PROBE | 8805 | 628 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 5127 | 886 | 0 | 20.5% |
| SIMPLIFY | 615 | 99 | 0 | 6.0% |
| SLOT_CROSSOVER | 4225 | 538 | 3 | 11.5% |
