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
- Occupied archive cells: island A 60, island B 54.
- Best composite score so far: A 0.1840, B 0.1836 (generation 131).
- Honeypot genome voided: True. Ledger chain intact: True (6000 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 1000; effective independent trials (clustered): 600.
- Hall of fame: {'bronze': 0, 'silver': 0, 'gold': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 10 | 1 | 0 | 5.7% |
| ATOM_DROP | 6 | 0 | 0 | 5.3% |
| ATOM_SWAP | 29 | 5 | 0 | 14.8% |
| ENSEMBLE | 0 | 0 | 0 | 4.3% |
| ENTRY_TRANSPLANT | 24 | 1 | 0 | 6.6% |
| EXIT_TRANSPLANT | 15 | 2 | 0 | 7.7% |
| INVERT | 7 | 1 | 0 | 4.1% |
| LIBRARY_PROBE | 354 | 16 | 0 | 3.1% |
| LLM_HYPOTHESIS | 0 | 0 | 0 | 11.4% |
| PARAM_STEP | 32 | 5 | 0 | 19.2% |
| SIMPLIFY | 2 | 0 | 0 | 6.4% |
| SLOT_CROSSOVER | 21 | 3 | 0 | 11.5% |
