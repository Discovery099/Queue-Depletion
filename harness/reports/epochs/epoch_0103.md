# Epoch 103 report

- Generations completed: 51500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 51001 to 51500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 315, island B 309.
- Best composite score so far: A 0.7338, B 0.5741 (generation 48034).
- Honeypot genome voided: True. Ledger chain intact: True (621520 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 103086; effective independent trials (clustered): 61853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3570 | 346 | 1 | 5.4% |
| ATOM_DROP | 1102 | 166 | 0 | 5.9% |
| ATOM_SWAP | 8164 | 610 | 1 | 13.0% |
| ENSEMBLE | 581 | 52 | 0 | 2.7% |
| ENTRY_TRANSPLANT | 4563 | 584 | 6 | 7.6% |
| EXIT_TRANSPLANT | 4371 | 506 | 8 | 7.4% |
| INVERT | 1578 | 58 | 0 | 3.2% |
| LIBRARY_PROBE | 12441 | 843 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 7634 | 1371 | 1 | 20.5% |
| SIMPLIFY | 998 | 162 | 0 | 6.0% |
| SLOT_CROSSOVER | 6469 | 923 | 4 | 11.7% |
