# Epoch 72 report

- Generations completed: 36000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 35501 to 36000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 1 |
| STAGE1_FAIL | 499 |

- Stage 1 pass rate: 0.20%.
- Canary adoption among stage 1 passes: 100.00% (1 genomes).
- Occupied archive cells: island A 290, island B 303.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (434528 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 72086; effective independent trials (clustered): 43253.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 2541 | 235 | 0 | 5.4% |
| ATOM_DROP | 708 | 102 | 0 | 5.9% |
| ATOM_SWAP | 5703 | 439 | 1 | 13.2% |
| ENSEMBLE | 387 | 29 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 3204 | 411 | 0 | 7.6% |
| EXIT_TRANSPLANT | 3029 | 337 | 2 | 7.4% |
| INVERT | 1096 | 36 | 0 | 3.2% |
| LIBRARY_PROBE | 9025 | 643 | 0 | 3.5% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.1% |
| PARAM_STEP | 5278 | 911 | 0 | 20.5% |
| SIMPLIFY | 637 | 102 | 0 | 6.0% |
| SLOT_CROSSOVER | 4363 | 559 | 4 | 11.5% |

## Monitor notes

- canary adoption above 2%: promotion halted for this epoch pending tightening (SPEC 15.1)
