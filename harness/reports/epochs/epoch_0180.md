# Epoch 180 report

- Generations completed: 90000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 89501 to 90000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 327, island B 319.
- Best composite score so far: A 0.7640, B 0.7879 (generation 88594).
- Honeypot genome voided: True. Ledger chain intact: True (1084592 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 180086; effective independent trials (clustered): 108053.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 6023 | 588 | 1 | 5.4% |
| ATOM_DROP | 2323 | 433 | 1 | 6.2% |
| ATOM_SWAP | 14056 | 1032 | 10 | 12.9% |
| ENSEMBLE | 891 | 82 | 2 | 2.7% |
| ENTRY_TRANSPLANT | 8142 | 1121 | 13 | 7.6% |
| EXIT_TRANSPLANT | 7568 | 1070 | 19 | 7.7% |
| INVERT | 2751 | 137 | 0 | 3.3% |
| LIBRARY_PROBE | 21003 | 1272 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 13493 | 2432 | 1 | 20.4% |
| SIMPLIFY | 1935 | 274 | 0 | 5.8% |
| SLOT_CROSSOVER | 11786 | 1851 | 10 | 11.8% |
