# Epoch 46 report

- Generations completed: 23000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: 0 Bronze, 0 Silver, 0 Gold in 1000 placebo generations

Generations 22501 to 23000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 275, island B 288.
- Best composite score so far: A 0.6711, B 0.5468 (generation 21335).
- Honeypot genome voided: True. Ledger chain intact: True (277710 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 46086; effective independent trials (clustered): 27653.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 1623 | 153 | 0 | 5.5% |
| ATOM_DROP | 433 | 61 | 0 | 6.0% |
| ATOM_SWAP | 3697 | 313 | 0 | 13.6% |
| ENSEMBLE | 92 | 5 | 0 | 2.6% |
| ENTRY_TRANSPLANT | 1968 | 242 | 0 | 7.7% |
| EXIT_TRANSPLANT | 1891 | 208 | 0 | 7.6% |
| INVERT | 703 | 23 | 0 | 3.3% |
| LIBRARY_PROBE | 6251 | 474 | 0 | 3.6% |
| LLM_HYPOTHESIS | 19 | 8 | 0 | 11.5% |
| PARAM_STEP | 3271 | 571 | 0 | 20.9% |
| SIMPLIFY | 384 | 57 | 0 | 6.0% |
| SLOT_CROSSOVER | 2668 | 346 | 2 | 11.7% |
