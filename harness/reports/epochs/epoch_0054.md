# Epoch 54 report

- Generations completed: 27000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 26501 to 27000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 281, island B 293.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (325774 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 54086; effective independent trials (clustered): 32454.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1929 | 175 | 0 | 5.5% |
| ATOM_DROP | 506 | 70 | 0 | 6.0% |
| ATOM_SWAP | 4325 | 350 | 1 | 13.5% |
| ENSEMBLE | 186 | 18 | 0 | 2.8% |
| ENTRY_TRANSPLANT | 2346 | 293 | 0 | 7.8% |
| EXIT_TRANSPLANT | 2256 | 240 | 1 | 7.5% |
| INVERT | 831 | 24 | 0 | 3.3% |
| LIBRARY_PROBE | 7076 | 523 | 0 | 3.6% |
| LLM_HYPOTHESIS | 19 | 8 | 0 | 11.5% |
| PARAM_STEP | 3893 | 660 | 0 | 20.8% |
| SIMPLIFY | 451 | 66 | 0 | 6.0% |
| SLOT_CROSSOVER | 3182 | 410 | 2 | 11.7% |
