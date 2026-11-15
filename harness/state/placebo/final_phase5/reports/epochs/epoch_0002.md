# Epoch 2 report

- Generations completed: 1000 (PLACEBO RUN ON DECOY MARKETS)
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 501 to 1000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 65, island B 66.
- Best composite score so far: A 0.1871, B 0.3283 (generation 942).
- Honeypot genome voided: True. Ledger chain intact: True (12000 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 2000; effective independent trials (clustered): 1200.
- Hall of fame: {'bronze': 0, 'silver': 0, 'gold': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 18 | 2 | 0 | 5.8% |
| ATOM_DROP | 8 | 0 | 0 | 5.3% |
| ATOM_SWAP | 62 | 10 | 0 | 14.9% |
| ENSEMBLE | 0 | 0 | 0 | 4.4% |
| ENTRY_TRANSPLANT | 37 | 2 | 0 | 6.8% |
| EXIT_TRANSPLANT | 27 | 2 | 0 | 7.2% |
| INVERT | 19 | 1 | 0 | 3.5% |
| LIBRARY_PROBE | 728 | 28 | 0 | 3.2% |
| LLM_HYPOTHESIS | 0 | 0 | 0 | 11.9% |
| PARAM_STEP | 61 | 10 | 0 | 20.0% |
| SIMPLIFY | 6 | 0 | 0 | 5.6% |
| SLOT_CROSSOVER | 34 | 4 | 0 | 11.4% |
