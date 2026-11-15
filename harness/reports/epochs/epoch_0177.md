# Epoch 177 report

- Generations completed: 88500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 88001 to 88500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 327, island B 319.
- Best composite score so far: A 0.7640, B 0.7660 (generation 86275).
- Honeypot genome voided: True. Ledger chain intact: True (1066552 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 177086; effective independent trials (clustered): 106253.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 5917 | 580 | 1 | 5.4% |
| ATOM_DROP | 2257 | 422 | 1 | 6.2% |
| ATOM_SWAP | 13805 | 1019 | 10 | 12.9% |
| ENSEMBLE | 882 | 82 | 2 | 2.7% |
| ENTRY_TRANSPLANT | 8021 | 1101 | 13 | 7.6% |
| EXIT_TRANSPLANT | 7451 | 1046 | 19 | 7.7% |
| INVERT | 2709 | 135 | 0 | 3.3% |
| LIBRARY_PROBE | 20680 | 1254 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 13271 | 2391 | 1 | 20.4% |
| SIMPLIFY | 1905 | 272 | 0 | 5.8% |
| SLOT_CROSSOVER | 11573 | 1813 | 10 | 11.8% |
