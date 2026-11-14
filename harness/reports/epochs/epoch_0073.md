# Epoch 73 report

- Generations completed: 36500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 36001 to 36500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 290, island B 303.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (440528 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 73086; effective independent trials (clustered): 43853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 2579 | 241 | 0 | 5.4% |
| ATOM_DROP | 721 | 105 | 0 | 5.9% |
| ATOM_SWAP | 5778 | 445 | 1 | 13.2% |
| ENSEMBLE | 391 | 30 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 3234 | 415 | 0 | 7.6% |
| EXIT_TRANSPLANT | 3074 | 341 | 2 | 7.4% |
| INVERT | 1115 | 37 | 0 | 3.2% |
| LIBRARY_PROBE | 9145 | 651 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.2% |
| PARAM_STEP | 5357 | 921 | 0 | 20.4% |
| SIMPLIFY | 648 | 102 | 0 | 6.0% |
| SLOT_CROSSOVER | 4429 | 561 | 4 | 11.4% |
