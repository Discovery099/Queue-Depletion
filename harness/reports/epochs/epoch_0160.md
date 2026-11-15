# Epoch 160 report

- Generations completed: 80000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 79501 to 80000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 3 |
| STAGE1_FAIL | 497 |

- Stage 1 pass rate: 0.60%.
- Canary adoption among stage 1 passes: 33.33% (1 genomes).
- Occupied archive cells: island A 326, island B 317.
- Best composite score so far: A 0.7610, B 0.7655 (generation 73770).
- Honeypot genome voided: True. Ledger chain intact: True (964312 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 160086; effective independent trials (clustered): 96053.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 5367 | 526 | 1 | 5.4% |
| ATOM_DROP | 1997 | 362 | 1 | 6.1% |
| ATOM_SWAP | 12471 | 935 | 9 | 12.9% |
| ENSEMBLE | 836 | 75 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 7233 | 998 | 10 | 7.6% |
| EXIT_TRANSPLANT | 6763 | 931 | 15 | 7.6% |
| INVERT | 2455 | 112 | 0 | 3.3% |
| LIBRARY_PROBE | 18698 | 1158 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 12009 | 2208 | 1 | 20.5% |
| SIMPLIFY | 1713 | 246 | 0 | 5.8% |
| SLOT_CROSSOVER | 10429 | 1608 | 9 | 11.8% |

## Monitor notes

- canary adoption above 2%: promotion halted for this epoch pending tightening (SPEC 15.1)
