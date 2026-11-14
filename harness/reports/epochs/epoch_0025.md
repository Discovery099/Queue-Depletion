# Epoch 25 report

- Generations completed: 12500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 12001 to 12500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 242, island B 228.
- Best composite score so far: A 0.5291, B 0.5468 (generation 12147).
- Honeypot genome voided: True. Ledger chain intact: True (151324 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 25100; effective independent trials (clustered): 11297.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 846 | 97 | 0 | 5.7% |
| ATOM_DROP | 239 | 32 | 0 | 5.9% |
| ATOM_SWAP | 1940 | 184 | 0 | 13.8% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 1034 | 135 | 0 | 7.8% |
| EXIT_TRANSPLANT | 957 | 104 | 0 | 7.5% |
| INVERT | 393 | 11 | 0 | 3.3% |
| LIBRARY_PROBE | 3990 | 327 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 1575 | 274 | 0 | 20.8% |
| SIMPLIFY | 208 | 27 | 0 | 5.9% |
| SLOT_CROSSOVER | 1308 | 187 | 0 | 11.9% |
