# Epoch 85 report

- Generations completed: 42500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 42001 to 42500.

| Outcome | Count |
|---|---|
| HOME_ONLY | 2 |
| STAGE1_FAIL | 498 |

- Stage 1 pass rate: 0.40%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 302, island B 306.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (512684 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 85086; effective independent trials (clustered): 38291.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 2958 | 280 | 0 | 5.4% |
| ATOM_DROP | 847 | 126 | 0 | 5.9% |
| ATOM_SWAP | 6749 | 513 | 1 | 13.1% |
| ENSEMBLE | 472 | 35 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 3789 | 493 | 1 | 7.6% |
| EXIT_TRANSPLANT | 3613 | 398 | 3 | 7.4% |
| INVERT | 1291 | 51 | 0 | 3.3% |
| LIBRARY_PROBE | 10460 | 730 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 6251 | 1105 | 1 | 20.5% |
| SIMPLIFY | 791 | 124 | 0 | 6.0% |
| SLOT_CROSSOVER | 5250 | 709 | 4 | 11.6% |
