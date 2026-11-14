# Epoch 2 report

- Generations completed: 1000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 501 to 1000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 62, island B 70.
- Best composite score so far: A 0.4187, B 0.3267 (generation 781).
- Honeypot genome voided: True. Ledger chain intact: True (13216 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 2100; effective independent trials (clustered): 1260.
- Hall of fame: {'bronze': 0, 'silver': 0, 'gold': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 20 | 4 | 0 | 6.2% |
| ATOM_DROP | 9 | 2 | 0 | 6.6% |
| ATOM_SWAP | 60 | 10 | 0 | 14.4% |
| ENSEMBLE | 0 | 0 | 0 | 4.3% |
| ENTRY_TRANSPLANT | 36 | 4 | 0 | 7.2% |
| EXIT_TRANSPLANT | 30 | 4 | 0 | 7.4% |
| INVERT | 17 | 2 | 0 | 3.7% |
| LIBRARY_PROBE | 780 | 59 | 0 | 3.3% |
| LLM_HYPOTHESIS | 0 | 0 | 0 | 11.3% |
| PARAM_STEP | 4 | 0 | 0 | 18.9% |
| SIMPLIFY | 8 | 1 | 0 | 6.0% |
| SLOT_CROSSOVER | 36 | 4 | 0 | 10.7% |
