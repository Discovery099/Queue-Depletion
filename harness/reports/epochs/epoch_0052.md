# Epoch 52 report

- Generations completed: 26000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 25501 to 26000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 280, island B 292.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (313750 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 52086; effective independent trials (clustered): 31254.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1859 | 170 | 0 | 5.5% |
| ATOM_DROP | 492 | 67 | 0 | 5.9% |
| ATOM_SWAP | 4167 | 343 | 0 | 13.6% |
| ENSEMBLE | 164 | 13 | 0 | 2.7% |
| ENTRY_TRANSPLANT | 2259 | 284 | 0 | 7.8% |
| EXIT_TRANSPLANT | 2161 | 234 | 0 | 7.6% |
| INVERT | 798 | 24 | 0 | 3.3% |
| LIBRARY_PROBE | 6848 | 513 | 0 | 3.6% |
| LLM_HYPOTHESIS | 19 | 8 | 0 | 11.5% |
| PARAM_STEP | 3750 | 635 | 0 | 20.8% |
| SIMPLIFY | 430 | 64 | 0 | 6.1% |
| SLOT_CROSSOVER | 3053 | 396 | 2 | 11.7% |
