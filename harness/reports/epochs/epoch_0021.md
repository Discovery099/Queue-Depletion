# Epoch 21 report

- Generations completed: 10500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 10001 to 10500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 227, island B 203.
- Best composite score so far: A 0.5290, B 0.5468 (generation 8637).
- Honeypot genome voided: True. Ledger chain intact: True (127324 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 21100; effective independent trials (clustered): 12660.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 673 | 90 | 0 | 5.9% |
| ATOM_DROP | 212 | 29 | 0 | 5.9% |
| ATOM_SWAP | 1593 | 153 | 0 | 13.8% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 861 | 110 | 0 | 7.7% |
| EXIT_TRANSPLANT | 775 | 83 | 0 | 7.5% |
| INVERT | 324 | 11 | 0 | 3.3% |
| LIBRARY_PROBE | 3556 | 290 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.2% |
| PARAM_STEP | 1263 | 222 | 0 | 20.8% |
| SIMPLIFY | 177 | 25 | 0 | 5.9% |
| SLOT_CROSSOVER | 1056 | 150 | 0 | 11.9% |
