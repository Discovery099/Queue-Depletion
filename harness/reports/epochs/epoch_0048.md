# Epoch 48 report

- Generations completed: 24000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 23501 to 24000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 276, island B 288.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (289710 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 48086; effective independent trials (clustered): 28853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1703 | 161 | 0 | 5.5% |
| ATOM_DROP | 457 | 64 | 0 | 6.0% |
| ATOM_SWAP | 3873 | 321 | 0 | 13.6% |
| ENSEMBLE | 112 | 6 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 2066 | 254 | 0 | 7.7% |
| EXIT_TRANSPLANT | 1976 | 215 | 0 | 7.6% |
| INVERT | 733 | 24 | 0 | 3.3% |
| LIBRARY_PROBE | 6449 | 487 | 0 | 3.6% |
| LLM_HYPOTHESIS | 19 | 8 | 0 | 11.5% |
| PARAM_STEP | 3417 | 592 | 0 | 20.9% |
| SIMPLIFY | 398 | 59 | 0 | 6.0% |
| SLOT_CROSSOVER | 2797 | 361 | 2 | 11.7% |
