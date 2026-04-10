# Module 06: Git Workflows for Data Teams (4h)

> GAP module — no sibling source. Written from git-scm.com, Pro Git (Chacon & Straub), GitHub docs, and pre-commit.com. One real CI example is cited from `../dataeng/.github/workflows/`.

## Learning goals
- Explain trunk-based development with short-lived feature branches and justify it over long-lived `develop`/`release` branches for data teams
- Resolve a merge conflict via `git rebase` and continue the rebase cleanly
- Install the `pre-commit` framework and wire it to `ruff`, `sqlfluff`, and `yamllint` for a data repo
- Write a `.gitignore` that blocks credentials, large data files, and notebook outputs
- Choose between `git merge` and `git rebase` based on whether the branch has been pushed/shared
- Use `git push --force-with-lease` instead of `--force`, and explain why

## Prerequisites
- [`../01_linux_bash/`](../01_linux_bash/) — shell basics
- Git installed locally (`git --version` ≥ 2.30)
- A GitHub account (optional — the lab can be done fully locally)

## Reading order
1. This README
2. [`labs/lab_04_git_workflow/README.md`](labs/lab_04_git_workflow/README.md)
3. [`quiz.md`](quiz.md)

## Concepts

### Branching strategy: trunk-based with short-lived feature branches
A branch is a lightweight movable pointer to a commit; creating one is O(1) because Git just writes a 41-byte file. Because branches are cheap, the modern default is **trunk-based development**: everyone commits to `main` via short-lived feature branches that merge (or rebase) back within hours or days, not weeks. Long-lived `develop` / `release` branches accumulate drift and make data-pipeline conflicts (schema, dbt sources, Dagster assets) painful to resolve.
Ref: *Pro Git, Chacon & Straub, Ch. 3 — Git Branching* ([book/en/v2/Git-Branching-Branches-in-a-Nutshell](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell))

### PR review checklist for data PRs
A data PR typically touches more than code. Reviewers should explicitly check:
- **Schema migrations** — is the change additive? Backward-compatible? Will a concurrent reader break?
- **dbt model changes** — materialization change (view → incremental)? Unique/not-null tests present? Downstream exposure updated?
- **Config drift** — profiles, `.env` templates, compose service versions all in sync?
- **Secrets** — no credentials, tokens, or `.env` files in the diff
- **CI status** — all required checks green before merge

GitHub enforces pre-merge requirements via **protected branches** (required status checks, required reviews, linear history). Ref: [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

A real example of CI gates on PRs: [`../../../dataeng/.github/workflows/dbt-ci.yml`](../../../dataeng/.github/workflows/dbt-ci.yml) runs `dbt compile`, `sqlfluff`, and pytest on every pull request touching `dbt_project/**`.

### Merge vs. rebase
`git merge` creates a merge commit that preserves the exact branch topology. `git rebase` replays your commits on top of a new base, producing a **linear history** but rewriting commit SHAs. Rule of thumb from Pro Git: **rebase local work you have not yet shared; merge public branches**. Rebasing commits that others have pulled will force them into a reconciliation dance.
Ref: *Pro Git, Ch. 3 — Rebasing* ([book/en/v2/Git-Branching-Rebasing](https://git-scm.com/book/en/v2/Git-Branching-Rebasing))

Conflict resolution loop during a rebase:
```bash
git rebase main
# <conflict>
# edit the file, then:
git add <file>
git rebase --continue
# or bail out:
git rebase --abort
```
Ref: [git-rebase docs](https://git-scm.com/docs/git-rebase).

### Pre-commit hooks
`pre-commit` is a framework that manages per-repo git hooks declared in `.pre-commit-config.yaml`. It installs a `.git/hooks/pre-commit` shim that runs the configured hooks in isolated environments on staged files only. For a data repo a baseline config runs:
- `ruff` — lint + format Python ([ruff via pre-commit](https://pre-commit.com/hooks.html))
- `sqlfluff` — lint SQL / dbt
- `yamllint` — lint `dbt_project.yml`, `profiles.yml`, compose files
- `check-added-large-files`, `detect-private-key`, `end-of-file-fixer` (built-in)

Install once per clone:
```bash
pip install pre-commit
pre-commit install          # wires .git/hooks/pre-commit
pre-commit run --all-files  # run against existing code
```
Ref: [pre-commit.com quick start](https://pre-commit.com/#quick-start).

### `.gitignore` for data projects
`.gitignore` uses shell glob patterns; each line is a pattern, `!` negates, trailing `/` scopes to directories. For a data repo, ignore at minimum:
```gitignore
# Credentials and env
.env
.env.*
!.env.example
*.pem
credentials.json
profiles.yml        # dbt — contains connection info; commit profiles.example.yml instead

# Data and large files
data/raw/
data/interim/
*.parquet
*.csv
*.duckdb
*.sqlite

# Notebook outputs (strip via nbstripout or ignore entirely)
.ipynb_checkpoints/

# Build/compile artifacts
target/             # dbt compiled SQL
dbt_packages/
logs/
__pycache__/
.venv/
```
Ref: [gitignore docs](https://git-scm.com/docs/gitignore).

### Rewriting history — safely
- `git commit --amend` replaces the tip commit with a new one (new SHA). Safe only if the commit has not been pushed.
- `git rebase -i <base>` opens an editor where commits can be `pick`, `squash`, `reword`, or `drop`. Use it to squash "wip" commits before opening a PR.
- **Never rewrite history on a branch others have pulled.** The only escape hatch for a shared branch is to force-push with `--force-with-lease`, which refuses to overwrite work you haven't seen yet — unlike `--force`, which clobbers unconditionally.

Ref: *Pro Git, Ch. 7 — Rewriting History* ([book/en/v2/Git-Tools-Rewriting-History](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History)) · [git-push `--force-with-lease`](https://git-scm.com/docs/git-push#Documentation/git-push.txt---force-with-lease).

### Remotes: `fetch` vs. `pull`
`git fetch` downloads refs and objects from a remote but does **not** touch your working tree or current branch. `git pull` is `git fetch` followed by either `git merge` or `git rebase` (configurable via `pull.rebase`). For deliberate workflows, prefer `git fetch` + inspect + explicit merge/rebase over `git pull`.
Ref: [git-fetch](https://git-scm.com/docs/git-fetch) · [git-pull](https://git-scm.com/docs/git-pull).

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_04_git_workflow` | Full feature-branch → rebase → PR round trip with a conflict resolution | 60m | [labs/lab_04_git_workflow/](labs/lab_04_git_workflow/) |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| `git rebase` leaves you in "detached HEAD" confusion | Edited conflict markers but forgot `git add` | `git add <file> && git rebase --continue` | [git-rebase](https://git-scm.com/docs/git-rebase) |
| `git push --force` destroys a teammate's commits | Used `--force` on a shared branch | Use `--force-with-lease` and re-pull first | [git-push](https://git-scm.com/docs/git-push) |
| `.env` with real credentials ends up in a commit | `.gitignore` written after the first commit | `git rm --cached .env`, add to `.gitignore`, rotate the credentials | [gitignore](https://git-scm.com/docs/gitignore) |
| Pre-commit hook doesn't run | Forgot `pre-commit install` after clone | Run `pre-commit install` | [pre-commit.com](https://pre-commit.com/#quick-start) |
| PR merged bypassing CI | Branch protection not configured | Enable required status checks | [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Create a branch, make a conflicting change on `main`, rebase and resolve the conflict
- [ ] Explain in one sentence when to `merge` vs `rebase`
- [ ] Write a `.pre-commit-config.yaml` with ruff + sqlfluff + yamllint and run it
- [ ] Write a `.gitignore` that blocks `.env`, `data/raw/`, `*.parquet`, and `target/`
- [ ] State why `--force-with-lease` is safer than `--force`
- [ ] Point to a real CI workflow that gates a data PR
