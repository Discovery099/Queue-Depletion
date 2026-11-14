# Epoch 60 report

- Generations completed: 30000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 29501 to 30000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 287, island B 298.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (361854 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 60086; effective independent trials (clustered): 36052.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 2153 | 193 | 0 | 5.5% |
| ATOM_DROP | 567 | 81 | 0 | 6.0% |
| ATOM_SWAP | 4815 | 386 | 1 | 13.5% |
| ENSEMBLE | 257 | 20 | 0 | 2.7% |
| ENTRY_TRANSPLANT | 2633 | 331 | 0 | 7.8% |
| EXIT_TRANSPLANT | 2523 | 273 | 1 | 7.6% |
| INVERT | 910 | 26 | 0 | 3.3% |
| LIBRARY_PROBE | 7688 | 557 | 0 | 3.6% |
| LLM_HYPOTHESIS | 19 | 8 | 0 | 11.5% |
| PARAM_STEP | 4347 | 737 | 0 | 20.8% |
| SIMPLIFY | 515 | 76 | 0 | 6.0% |
| SLOT_CROSSOVER | 3573 | 457 | 2 | 11.7% |
