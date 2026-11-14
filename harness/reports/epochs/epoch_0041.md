# Epoch 41 report

- Generations completed: 20500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 20001 to 20500.

| Outcome | Count |
|---|---|
| ERROR | 19 |
| STAGE1_FAIL | 481 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 268, island B 281.
- Best composite score so far: A 0.6363, B 0.5468 (generation 18133).
- Honeypot genome voided: True. Ledger chain intact: True (247658 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 41086; effective independent trials (clustered): 24654.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1445 | 147 | 0 | 5.6% |
| ATOM_DROP | 385 | 56 | 0 | 6.0% |
| ATOM_SWAP | 3300 | 279 | 0 | 13.5% |
| ENSEMBLE | 20 | 0 | 0 | 2.5% |
| ENTRY_TRANSPLANT | 1732 | 216 | 0 | 7.7% |
| EXIT_TRANSPLANT | 1667 | 186 | 0 | 7.6% |
| INVERT | 626 | 21 | 0 | 3.3% |
| LIBRARY_PROBE | 5737 | 453 | 0 | 3.6% |
| LLM_HYPOTHESIS | 19 | 8 | 0 | 11.5% |
| PARAM_STEP | 2890 | 521 | 0 | 21.0% |
| SIMPLIFY | 349 | 53 | 0 | 6.1% |
| SLOT_CROSSOVER | 2330 | 299 | 1 | 11.6% |
