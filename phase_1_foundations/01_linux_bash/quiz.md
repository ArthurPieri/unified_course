# 01 Linux & Bash — Exit Quiz

10 questions. One best answer each. Answer key at the bottom with primary-source citations.

---

**Q1.** A file is listed as `-rwxr-xr--`. Which octal value matches these permissions?
A) 777
B) 755
C) 754
D) 644

**Q2.** `kill` (with no signal flag) sends which signal by default?
A) SIGKILL (9)
B) SIGTERM (15)
C) SIGHUP (1)
D) SIGSTOP (19)

**Q3.** You need a bash script to abort on the first failed command, error on unset variables, and fail a pipeline if any stage fails. Which line do you add near the top?
A) `set -x`
B) `set -euo pipefail`
C) `trap 'exit 1' ERR`
D) `shopt -s failglob`

**Q4.** Which command lists all TCP sockets in the `LISTEN` state together with the process that owns each?
A) `ps aux | grep LISTEN`
B) `ss -tlnp`
C) `ping -l`
D) `netstat -r`

**Q5.** In a crontab, what does `*/15 * * * *` mean?
A) Run once at 15:00 every day
B) Run every 15 seconds
C) Run every 15 minutes
D) Run on the 15th of each month

**Q6.** What is the purpose of `set -o pipefail` in a bash script?
A) Forces `|` to forward stderr as well as stdout
B) Makes a pipeline's exit status non-zero if any command in it fails, not just the last
C) Prevents a pipeline from buffering
D) Runs all pipeline commands in parallel

**Q7.** You want to extract the `.State.Health.Status` field from `docker inspect <container>` JSON output in a shell pipeline. Which tool is the right choice?
A) `awk`
B) `grep -o`
C) `jq -r`
D) `cut -d.`

**Q8.** `export FOO=bar` differs from `FOO=bar` in that:
A) `export` writes the variable to `~/.bashrc` automatically
B) `export` makes `FOO` visible to subprocesses of the current shell; without `export` it is shell-local
C) `export` is required for any assignment inside a function
D) There is no difference

**Q9.** Which directory's contents are cleared on reboot?
A) `/var/tmp`
B) `/tmp`
C) `/home`
D) `/var/log`

**Q10.** `find /var/log -name '*.log' -print0 | xargs -0 gzip` — why `-print0` and `-0`?
A) Performance — `-0` runs faster
B) To preserve filenames containing spaces or newlines by using a NUL separator
C) To enable parallel execution
D) Because `xargs` requires it on all GNU systems

---

## Answer key

**Q1 — C (754).** `rwx` = 7, `r-x` = 5, `r--` = 4. Ref: [GNU coreutils: chmod](https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html) · `../linux_fundamentals/course/01-linux-fundamentals.md:L680-L699`.

**Q2 — B (SIGTERM).** Default `kill` signal is 15 / SIGTERM, which the process can trap. Ref: [signal(7)](https://man7.org/linux/man-pages/man7/signal.7.html) · `../linux_fundamentals/course/01-linux-fundamentals.md:L965-L974`.

**Q3 — B.** `-e` exits on error, `-u` errors on unset, `-o pipefail` propagates pipeline failures. Ref: [Bash Reference Manual: The Set Builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html).

**Q4 — B (`ss -tlnp`).** `-t` TCP, `-l` listening, `-n` numeric, `-p` show process. Ref: [Linux man-pages: ss(8)](https://man7.org/linux/man-pages/man8/ss.8.html) · `../linux_fundamentals/course/02-system-administration.md:L1141-L1166`.

**Q5 — C (every 15 minutes).** The `*/N` step value in the minute field. Ref: [Linux man-pages: crontab(5)](https://man7.org/linux/man-pages/man5/crontab.5.html) · `../linux_fundamentals/course/02-system-administration.md:L542-L572`.

**Q6 — B.** Without `pipefail`, only the last command's exit status is reported. Ref: [Bash Reference Manual: The Set Builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html).

**Q7 — C (`jq -r`).** `jq` is the standard JSON processor; `-r` strips quotes for shell use. Ref: [jq manual](https://jqlang.github.io/jq/manual/).

**Q8 — B.** `export` marks the variable for inheritance by child processes. Ref: [Bash Reference Manual: Bourne Shell Builtins (export)](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html).

**Q9 — B (`/tmp`).** `/tmp` is cleared on reboot; `/var/tmp` persists. Ref: [Linux man-pages: hier(7)](https://man7.org/linux/man-pages/man7/hier.7.html) · `../linux_fundamentals/course/01-linux-fundamentals.md:L219-L221`.

**Q10 — B.** NUL (`\0`) is the only byte that cannot appear in a filename, so `-print0`/`-0` is the safe separator. Ref: [Linux man-pages: xargs(1)](https://man7.org/linux/man-pages/man1/xargs.1.html) · [Linux man-pages: find(1)](https://man7.org/linux/man-pages/man1/find.1.html).
