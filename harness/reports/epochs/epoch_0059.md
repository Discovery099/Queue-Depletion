# Epoch 59 report

- Generations completed: 29500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 29001 to 29500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 286, island B 297.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (355814 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 59086; effective independent trials (clustered): 35453.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 2126 | 188 | 0 | 5.5% |
| ATOM_DROP | 559 | 80 | 0 | 6.0% |
| ATOM_SWAP | 4730 | 378 | 1 | 13.5% |
| ENSEMBLE | 243 | 20 | 0 | 2.7% |
| ENTRY_TRANSPLANT | 2580 | 325 | 0 | 7.8% |
| EXIT_TRANSPLANT | 2475 | 268 | 1 | 7.6% |
| INVERT | 894 | 26 | 0 | 3.3% |
| LIBRARY_PROBE | 7584 | 552 | 0 | 3.6% |
| LLM_HYPOTHESIS | 19 | 8 | 0 | 11.5% |
| PARAM_STEP | 4275 | 724 | 0 | 20.8% |
| SIMPLIFY | 501 | 75 | 0 | 6.1% |
| SLOT_CROSSOVER | 3514 | 448 | 2 | 11.7% |
