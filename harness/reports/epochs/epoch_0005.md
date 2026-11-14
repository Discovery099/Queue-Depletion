# Epoch 5 report

- Generations completed: 2500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 2001 to 2500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 83, island B 83.
- Best composite score so far: A 0.4187, B 0.3901 (generation 2160).
- Honeypot genome voided: True. Ledger chain intact: True (31228 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 5100; effective independent trials (clustered): 3060.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 76 | 13 | 0 | 6.3% |
| ATOM_DROP | 27 | 8 | 0 | 7.5% |
| ATOM_SWAP | 221 | 24 | 0 | 14.2% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 125 | 18 | 0 | 8.0% |
| EXIT_TRANSPLANT | 112 | 16 | 0 | 8.0% |
| INVERT | 46 | 2 | 0 | 3.5% |
| LIBRARY_PROBE | 1714 | 141 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 12 | 0 | 0 | 17.6% |
| SIMPLIFY | 23 | 3 | 0 | 6.1% |
| SLOT_CROSSOVER | 134 | 14 | 0 | 11.3% |
