# Epoch 8 report

- Generations completed: 4000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 3501 to 4000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 127, island B 108.
- Best composite score so far: A 0.4406, B 0.4655 (generation 3714).
- Honeypot genome voided: True. Ledger chain intact: True (49228 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 8100; effective independent trials (clustered): 4862.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 209 | 32 | 0 | 6.1% |
| ATOM_DROP | 55 | 10 | 0 | 6.4% |
| ATOM_SWAP | 487 | 49 | 0 | 14.0% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 273 | 37 | 0 | 7.9% |
| EXIT_TRANSPLANT | 229 | 24 | 0 | 7.5% |
| INVERT | 101 | 4 | 0 | 3.4% |
| LIBRARY_PROBE | 2099 | 170 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 196 | 26 | 0 | 19.7% |
| SIMPLIFY | 51 | 7 | 0 | 6.0% |
| SLOT_CROSSOVER | 290 | 34 | 0 | 11.5% |
