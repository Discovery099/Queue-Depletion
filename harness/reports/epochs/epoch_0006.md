# Epoch 6 report

- Generations completed: 3000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 2501 to 3000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 107, island B 88.
- Best composite score so far: A 0.4406, B 0.3901 (generation 2635).
- Honeypot genome voided: True. Ledger chain intact: True (37228 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 6100; effective independent trials (clustered): 3662.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 124 | 22 | 0 | 6.4% |
| ATOM_DROP | 34 | 8 | 0 | 7.1% |
| ATOM_SWAP | 337 | 33 | 0 | 14.2% |
| ENSEMBLE | 0 | 0 | 0 | 4.7% |
| ENTRY_TRANSPLANT | 173 | 25 | 0 | 8.2% |
| EXIT_TRANSPLANT | 155 | 17 | 0 | 7.7% |
| INVERT | 67 | 3 | 0 | 3.5% |
| LIBRARY_PROBE | 1855 | 153 | 0 | 3.7% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.4% |
| PARAM_STEP | 40 | 1 | 0 | 17.2% |
| SIMPLIFY | 28 | 4 | 0 | 6.3% |
| SLOT_CROSSOVER | 177 | 19 | 0 | 11.5% |
