# Phase 0 Self-Assessment Quiz (20 questions, 45 min)

Score ≥ 70% (14/20) = Phase 1 is review. Score < 70% = take Phase 1 in full.

All answers cite primary sources. No tricks — if a question looks ambiguous it's testing whether you know the precise definition.

---

## SQL (6 questions)

**Q1.** Which window function assigns consecutive integers without gaps when ties occur?
A) `ROW_NUMBER()` B) `RANK()` C) `DENSE_RANK()` D) `NTILE()`

**Q2.** What does `EXPLAIN ANALYZE` do in PostgreSQL that `EXPLAIN` alone does not?
A) Shows the query plan
B) Executes the query and reports actual row counts + timing
C) Creates missing indexes
D) Rewrites the query for performance

**Q3.** A CTE declared with `WITH RECURSIVE` requires what two parts?
A) `SELECT` + `JOIN`
B) An anchor (non-recursive) term and a recursive term joined by `UNION` / `UNION ALL`
C) A window function and a partition clause
D) A primary key and a foreign key

**Q4.** In a LEFT JOIN, if a row on the left has no match on the right, the right-side columns are:
A) Omitted from the result
B) Set to zero
C) Set to NULL
D) Duplicated from the previous row

**Q5.** `SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)` computes:
A) A grand total
B) A per-customer running total ordered by date
C) The max amount per customer
D) A count of orders

**Q6.** An index on `(a, b)` can efficiently serve which query filter?
A) `WHERE b = 1`
B) `WHERE a = 1`
C) `WHERE a = 1 AND b = 2`
D) Both B and C

---

## Python (5 questions)

**Q7.** A Python generator is a function that uses:
A) `return` B) `yield` C) `async def` D) `@generator`

**Q8.** The file that declares a Python project's build system and dependencies per PEP 518 is:
A) `setup.py` B) `requirements.txt` C) `pyproject.toml` D) `Pipfile`

**Q9.** `uv pip install -e .` installs the current project in:
A) Production mode B) Editable mode C) Frozen mode D) Global site-packages only

**Q10.** A pytest fixture with `scope="session"` is:
A) Created once per test function
B) Created once per test module
C) Created once per test session (shared across all tests)
D) Never cached

**Q11.** Which of these is NOT part of the Python virtual environment mental model?
A) Isolates installed packages per project
B) Prevents version conflicts across projects
C) Modifies the system Python installation
D) Activated via a shell script

---

## Git (4 questions)

**Q12.** `git merge` and `git rebase` both integrate changes, but `rebase`:
A) Creates a merge commit B) Rewrites commit history onto a new base C) Deletes old commits from the remote D) Requires a pull request

**Q13.** You're on branch `feature/x`, make 3 commits, then `git rebase main`. A conflict appears. You should:
A) `git reset --hard` to discard everything
B) Resolve the conflict, `git add` the resolved files, then `git rebase --continue`
C) `git merge --abort`
D) Force-push immediately

**Q14.** `.gitignore` patterns apply to:
A) Only staged files B) Only untracked files C) Already-committed files D) Remote branches

**Q15.** A detached HEAD means:
A) The repo is corrupted
B) HEAD points to a specific commit rather than a branch tip
C) The remote is unreachable
D) All branches have been deleted

---

## Networking (3 questions)

**Q16.** The default HTTPS port is:
A) 80 B) 443 C) 22 D) 8080

**Q17.** TCP vs. UDP: which guarantees ordered, reliable delivery?
A) TCP B) UDP C) Both D) Neither

**Q18.** DNS resolves:
A) IP addresses to MAC addresses
B) Hostnames to IP addresses
C) Ports to services
D) URLs to HTML

---

## Linux / Bash (2 questions)

**Q19.** `chmod 755 script.sh` gives:
A) Owner rwx, group rx, others rx
B) Everyone rwx
C) Owner rw, group r, others r
D) Owner rwx, others none

**Q20.** In a bash pipeline `cmd1 | cmd2 | cmd3`, the exit code available via `$?` (without `pipefail`) is:
A) The first non-zero exit code
B) The exit code of `cmd1`
C) The exit code of `cmd3`
D) Always zero

---

## Answers

1. C — `DENSE_RANK` gives consecutive integers (1,1,2 where `RANK` gives 1,1,3). Ref: [PostgreSQL window functions](https://www.postgresql.org/docs/current/tutorial-window.html)
2. B. Ref: [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html)
3. B. Ref: [PostgreSQL WITH queries](https://www.postgresql.org/docs/current/queries-with.html)
4. C. Ref: [PostgreSQL joins](https://www.postgresql.org/docs/current/tutorial-join.html)
5. B — running total per partition, ordered. Ref: [PostgreSQL window frames](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS)
6. D — a composite index on `(a,b)` serves queries filtering on `a` alone or `a` and `b`, but not `b` alone. Ref: [PostgreSQL multicolumn indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
7. B. Ref: [Python yield expressions](https://docs.python.org/3/reference/expressions.html#yield-expressions)
8. C. Ref: [PEP 518](https://peps.python.org/pep-0518/)
9. B. Ref: [uv pip install docs](https://docs.astral.sh/uv/pip/packages/)
10. C. Ref: [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html#fixture-scopes)
11. C — venvs do not modify the system Python. Ref: [Python venv](https://docs.python.org/3/library/venv.html)
12. B. Ref: [git-rebase docs](https://git-scm.com/docs/git-rebase)
13. B. Ref: [git-rebase docs](https://git-scm.com/docs/git-rebase#_recovering_from_upstream_rebase)
14. B — `.gitignore` does not un-track already-committed files. Ref: [gitignore docs](https://git-scm.com/docs/gitignore)
15. B. Ref: [git-checkout detached HEAD](https://git-scm.com/docs/git-checkout#_detached_head)
16. B. Ref: [IANA ports](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)
17. A. Ref: [RFC 793 (TCP)](https://www.rfc-editor.org/rfc/rfc793)
18. B. Ref: [RFC 1034 (DNS)](https://www.rfc-editor.org/rfc/rfc1034)
19. A — 7=rwx, 5=r-x. Ref: [GNU coreutils chmod](https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html)
20. C — without `set -o pipefail`, only the last command's exit code is reported. Ref: [Bash reference manual — Pipelines](https://www.gnu.org/software/bash/manual/html_node/Pipelines.html)
