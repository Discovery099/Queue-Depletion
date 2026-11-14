# Epoch 4 report

- Generations completed: 2000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 1501 to 2000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 73, island B 79.
- Best composite score so far: A 0.4187, B 0.3441 (generation 1040).
- Honeypot genome voided: True. Ledger chain intact: True (25216 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 4100; effective independent trials (clustered): 2461.
- Hall of fame: {'bronze': 0, 'silver': 0, 'gold': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 38 | 6 | 0 | 6.0% |
| ATOM_DROP | 17 | 4 | 0 | 6.7% |
| ATOM_SWAP | 123 | 15 | 0 | 13.9% |
| ENSEMBLE | 0 | 0 | 0 | 4.4% |
| ENTRY_TRANSPLANT | 68 | 8 | 0 | 7.4% |
| EXIT_TRANSPLANT | 68 | 10 | 0 | 7.7% |
| INVERT | 30 | 2 | 0 | 3.5% |
| LIBRARY_PROBE | 1550 | 125 | 0 | 3.4% |
| LLM_HYPOTHESIS | 0 | 0 | 0 | 11.8% |
| PARAM_STEP | 7 | 0 | 0 | 18.0% |
| SIMPLIFY | 18 | 3 | 0 | 6.2% |
| SLOT_CROSSOVER | 81 | 9 | 0 | 11.0% |
