# Epoch 158 report

- Generations completed: 79000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 78501 to 79000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 326, island B 317.
- Best composite score so far: A 0.7610, B 0.7655 (generation 73770).
- Honeypot genome voided: True. Ledger chain intact: True (952236 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 158086; effective independent trials (clustered): 94853.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 5309 | 520 | 1 | 5.4% |
| ATOM_DROP | 1956 | 349 | 1 | 6.1% |
| ATOM_SWAP | 12302 | 920 | 8 | 12.9% |
| ENSEMBLE | 829 | 74 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 7125 | 976 | 9 | 7.6% |
| EXIT_TRANSPLANT | 6673 | 919 | 14 | 7.6% |
| INVERT | 2427 | 109 | 0 | 3.3% |
| LIBRARY_PROBE | 18484 | 1146 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 11868 | 2188 | 1 | 20.5% |
| SIMPLIFY | 1693 | 243 | 0 | 5.8% |
| SLOT_CROSSOVER | 10305 | 1586 | 9 | 11.8% |
