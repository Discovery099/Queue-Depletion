# Epoch 133 report

- Generations completed: 66500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 66001 to 66500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 324, island B 311.
- Best composite score so far: A 0.7610, B 0.7138 (generation 66118).
- Honeypot genome voided: True. Ledger chain intact: True (801940 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 133086; effective independent trials (clustered): 79854.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4520 | 448 | 1 | 5.4% |
| ATOM_DROP | 1572 | 264 | 0 | 6.0% |
| ATOM_SWAP | 10413 | 780 | 5 | 13.0% |
| ENSEMBLE | 733 | 63 | 1 | 2.6% |
| ENTRY_TRANSPLANT | 5968 | 794 | 9 | 7.6% |
| EXIT_TRANSPLANT | 5680 | 728 | 10 | 7.6% |
| INVERT | 2055 | 84 | 0 | 3.3% |
| LIBRARY_PROBE | 15704 | 1016 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 9964 | 1821 | 1 | 20.5% |
| SIMPLIFY | 1367 | 211 | 0 | 5.9% |
| SLOT_CROSSOVER | 8495 | 1254 | 9 | 11.7% |
