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
- Occupied archive cells: island A 61, island B 69.
- Best composite score so far: A 0.1415, B 0.2380 (generation 942).
- Honeypot genome voided: True. Ledger chain intact: True (12000 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 2000; effective independent trials (clustered): 1200.
- Hall of fame: {'bronze': 0, 'silver': 0, 'gold': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 16 | 1 | 0 | 5.5% |
| ATOM_DROP | 7 | 0 | 0 | 5.5% |
| ATOM_SWAP | 64 | 6 | 0 | 13.7% |
| ENSEMBLE | 0 | 0 | 0 | 4.5% |
| ENTRY_TRANSPLANT | 34 | 4 | 0 | 7.7% |
| EXIT_TRANSPLANT | 30 | 1 | 0 | 6.8% |
| INVERT | 16 | 1 | 0 | 3.7% |
| LIBRARY_PROBE | 732 | 17 | 0 | 3.2% |
| LLM_HYPOTHESIS | 0 | 0 | 0 | 12.0% |
| PARAM_STEP | 62 | 10 | 0 | 20.2% |
| SIMPLIFY | 3 | 0 | 0 | 6.3% |
| SLOT_CROSSOVER | 36 | 3 | 0 | 10.9% |
