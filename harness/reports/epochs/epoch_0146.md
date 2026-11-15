# Epoch 146 report

- Generations completed: 73000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 72501 to 73000.

| Outcome | Count |
|---|---|
| HOME_ONLY | 3 |
| STAGE1_FAIL | 497 |

- Stage 1 pass rate: 0.60%.
- Canary adoption among stage 1 passes: 66.67% (2 genomes).
- Occupied archive cells: island A 325, island B 316.
- Best composite score so far: A 0.7610, B 0.7245 (generation 70498).
- Honeypot genome voided: True. Ledger chain intact: True (880144 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 146086; effective independent trials (clustered): 87653.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 4914 | 483 | 1 | 5.4% |
| ATOM_DROP | 1769 | 306 | 0 | 6.1% |
| ATOM_SWAP | 11370 | 849 | 8 | 12.9% |
| ENSEMBLE | 785 | 71 | 1 | 2.7% |
| ENTRY_TRANSPLANT | 6575 | 893 | 9 | 7.6% |
| EXIT_TRANSPLANT | 6182 | 821 | 14 | 7.6% |
| INVERT | 2247 | 97 | 0 | 3.3% |
| LIBRARY_PROBE | 17148 | 1085 | 0 | 3.4% |
| LLM_HYPOTHESIS | 29 | 17 | 0 | 13.0% |
| PARAM_STEP | 10960 | 2002 | 1 | 20.5% |
| SIMPLIFY | 1546 | 227 | 0 | 5.8% |
| SLOT_CROSSOVER | 9475 | 1417 | 9 | 11.7% |

## Monitor notes

- canary adoption above 2%: promotion halted for this epoch pending tightening (SPEC 15.1)
