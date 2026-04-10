# Fast-Track Rubric — 6 Self-Diagnostic Deliverables

The fast-track is an alternative to the full capstone for learners who already integrated Phase 3–5 skills during the phase itself and only need to **prove** it. It is not a shortcut for skipping integration work — it is a way to harvest integration work you already did.

**Rationale for the specific shape of this rubric.** The v1 plan had a 6-item checklist that the adversarial review called "cosmetic without a verification mechanism" (`../UNIFIED_COURSE_PLAN_adversarial_analysis_v2.md` L97–L103). Finding #3 recommended "Option A (lightweight): Convert the 6-item rubric to a 90-minute self-diagnostic exercise with specific deliverables" where "each checkbox" is replaced with a "similar concrete bar" (L116–L117). This document is that replacement. Each deliverable is small (< 4 hours), tangible, and has a binary self-check — if you cannot produce the artifact in the time budget, that is the signal to switch to the full capstone (`../UNIFIED_COURSE_PLAN.md` L569).

**Ground rule.** All six deliverables must exist in a single public Git repository, one subdirectory each, with the repository README linking to each one. "I have it locally" does not count. "I did something similar in the Phase 3 lab" does not count — you must produce the artifact fresh, against your own stack, and be able to demo it.

---

## Deliverable 1 — dbt model with contract and unit test

**Goal.** Prove you can write a dbt model with a hard schema contract and a real unit test, running against your Phase 3 stack (`../phase_3_core_tools/05_dbt/`).

**What good looks like.**
- A single `mart_*` model in `models/marts/` with a `version: 2` YAML file declaring a contract (`contract: {enforced: true}`) and explicit column types for every column.
- At least one `not_null` and one `unique` test on the primary key.
- At least one `dbt unit test` (`docs.getdbt.com/docs/build/unit-tests`) with a fixture input and an expected output covering a non-trivial transformation branch (a CASE statement, a NULL handling decision, a join fallout).
- The model builds and tests pass against Trino + Iceberg on the Phase 3 compose stack.

**How to self-check.** From a fresh `docker compose up -d` using `../phase_3_core_tools/compose/full-stack/docker-compose.yml`, run `dbt build --select <your_mart>` and `dbt test`. Both must exit 0. Change the expected output in the unit test to a wrong value and rerun — the unit test must fail. Revert.

**Time budget.** ~3 hours.

---

## Deliverable 2 — Dagster asset with freshness SLO

**Goal.** Prove you can wire a Dagster software-defined asset that depends on the dbt model from Deliverable 1 and fails loudly when a freshness SLO is breached.

**What good looks like.**
- A Dagster asset (or `@asset_check`) depending on the Deliverable 1 mart.
- A `FreshnessPolicy` (or the current Dagster equivalent for your version) declaring an expected maximum age — e.g. 24 hours.
- A test that demonstrates the breach: run the asset, wait past the SLO (or fake the clock), and show that Dagster reports the asset as stale and surfaces an alert (UI badge, sensor, or log line is acceptable — it must be visible without opening source code).
- The asset uses the Phase 3 Dagster project layout (`../dataeng/dagster/lakehouse/` is the reference).

**How to self-check.** Open the Dagster UI, find the asset, confirm the freshness policy is shown. Force a stale state and confirm the UI flips to the stale indicator. A screenshot of the stale state goes in the deliverable's README.

**Time budget.** ~3 hours.

---

## Deliverable 3 — ADR: Iceberg vs Delta for a hypothetical scenario

**Goal.** Prove you can write a tight architecture decision record that weighs real trade-offs, not marketing copy.

**What good looks like.**
- One page (< 500 words) using a minimal ADR template: **Context**, **Decision**, **Consequences**, **Alternatives considered**.
- The scenario is hypothetical but concrete: pick a constraint (e.g., "multi-engine query required — Spark + Trino + Flink" or "single-engine Databricks shop with merge-heavy workloads").
- The decision cites at least one primary source per table format (`iceberg.apache.org/spec/` and `docs.delta.io`).
- The "Consequences" section names at least one real downside of the chosen option. "No downsides" is a red flag and fails the deliverable.
- Does not copy-paste a generic "Iceberg vs Delta" blog post.

**How to self-check.** Give the ADR to someone who has never used either format. They should be able to (a) restate your scenario, (b) restate your decision, and (c) name the downside you accepted — without asking you.

**Time budget.** ~2 hours.

---

## Deliverable 4 — Docker Compose stack you can explain line by line

**Goal.** Prove the compose file you use is yours, not magic you copy-pasted from the Phase 3 lab.

**What good looks like.**
- A working `docker-compose.yml` with at minimum: MinIO, Hive Metastore, Trino, dbt runner, Dagster webserver + daemon. Phase 3's `../phase_3_core_tools/compose/full-stack/docker-compose.yml` is the reference — you may start from it but must annotate it.
- Every non-trivial line has a comment explaining *why*, not *what*. "Depends_on hive-metastore because Trino's iceberg connector fails to register the catalog if HMS is not ready" is good. "Trino service" is not.
- A short (< 300 word) walkthrough document in the deliverable subdirectory that names each service, its role, its ports, and one specific thing that would break if it were removed.

**How to self-check.** Record yourself (or a study partner) reading the compose file top to bottom, explaining each service in one sentence, without pausing to look things up. If you pause for more than 10 seconds on any service, that service is not yet yours.

**Time budget.** ~3 hours.

---

## Deliverable 5 — Prometheus alert rule on pipeline health

**Goal.** Prove you can instrument a real pipeline-health metric and write an alert rule that fires on a real condition, not a toy counter.

**What good looks like.**
- One Prometheus `alerting` rule in a `rules.yml` scraped by the Prometheus instance in your stack. Reference config: `../dataeng/prometheus/prometheus.yml`.
- The rule is tied to a metric that actually reflects pipeline health — Dagster run status, dbt test failures, Trino query errors, or a freshness gauge you pushed yourself. Not CPU. Not memory. Not "up".
- The rule has a `for:` duration (so flapping does not page), a `severity` label, and a human-readable `summary` + `description` annotation (`prometheus.io/docs/prometheus/latest/configuration/alerting_rules/`).
- A test case where you deliberately break the pipeline (kill a container, fail a dbt test) and the alert transitions to firing within the `for` duration plus one scrape interval.

**How to self-check.** Run `promtool check rules rules.yml` — it must exit 0. Break the pipeline. Watch the Prometheus `/alerts` page show the rule go `pending` then `firing`. Screenshot both states into the deliverable's README.

**Time budget.** ~2.5 hours.

---

## Deliverable 6 — Git PR with CI that blocks on failure

**Goal.** Prove you can gate merges on automated checks, not on human diligence.

**What good looks like.**
- A GitHub repository with a `.github/workflows/` file (reference: `../dataeng/.github/workflows/dbt-ci.yml`) that runs on every PR:
  - `dbt compile` against a CI profile
  - `dbt test` (either the full test suite or a designated CI subset)
  - At minimum, one additional lint step (ruff, sqlfluff, or pre-commit)
- Branch protection on `main` requires the workflow to pass before merge is allowed.
- A demonstration PR exists in the repo showing: (a) one commit where CI is green and merge is allowed, and (b) one commit where CI is red (e.g., a deliberately broken model) and the merge button is disabled. Both states are preserved in the PR timeline.

**How to self-check.** Open the demonstration PR. The "Merge" button must be grey/disabled on the broken commit, and the reason must be visible ("required status checks have not succeeded"). After pushing the fix, the button must go green automatically.

**Time budget.** ~3 hours.

---

## Scoring

The fast-track is pass/fail, not graded. All six deliverables must exist and all six self-checks must pass. If any deliverable's self-check fails, the fast-track fails — you either redo that deliverable or switch to the full capstone.

The plan (`../UNIFIED_COURSE_PLAN.md` L569) is explicit: "Learners who cannot produce these artifacts from existing Phase 3–5 work should complete Phase 6 — the gap is the signal that integration competence is missing." If you find yourself arguing why a deliverable should count despite the self-check failing, that is the signal.

## Total time budget

~16.5 hours of focused work if you have most of the raw material from Phase 3–5. Plan on 20–24 hours including setup, debugging, and writing. If you are past 30 hours, stop and switch to the full capstone — at that point the capstone is the cheaper path.
