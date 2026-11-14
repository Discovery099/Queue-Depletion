# Epoch 84 report

- Generations completed: 42000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 41501 to 42000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 301, island B 306.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (506620 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 84086; effective independent trials (clustered): 50453.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 2922 | 275 | 0 | 5.4% |
| ATOM_DROP | 833 | 124 | 0 | 5.9% |
| ATOM_SWAP | 6679 | 509 | 1 | 13.1% |
| ENSEMBLE | 463 | 35 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 3745 | 486 | 1 | 7.6% |
| EXIT_TRANSPLANT | 3568 | 393 | 2 | 7.4% |
| INVERT | 1278 | 51 | 0 | 3.3% |
| LIBRARY_PROBE | 10350 | 725 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 6170 | 1091 | 0 | 20.5% |
| SIMPLIFY | 780 | 123 | 0 | 6.0% |
| SLOT_CROSSOVER | 5183 | 700 | 4 | 11.6% |
