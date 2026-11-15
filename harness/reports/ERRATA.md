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
8. **Genome distance made step-based (after generation 2,868).** The first distance definition scored a one-grid-step parameter move
   below the novelty threshold of 0.05, so almost every PARAM_STEP child was rejected as "already tried" (11 uses in 500 proposals)
   and proposals became slow. The parameter part is now total grid steps divided by 8: one step is exactly 0.05 (novel), three steps
   are 0.15 (the "same strategy" limit used by the archive and the Vault Keeper). No verdict of an earlier generation changes; the
   search before this point simply under-used parameter refinement.
9. **Engine 1.2.0 to 1.3.0 (after generation 15,008).** The rolling simple average now sums its window afresh for every bar instead of
   keeping a running sum. The running sum accumulated rounding error, so two values that should tie could compare unequal; the
   independent Pine replay found this on 3 of 196 atoms (1 to 3 bars each out of about 3,900). Results of earlier generations can
   differ on such tie bars only. The hall of fame was empty. Also in 1.3.0: a history reference on a constant is the constant itself
   (Pine has no `50.0[1]`); the reproducibility self-test therefore covers generations sealed under 1.3.0 only.
10. **Behavioural duplicates in the archive.** Parameter steps that change nothing in practice (for example a longer cool-down that
    never binds) produce genomes with different identifiers and identical trades. They are counted as separate trials (conservative)
    but crowd the leader list; the behavioural-distance rule of SPEC 9.7 is not yet enforced at proposal time.
11. **Aborted trial rows were missing from the hash-chained mirror.** When a batch was interrupted (the session's worker process
    restarted twice), its open trial rows were marked ABORTED in the sqlite table by a direct update that bypassed the jsonl mirror.
    Found when the ledger was first restored from snapshots: 96 rows were ABORTED in one store and OPEN in the other. The 96 close
    events were appended to the mirror, and the loop now marks aborted rows through the ledger so both stores always agree.
12. **Ledgers are stored in version control as compressed shards** (`ledger/snapshots/`, written by `tools/snapshot.py`), because the
    working files exceed GitHub's 100 MB file limit. A restore reproduces `trials.jsonl`, `graveyard.jsonl` and the lineage database
    exactly and rebuilds the sqlite trial table from the mirror.
13. **What is and is not in the repository.** Not committed, because of size or by design: `runs/` (one folder per generation,
    3.6 GB), `library/raw/` and the three library archives (the owner holds them), the working ledgers (see item 12), `data/vault/`
    (rebuilt and hash-checked by `vault/rebuild.py`), and the generation folders of the 50-generation dry run and of the placebo runs
    (their summaries remain under `reports/`). The per-generation folders therefore exist only on the machine that ran them; the
    ledgers, lineage (every genome and its daily result series), archive, lessons and reports are in the repository.
14. **Two defects introduced with engine 1.4.0, found within 500 generations.** (a) A genome with no trades at all raised an
    exception in the new in-sample calculation instead of failing its gates; 19 generations between 20,011 and 20,478 are recorded
    as ERROR with their trial rows ABORTED. All would have failed stage 1 (no trades). (b) The epoch routine referenced the exchange
    result before computing it and stopped the loop at generation 20,500; generations 20,489 to 20,500 were re-run after the fix,
    so their first attempts remain in the trial ledger as extra rows (over-counting only). Both paths now have tests.
15. **Parent selection made faster at generation 90,417.** The 10% "uniformly at random" parent draw read every evaluated genome of
    the island each time, which had become the bottleneck with 45,000 genomes per island. It now looks up one random generation by
    index. The distribution is unchanged in intent (uniform over the island's evaluated generations); the sequence of proposals for
    a given seed differs from this point on.
