# Epoch 181 report

- Generations completed: 90500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 90001 to 90500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 327, island B 319.
- Best composite score so far: A 0.7640, B 0.7879 (generation 88594).
- Honeypot genome voided: True. Ledger chain intact: True (1090592 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 181086; effective independent trials (clustered): 108653.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 6064 | 590 | 1 | 5.4% |
| ATOM_DROP | 2338 | 434 | 1 | 6.2% |
| ATOM_SWAP | 14140 | 1035 | 10 | 12.9% |
| ENSEMBLE | 892 | 83 | 2 | 2.7% |
| ENTRY_TRANSPLANT | 8182 | 1126 | 13 | 7.6% |
| EXIT_TRANSPLANT | 7606 | 1078 | 19 | 7.7% |
| INVERT | 2765 | 137 | 0 | 3.3% |
| LIBRARY_PROBE | 21126 | 1277 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 12.9% |
| PARAM_STEP | 13561 | 2443 | 1 | 20.4% |
| SIMPLIFY | 1944 | 278 | 0 | 5.8% |
| SLOT_CROSSOVER | 11853 | 1867 | 10 | 11.8% |
