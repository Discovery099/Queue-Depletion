# Epoch 87 report

- Generations completed: 43500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 43001 to 43500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 302, island B 307.
- Best composite score so far: A 0.6862, B 0.5468 (generation 43033).
- Honeypot genome voided: True. Ledger chain intact: True (524684 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 87086; effective independent trials (clustered): 52253.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 3025 | 287 | 0 | 5.4% |
| ATOM_DROP | 870 | 129 | 0 | 5.9% |
| ATOM_SWAP | 6907 | 528 | 1 | 13.1% |
| ENSEMBLE | 480 | 35 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 3880 | 506 | 1 | 7.6% |
| EXIT_TRANSPLANT | 3706 | 414 | 3 | 7.4% |
| INVERT | 1322 | 51 | 0 | 3.3% |
| LIBRARY_PROBE | 10679 | 744 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 6402 | 1136 | 1 | 20.5% |
| SIMPLIFY | 816 | 129 | 0 | 6.0% |
| SLOT_CROSSOVER | 5384 | 731 | 4 | 11.6% |
