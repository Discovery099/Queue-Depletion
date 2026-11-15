# Epoch 178 report

- Generations completed: 89000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 88501 to 89000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 327, island B 319.
- Best composite score so far: A 0.7640, B 0.7879 (generation 88594).
- Honeypot genome voided: True. Ledger chain intact: True (1072552 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 178086; effective independent trials (clustered): 106853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 5951 | 583 | 1 | 5.4% |
| ATOM_DROP | 2278 | 426 | 1 | 6.2% |
| ATOM_SWAP | 13888 | 1025 | 10 | 12.9% |
| ENSEMBLE | 886 | 82 | 2 | 2.7% |
| ENTRY_TRANSPLANT | 8063 | 1108 | 13 | 7.6% |
| EXIT_TRANSPLANT | 7494 | 1052 | 19 | 7.7% |
| INVERT | 2721 | 135 | 0 | 3.3% |
| LIBRARY_PROBE | 20788 | 1266 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 12.9% |
| PARAM_STEP | 13338 | 2410 | 1 | 20.4% |
| SIMPLIFY | 1914 | 273 | 0 | 5.8% |
| SLOT_CROSSOVER | 11650 | 1827 | 10 | 11.8% |
