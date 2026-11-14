# Epoch 10 report

- Generations completed: 5000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 4501 to 5000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 155, island B 127.
- Best composite score so far: A 0.4434, B 0.4655 (generation 4267).
- Honeypot genome voided: True. Ledger chain intact: True (61228 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 10100; effective independent trials (clustered): 6061.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 298 | 46 | 0 | 6.1% |
| ATOM_DROP | 79 | 13 | 0 | 6.2% |
| ATOM_SWAP | 653 | 62 | 0 | 13.8% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 368 | 50 | 0 | 7.9% |
| EXIT_TRANSPLANT | 322 | 38 | 0 | 7.7% |
| INVERT | 132 | 6 | 0 | 3.4% |
| LIBRARY_PROBE | 2321 | 192 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 356 | 48 | 0 | 19.7% |
| SIMPLIFY | 69 | 10 | 0 | 6.1% |
| SLOT_CROSSOVER | 392 | 49 | 0 | 11.6% |
