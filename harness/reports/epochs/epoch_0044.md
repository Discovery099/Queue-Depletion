# Epoch 44 report

- Generations completed: 22000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 21501 to 22000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 271, island B 287.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (265670 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 44086; effective independent trials (clustered): 26454.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1558 | 152 | 0 | 5.6% |
| ATOM_DROP | 417 | 59 | 0 | 6.0% |
| ATOM_SWAP | 3543 | 297 | 0 | 13.6% |
| ENSEMBLE | 63 | 3 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 1885 | 235 | 0 | 7.7% |
| EXIT_TRANSPLANT | 1794 | 198 | 0 | 7.6% |
| INVERT | 676 | 21 | 0 | 3.3% |
| LIBRARY_PROBE | 6032 | 466 | 0 | 3.6% |
| LLM_HYPOTHESIS | 19 | 8 | 0 | 11.5% |
| PARAM_STEP | 3112 | 547 | 0 | 20.9% |
| SIMPLIFY | 370 | 55 | 0 | 6.0% |
| SLOT_CROSSOVER | 2531 | 321 | 2 | 11.6% |
