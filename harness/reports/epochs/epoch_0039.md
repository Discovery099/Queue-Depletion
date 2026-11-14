# Epoch 39 report

- Generations completed: 19500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 19001 to 19500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 266, island B 277.
- Best composite score so far: A 0.6363, B 0.5468 (generation 18133).
- Honeypot genome voided: True. Ledger chain intact: True (235376 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 39100; effective independent trials (clustered): 23461.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1384 | 143 | 0 | 5.6% |
| ATOM_DROP | 364 | 53 | 0 | 6.0% |
| ATOM_SWAP | 3143 | 273 | 0 | 13.6% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 1639 | 202 | 0 | 7.7% |
| EXIT_TRANSPLANT | 1556 | 172 | 0 | 7.5% |
| INVERT | 594 | 21 | 0 | 3.3% |
| LIBRARY_PROBE | 5553 | 443 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 2725 | 493 | 0 | 21.0% |
| SIMPLIFY | 330 | 52 | 0 | 6.1% |
| SLOT_CROSSOVER | 2202 | 288 | 1 | 11.7% |
