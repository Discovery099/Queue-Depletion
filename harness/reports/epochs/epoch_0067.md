# Epoch 67 report

- Generations completed: 33500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 33001 to 33500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 287, island B 301.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (404474 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 67086; effective independent trials (clustered): 40252.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 2386 | 222 | 0 | 5.4% |
| ATOM_DROP | 653 | 95 | 0 | 5.9% |
| ATOM_SWAP | 5327 | 420 | 1 | 13.2% |
| ENSEMBLE | 335 | 23 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 2954 | 376 | 0 | 7.6% |
| EXIT_TRANSPLANT | 2830 | 313 | 2 | 7.4% |
| INVERT | 1027 | 32 | 0 | 3.2% |
| LIBRARY_PROBE | 8446 | 605 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 4888 | 843 | 0 | 20.5% |
| SIMPLIFY | 580 | 90 | 0 | 6.0% |
| SLOT_CROSSOVER | 4045 | 521 | 3 | 11.5% |
