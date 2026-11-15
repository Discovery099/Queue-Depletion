# Placebo pipeline run `final_phase5`

The whole search loop was run for 1000 generations on a decoy market (phase number 5) built from research data
with no exploitable directional structure. Every promotion on such a market is a false discovery.

- Promotions: 0 Bronze, 0 Silver, 0 Gold.
- Stage 1 passes (before confirmation and stage 2): 0.
- Requirement (zero Gold, zero Silver, at most 2 Bronze per 1,000 generations): HOLDS.
- Outcomes: {'STAGE1_FAIL': 1000}.
- Best composite score reached on the decoy: 0.328. Among 584 decoy genomes with at least 150 trades: mean win-rate alpha
  +0.72 points (maximum +10.1), mean profit factor 0.92 (maximum 1.63).

Statement to place next to any real certification: "this pipeline promoted 0 strategies to Silver and
0 to Bronze in 1000 generations on markets with no edge".

Limit: the decoy genomes all stopped at the stage 1 screen, so this measures the false-discovery rate of the screen and its
confirmation. Stages 2 to 4 were not reached and are therefore not separately calibrated by this run.
