# Epoch 45 report

- Generations completed: 22500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 22001 to 22500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 271, island B 288.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (271710 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 45086; effective independent trials (clustered): 27053.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1600 | 152 | 0 | 5.5% |
| ATOM_DROP | 423 | 60 | 0 | 6.0% |
| ATOM_SWAP | 3615 | 302 | 0 | 13.6% |
| ENSEMBLE | 75 | 4 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 1934 | 237 | 0 | 7.7% |
| EXIT_TRANSPLANT | 1843 | 203 | 0 | 7.6% |
| INVERT | 691 | 23 | 0 | 3.3% |
| LIBRARY_PROBE | 6135 | 467 | 0 | 3.6% |
| LLM_HYPOTHESIS | 19 | 8 | 0 | 11.5% |
| PARAM_STEP | 3188 | 560 | 0 | 20.9% |
| SIMPLIFY | 377 | 56 | 0 | 6.0% |
| SLOT_CROSSOVER | 2600 | 331 | 2 | 11.7% |
