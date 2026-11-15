# Epoch 147 report

- Generations completed: 73500
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 73001 to 73500.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 325, island B 316.
- Best composite score so far: A 0.7610, B 0.7465 (generation 73424).
- Honeypot genome voided: True. Ledger chain intact: True (886144 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 147086; effective independent trials (clustered): 66191.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4950 | 484 | 1 | 5.4% |
| ATOM_DROP | 1785 | 311 | 0 | 6.1% |
| ATOM_SWAP | 11449 | 855 | 8 | 12.9% |
| ENSEMBLE | 788 | 72 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 6618 | 901 | 9 | 7.6% |
| EXIT_TRANSPLANT | 6215 | 828 | 14 | 7.6% |
| INVERT | 2255 | 97 | 0 | 3.3% |
| LIBRARY_PROBE | 17271 | 1095 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 11050 | 2022 | 1 | 20.5% |
| SIMPLIFY | 1561 | 228 | 0 | 5.8% |
| SLOT_CROSSOVER | 9529 | 1426 | 9 | 11.7% |
