# Epoch 77 report

- Generations completed: 38500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 38001 to 38500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 293, island B 306.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (464568 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 77086; effective independent trials (clustered): 46254.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 2697 | 257 | 0 | 5.4% |
| ATOM_DROP | 759 | 111 | 0 | 5.9% |
| ATOM_SWAP | 6114 | 463 | 1 | 13.1% |
| ENSEMBLE | 426 | 34 | 0 | 2.7% |
| ENTRY_TRANSPLANT | 3414 | 437 | 0 | 7.6% |
| EXIT_TRANSPLANT | 3272 | 356 | 2 | 7.4% |
| INVERT | 1174 | 39 | 0 | 3.2% |
| LIBRARY_PROBE | 9556 | 674 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 5647 | 981 | 0 | 20.5% |
| SIMPLIFY | 695 | 112 | 0 | 6.0% |
| SLOT_CROSSOVER | 4717 | 608 | 4 | 11.5% |
