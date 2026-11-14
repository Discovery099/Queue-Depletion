# Epoch 101 report

- Generations completed: 50500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 50001 to 50500.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 314, island B 308.
- Best composite score so far: A 0.7338, B 0.5741 (generation 48034).
- Honeypot genome voided: True. Ledger chain intact: True (609496 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 101086; effective independent trials (clustered): 60653.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3494 | 341 | 1 | 5.4% |
| ATOM_DROP | 1077 | 164 | 0 | 5.9% |
| ATOM_SWAP | 8009 | 597 | 1 | 13.0% |
| ENSEMBLE | 567 | 51 | 0 | 2.7% |
| ENTRY_TRANSPLANT | 4471 | 577 | 6 | 7.6% |
| EXIT_TRANSPLANT | 4294 | 484 | 8 | 7.4% |
| INVERT | 1544 | 58 | 0 | 3.3% |
| LIBRARY_PROBE | 12236 | 832 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 7474 | 1341 | 1 | 20.5% |
| SIMPLIFY | 980 | 159 | 0 | 6.0% |
| SLOT_CROSSOVER | 6325 | 888 | 4 | 11.6% |
