# Epoch 34 report

- Generations completed: 17000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 16501 to 17000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 261, island B 263.
- Best composite score so far: A 0.5974, B 0.5468 (generation 15525).
- Honeypot genome voided: True. Ledger chain intact: True (205364 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 34100; effective independent trials (clustered): 20461.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1188 | 129 | 0 | 5.6% |
| ATOM_DROP | 317 | 42 | 0 | 5.9% |
| ATOM_SWAP | 2740 | 252 | 0 | 13.7% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 1402 | 177 | 0 | 7.7% |
| EXIT_TRANSPLANT | 1342 | 146 | 0 | 7.5% |
| INVERT | 524 | 16 | 0 | 3.3% |
| LIBRARY_PROBE | 4995 | 395 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 2334 | 413 | 0 | 20.9% |
| SIMPLIFY | 282 | 42 | 0 | 6.0% |
| SLOT_CROSSOVER | 1866 | 247 | 0 | 11.7% |
