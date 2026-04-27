# Module 01: Linux & Bash Scripting (16h)

Working-level Linux and bash for a data engineer: enough to operate a container host, run healthchecks, script recurring jobs, and chase down problems in logs. Not a sysadmin course — the goal is to be unblocked when a Compose stack misbehaves or a pipeline needs a cron entry.

## Learning goals
- Navigate the Linux filesystem hierarchy and read `ls -l` output (type, permissions, owner, size).
- Change permissions and ownership with `chmod`/`chown` using both symbolic and octal notation.
- Inspect and control processes with `ps`, `top`, `kill`, and the common signals (SIGTERM vs SIGKILL).
- Configure `PATH`, environment variables, and shell startup (`~/.bashrc`) without breaking the login shell.
- Write a defensive bash script that uses `set -euo pipefail`, exit codes, loops, conditionals, and `jq` for JSON.
- Wire a recurring job into `cron` and understand why `anacron` exists.
- Pipe `grep`/`sed`/`awk`/`xargs` to transform text at the working level.

## Prerequisites
- [`../../phase_0_orientation/03_hardware_check/`](../../phase_0_orientation/03_hardware_check/) — a working local shell (macOS zsh or Linux bash) with `bash` ≥ 4.

## Reading order
1. This README
2. [`labs/lab_01_bash_scripting/README.md`](labs/lab_01_bash_scripting/README.md)
3. [`quiz.md`](quiz.md)

## Concepts

### Filesystem hierarchy
Linux mounts everything under a single root `/`. Config lives in `/etc`, logs in `/var/log`, user files in `/home`, ephemerals in `/tmp` (cleared on reboot) vs. `/var/tmp` (persists). `/proc` and `/sys` are virtual filesystems that expose process and kernel state as files — this is why `cat /proc/cpuinfo` works.
Ref: [Linux man-pages: hier(7)](https://man7.org/linux/man-pages/man7/hier.7.html)

### Permissions (chmod, chown)
Every file has three permission sets (owner / group / other) for read (4) / write (2) / execute (1). `755` = `rwxr-xr-x` (typical script), `644` = `rw-r--r--` (typical file), `600` = `rw-------` (SSH private key). `chmod` changes the bits, `chown user:group file` changes ownership. The sticky bit on `/tmp` (`1777`) means only a file's owner can delete it — relevant because Docker bind-mounts often land in `/tmp`.
Ref: [GNU coreutils: chmod](https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html)

### Processes and signals
`ps aux` lists every process; `top` / `htop` show a live view; `kill PID` sends **SIGTERM (15)** — a polite request the process can trap and clean up after. `kill -9 PID` sends **SIGKILL**, which cannot be caught — use it as a last resort because it leaves no chance to flush buffers or release locks. `docker stop` works the same way: SIGTERM first, then SIGKILL after a grace period.
Ref: [Linux man-pages: signal(7)](https://man7.org/linux/man-pages/man7/signal.7.html) · [Docker CLI: docker stop](https://docs.docker.com/reference/cli/docker/container/stop/)

### Package management
Three families, same job (install, upgrade, remove, resolve dependencies): Debian/Ubuntu uses `apt` (`.deb`), Red Hat/Fedora uses `dnf` (`.rpm`), macOS uses Homebrew (`brew`). `dpkg`/`rpm` are low-level and do **not** resolve dependencies — always use the high-level wrapper. You rarely install system packages on a data platform; most tools ship as container images or Python packages.
Ref: [Debian — Package management](https://www.debian.org/doc/manuals/debian-reference/ch02.en.html) · [Fedora — DNF](https://docs.fedoraproject.org/en-US/quick-docs/dnf/) · [Homebrew](https://brew.sh/)

### Environment variables and shell configuration
`env` / `printenv` list variables. `$PATH` is a colon-separated list of directories the shell searches for executables — misconfigure it and `ls` stops working, which is why you edit `~/.bashrc` and keep a second terminal open. `export FOO=bar` makes `FOO` available to child processes; without `export`, it is local to the current shell. Login shells also read `~/.bash_profile` (or `~/.profile`). On macOS, interactive shells default to zsh and read `~/.zshrc`.
Ref: [Bash Reference Manual: Bash Startup Files](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html)

### Bash scripting: the defensive prelude
Start every script with:

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
```

- `-e` exits on the first failed command.
- `-u` errors on unset variables (catches typos).
- `-o pipefail` makes `a | b` fail if either side fails, not just the last.
- `IFS=$'\n\t'` stops word-splitting on spaces, which prevents filename bugs.

Every command returns an **exit code**: `0` = success, non-zero = failure. You check it with `$?`, but usually with `if cmd; then ...` or `cmd || handle_error`.
Ref: [Bash Reference Manual: The Set Builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html) · [Bash Reference Manual: Exit Status](https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html)

### Variables, conditionals, loops
Variables have no type: `name="alice"`, reference with `"$name"` (always quote to survive spaces). Conditionals use `[[ ... ]]` (bash) over `[ ... ]` (POSIX) — better string handling and no glob expansion. Loops: `for svc in postgres minio trino; do ...; done` and `while read -r line; do ...; done < file`.
Ref: [Bash Reference Manual: Conditional Constructs](https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html) · [Bash Reference Manual: Looping Constructs](https://www.gnu.org/software/bash/manual/html_node/Looping-Constructs.html)

### Piping, redirection, process substitution
Every command has three streams: stdin (0), stdout (1), stderr (2). `cmd > out.log` redirects stdout (overwrite), `>>` appends, `2>&1` merges stderr into stdout, `&>` does both in one token. Pipes `a | b` send `a`'s stdout to `b`'s stdin. **Process substitution** `<(cmd)` gives you a filename-like handle to a command's output — useful for `diff <(ls dir_a) <(ls dir_b)`.
Ref: [Bash Reference Manual: Redirections](https://www.gnu.org/software/bash/manual/html_node/Redirections.html) · [Bash Reference Manual: Process Substitution](https://www.gnu.org/software/bash/manual/html_node/Process-Substitution.html)

### jq for JSON
`jq` is a command-line JSON processor. Data APIs, Docker `inspect`, and `kubectl -o json` all emit JSON — `jq` is how you query it in a shell pipeline: `docker inspect pg | jq -r '.[0].State.Health.Status'`. Use `-r` for raw (unquoted) output when piping to another command.
Ref: [jq manual](https://jqlang.github.io/jq/manual/)

### Text processing: grep / sed / awk / xargs
- `grep -n pattern file` — find lines, with line numbers. `-r` recurses, `-v` inverts, `-i` is case-insensitive.
- `sed 's/old/new/g' file` — stream edit. `-i` edits in place (note: `sed -i` on macOS requires an empty backup suffix: `sed -i '' ...`).
- `awk -F: '{print $1,$3}' /etc/passwd` — column-oriented processing with a default field separator.
- `xargs` converts stdin lines into arguments: `find . -name '*.log' | xargs gzip` compresses each. Use `-0` with `find -print0` when filenames might contain spaces.
Ref: [GNU grep manual](https://www.gnu.org/software/grep/manual/grep.html) · [GNU sed manual](https://www.gnu.org/software/sed/manual/sed.html) · [GNU awk manual](https://www.gnu.org/software/gawk/manual/gawk.html) · [Linux man-pages: xargs(1)](https://man7.org/linux/man-pages/man1/xargs.1.html)

### Cron scheduling
`crontab -e` edits your user's scheduled jobs. Five fields: `minute hour day-of-month month day-of-week command`. `*/15 * * * *` = every 15 minutes. `@daily` = midnight. cron only fires if the machine is on at the scheduled time; `anacron` catches up after downtime — useful for laptops, irrelevant for always-on servers. Data platforms usually outgrow cron and move to Dagster/Airflow, but cron is still the right answer for "run this healthcheck every 5 minutes on the host".
Ref: [Linux man-pages: crontab(5)](https://man7.org/linux/man-pages/man5/crontab.5.html) · [Linux man-pages: cron(8)](https://man7.org/linux/man-pages/man8/cron.8.html)

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_01_bash_scripting` | Write a defensive `healthcheck.sh` that checks three services in a Docker Compose stack and returns meaningful exit codes | 60m | [labs/lab_01_bash_scripting/](labs/lab_01_bash_scripting/) |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| `./script.sh: Permission denied` | File is not executable | `chmod +x script.sh` | [GNU coreutils: chmod](https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html) |
| Script runs in one terminal, fails in another | Variable was set but not `export`ed; child process never saw it | `export VAR=value` and add to `~/.bashrc` | [Bash: Bourne Shell Builtins (export)](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html) |
| `unbound variable` on what looks like valid code | `set -u` plus a typo in a variable name | Fix the typo, or use `"${VAR:-default}"` for intentional defaults | [Bash: Shell Parameter Expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html) |
| Pipeline "succeeds" even though a middle stage failed | Default bash only reports the exit of the **last** command in a pipe | `set -o pipefail` | [Bash: The Set Builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html) |
| cron job works by hand but not from crontab | cron runs with a minimal `PATH` and no shell init files | Use absolute paths; set `PATH=` at the top of the crontab | [Linux man-pages: crontab(5)](https://man7.org/linux/man-pages/man5/crontab.5.html) |
| `kill PID` does nothing | Process is trapping SIGTERM or stuck in uninterruptible sleep | `kill -9 PID` (SIGKILL) — last resort only | [signal(7)](https://man7.org/linux/man-pages/man7/signal.7.html) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Explain what `755`, `644`, `600` mean without looking them up.
- [ ] Write a one-liner that finds all `.log` files under `/var/log` modified in the last day and gzips them (`find … -print0 | xargs -0 gzip`).
- [ ] Write a bash script starting with `set -euo pipefail` that loops over three service names and returns a non-zero exit code if any fail a check.
- [ ] Explain the difference between SIGTERM and SIGKILL and why `docker stop` uses SIGTERM first.
- [ ] Parse a field out of `docker inspect` JSON with `jq -r`.
- [ ] Write a crontab line that runs a script every 15 minutes and logs to `/var/log/myjob.log`.
