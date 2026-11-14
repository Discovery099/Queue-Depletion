# Epoch 47 report

- Generations completed: 23500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 23001 to 23500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 276, island B 288.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (283710 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 47086; effective independent trials (clustered): 28254.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1653 | 157 | 0 | 5.5% |
| ATOM_DROP | 444 | 63 | 0 | 6.0% |
| ATOM_SWAP | 3779 | 318 | 0 | 13.6% |
| ENSEMBLE | 103 | 5 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 2017 | 247 | 0 | 7.7% |
| EXIT_TRANSPLANT | 1937 | 211 | 0 | 7.6% |
| INVERT | 715 | 24 | 0 | 3.3% |
| LIBRARY_PROBE | 6356 | 484 | 0 | 3.6% |
| LLM_HYPOTHESIS | 19 | 8 | 0 | 11.5% |
| PARAM_STEP | 3352 | 583 | 0 | 20.9% |
| SIMPLIFY | 394 | 58 | 0 | 6.0% |
| SLOT_CROSSOVER | 2731 | 354 | 2 | 11.7% |
