# Epoch 94 report

- Generations completed: 47000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 46501 to 47000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 311, island B 307.
- Best composite score so far: A 0.7050, B 0.5468 (generation 45871).
- Honeypot genome voided: True. Ledger chain intact: True (566784 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 94086; effective independent trials (clustered): 56454.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3238 | 310 | 1 | 5.4% |
| ATOM_DROP | 964 | 148 | 0 | 5.9% |
| ATOM_SWAP | 7463 | 565 | 1 | 13.1% |
| ENSEMBLE | 532 | 45 | 0 | 2.7% |
| ENTRY_TRANSPLANT | 4172 | 536 | 3 | 7.6% |
| EXIT_TRANSPLANT | 3992 | 450 | 5 | 7.4% |
| INVERT | 1428 | 56 | 0 | 3.3% |
| LIBRARY_PROBE | 11466 | 793 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 6945 | 1237 | 1 | 20.5% |
| SIMPLIFY | 904 | 144 | 0 | 6.0% |
| SLOT_CROSSOVER | 5867 | 817 | 4 | 11.6% |
