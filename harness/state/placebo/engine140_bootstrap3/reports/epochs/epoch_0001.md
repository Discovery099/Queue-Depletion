# Epoch 1 report

- Generations completed: 500 (PLACEBO RUN ON DECOY MARKETS)
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 1 to 500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 57, island B 59.
- Best composite score so far: A 0.1415, B 0.1748 (generation 402).
- Honeypot genome voided: True. Ledger chain intact: True (6000 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 1000; effective independent trials (clustered): 599.
- Hall of fame: {'bronze': 0, 'silver': 0, 'gold': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 9 | 1 | 0 | 5.8% |
| ATOM_DROP | 2 | 0 | 0 | 6.4% |
| ATOM_SWAP | 32 | 6 | 0 | 15.0% |
| ENSEMBLE | 0 | 0 | 0 | 4.2% |
| ENTRY_TRANSPLANT | 23 | 3 | 0 | 7.5% |
| EXIT_TRANSPLANT | 16 | 1 | 0 | 6.9% |
| INVERT | 7 | 1 | 0 | 4.1% |
| LIBRARY_PROBE | 357 | 9 | 0 | 3.0% |
| LLM_HYPOTHESIS | 0 | 0 | 0 | 11.3% |
| PARAM_STEP | 33 | 2 | 0 | 16.6% |
| SIMPLIFY | 0 | 0 | 0 | 8.5% |
| SLOT_CROSSOVER | 21 | 2 | 0 | 10.7% |
