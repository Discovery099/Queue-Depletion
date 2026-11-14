# Epoch 76 report

- Generations completed: 38000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 37501 to 38000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 292, island B 304.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (458568 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 76086; effective independent trials (clustered): 45653.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 2675 | 252 | 0 | 5.4% |
| ATOM_DROP | 747 | 110 | 0 | 5.9% |
| ATOM_SWAP | 6019 | 455 | 1 | 13.1% |
| ENSEMBLE | 418 | 32 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 3368 | 434 | 0 | 7.7% |
| EXIT_TRANSPLANT | 3221 | 349 | 2 | 7.4% |
| INVERT | 1159 | 38 | 0 | 3.2% |
| LIBRARY_PROBE | 9447 | 670 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 5578 | 967 | 0 | 20.5% |
| SIMPLIFY | 683 | 108 | 0 | 6.0% |
| SLOT_CROSSOVER | 4656 | 601 | 4 | 11.5% |
