# Understanding of the specification (B.1 step 1)

## Mission

Search for, harden and certify an ES and YM futures strategy whose 80% win rate comes from entry skill, proved against a
random-entry twin, and that also holds profit factor, payoff, trade frequency, timeframe, instrument and unseen-data
requirements at the same time (the Gold vector, SPEC 2.1). Start from the owner's Smart Trend V1 but treat it as a starting
point only. Use about 16,000 library scripts as a source of ideas, never of code. Run up to 100,000 generations, save each in
its own folder, and report truthfully whatever is found, including nothing.

## The five framing facts (SPEC 1.2), as held here

1. **The baseline is far from the target.** Reproduced in Generation 0: about 35 to 36% winners and a profit factor between
   0.93 and 1.03 at 5 minutes with about 564 trades a year per instrument (`baseline/reference_metrics.json`). Tuning it cannot
   reach 80%; the payoff geometry has to change.
2. **Win rate alone is the easiest metric to fake.** A wide stop and a near target win most trades with no edge. Every win rate
   is reported with its geometry baseline and its alpha; a strategy that reaches its headline by geometry is a failure.
3. **100,000 trials on one dataset is the largest overfitting risk.** Every backtest is logged before its result is read, and the
   statistical gates use the trial count as it grows.
4. **The 30% holdout survives only if almost nobody looks at it.** It is sealed behind the Vault Keeper with a budget of 60 noisy
   queries and 5 one-shot exams. It has not been read.
5. **Not finding a strategy is a valid result.** Gates are never loosened to manufacture a pass.

## Ambiguities found, and the conservative reading adopted

| Topic | Ambiguity | Reading adopted |
|---|---|---|
| Walk-forward for fixed rules (5.3, 12.2) | The folds describe fitting, but a genome has no fitted parameters | The genome is not re-fitted per fold. For test fold k, in-sample is its own record in folds 1 to k-1 minus a 3-session purge. Selection happens in the search, so islands score on disjoint halves of the test folds |
| Islands versus stage 1 thresholds (15.9, 12.1) | An island sees 3 of 6 test folds, but stage 1 asks for 300 trades and "5 of 6 folds" | Stage 1 uses home folds with sample thresholds scaled by one half and every fold required; a pass must then pass all six folds at full thresholds before stage 2. This performs the island exchange immediately |
| Inner holdout and the eight folds (5.3, 5.4) | Folds are "of the Research block" but the last 15% may not be scored before stage 4 | Folds divide the first 85% of Research sessions (947); holdout bars are not loaded by search stages |
| Twins at stage 1 (11.4, 19.2) | 200 twins on every generation | 200 twins whenever the candidate could still pass; 40 once another stage 1 gate has already failed (the alpha is then only a score input). The twin gate itself is never judged on fewer than 200 |
| Twin "identical stop and target" (11.4) | With level-based targets, random bars face different geometry | Twin entries are matched on time of day, direction and target-to-stop ratio (tightening, generation 2001 onward) |
| Lookbacks in minutes or bars (13.2) | Which lookbacks are "about bars" | Indicator lengths are bar counts (the same oscillator on any chart timeframe); session logic, time stops and cool-downs are clock minutes |
| Higher-timeframe values (13.2, 14.8) | `request.security` in Pine against session-anchored bars in Python | Higher-timeframe bars are built by counting chart bars from the session open, in both Python and Pine, and published only when complete. No `request.security` for timeframes |
| Roll adjustment (4.1, 4.2) | The data cannot prove adjustment | Treated as unadjusted (evidence in `data/DATA_QUALITY.md`); the search offers INTRADAY_FLAT only |
| Vault file permissions (5.1) | "Read permission removed" cannot bind a root process | The directory is mode 000, the research loader refuses vault paths, the static audit forbids vault references, and only `vault/keeper.py` reopens it |
| "One module per gate" (6.1) | Layout detail | Gates are grouped by stage (`gates/stage1.py` to `stage3.py`, `stats.py`); each gate still writes threshold, value and verdict |
| Language-model roles as separate processes (15.7, 17) | No model API is wired into the loop | Orchestrator, Evaluator, Auditor, Red Team and Vault Keeper are plain code. The Strategist is the agent session writing reviews and a hypothesis queue; when the queue is empty its share goes to LIBRARY_PROBE. The firewall for the Strategist is procedural, not enforced |
| ENSEMBLE operator (9.4) | Needs archive members with low trade overlap | Not implemented yet; its 3% share goes to LIBRARY_PROBE and each such generation says so |

## What cannot be claimed

Timeframes below 5 minutes; independence between ES and YM; anything about live fills; any vault result (none exists).
