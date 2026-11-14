# Epoch 95 report

- Generations completed: 47500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 47001 to 47500.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 311, island B 307.
- Best composite score so far: A 0.7338, B 0.5468 (generation 47013).
- Honeypot genome voided: True. Ledger chain intact: True (572836 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 95086; effective independent trials (clustered): 57053.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3284 | 319 | 1 | 5.4% |
| ATOM_DROP | 976 | 149 | 0 | 5.9% |
| ATOM_SWAP | 7550 | 572 | 1 | 13.1% |
| ENSEMBLE | 534 | 45 | 0 | 2.7% |
| ENTRY_TRANSPLANT | 4211 | 543 | 3 | 7.6% |
| EXIT_TRANSPLANT | 4035 | 455 | 6 | 7.4% |
| INVERT | 1444 | 56 | 0 | 3.3% |
| LIBRARY_PROBE | 11575 | 799 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 7017 | 1256 | 1 | 20.5% |
| SIMPLIFY | 918 | 148 | 0 | 6.0% |
| SLOT_CROSSOVER | 5927 | 828 | 4 | 11.6% |
