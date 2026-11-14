# Epoch 14 report

- Generations completed: 7000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 6501 to 7000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 193, island B 156.
- Best composite score so far: A 0.4434, B 0.5468 (generation 5480).
- Honeypot genome voided: True. Ledger chain intact: True (85228 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 14100; effective independent trials (clustered): 8462.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 423 | 60 | 0 | 6.0% |
| ATOM_DROP | 128 | 18 | 0 | 6.0% |
| ATOM_SWAP | 1008 | 93 | 0 | 13.8% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 547 | 73 | 0 | 7.9% |
| EXIT_TRANSPLANT | 497 | 59 | 0 | 7.7% |
| INVERT | 207 | 9 | 0 | 3.4% |
| LIBRARY_PROBE | 2773 | 225 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 677 | 96 | 0 | 19.9% |
| SIMPLIFY | 102 | 14 | 0 | 6.0% |
| SLOT_CROSSOVER | 628 | 84 | 0 | 11.8% |
