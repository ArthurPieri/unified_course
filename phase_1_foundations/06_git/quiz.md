# Module 06: Git — Exit Quiz

8 multiple-choice questions. Pass mark: 7/8. Answers with primary-source citations at the bottom.

---

**Q1.** In trunk-based development with short-lived feature branches, what is the recommended typical lifetime of a feature branch before it merges back to `main`?

A. Weeks to months, until the feature is complete
B. Hours to days
C. A full release cycle
D. Until the next quarterly planning meeting

---

**Q2.** Which statement best describes the difference between `git merge` and `git rebase`?

A. `merge` is faster; `rebase` is slower
B. `merge` preserves the branch topology with a merge commit; `rebase` replays commits on a new base and rewrites their SHAs
C. `rebase` is only for remote branches; `merge` is only local
D. They are identical aliases

---

**Q3.** You are mid-rebase, you have edited a conflicted file, and you want to proceed. Which sequence is correct?

A. `git commit` then `git rebase --continue`
B. `git rebase --continue` alone
C. `git add <file>` then `git rebase --continue`
D. `git merge --continue`

---

**Q4.** Which git push flag refuses to overwrite remote commits you have not yet fetched, making it the safer alternative to `--force`?

A. `--force-if-includes`
B. `--force-with-lease`
C. `--safe-force`
D. `--no-force`

---

**Q5.** You just pushed a feature branch to a shared remote. Which operation is explicitly discouraged by the Pro Git "golden rule of rebasing"?

A. Opening a pull request
B. Running `git fetch`
C. Rebasing the pushed commits and force-pushing over them while others have pulled
D. Merging `main` into the feature branch

---

**Q6.** What does `pre-commit install` do?

A. Installs the `pre-commit` Python package
B. Writes a `.git/hooks/pre-commit` shim that runs the hooks declared in `.pre-commit-config.yaml` on staged files
C. Runs every hook against every file in the repo
D. Uploads hooks to GitHub

---

**Q7.** Which `.gitignore` entry will correctly exclude all `.env` files while still keeping `.env.example` tracked?

A. `.env*`
B. `.env` then on a separate line `!.env.example`
C. `*.env` only
D. `.env.example` only

---

**Q8.** On GitHub, which feature lets you require that specific CI status checks pass before a pull request can be merged into `main`?

A. Actions secrets
B. CODEOWNERS file alone
C. Branch protection rules (protected branches)
D. Repository topics

---

## Answer key

1. **B** — Short-lived means hours to days. Ref: *Pro Git, Ch. 3 — Branching Workflows*, https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows
2. **B** — Merge creates a merge commit preserving topology; rebase replays commits producing new SHAs. Ref: *Pro Git, Ch. 3 — Rebasing*, https://git-scm.com/book/en/v2/Git-Branching-Rebasing
3. **C** — After resolving, stage the file with `git add` then `git rebase --continue`. Ref: [git-rebase](https://git-scm.com/docs/git-rebase)
4. **B** — `--force-with-lease` refuses to overwrite unseen remote updates. Ref: [git-push --force-with-lease](https://git-scm.com/docs/git-push#Documentation/git-push.txt---force-with-lease)
5. **C** — Pro Git: "Do not rebase commits that exist outside your repository and that people may have based work on." Ref: *Pro Git, Ch. 3 — Rebasing* (section "The Perils of Rebasing"), https://git-scm.com/book/en/v2/Git-Branching-Rebasing
6. **B** — It installs a repo-local `.git/hooks/pre-commit` shim that dispatches to `.pre-commit-config.yaml` hooks. Ref: [pre-commit quick start](https://pre-commit.com/#quick-start)
7. **B** — A negated pattern `!.env.example` re-includes a file excluded by an earlier pattern. Ref: [gitignore docs](https://git-scm.com/docs/gitignore)
8. **C** — Protected branches support required status checks. Ref: [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
