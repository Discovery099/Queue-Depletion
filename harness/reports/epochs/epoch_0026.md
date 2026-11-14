# Epoch 26 report

- Generations completed: 13000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 12501 to 13000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 244, island B 235.
- Best composite score so far: A 0.5291, B 0.5468 (generation 12147).
- Honeypot genome voided: True. Ledger chain intact: True (157324 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 26100; effective independent trials (clustered): 15661.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 880 | 102 | 0 | 5.7% |
| ATOM_DROP | 250 | 32 | 0 | 5.8% |
| ATOM_SWAP | 2023 | 191 | 0 | 13.8% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 1073 | 138 | 0 | 7.8% |
| EXIT_TRANSPLANT | 994 | 108 | 0 | 7.5% |
| INVERT | 408 | 11 | 0 | 3.3% |
| LIBRARY_PROBE | 4106 | 333 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 1662 | 288 | 0 | 20.8% |
| SIMPLIFY | 220 | 30 | 0 | 5.9% |
| SLOT_CROSSOVER | 1374 | 197 | 0 | 11.9% |
