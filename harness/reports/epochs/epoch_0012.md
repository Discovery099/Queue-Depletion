# Epoch 12 report

- Generations completed: 6000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 5501 to 6000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 179, island B 142.
- Best composite score so far: A 0.4434, B 0.5468 (generation 5480).
- Honeypot genome voided: True. Ledger chain intact: True (73228 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 12100; effective independent trials (clustered): 7261.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 366 | 55 | 0 | 6.0% |
| ATOM_DROP | 112 | 17 | 0 | 6.1% |
| ATOM_SWAP | 812 | 77 | 0 | 13.8% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 452 | 61 | 0 | 7.9% |
| EXIT_TRANSPLANT | 409 | 49 | 0 | 7.7% |
| INVERT | 169 | 7 | 0 | 3.4% |
| LIBRARY_PROBE | 2551 | 207 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 529 | 77 | 0 | 20.0% |
| SIMPLIFY | 78 | 11 | 0 | 6.0% |
| SLOT_CROSSOVER | 512 | 63 | 0 | 11.6% |
