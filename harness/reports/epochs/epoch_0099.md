# Epoch 99 report

- Generations completed: 49500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 49001 to 49500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 312, island B 308.
- Best composite score so far: A 0.7338, B 0.5741 (generation 48034).
- Honeypot genome voided: True. Ledger chain intact: True (596848 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 99086; effective independent trials (clustered): 59454.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3425 | 336 | 1 | 5.4% |
| ATOM_DROP | 1040 | 157 | 0 | 5.9% |
| ATOM_SWAP | 7841 | 588 | 1 | 13.0% |
| ENSEMBLE | 554 | 48 | 0 | 2.7% |
| ENTRY_TRANSPLANT | 4373 | 565 | 4 | 7.6% |
| EXIT_TRANSPLANT | 4198 | 473 | 6 | 7.4% |
| INVERT | 1512 | 57 | 0 | 3.3% |
| LIBRARY_PROBE | 12025 | 821 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 7330 | 1313 | 1 | 20.5% |
| SIMPLIFY | 962 | 154 | 0 | 6.0% |
| SLOT_CROSSOVER | 6211 | 871 | 4 | 11.6% |
