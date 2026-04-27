# Module 06: Git — References

## Primary docs (git-scm.com)
- [Git reference manual index](https://git-scm.com/docs/) — canonical command reference
- [git-branch](https://git-scm.com/docs/git-branch) — branch creation / listing / deletion
- [git-rebase](https://git-scm.com/docs/git-rebase) — rebase semantics, `--continue`, `--abort`, interactive mode
- [git-merge](https://git-scm.com/docs/git-merge) — merge semantics, conflict markers
- [git-fetch](https://git-scm.com/docs/git-fetch) — download refs without modifying working tree
- [git-pull](https://git-scm.com/docs/git-pull) — fetch + integrate
- [git-push](https://git-scm.com/docs/git-push) — upload refs; `--force-with-lease` section
- [git-commit](https://git-scm.com/docs/git-commit) — `--amend` behavior
- [gitignore](https://git-scm.com/docs/gitignore) — pattern syntax, precedence

## Pro Git book (Chacon & Straub, 2nd ed.) — free at git-scm.com/book
- *Pro Git, Ch. 3 — Git Branching* — branch mechanics, workflows, rebasing
  https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell
- *Pro Git, Ch. 3 — Rebasing* — merge vs. rebase, the golden rule of rebasing
  https://git-scm.com/book/en/v2/Git-Branching-Rebasing
- *Pro Git, Ch. 7 — Rewriting History* — `--amend`, interactive rebase, filter-branch warnings
  https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History

## GitHub docs
- [Pull requests overview](https://docs.github.com/en/pull-requests) — PR model, reviews, draft PRs
- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) — required checks, required reviews, linear history
- [Managing a branch protection rule](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)

## pre-commit framework
- [pre-commit.com](https://pre-commit.com/) — framework landing page
- [Quick start](https://pre-commit.com/#quick-start) — install + first config
- [Supported hooks](https://pre-commit.com/hooks.html) — community hook index (ruff, sqlfluff, yamllint, detect-private-key, check-added-large-files)

## CI workflow examples
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions) — how to author path-filtered CI workflows (e.g., dbt compile + sqlfluff + pytest on PRs touching `dbt_project/**`)
- [GitHub Actions — Using conditions to control job execution](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/using-conditions-to-control-job-execution) — `paths:` filter for monorepo CI
