# Epoch 43 report

- Generations completed: 21500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 21001 to 21500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 270, island B 285.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (259658 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 43086; effective independent trials (clustered): 25853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1520 | 149 | 0 | 5.5% |
| ATOM_DROP | 405 | 59 | 0 | 6.0% |
| ATOM_SWAP | 3470 | 293 | 0 | 13.5% |
| ENSEMBLE | 41 | 2 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 1822 | 230 | 0 | 7.7% |
| EXIT_TRANSPLANT | 1762 | 196 | 0 | 7.6% |
| INVERT | 658 | 21 | 0 | 3.3% |
| LIBRARY_PROBE | 5929 | 457 | 0 | 3.6% |
| LLM_HYPOTHESIS | 19 | 8 | 0 | 11.5% |
| PARAM_STEP | 3045 | 537 | 0 | 20.9% |
| SIMPLIFY | 361 | 55 | 0 | 6.1% |
| SLOT_CROSSOVER | 2468 | 315 | 1 | 11.6% |
