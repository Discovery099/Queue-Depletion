# Epoch 92 report

- Generations completed: 46000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 45501 to 46000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 311, island B 307.
- Best composite score so far: A 0.7050, B 0.5468 (generation 45871).
- Honeypot genome voided: True. Ledger chain intact: True (554772 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 92086; effective independent trials (clustered): 55254.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3172 | 302 | 1 | 5.4% |
| ATOM_DROP | 936 | 142 | 0 | 5.9% |
| ATOM_SWAP | 7320 | 557 | 1 | 13.1% |
| ENSEMBLE | 517 | 42 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 4083 | 531 | 2 | 7.6% |
| EXIT_TRANSPLANT | 3904 | 439 | 5 | 7.4% |
| INVERT | 1409 | 55 | 0 | 3.3% |
| LIBRARY_PROBE | 11239 | 784 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 6789 | 1209 | 1 | 20.5% |
| SIMPLIFY | 884 | 142 | 0 | 6.0% |
| SLOT_CROSSOVER | 5718 | 794 | 4 | 11.6% |
