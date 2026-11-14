# Epoch 20 report

- Generations completed: 10000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 9501 to 10000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 224, island B 198.
- Best composite score so far: A 0.5290, B 0.5468 (generation 8637).
- Honeypot genome voided: True. Ledger chain intact: True (121324 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 20100; effective independent trials (clustered): 12062.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 641 | 87 | 0 | 5.9% |
| ATOM_DROP | 201 | 27 | 0 | 5.9% |
| ATOM_SWAP | 1507 | 145 | 0 | 13.8% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 807 | 107 | 0 | 7.8% |
| EXIT_TRANSPLANT | 737 | 82 | 0 | 7.5% |
| INVERT | 314 | 11 | 0 | 3.3% |
| LIBRARY_PROBE | 3437 | 280 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.2% |
| PARAM_STEP | 1186 | 199 | 0 | 20.6% |
| SIMPLIFY | 167 | 22 | 0 | 5.9% |
| SLOT_CROSSOVER | 993 | 140 | 0 | 11.9% |
