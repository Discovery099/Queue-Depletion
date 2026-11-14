# Gate changes (Constitution Article 15: gates only tighten)

| Effective from generation | Gate | Change | Reason |
|---|---|---|---|
| 1 | structural.min_stop_atr | New floor: initial stop at least 0.3 ATR from the reference price | A stop inside ordinary bar noise is exit geometry, not a risk rule |
| 1 | score.sample_shrink | Composite score multiplied by min(1, trades / required trades) | A tiny sample must not lead the archive |
| 1 | stage 1 confirmation | A home-fold pass must also pass all six test folds at full thresholds before stage 2 | Performs the island exchange of SPEC 15.9 immediately instead of every 2,500 generations |
| 2001 | twin.win_rate_alpha (random-entry twin) | Twin entries are also matched to the candidate's target-to-stop distance ratio (quintile bins), not only to time of day and direction | The survey showed that level-based targets (opening-range edge, prior close) gave candidates a much shorter path to target than random bars had, producing 'alpha' of +20 points with profit factor below 1. That is exit geometry chosen by the entry, which the twin must neutralise. Generations 1 to 2000 all failed stage 1 on other gates, so no earlier verdict changes; their recorded alpha values for level-target genomes are overstated and are flagged as such in the review. |
