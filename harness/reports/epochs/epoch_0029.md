# Epoch 29 report

- Generations completed: 14500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 14001 to 14500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 253, island B 245.
- Best composite score so far: A 0.5341, B 0.5468 (generation 13159).
- Honeypot genome voided: True. Ledger chain intact: True (175324 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 29100; effective independent trials (clustered): 17463.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 994 | 113 | 0 | 5.7% |
| ATOM_DROP | 282 | 37 | 0 | 5.9% |
| ATOM_SWAP | 2297 | 219 | 0 | 13.8% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 1196 | 153 | 0 | 7.8% |
| EXIT_TRANSPLANT | 1122 | 122 | 0 | 7.5% |
| INVERT | 446 | 14 | 0 | 3.3% |
| LIBRARY_PROBE | 4437 | 356 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 1907 | 336 | 0 | 20.9% |
| SIMPLIFY | 241 | 32 | 0 | 5.9% |
| SLOT_CROSSOVER | 1568 | 214 | 0 | 11.8% |
