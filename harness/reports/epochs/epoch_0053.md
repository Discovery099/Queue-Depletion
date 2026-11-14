# Epoch 53 report

- Generations completed: 26500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 26001 to 26500.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 280, island B 293.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (319762 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 53086; effective independent trials (clustered): 31853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1890 | 172 | 0 | 5.5% |
| ATOM_DROP | 500 | 69 | 0 | 6.0% |
| ATOM_SWAP | 4239 | 345 | 1 | 13.5% |
| ENSEMBLE | 178 | 17 | 0 | 2.8% |
| ENTRY_TRANSPLANT | 2306 | 289 | 0 | 7.8% |
| EXIT_TRANSPLANT | 2203 | 235 | 0 | 7.5% |
| INVERT | 815 | 24 | 0 | 3.3% |
| LIBRARY_PROBE | 6972 | 518 | 0 | 3.6% |
| LLM_HYPOTHESIS | 19 | 8 | 0 | 11.5% |
| PARAM_STEP | 3821 | 649 | 0 | 20.8% |
| SIMPLIFY | 444 | 66 | 0 | 6.1% |
| SLOT_CROSSOVER | 3113 | 404 | 2 | 11.7% |
