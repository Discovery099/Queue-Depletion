# Epoch 24 report

- Generations completed: 12000
- Best certified tier: none
- Vault queries used: 0 of 60 (Vault-A), 0 of 5 (Vault-B)
- Pipeline false-discovery rate, latest placebo run: not yet run

Generations 11501 to 12000.

| Outcome | Count |
|---|---|
| STAGE1_FAIL | 500 |

- Stage 1 pass rate: 0.00%.
- Canary adoption among stage 1 passes: 0.00% (0 genomes).
- Occupied archive cells: island A 238, island B 221.
- Best composite score so far: A 0.5290, B 0.5468 (generation 8637).
- Honeypot genome voided: True. Ledger chain intact: True (145324 records). Frozen files unchanged: True.
- Raw stage 1 trials to date: 24100; effective independent trials (clustered): 14461.
- Hall of fame: {'bronze': 0, 'gold': 0, 'silver': 0}. Stage 3 candidates outside the 10% false-discovery set: none.

## Operators

| Operator | Uses | Improved on parent | Stage 1 passes | Share next epoch |
|---|---|---|---|---|
| ATOM_ADD | 807 | 94 | 0 | 5.7% |
| ATOM_DROP | 231 | 32 | 0 | 5.9% |
| ATOM_SWAP | 1859 | 175 | 0 | 13.8% |
| ENSEMBLE | 0 | 0 | 0 | 4.6% |
| ENTRY_TRANSPLANT | 993 | 131 | 0 | 7.8% |
| EXIT_TRANSPLANT | 916 | 98 | 0 | 7.5% |
| INVERT | 376 | 11 | 0 | 3.3% |
| LIBRARY_PROBE | 3879 | 319 | 0 | 3.6% |
| LLM_HYPOTHESIS | 10 | 2 | 0 | 9.3% |
| PARAM_STEP | 1487 | 254 | 0 | 20.7% |
| SIMPLIFY | 204 | 27 | 0 | 5.9% |
| SLOT_CROSSOVER | 1238 | 179 | 0 | 11.9% |
