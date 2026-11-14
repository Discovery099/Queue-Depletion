# Epoch 37 report

- Generations completed: 18500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 18001 to 18500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 265, island B 270.
- Best composite score so far: A 0.6363, B 0.5468 (generation 18133).
- Honeypot genome voided: True. Ledger chain intact: True (223376 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 37100; effective independent trials (clustered): 22262.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1306 | 139 | 0 | 5.6% |
| ATOM_DROP | 344 | 50 | 0 | 6.0% |
| ATOM_SWAP | 2982 | 263 | 0 | 13.6% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 1532 | 192 | 0 | 7.7% |
| EXIT_TRANSPLANT | 1472 | 162 | 0 | 7.5% |
| INVERT | 566 | 18 | 0 | 3.3% |
| LIBRARY_PROBE | 5321 | 425 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 2578 | 462 | 0 | 21.0% |
| SIMPLIFY | 318 | 49 | 0 | 6.1% |
| SLOT_CROSSOVER | 2071 | 274 | 1 | 11.7% |
