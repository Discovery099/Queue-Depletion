# Epoch 50 report

- Generations completed: 25000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 24501 to 25000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 279, island B 289.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (301750 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 50086; effective independent trials (clustered): 30054.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1796 | 163 | 0 | 5.5% |
| ATOM_DROP | 473 | 66 | 0 | 6.0% |
| ATOM_SWAP | 4034 | 332 | 0 | 13.6% |
| ENSEMBLE | 136 | 10 | 0 | 2.7% |
| ENTRY_TRANSPLANT | 2157 | 266 | 0 | 7.7% |
| EXIT_TRANSPLANT | 2072 | 226 | 0 | 7.6% |
| INVERT | 766 | 24 | 0 | 3.3% |
| LIBRARY_PROBE | 6642 | 498 | 0 | 3.6% |
| LLM_HYPOTHESIS | 19 | 8 | 0 | 11.5% |
| PARAM_STEP | 3566 | 606 | 0 | 20.8% |
| SIMPLIFY | 409 | 62 | 0 | 6.1% |
| SLOT_CROSSOVER | 2930 | 380 | 2 | 11.7% |
