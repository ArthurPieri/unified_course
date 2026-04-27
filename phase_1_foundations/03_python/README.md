# Module 03: Python Engineering for Data (12h)

> GAP module — no comprehensive sibling source. Citations are to primary docs and PEPs.

## Learning goals
- Scaffold a reproducible Python project with `pyproject.toml` and a lockfile
- Choose `src/` vs. flat layout and justify it
- Configure `ruff`, `mypy`, and `pre-commit` so code quality is enforced on every commit
- Write `pytest` tests using fixtures and `@pytest.mark.parametrize`
- Know when to reach for `@dataclass` vs. a Pydantic model

## Prerequisites
- [../01_linux_bash/](../01_linux_bash/) — shell, PATH, environment variables
- Python 3.10+ installed and on `PATH`

## Reading order
1. This README
2. [labs/lab_02_python_project/README.md](labs/lab_02_python_project/README.md)
3. [quiz.md](./quiz.md)

## Concepts

### `pyproject.toml` is the project spec
`pyproject.toml` is the single declarative file that describes a Python project: build backend, dependencies, tool config. PEP 518 introduced the file and the `[build-system]` table to declare build requirements. PEP 621 standardized the `[project]` table — name, version, `requires-python`, `dependencies`, optional-dependencies — so the metadata is portable across tools.
Ref: [PEP 518](https://peps.python.org/pep-0518/) · [PEP 621](https://peps.python.org/pep-0621/)

A minimal working `pyproject.toml` includes a `[project]` block with `requires-python = ">=3.10"`, `[project.optional-dependencies]` for `dev`/`dlt`/`dbt` groups, and tool tables `[tool.ruff]`, `[tool.ruff.lint]`, `[tool.pytest.ini_options]`.

### `src/` layout vs. flat layout
In a `src/` layout the importable package lives at `src/<pkg>/` instead of `<pkg>/` at the repo root. The practical consequence: running tests or scripts from the project root can only import the package via the installed distribution, which catches packaging bugs early (missing `__init__.py`, files excluded from the wheel). The Python Packaging User Guide documents both layouts and the trade-off.
Ref: [Packaging User Guide — src layout vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)

### Virtual environments and reproducibility
A virtual environment isolates a project's interpreter and installed packages from the system Python. `venv` is built into the standard library.
Ref: [`venv` — Creation of virtual environments](https://docs.python.org/3/library/venv.html)

Reproducibility needs more than a venv: it needs a **lockfile** that pins every transitive dependency and a pinned Python version. `uv` writes `uv.lock` automatically on `uv add` / `uv sync` and honours a `.python-version` file to pin the interpreter; `uv sync` recreates the exact resolved set on another machine.
Ref: [uv — Projects](https://docs.astral.sh/uv/concepts/projects/) · [uv — Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/) · [uv — Python versions](https://docs.astral.sh/uv/concepts/python-versions/)

`uv` is the recommended tool in this course because it resolves, installs, locks, and runs from a single binary. `pip` + `venv` and Poetry remain valid alternatives; pick one and commit to it per project.
Ref: [uv — Getting started](https://docs.astral.sh/uv/getting-started/) · [pip](https://pip.pypa.io/en/stable/) · [Poetry](https://python-poetry.org/docs/)

### Code quality: `ruff`, `mypy`, `pre-commit`
`ruff` is a linter and formatter. A single tool replaces the `flake8` + `isort` + `black` stack; rules are selected via `[tool.ruff.lint] select = [...]`. A practical starting set is `select = ["E", "F", "I", "W"]` — pycodestyle errors/warnings, pyflakes, and import sorting.
Ref: [Ruff — Configuration](https://docs.astral.sh/ruff/configuration/) · [Ruff — Rules](https://docs.astral.sh/ruff/rules/) · [Ruff — Formatter](https://docs.astral.sh/ruff/formatter/)

`mypy` is a static type checker. It reads the annotations you already write (`def greet(name: str) -> str:`) and flags mismatches before runtime.
Ref: [mypy — Introduction](https://mypy.readthedocs.io/en/stable/) · [mypy — Configuration file](https://mypy.readthedocs.io/en/stable/config_file.html)

`pre-commit` runs these tools as git hooks so bad code never lands in a commit. Hooks are declared in `.pre-commit-config.yaml` with a `repos:` list; each repo pins a `rev` and lists `hooks` by `id`. `pre-commit install` writes the git hook; `pre-commit run --all-files` runs them ad-hoc.
Ref: [pre-commit — Quick start](https://pre-commit.com/#quick-start) · [pre-commit — Plugins](https://pre-commit.com/#pre-commit-configyaml---hooks)

### Testing with `pytest`
`pytest` discovers files matching `test_*.py` and functions matching `test_*` and uses plain `assert` statements. Test discovery paths are configured via `[tool.pytest.ini_options] testpaths = [...]` in `pyproject.toml`.
Ref: [pytest — Getting started](https://docs.pytest.org/en/stable/getting-started.html) · [pytest — How to invoke](https://docs.pytest.org/en/stable/how-to/usage.html)

**Fixtures** are functions decorated with `@pytest.fixture` that provide setup/teardown and are injected by parameter name. They have scopes (`function`, `class`, `module`, `session`) that control how often they run. A `conftest.py` file shares fixtures across every test file in its directory and subdirectories — no import needed. Two common patterns: a fixture that uses `monkeypatch` to set environment variables (e.g., mock cloud credentials), and a fixture that builds on the built-in `tmp_path` to create a temporary directory structure for pipeline tests.
Ref: [pytest — Fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) · [pytest — conftest.py](https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files) · [pytest — monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html) · [pytest — tmp_path](https://docs.pytest.org/en/stable/how-to/tmp_path.html)

**Parametrize** runs the same test body against multiple inputs:
```python
@pytest.mark.parametrize("name,expected", [("Ada", "Hello, Ada"), ("", "Hello, ")])
def test_greet(name, expected):
    assert greet(name) == expected
```
Ref: [pytest — Parametrizing tests](https://docs.pytest.org/en/stable/how-to/parametrize.html)

### `dataclass` vs. Pydantic
Use `@dataclass` (stdlib) for plain in-process value objects where you control the inputs: it generates `__init__`, `__repr__`, `__eq__`. No runtime validation — annotations are hints.
Ref: [`dataclasses`](https://docs.python.org/3/library/dataclasses.html)

Use a Pydantic `BaseModel` when data crosses a trust boundary (HTTP payloads, config files, external APIs) and you need runtime validation and coercion.
Ref: [Pydantic — Models](https://docs.pydantic.dev/latest/concepts/models/)

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_02_python_project` | Scaffold a uv project with ruff + mypy + pytest + pre-commit, all hooks green | 60m | [labs/lab_02_python_project/](labs/lab_02_python_project/) |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| `ModuleNotFoundError` when running tests | `src/` layout but package not installed into the venv | `uv sync` (or `pip install -e .`) so the package is importable | [Packaging User Guide — src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) |
| `ruff` and the formatter disagree | Using `black` alongside `ruff format` | Drop `black`; `ruff format` is Black-compatible | [Ruff — Formatter](https://docs.astral.sh/ruff/formatter/) |
| `pre-commit` hook runs an old version | `rev:` in `.pre-commit-config.yaml` is stale | `pre-commit autoupdate` | [pre-commit — autoupdate](https://pre-commit.com/#pre-commit-autoupdate) |
| CI installs different versions than laptop | No lockfile committed | Commit `uv.lock`; use `uv sync --frozen` in CI | [uv — Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Explain what PEP 518 and PEP 621 each standardize
- [ ] Create a uv project, add a dev dep, and commit `uv.lock`
- [ ] Configure `[tool.ruff]`, `[tool.mypy]`, and `[tool.pytest.ini_options]` in `pyproject.toml`
- [ ] Write a `conftest.py` fixture and consume it from a parametrized test
- [ ] State one case where you would use Pydantic instead of `@dataclass`
