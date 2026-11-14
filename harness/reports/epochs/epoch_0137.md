# Epoch 137 report

- Generations completed: 68500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 68001 to 68500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 325, island B 312.
- Best composite score so far: A 0.7610, B 0.7138 (generation 66118).
- Honeypot genome voided: True. Ledger chain intact: True (825980 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 137086; effective independent trials (clustered): 82252.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4635 | 457 | 1 | 5.4% |
| ATOM_DROP | 1628 | 279 | 0 | 6.1% |
| ATOM_SWAP | 10701 | 800 | 5 | 13.0% |
| ENSEMBLE | 746 | 65 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 6165 | 826 | 9 | 7.6% |
| EXIT_TRANSPLANT | 5837 | 757 | 10 | 7.6% |
| INVERT | 2110 | 91 | 0 | 3.3% |
| LIBRARY_PROBE | 16146 | 1035 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 10276 | 1870 | 1 | 20.5% |
| SIMPLIFY | 1427 | 215 | 0 | 5.9% |
| SLOT_CROSSOVER | 8800 | 1311 | 9 | 11.7% |
