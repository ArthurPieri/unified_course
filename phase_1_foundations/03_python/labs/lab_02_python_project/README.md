# Lab 02: Scaffold a uv-managed Python project

## Goal
By the end you have a working `demo_project` with `pyproject.toml`, a src-layout package, a parametrized pytest test, and pre-commit hooks running `ruff` + `mypy` — all three commands exit 0.

## Prerequisites
- Python 3.10+ on `PATH`
- `uv` installed ([uv — Getting started](https://docs.astral.sh/uv/getting-started/))
- Git initialized in the parent directory (for pre-commit)

## Setup
```bash
uv --version                 # sanity check
uv init demo_project         # scaffolds pyproject.toml + src/demo_project
cd demo_project
git init                     # pre-commit needs a git repo
```

## Steps

1. **Inspect the generated layout.**
   ```bash
   ls -R
   cat pyproject.toml
   ```
   You should see `src/demo_project/` and a `[project]` table (PEP 621 schema — [PEP 621](https://peps.python.org/pep-0621/)).

2. **Add dev dependencies.**
   ```bash
   uv add --dev ruff mypy pytest pre-commit
   ```
   This writes `[dependency-groups] dev = [...]` and updates `uv.lock` ([uv — Projects](https://docs.astral.sh/uv/concepts/projects/)).

3. **Write the module.** Create `src/demo_project/hello.py`:
   ```python
   def greet(name: str) -> str:
       return f"Hello, {name}"
   ```

4. **Write a parametrized test.** Create `tests/test_hello.py`:
   ```python
   import pytest
   from demo_project.hello import greet

   @pytest.mark.parametrize(
       "name,expected",
       [("Ada", "Hello, Ada"), ("Grace", "Hello, Grace"), ("", "Hello, ")],
   )
   def test_greet(name: str, expected: str) -> None:
       assert greet(name) == expected
   ```
   See [pytest — Parametrizing tests](https://docs.pytest.org/en/stable/how-to/parametrize.html).

5. **Configure tool tables** in `pyproject.toml` (schema per PEP 621 tool-table convention — [PEP 621](https://peps.python.org/pep-0621/)):
   ```toml
   [tool.ruff]
   target-version = "py310"
   line-length = 100

   [tool.ruff.lint]
   select = ["E", "F", "I", "W"]

   [tool.mypy]
   python_version = "3.10"
   strict = true
   files = ["src"]

   [tool.pytest.ini_options]
   testpaths = ["tests"]
   ```
   `[tool.ruff]` options: [Ruff — Configuration](https://docs.astral.sh/ruff/configuration/). `[tool.mypy]`: [mypy — Config file](https://mypy.readthedocs.io/en/stable/config_file.html).

6. **Create `.pre-commit-config.yaml`** (syntax per [pre-commit — `.pre-commit-config.yaml`](https://pre-commit.com/#pre-commit-configyaml---hooks)):
   ```yaml
   repos:
     - repo: https://github.com/astral-sh/ruff-pre-commit
       rev: v0.6.9
       hooks:
         - id: ruff
         - id: ruff-format
     - repo: https://github.com/pre-commit/mirrors-mypy
       rev: v1.11.2
       hooks:
         - id: mypy
           files: ^src/
   ```
   Install the git hook:
   ```bash
   uv run pre-commit install
   ```

7. **Run the three checks.**
   ```bash
   uv run ruff check .
   uv run mypy src
   uv run pytest
   ```
   Expected: each command prints a success summary and exits 0.

## Verify
- [ ] `uv run ruff check .` exits 0
- [ ] `uv run mypy src` exits 0
- [ ] `uv run pytest` reports 3 passing parametrized cases
- [ ] `uv run pre-commit run --all-files` exits 0
- [ ] `uv.lock` exists and is committed

## Cleanup
```bash
cd ..
rm -rf demo_project
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: demo_project` in pytest | Run via `uv run pytest` so the venv has the editable install |
| `mypy` complains about missing stubs for `pytest` | `uv add --dev types-... ` or set `[[tool.mypy.overrides]] ignore_missing_imports = true` ([mypy config](https://mypy.readthedocs.io/en/stable/config_file.html)) |
| pre-commit hook versions drift | `uv run pre-commit autoupdate` ([pre-commit — autoupdate](https://pre-commit.com/#pre-commit-autoupdate)) |

## Stretch goals
- Add a failing test, `git add` it, `git commit` — confirm `pre-commit` blocks the commit until the test passes.
- Add a `[project.scripts] demo = "demo_project.hello:greet"` entry and run it via `uv run demo` ([PEP 621 — entry points](https://peps.python.org/pep-0621/)).
- Split dev tools into `[dependency-groups]` and compare `uv sync` vs. `uv sync --frozen` behavior on a second clone ([uv — Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)).

## References
See `../../references.md` (module-level).
