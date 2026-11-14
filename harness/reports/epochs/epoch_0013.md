# Epoch 13 report

- Generations completed: 6500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 6001 to 6500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 187, island B 149.
- Best composite score so far: A 0.4434, B 0.5468 (generation 5480).
- Honeypot genome voided: True. Ledger chain intact: True (79228 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 13100; effective independent trials (clustered): 7861.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 402 | 59 | 0 | 6.0% |
| ATOM_DROP | 124 | 18 | 0 | 6.0% |
| ATOM_SWAP | 913 | 84 | 0 | 13.8% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 502 | 65 | 0 | 7.8% |
| EXIT_TRANSPLANT | 442 | 51 | 0 | 7.6% |
| INVERT | 181 | 9 | 0 | 3.4% |
| LIBRARY_PROBE | 2659 | 219 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 604 | 87 | 0 | 20.0% |
| SIMPLIFY | 92 | 14 | 0 | 6.1% |
| SLOT_CROSSOVER | 571 | 72 | 0 | 11.7% |
