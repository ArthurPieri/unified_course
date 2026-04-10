# References — 03_python

## Primary docs
- [Python 3 docs](https://docs.python.org/3/) — language and standard library reference
- [`venv`](https://docs.python.org/3/library/venv.html) — stdlib virtual environments
- [`dataclasses`](https://docs.python.org/3/library/dataclasses.html) — stdlib value objects

## PEPs
- [PEP 518 — Build system requirements](https://peps.python.org/pep-0518/) — defines `pyproject.toml` and `[build-system]`
- [PEP 621 — Project metadata](https://peps.python.org/pep-0621/) — defines the `[project]` table schema

## Packaging
- [Python Packaging User Guide — src layout vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)

## Tooling
- [uv — Getting started](https://docs.astral.sh/uv/getting-started/)
- [uv — Projects](https://docs.astral.sh/uv/concepts/projects/)
- [uv — Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)
- [uv — Python versions](https://docs.astral.sh/uv/concepts/python-versions/)
- [Ruff — Configuration](https://docs.astral.sh/ruff/configuration/)
- [Ruff — Rules](https://docs.astral.sh/ruff/rules/)
- [Ruff — Formatter](https://docs.astral.sh/ruff/formatter/)
- [mypy — Introduction](https://mypy.readthedocs.io/en/stable/)
- [mypy — Configuration file](https://mypy.readthedocs.io/en/stable/config_file.html)
- [pre-commit — Quick start](https://pre-commit.com/#quick-start)
- [pre-commit — `.pre-commit-config.yaml`](https://pre-commit.com/#pre-commit-configyaml---hooks)
- [pip](https://pip.pypa.io/en/stable/) — alternative installer
- [Poetry](https://python-poetry.org/docs/) — alternative project tool

## Testing
- [pytest — Getting started](https://docs.pytest.org/en/stable/getting-started.html)
- [pytest — Fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [pytest — conftest.py](https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files)
- [pytest — Parametrizing tests](https://docs.pytest.org/en/stable/how-to/parametrize.html)
- [pytest — `monkeypatch`](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)
- [pytest — `tmp_path`](https://docs.pytest.org/en/stable/how-to/tmp_path.html)

## Validation
- [Pydantic — Models](https://docs.pydantic.dev/latest/concepts/models/)

## Sibling sources
- `../dataeng/pyproject.toml:L1-L33` — real `[project]`, optional-dependencies groups, `[tool.ruff]`, `[tool.pytest.ini_options]`
- `../dataeng/tests/conftest.py:L1-L37` — real pytest fixtures (`monkeypatch`-based env setup, `tmp_path`-based pipeline dir)
