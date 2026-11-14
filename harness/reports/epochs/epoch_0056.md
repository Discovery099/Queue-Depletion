# Epoch 56 report

- Generations completed: 28000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 27501 to 28000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 282, island B 294.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (337814 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 56086; effective independent trials (clustered): 33653.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 2003 | 179 | 0 | 5.5% |
| ATOM_DROP | 521 | 72 | 0 | 6.0% |
| ATOM_SWAP | 4482 | 359 | 1 | 13.5% |
| ENSEMBLE | 209 | 18 | 0 | 2.7% |
| ENTRY_TRANSPLANT | 2438 | 302 | 0 | 7.8% |
| EXIT_TRANSPLANT | 2355 | 252 | 1 | 7.5% |
| INVERT | 860 | 24 | 0 | 3.3% |
| LIBRARY_PROBE | 7281 | 532 | 0 | 3.6% |
| LLM_HYPOTHESIS | 19 | 8 | 0 | 11.5% |
| PARAM_STEP | 4053 | 691 | 0 | 20.8% |
| SIMPLIFY | 467 | 69 | 0 | 6.0% |
| SLOT_CROSSOVER | 3312 | 428 | 2 | 11.7% |
