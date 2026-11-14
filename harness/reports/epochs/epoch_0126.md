# Epoch 126 report

- Generations completed: 63000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 62501 to 63000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 323, island B 311.
- Best composite score so far: A 0.7610, B 0.6892 (generation 62036).
- Honeypot genome voided: True. Ledger chain intact: True (759876 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 126086; effective independent trials (clustered): 75653.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4309 | 425 | 1 | 5.4% |
| ATOM_DROP | 1452 | 238 | 0 | 6.0% |
| ATOM_SWAP | 9903 | 742 | 5 | 13.0% |
| ENSEMBLE | 693 | 60 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 5626 | 735 | 7 | 7.6% |
| EXIT_TRANSPLANT | 5388 | 677 | 10 | 7.5% |
| INVERT | 1926 | 80 | 0 | 3.3% |
| LIBRARY_PROBE | 14926 | 972 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 9442 | 1722 | 1 | 20.5% |
| SIMPLIFY | 1273 | 201 | 0 | 5.9% |
| SLOT_CROSSOVER | 8033 | 1182 | 9 | 11.7% |
