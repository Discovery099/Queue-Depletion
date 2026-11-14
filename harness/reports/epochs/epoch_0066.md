# Epoch 66 report

- Generations completed: 33000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 32501 to 33000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 287, island B 300.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (398474 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 66086; effective independent trials (clustered): 39653.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 2352 | 217 | 0 | 5.4% |
| ATOM_DROP | 641 | 93 | 0 | 5.9% |
| ATOM_SWAP | 5259 | 417 | 1 | 13.2% |
| ENSEMBLE | 322 | 23 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 2906 | 368 | 0 | 7.6% |
| EXIT_TRANSPLANT | 2786 | 306 | 2 | 7.4% |
| INVERT | 1018 | 31 | 0 | 3.2% |
| LIBRARY_PROBE | 8328 | 598 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.2% |
| PARAM_STEP | 4814 | 826 | 0 | 20.4% |
| SIMPLIFY | 565 | 88 | 0 | 6.0% |
| SLOT_CROSSOVER | 3980 | 511 | 3 | 11.5% |
