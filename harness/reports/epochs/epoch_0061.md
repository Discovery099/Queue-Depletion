# Epoch 61 report

- Generations completed: 30500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 30001 to 30500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 287, island B 298.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (368410 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 61086; effective independent trials (clustered): 36653.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 2185 | 198 | 0 | 5.4% |
| ATOM_DROP | 577 | 84 | 0 | 5.9% |
| ATOM_SWAP | 4904 | 390 | 1 | 13.2% |
| ENSEMBLE | 270 | 21 | 0 | 2.7% |
| ENTRY_TRANSPLANT | 2684 | 333 | 0 | 7.6% |
| EXIT_TRANSPLANT | 2562 | 276 | 1 | 7.4% |
| INVERT | 935 | 29 | 0 | 3.2% |
| LIBRARY_PROBE | 7780 | 563 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.2% |
| PARAM_STEP | 4421 | 751 | 0 | 20.4% |
| SIMPLIFY | 523 | 78 | 0 | 5.9% |
| SLOT_CROSSOVER | 3630 | 466 | 2 | 11.5% |
