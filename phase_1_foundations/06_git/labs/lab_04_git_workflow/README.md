# Lab 04: Feature-Branch → Rebase → PR Workflow

## Goal
Execute a full feature-branch workflow end-to-end — create a branch, trigger a merge conflict, resolve it via rebase, and (optionally) push and open a pull request — leaving behind a linear history.

## Prerequisites
- `git --version` >= 2.30
- A text editor
- (Optional) A GitHub account and an empty personal repo for the push / PR step. The lab is fully completable locally without a remote.

## Setup
```bash
mkdir -p ~/tmp && cd ~/tmp
git init demo-repo
cd demo-repo
git config user.email "you@example.com"
git config user.name  "You"

printf "hello\n" > greeting.txt
git add greeting.txt
git commit -m "initial commit"

# Optional remote — skip if you have no GitHub repo
# git remote add origin git@github.com:<you>/demo-repo.git
# git push -u origin main
```

## Steps

1. **Create and switch to a feature branch, modify the file, commit.**
   ```bash
   git switch -c feature/add-greeting
   printf "hello\nbonjour\n" > greeting.txt
   git commit -am "feat: add french greeting"
   ```

2. **Switch back to `main` and make a conflicting edit.**
   ```bash
   git switch main
   printf "hello\nhola\n" > greeting.txt
   git commit -am "feat: add spanish greeting"
   ```

3. **Rebase the feature branch onto `main` — expect a conflict.**
   ```bash
   git switch feature/add-greeting
   git rebase main
   ```
   Expected output (abridged):
   ```
   Auto-merging greeting.txt
   CONFLICT (content): Merge conflict in greeting.txt
   error: could not apply <sha>... feat: add french greeting
   ```

4. **Resolve the conflict.** Open `greeting.txt`. You will see conflict markers:
   ```
   hello
   <<<<<<< HEAD
   hola
   =======
   bonjour
   >>>>>>> <sha> (feat: add french greeting)
   ```
   Edit it so both greetings are kept:
   ```
   hello
   hola
   bonjour
   ```
   Then stage and continue:
   ```bash
   git add greeting.txt
   git rebase --continue
   ```
   Expected output:
   ```
   Successfully rebased and updated refs/heads/feature/add-greeting.
   ```

5. **Push with `--force-with-lease` (only if you added a remote in setup).**
   ```bash
   git push --force-with-lease -u origin feature/add-greeting
   ```
   `--force-with-lease` is required because the rebase rewrote the branch's commit SHAs; it refuses to overwrite remote work you have not yet fetched. Ref: [git-push](https://git-scm.com/docs/git-push#Documentation/git-push.txt---force-with-lease).

6. **Open a pull request.** In the GitHub UI, click "Compare & pull request" on `feature/add-greeting` and open the PR against `main`. Take a screenshot of the PR page, or paste the PR URL into a scratch note. Ref: [GitHub pull requests](https://docs.github.com/en/pull-requests). Skip this step if you have no remote.

## Verify
- [ ] `git log --oneline --graph --all` shows a **linear** history — your feature commit sits on top of the `main` commit, no merge commit.
- [ ] `cat greeting.txt` prints `hello` / `hola` / `bonjour` (three lines).
- [ ] `git status` is clean.
- [ ] (If using remote) `git ls-remote origin feature/add-greeting` returns a ref.

## Cleanup
```bash
cd ~/tmp
rm -rf demo-repo
# If you created a GitHub repo just for this lab, delete it in the GitHub UI.
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| `fatal: no such ref: main` | Older Git defaulted to `master`. `git branch -m master main` or redo setup with `git init -b main`. |
| `git rebase --continue` says "no changes" | You forgot `git add` after resolving. Stage the file first. |
| `! [rejected] ... (stale info)` on push | Someone pushed since your last fetch. Run `git fetch` + review before retrying `--force-with-lease`. |
| Conflict markers left in committed file | Run `git rebase --abort`, redo step 4 carefully. |

## Stretch goals
- Add a `.pre-commit-config.yaml` with `ruff` and run `pre-commit install`. Commit a Python file with a deliberate lint error (`import os` unused). Observe the hook blocking the commit. Fix the error and commit again. Ref: [pre-commit quick start](https://pre-commit.com/#quick-start).
- Use `git rebase -i HEAD~2` to squash the two feature commits into one before pushing.
- Enable a branch protection rule on `main` in the GitHub repo requiring one review before merge. Ref: [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

## References
See `../../references.md` (module-level).
