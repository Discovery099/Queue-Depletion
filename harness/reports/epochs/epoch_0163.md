# Epoch 163 report

- Generations completed: 81500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 81001 to 81500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 327, island B 318.
- Best composite score so far: A 0.7610, B 0.7660 (generation 80566).
- Honeypot genome voided: True. Ledger chain intact: True (982348 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 163086; effective independent trials (clustered): 97853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 5455 | 536 | 1 | 5.4% |
| ATOM_DROP | 2052 | 371 | 1 | 6.1% |
| ATOM_SWAP | 12716 | 952 | 9 | 12.9% |
| ENSEMBLE | 840 | 75 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 7374 | 1015 | 10 | 7.6% |
| EXIT_TRANSPLANT | 6884 | 946 | 17 | 7.6% |
| INVERT | 2500 | 115 | 0 | 3.3% |
| LIBRARY_PROBE | 19049 | 1173 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 12236 | 2246 | 1 | 20.5% |
| SIMPLIFY | 1749 | 251 | 0 | 5.8% |
| SLOT_CROSSOVER | 10616 | 1638 | 10 | 11.8% |
