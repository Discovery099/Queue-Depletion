# Epoch 16 report

- Generations completed: 8000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 7501 to 8000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 205, island B 174.
- Best composite score so far: A 0.4975, B 0.5468 (generation 7677).
- Honeypot genome voided: True. Ledger chain intact: True (97228 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 16100; effective independent trials (clustered): 9663.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 494 | 69 | 0 | 6.0% |
| ATOM_DROP | 151 | 21 | 0 | 6.0% |
| ATOM_SWAP | 1188 | 108 | 0 | 13.8% |
| ENSEMBLE | 0 | 0 | 0 | 4.7% |
| ENTRY_TRANSPLANT | 637 | 85 | 0 | 7.9% |
| EXIT_TRANSPLANT | 559 | 63 | 0 | 7.6% |
| INVERT | 252 | 9 | 0 | 3.3% |
| LIBRARY_PROBE | 2996 | 241 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 851 | 122 | 0 | 20.0% |
| SIMPLIFY | 117 | 17 | 0 | 6.1% |
| SLOT_CROSSOVER | 745 | 102 | 0 | 11.9% |
