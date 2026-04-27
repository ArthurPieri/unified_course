# Module 01: CI/CD for Data Pipelines (8h)

> Phase 5 · Advanced. How data teams use GitHub Actions to test, build, and deploy pipelines without breaking production.

## Learning goals
- Explain why CI/CD matters more — not less — for data platforms than for stateless services.
- Read a GitHub Actions workflow file and name every top-level key (`on`, `jobs`, `steps`, `uses`, `runs-on`).
- Choose the right trigger (`push`, `pull_request`, `schedule`, `workflow_dispatch`) for a given job.
- Configure secrets and OIDC-based cloud auth instead of long-lived access keys.
- Design a dbt PR check and a full-stack integration test, citing a real working example.
- Identify when to use environment protection rules and preview environments.

## Prerequisites
- `phase_1_foundations/04_docker_compose` (images, containers, services)
- `phase_3_lakehouse/05_dbt` (understanding what `dbt compile` and `dbt test` do)
- Working knowledge of Git branches and pull requests

## Reading order
1. This README
2. `labs/lab_L5a_cicd_k8s/README.md`
3. `quiz.md`

## Concepts

### Why CI/CD matters for data
Data pipelines have a property that stateless APIs do not: a bad production change often cannot be rolled back cleanly. If a dbt model drops a column or rewrites history, replaying the previous version does not undo the damage to downstream tables, BI caches, or reverse-ETL exports. The only safe strategy is to catch errors *before* merge. CI lets you run `dbt compile`, `dbt test`, unit tests, and linters against every pull request so broken SQL never reaches `main`. CD then automates the deployment itself so humans do not fat-finger `kubectl apply` at 2 a.m.

Ref: [dbt docs — Continuous integration jobs](https://docs.getdbt.com/docs/deploy/continuous-integration) · see the CI/CD examples in this repo's `phase_5_advanced/01_cicd/`

### GitHub Actions anatomy
A **workflow** is a YAML file under `.github/workflows/`. It contains one or more **jobs**, which run in parallel by default on a **runner** (a VM or container GitHub provides, or a self-hosted machine). Each job contains **steps**: either a shell command (`run:`) or a reusable **action** (`uses:`). Actions are referenced by `owner/repo@ref`, for example `actions/checkout@v4`. A **matrix** runs the same job across a set of variables (Python 3.11, 3.12, 3.13) without duplicating YAML.

Ref: [GitHub Actions — Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) · [About workflows](https://docs.github.com/en/actions/using-workflows/about-workflows)

### Triggers
The `on:` key defines when a workflow runs. `push` fires on every commit to a branch; `pull_request` fires when a PR is opened, updated, or reopened; `schedule` uses cron syntax for periodic runs; `workflow_dispatch` adds a manual "Run workflow" button in the GitHub UI, optionally with typed inputs. For data teams: use `pull_request` for lint/compile/unit tests, `push` to `main` for deploys, `schedule` for nightly freshness checks, and `workflow_dispatch` for expensive integration runs you only want to kick off by hand.

Example (typical dbt CI workflow trigger):
```yaml
on:
  pull_request:
    paths:
      - 'dbt_project/**'
      - '.github/workflows/dbt-ci.yml'
```
The `paths` filter skips the workflow when unrelated files change — cheaper and faster.

Ref: [GitHub Actions — Events that trigger workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)

### Secrets and OIDC
Never commit credentials. GitHub provides two mechanisms:
1. **Repository/organization secrets** — encrypted values injected as environment variables via `${{ secrets.NAME }}`. Good for API tokens.
2. **OpenID Connect (OIDC) federation** — the runner requests a short-lived JWT from GitHub, exchanges it with AWS/GCP/Azure for a temporary credential. No long-lived keys ever touch the repo. This is the recommended pattern for deploying to cloud.

Ref: [GitHub Actions — Encrypted secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) · [About security hardening with OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)

### Data-specific pipelines: dbt PR check
A typical dbt CI workflow runs three things on every PR that touches `dbt_project/`:
1. `dbt deps` to install packages (`L20-L21`)
2. `dbt compile --target dev` as a pure syntax/ref check (`L22-L23`)
3. `sqlfluff lint` on changed files only, detected via `git diff --name-only origin/main...HEAD` (`L24-L33`)

A second job (`L35-L50`) runs `dbt test --select test_type:unit` — unit tests use mocked inputs so they don't need a live warehouse. This is the modern dbt pattern: unit tests in CI, data tests against a staging warehouse.

Ref: [dbt docs — Unit tests](https://docs.getdbt.com/docs/build/unit-tests)

### Full-stack integration test
A full-stack integration workflow spins up the entire compose stack (MinIO, HMS, Trino, Postgres) inside the runner, initialises buckets and schemas, runs a health check, and tears down. Key design choices:
- Triggered only by `workflow_dispatch` and `push` to `main` on specific paths (`L2-L9`) — it's expensive.
- `timeout-minutes: 30` (`L15`) caps runaway cost.
- A polling loop waits for `docker compose ps` to report `healthy` (`L39-L45`).
- `if: always()` on the cleanup step (`L55-L57`) guarantees teardown even on failure.

This is the **ephemeral stack** pattern: every run starts from nothing, so flakes caused by leftover state are impossible.

### Preview environments
A preview environment is a throwaway deployment of a branch, torn down when the PR is merged or closed. In data land this often means: a namespaced schema in the warehouse (`pr_123_analytics`), a branch of an Iceberg table, or a kind cluster spun up inside the runner. The value is that reviewers can click through a dashboard built from the branch's dbt models before approving.

Ref: [dbt Cloud — Slim CI and deferral](https://docs.getdbt.com/docs/deploy/continuous-integration)

### Deployment gates
GitHub Actions **environments** attach protection rules to deployment jobs: required reviewers, wait timers, and branch restrictions. A job targets an environment with `environment: production`, and the run pauses until a named approver clicks approve. Combine with OIDC so the production credentials are *only* issued after approval. This is the minimum bar for any deploy job that touches customer data.

Ref: [GitHub Actions — Using environments for deployment](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_L5a_cicd_k8s` | Build a GitHub Actions workflow that tests a Python package on PR and deploys Trino to a kind cluster on merge | 90m | [labs/lab_L5a_cicd_k8s/](labs/lab_L5a_cicd_k8s/) |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| Workflow runs on every commit, wasting minutes | No `paths` filter on the trigger | Add `paths:` under `pull_request` / `push` | [GitHub Actions — Events that trigger workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows) |
| `dbt compile` works locally, fails in CI | Missing `profiles.yml` or `DBT_PROFILES_DIR` | Check profile path, use env vars not hard-coded creds | [dbt — profiles.yml](https://docs.getdbt.com/docs/core/connect-data-platform/profiles.yml) |
| AWS step fails with `The security token included in the request is invalid` | Still using long-lived `AWS_ACCESS_KEY_ID` | Migrate to OIDC with `aws-actions/configure-aws-credentials` | [GitHub Actions OIDC with AWS](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services) |
| Integration test passes locally, fails in runner | Race condition — services not healthy yet | Poll `docker compose ps` for `healthy` before continuing | [Docker Compose — wait for dependencies](https://docs.docker.com/compose/how-tos/startup-order/) |
| Secret value appears as `***` in logs but still leaks via filename | Secret used in a filename | Never interpolate secrets into filenames or URLs written to logs | [GitHub — secret masking](https://docs.github.com/en/actions/security-guides/encrypted-secrets#accessing-your-secrets) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Explain to a non-data engineer why rolling back a bad dbt deploy is harder than rolling back a bad API deploy.
- [ ] Read a `dbt-ci.yml` workflow (see [GitHub Actions: workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)) and identify the trigger, jobs, and their dependencies.
- [ ] Write a workflow that runs `ruff` and `pytest` on every PR to a Python repo.
- [ ] Configure an `environment: production` gate on a deploy job.
- [ ] List three reasons OIDC is safer than `AWS_ACCESS_KEY_ID` in secrets.
