# Epoch 75 report

- Generations completed: 37500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 37001 to 37500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 292, island B 305.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (452568 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 75086; effective independent trials (clustered): 45054.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 2647 | 247 | 0 | 5.4% |
| ATOM_DROP | 740 | 109 | 0 | 5.9% |
| ATOM_SWAP | 5943 | 452 | 1 | 13.1% |
| ENSEMBLE | 405 | 31 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 3320 | 430 | 0 | 7.7% |
| EXIT_TRANSPLANT | 3178 | 345 | 2 | 7.4% |
| INVERT | 1142 | 38 | 0 | 3.2% |
| LIBRARY_PROBE | 9332 | 662 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.2% |
| PARAM_STEP | 5500 | 944 | 0 | 20.4% |
| SIMPLIFY | 670 | 106 | 0 | 6.0% |
| SLOT_CROSSOVER | 4594 | 589 | 4 | 11.5% |
