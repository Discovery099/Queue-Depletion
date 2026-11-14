# Epoch 28 report

- Generations completed: 14000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 13501 to 14000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 250, island B 244.
- Best composite score so far: A 0.5341, B 0.5468 (generation 13159).
- Honeypot genome voided: True. Ledger chain intact: True (169324 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 28100; effective independent trials (clustered): 16862.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 959 | 108 | 0 | 5.7% |
| ATOM_DROP | 269 | 34 | 0 | 5.8% |
| ATOM_SWAP | 2203 | 212 | 0 | 13.8% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 1160 | 151 | 0 | 7.8% |
| EXIT_TRANSPLANT | 1078 | 117 | 0 | 7.5% |
| INVERT | 436 | 13 | 0 | 3.3% |
| LIBRARY_PROBE | 4325 | 350 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 1825 | 317 | 0 | 20.8% |
| SIMPLIFY | 234 | 32 | 0 | 5.9% |
| SLOT_CROSSOVER | 1501 | 208 | 0 | 11.8% |
