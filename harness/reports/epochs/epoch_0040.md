# Epoch 40 report

- Generations completed: 20000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 19501 to 20000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 268, island B 278.
- Best composite score so far: A 0.6363, B 0.5468 (generation 18133).
- Honeypot genome voided: True. Ledger chain intact: True (241376 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 40100; effective independent trials (clustered): 24062.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1415 | 145 | 0 | 5.6% |
| ATOM_DROP | 379 | 56 | 0 | 6.0% |
| ATOM_SWAP | 3226 | 276 | 0 | 13.6% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 1677 | 211 | 0 | 7.7% |
| EXIT_TRANSPLANT | 1609 | 176 | 0 | 7.5% |
| INVERT | 610 | 21 | 0 | 3.3% |
| LIBRARY_PROBE | 5663 | 450 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 2809 | 509 | 0 | 21.0% |
| SIMPLIFY | 337 | 52 | 0 | 6.1% |
| SLOT_CROSSOVER | 2265 | 295 | 1 | 11.7% |
