# Epoch 68 report

- Generations completed: 34000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 33501 to 34000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 287, island B 303.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (410474 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 68086; effective independent trials (clustered): 40853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 2414 | 224 | 0 | 5.4% |
| ATOM_DROP | 666 | 97 | 0 | 5.9% |
| ATOM_SWAP | 5386 | 422 | 1 | 13.2% |
| ENSEMBLE | 345 | 24 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 3009 | 386 | 0 | 7.6% |
| EXIT_TRANSPLANT | 2873 | 321 | 2 | 7.4% |
| INVERT | 1038 | 32 | 0 | 3.2% |
| LIBRARY_PROBE | 8571 | 610 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 4975 | 865 | 0 | 20.5% |
| SIMPLIFY | 590 | 93 | 0 | 6.0% |
| SLOT_CROSSOVER | 4104 | 524 | 3 | 11.5% |
