# Epoch 200 report

- Generations completed: 100000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 99501 to 100000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 327, island B 322.
- Best composite score so far: A 0.7640, B 0.7879 (generation 88594).
- Honeypot genome voided: True. Ledger chain intact: True (1204860 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 200086; effective independent trials (clustered): 120053.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 6642 | 656 | 1 | 5.4% |
| ATOM_DROP | 2645 | 493 | 1 | 6.2% |
| ATOM_SWAP | 15594 | 1118 | 10 | 12.8% |
| ENSEMBLE | 935 | 87 | 2 | 2.7% |
| ENTRY_TRANSPLANT | 9048 | 1268 | 16 | 7.7% |
| EXIT_TRANSPLANT | 8374 | 1230 | 22 | 7.7% |
| INVERT | 3047 | 147 | 0 | 3.3% |
| LIBRARY_PROBE | 23305 | 1391 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 12.9% |
| PARAM_STEP | 15011 | 2693 | 4 | 20.3% |
| SIMPLIFY | 2147 | 309 | 0 | 5.8% |
| SLOT_CROSSOVER | 13223 | 2093 | 10 | 11.8% |
