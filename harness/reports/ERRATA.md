# Errata and deviations (SPEC 19.7)

Every entry states what happened, what it could have affected, and what was done.

1. **Vault bars seen once (before the specification was read).** The agent's first look at the raw CSV files printed the final three
   bars of each file (2026-03-06, 15:45 to 15:55). Those six bars lie in the vault period. They inform no design choice and no rule
   refers to them. The vault was sealed afterwards and has not been read since; the vault ledger is empty.
2. **Development backtests run before the ledger wrapper existed.** While the engine and gates were being built, four hand-written
   genomes were run through stage 1 as smoke tests, and the unit tests run about a dozen fixed, hand-written genomes (a canary genome,
   a geometry-only genome, two planted-foresight genomes that read the future on purpose, and plain rule sets used to exercise stages
   2 to 4). None was chosen, tuned or kept because of its result, and none is in the archive. They are logged retroactively in the trial
   ledger as 16 rows with stage `dev`, so they count toward the trial total. Unit tests that run in temporary folders use their own
   temporary ledgers.
3. **The 50-generation dry run was first written into the live run folder.** It was moved, complete, to `reports/dryrun_001/` and the
   real run starts again at generation 1. Its 300 trial rows stay in the append-only ledger, so generation numbers 1 to 50 appear
   twice there (dry run under engine 1.0.0, real run under 1.1.0). The trial count used by the statistical gates therefore over-counts
   by 100 candidate rows, which is the conservative direction. All 50 dry-run generations failed stage 1.
4. **Engine 1.0.0 to 1.1.0.** After the dry run: order prices are rounded to the tick grid inside the expression layer and the
   structural limits are checked on the rounded prices; limit entries, targets and partial targets that gap through fill at the worst
   in-range price; the Vault Keeper refuses any strategy within genome distance 0.15 of a previously queried one, including an
   identical strategy submitted under a new lineage name. The engine acceptance suite was re-run and passes. The hall of fame was
   empty, so nothing needed re-scoring.
5. **Atom admission ran twice** (the first run was stopped for being slow), so the standalone information tests of some atoms have two
   ledger rows each. Over-counting only.
6. **Library layout differs from the specification.** The supplied archives contain `<type>/<version>/<name>.pine` only: there is no
   index, provenance or licence folder. The inventory, licences and authors were derived from the files themselves
   (`library/mine.py`). 4,499 scripts state no licence.
7. **Canary identities are inferable.** Canary atoms have zero supporting scripts in `library/ontology.json`. The search is programmatic
   and never reads that field, but a human or language-model Strategist could. The information firewall of SPEC 15.7 is therefore
   procedural for the Strategist role, not enforced.
