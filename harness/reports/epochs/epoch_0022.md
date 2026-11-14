# Epoch 22 report

- Generations completed: 11000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 10501 to 11000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 232, island B 208.
- Best composite score so far: A 0.5290, B 0.5468 (generation 8637).
- Honeypot genome voided: True. Ledger chain intact: True (133324 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 22100; effective independent trials (clustered): 13260.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 706 | 91 | 0 | 5.8% |
| ATOM_DROP | 219 | 30 | 0 | 5.9% |
| ATOM_SWAP | 1682 | 161 | 0 | 13.8% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 915 | 124 | 0 | 7.8% |
| EXIT_TRANSPLANT | 822 | 85 | 0 | 7.4% |
| INVERT | 339 | 11 | 0 | 3.3% |
| LIBRARY_PROBE | 3668 | 299 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.2% |
| PARAM_STEP | 1341 | 232 | 0 | 20.7% |
| SIMPLIFY | 188 | 26 | 0 | 5.9% |
| SLOT_CROSSOVER | 1110 | 159 | 0 | 11.9% |
