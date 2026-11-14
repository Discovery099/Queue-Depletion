# Epoch 49 report

- Generations completed: 24500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 24001 to 24500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 277, island B 288.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (295710 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 49086; effective independent trials (clustered): 29453.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1747 | 161 | 0 | 5.5% |
| ATOM_DROP | 463 | 66 | 0 | 6.0% |
| ATOM_SWAP | 3962 | 326 | 0 | 13.5% |
| ENSEMBLE | 126 | 10 | 0 | 2.7% |
| ENTRY_TRANSPLANT | 2107 | 260 | 0 | 7.7% |
| EXIT_TRANSPLANT | 2024 | 221 | 0 | 7.6% |
| INVERT | 748 | 24 | 0 | 3.3% |
| LIBRARY_PROBE | 6552 | 496 | 0 | 3.6% |
| LLM_HYPOTHESIS | 19 | 8 | 0 | 11.5% |
| PARAM_STEP | 3481 | 595 | 0 | 20.8% |
| SIMPLIFY | 405 | 60 | 0 | 6.0% |
| SLOT_CROSSOVER | 2866 | 369 | 2 | 11.7% |
