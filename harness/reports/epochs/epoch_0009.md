# Epoch 9 report

- Generations completed: 4500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 4001 to 4500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 139, island B 119.
- Best composite score so far: A 0.4434, B 0.4655 (generation 4267).
- Honeypot genome voided: True. Ledger chain intact: True (55228 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 9100; effective independent trials (clustered): 5461.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 253 | 39 | 0 | 6.1% |
| ATOM_DROP | 67 | 10 | 0 | 6.1% |
| ATOM_SWAP | 572 | 56 | 0 | 13.9% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 324 | 45 | 0 | 7.9% |
| EXIT_TRANSPLANT | 275 | 30 | 0 | 7.6% |
| INVERT | 119 | 6 | 0 | 3.4% |
| LIBRARY_PROBE | 2209 | 181 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 270 | 39 | 0 | 20.0% |
| SIMPLIFY | 62 | 9 | 0 | 6.1% |
| SLOT_CROSSOVER | 339 | 39 | 0 | 11.4% |
