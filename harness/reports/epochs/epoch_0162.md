# Epoch 162 report

- Generations completed: 81000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 80501 to 81000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 326, island B 318.
- Best composite score so far: A 0.7610, B 0.7660 (generation 80566).
- Honeypot genome voided: True. Ledger chain intact: True (976348 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 162086; effective independent trials (clustered): 97254.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 5428 | 533 | 1 | 5.4% |
| ATOM_DROP | 2033 | 368 | 1 | 6.1% |
| ATOM_SWAP | 12632 | 944 | 9 | 12.9% |
| ENSEMBLE | 839 | 75 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 7335 | 1012 | 10 | 7.6% |
| EXIT_TRANSPLANT | 6843 | 941 | 17 | 7.6% |
| INVERT | 2483 | 114 | 0 | 3.3% |
| LIBRARY_PROBE | 18937 | 1168 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 12152 | 2237 | 1 | 20.5% |
| SIMPLIFY | 1738 | 249 | 0 | 5.8% |
| SLOT_CROSSOVER | 10551 | 1628 | 10 | 11.8% |
