# Epoch 172 report

- Generations completed: 86000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 85501 to 86000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 327, island B 318.
- Best composite score so far: A 0.7610, B 0.7660 (generation 80566).
- Honeypot genome voided: True. Ledger chain intact: True (1036488 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 172086; effective independent trials (clustered): 103253.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 5751 | 561 | 1 | 5.4% |
| ATOM_DROP | 2191 | 409 | 1 | 6.2% |
| ATOM_SWAP | 13402 | 993 | 9 | 12.9% |
| ENSEMBLE | 870 | 81 | 2 | 2.7% |
| ENTRY_TRANSPLANT | 7803 | 1076 | 12 | 7.6% |
| EXIT_TRANSPLANT | 7255 | 1011 | 19 | 7.7% |
| INVERT | 2627 | 123 | 0 | 3.3% |
| LIBRARY_PROBE | 20111 | 1229 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 12.9% |
| PARAM_STEP | 12892 | 2339 | 1 | 20.4% |
| SIMPLIFY | 1854 | 263 | 0 | 5.8% |
| SLOT_CROSSOVER | 11215 | 1753 | 10 | 11.8% |
