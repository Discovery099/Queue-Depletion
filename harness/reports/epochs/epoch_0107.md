# Epoch 107 report

- Generations completed: 53500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 53001 to 53500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 316, island B 310.
- Best composite score so far: A 0.7610, B 0.6280 (generation 53323).
- Honeypot genome voided: True. Ledger chain intact: True (645596 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 107086; effective independent trials (clustered): 64253.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3707 | 363 | 1 | 5.4% |
| ATOM_DROP | 1155 | 182 | 0 | 6.0% |
| ATOM_SWAP | 8482 | 633 | 1 | 13.0% |
| ENSEMBLE | 599 | 53 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 4743 | 610 | 6 | 7.6% |
| EXIT_TRANSPLANT | 4535 | 527 | 9 | 7.4% |
| INVERT | 1645 | 63 | 0 | 3.3% |
| LIBRARY_PROBE | 12871 | 870 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 7954 | 1426 | 1 | 20.5% |
| SIMPLIFY | 1039 | 164 | 0 | 6.0% |
| SLOT_CROSSOVER | 6741 | 967 | 5 | 11.7% |
