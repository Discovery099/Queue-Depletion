# Epoch 151 report

- Generations completed: 75500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 75001 to 75500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 326, island B 316.
- Best composite score so far: A 0.7610, B 0.7655 (generation 73770).
- Honeypot genome voided: True. Ledger chain intact: True (910196 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 151086; effective independent trials (clustered): 90653.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 5087 | 502 | 1 | 5.4% |
| ATOM_DROP | 1839 | 322 | 1 | 6.1% |
| ATOM_SWAP | 11757 | 875 | 8 | 12.9% |
| ENSEMBLE | 802 | 72 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 6807 | 926 | 9 | 7.6% |
| EXIT_TRANSPLANT | 6391 | 863 | 14 | 7.6% |
| INVERT | 2318 | 101 | 0 | 3.3% |
| LIBRARY_PROBE | 17699 | 1110 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 11365 | 2088 | 1 | 20.5% |
| SIMPLIFY | 1610 | 233 | 0 | 5.8% |
| SLOT_CROSSOVER | 9796 | 1478 | 9 | 11.7% |
