# Quiz — 01_cicd

Ten multiple-choice questions. Answer key at the bottom.

---

**1.** Why is rolling back a bad dbt deploy generally harder than rolling back a bad REST API deploy?
- A. dbt has no version control integration.
- B. Data changes mutate persistent state that downstream consumers may have already read.
- C. dbt cannot run twice in the same day.
- D. GitHub does not support dbt projects.

**2.** In a GitHub Actions workflow file, which key specifies the operating system image the job runs on?
- A. `uses:`
- B. `runs-on:`
- C. `env:`
- D. `with:`

**3.** Which trigger is most appropriate for a workflow that should only run when a human clicks a button in the GitHub UI?
- A. `push`
- B. `pull_request`
- C. `schedule`
- D. `workflow_dispatch`

**4.** What is the main security benefit of OIDC federation over storing `AWS_ACCESS_KEY_ID` as a GitHub secret?
- A. OIDC is faster.
- B. OIDC credentials are short-lived and minted per run, so there is no long-lived key to leak.
- C. OIDC avoids paying for GitHub minutes.
- D. OIDC works without IAM policies.

**5.** In a GitHub Actions workflow, what does the `paths:` filter under `pull_request` do?
- A. Restricts which directories dbt will compile.
- B. Skips the workflow unless one of the listed paths changed.
- C. Deletes files outside the listed paths.
- D. Sets the working directory for all steps.

**6.** Why does `pipeline-validation.yml` use `if: always()` on its cleanup step?
- A. To guarantee teardown even when an earlier step failed.
- B. To force the workflow to succeed.
- C. Because `always()` is required on every step.
- D. To re-run the cleanup on every event.

**7.** Which statement about GitHub Actions **environments** is correct?
- A. Environments are the same as runners.
- B. Environments attach protection rules (required reviewers, wait timers) to deployment jobs.
- C. Environments replace repository secrets.
- D. Environments automatically enable OIDC.

**8.** A dbt **unit test** differs from a dbt **data test** in that:
- A. Unit tests use mocked inputs and do not require a live warehouse.
- B. Unit tests only run in production.
- C. Unit tests are written in Python, not YAML.
- D. Unit tests cannot be run by `dbt test`.

**9.** What does a **matrix** strategy in GitHub Actions do?
- A. Combines multiple workflow files into one.
- B. Runs the same job across a set of variable combinations without duplicating YAML.
- C. Encrypts secrets at rest.
- D. Reorders steps for optimal performance.

**10.** What is a **preview environment** in a data-team context?
- A. A read-only copy of the production dashboard.
- B. A throwaway deployment of a branch — often a namespaced schema or Iceberg branch — that reviewers can inspect before merge.
- C. A local developer laptop.
- D. A Git tag.

---

## Answer key
1. **B** — mutated persistent state cannot be un-read by downstream consumers.
2. **B** — `runs-on:` selects the runner image (e.g. `ubuntu-latest`).
3. **D** — `workflow_dispatch` adds a manual "Run workflow" button.
4. **B** — short-lived, per-run credentials; no long-lived key in secrets.
5. **B** — `paths:` is a filter; if nothing matches, the workflow is skipped.
6. **A** — `if: always()` runs the step regardless of prior failures, ensuring teardown.
7. **B** — environments carry protection rules and environment-scoped secrets.
8. **A** — unit tests mock their inputs; data tests query real tables.
9. **B** — one job definition, many variable combinations (Python versions, OSes, etc.).
10. **B** — throwaway per-branch deployment for review.
