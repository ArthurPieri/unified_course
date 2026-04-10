# Phase 1 — Checkpoint Q1 (20 questions)

Draws from all six Phase 1 modules. Pass = 16/20. Below that, re-read the module you missed — the answer key cites the source module for each question.

---

**Q1.** `set -euo pipefail` does all of the following EXCEPT:
A) Exit on the first command that returns non-zero
B) Treat references to unset variables as errors
C) Fail a pipeline if any command in it fails
D) Automatically retry failed commands

**Q2.** The POSIX signal sent by `kill <pid>` with no flag is:
A) SIGKILL (9)   B) SIGTERM (15)   C) SIGHUP (1)   D) SIGSTOP (19)

**Q3.** You run `chmod 640 secret.env`. The file owner gets ___ and "other" gets ___:
A) rw- / ---   B) rwx / r--   C) rw- / r--   D) r-- / ---

**Q4.** The RFC 1918 private address ranges are:
A) 10/8, 172.16/12, 192.168/16
B) 10/8, 172.0/8, 192.168/16
C) 127/8, 172.16/12, 192.168/16
D) 10/8, 169.254/16, 192.168/16

**Q5.** `dig example.com A +trace` differs from `dig example.com A` because it:
A) Uses TCP instead of UDP
B) Walks the delegation chain from the root, bypassing the recursive resolver
C) Returns only the SOA record
D) Forces DNSSEC validation

**Q6.** The correct order of events for `curl https://api.example.com` is:
A) TLS → DNS → TCP → HTTP
B) DNS → TCP → TLS → HTTP
C) DNS → TLS → TCP → HTTP
D) TCP → DNS → TLS → HTTP

**Q7.** In a modern Python project, `pyproject.toml` is standardized by:
A) PEP 8   B) PEP 440   C) PEP 518 (+ PEP 621 for project metadata)   D) PEP 3000

**Q8.** `pytest` fixtures are composed primarily via:
A) Class inheritance
B) The `@pytest.fixture` decorator and function-argument injection
C) A `conftest.json` file
D) Global variables

**Q9.** You want to run `ruff`, `mypy`, and `pytest` only on changed files before every commit. The canonical tool is:
A) `make`   B) `husky`   C) `pre-commit` (pre-commit.com)   D) A shell alias

**Q10.** In a Dockerfile, the difference between `CMD` and `ENTRYPOINT` is best described as:
A) `CMD` runs at build time; `ENTRYPOINT` runs at runtime
B) `ENTRYPOINT` sets the executable; `CMD` sets its default arguments (and is overridable on `docker run`)
C) They are synonyms
D) `CMD` is deprecated in favor of `ENTRYPOINT`

**Q11.** A Compose `depends_on` with `condition: service_healthy` requires that the dependency has:
A) A `restart: always` policy
B) A `healthcheck:` block
C) A named volume
D) A `profiles:` entry

**Q12.** Which Compose feature lets you activate optional services (e.g., `metabase`) only when explicitly requested?
A) `extends:`   B) `profiles:`   C) `x-optional:`   D) `enabled:`

**Q13.** In PostgreSQL, `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_ts)` assigns:
A) A monotonic per-customer row number ordered by order timestamp
B) A global row number ignoring the partition
C) A dense rank with ties
D) A random number per partition

**Q14.** `EXPLAIN ANALYZE` differs from `EXPLAIN` in that it:
A) Shows the estimated plan without execution
B) **Executes** the query and reports actual row counts and timings
C) Shows the parse tree
D) Requires superuser privileges

**Q15.** A query that filters `WHERE email = 'x@y.com'` on a 10M-row table performs a Seq Scan despite a B-tree index on `email`. The most common cause is:
A) The index is bloated and `VACUUM ANALYZE` would fix it
B) The planner estimates too many rows returned (missing/stale statistics)
C) B-tree indexes cannot be used for equality
D) The column is indexed but not unique

**Q16.** `pg_dump -Fc mydb > mydb.dump` produces:
A) A plain SQL file
B) A custom-format archive (restorable with `pg_restore`, supports selective restore)
C) A tar archive
D) A binary snapshot of the data directory

**Q17.** Trunk-based development with short-lived feature branches is preferred over long-lived `develop`/`release` branches in data teams primarily because:
A) Git performs better on short branches
B) It reduces merge-debt and keeps integration failures close to their cause
C) It is mandated by the Git documentation
D) It is the only workflow pre-commit supports

**Q18.** `git push --force-with-lease` is safer than `git push --force` because it:
A) Refuses the push if the remote has commits you have not fetched (prevents clobbering a teammate's work)
B) Runs the pre-commit hooks again
C) Compresses the pack
D) Creates a backup branch on the remote

**Q19.** You are mid-rebase with a conflict. The correct continuation sequence is:
A) `git rebase --skip`, edit, `git rebase --continue`
B) Edit conflict markers, `git add <file>`, `git rebase --continue`
C) `git merge --abort`, redo the branch
D) `git commit -am 'fix'`, `git rebase --continue`

**Q20.** Which item does NOT belong in a data-engineering repo's `.gitignore`?
A) `.env` files with credentials
B) Large raw data files (`*.parquet`, `*.csv`)
C) Jupyter notebook outputs (`*.ipynb_checkpoints`)
D) `pyproject.toml`

---

## Answers

| # | Ans | Source module | Primary citation |
|---|---|---|---|
| 1 | D | 01_linux_bash | [GNU bash manual — set](https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin) |
| 2 | B | 01_linux_bash | `kill(1)` — default signal is SIGTERM (man7.org) |
| 3 | C | 01_linux_bash | GNU coreutils `chmod` — octal mode |
| 4 | A | 02_networking | [RFC 1918 §3](https://www.rfc-editor.org/rfc/rfc1918) |
| 5 | B | 02_networking | [dig(1)](https://linux.die.net/man/1/dig) — `+trace` |
| 6 | B | 02_networking | [RFC 9110 §7](https://www.rfc-editor.org/rfc/rfc9110); TLS 1.3 RFC 8446 |
| 7 | C | 03_python | [PEP 518](https://peps.python.org/pep-0518/), [PEP 621](https://peps.python.org/pep-0621/) |
| 8 | B | 03_python | [pytest fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html) |
| 9 | C | 03_python | [pre-commit.com](https://pre-commit.com/) |
| 10 | B | 04_docker | [Dockerfile reference — CMD/ENTRYPOINT](https://docs.docker.com/reference/dockerfile/#cmd) |
| 11 | B | 04_docker | [Compose `depends_on`](https://docs.docker.com/reference/compose-file/services/#depends_on) |
| 12 | B | 04_docker | [Compose profiles](https://docs.docker.com/compose/how-tos/profiles/) |
| 13 | A | 05_sql_postgres | [PostgreSQL — Window Functions](https://www.postgresql.org/docs/current/tutorial-window.html) |
| 14 | B | 05_sql_postgres | [PostgreSQL — Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html) |
| 15 | B | 05_sql_postgres | [PostgreSQL — Planner Statistics](https://www.postgresql.org/docs/current/planner-stats.html) |
| 16 | B | 05_sql_postgres | [`pg_dump` — `-Fc`](https://www.postgresql.org/docs/current/app-pgdump.html) |
| 17 | B | 06_git | *Pro Git*, Chacon & Straub, Ch. 3 — Branching workflows |
| 18 | A | 06_git | [git-push — `--force-with-lease`](https://git-scm.com/docs/git-push#Documentation/git-push.txt---force-with-leaseltrefnamegt) |
| 19 | B | 06_git | [git-rebase — resolving conflicts](https://git-scm.com/docs/git-rebase#_resolving_conflicts) |
| 20 | D | 06_git | [gitignore(5)](https://git-scm.com/docs/gitignore) — `pyproject.toml` is source-of-truth, must be tracked |
