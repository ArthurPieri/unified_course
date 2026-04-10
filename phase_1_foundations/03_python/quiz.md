# Quiz — 03_python

10 multiple-choice questions. Answers and sources at the bottom.

---

**1.** Which PEP defines the `[build-system]` table in `pyproject.toml`?
- A. PEP 8
- B. PEP 440
- C. PEP 518
- D. PEP 621

**2.** Which PEP standardizes the `[project]` table (`name`, `version`, `dependencies`, …)?
- A. PEP 517
- B. PEP 518
- C. PEP 621
- D. PEP 660

**3.** A main benefit of the `src/` layout over the flat layout is:
- A. It makes imports shorter
- B. It forces tests to import the installed package, catching packaging bugs early
- C. It lets you skip writing `__init__.py`
- D. It is required by `pyproject.toml`

**4.** What does `uv sync --frozen` do?
- A. Upgrades the lockfile to the newest compatible versions
- B. Installs exactly the versions pinned in `uv.lock` without re-resolving
- C. Writes a new `uv.lock` from scratch
- D. Deletes the virtual environment

**5.** Which single tool replaces the `flake8 + isort + black` stack in this course?
- A. mypy
- B. pylint
- C. ruff
- D. pyright

**6.** Where do you put a pytest fixture so every test file in a directory tree can use it without importing?
- A. In `pytest.ini`
- B. In `conftest.py`
- C. In `__init__.py`
- D. In `setup.cfg`

**7.** Which decorator runs the same test body against multiple input/expected pairs?
- A. `@pytest.fixture`
- B. `@pytest.mark.skip`
- C. `@pytest.mark.parametrize`
- D. `@pytest.mark.xfail`

**8.** In `.pre-commit-config.yaml`, what does the `rev:` field under a `repos:` entry pin?
- A. The Python version the hook runs on
- B. The git revision (tag/SHA) of the hook repository
- C. The severity level of the hook
- D. The number of retries

**9.** When should you prefer a Pydantic `BaseModel` over a stdlib `@dataclass`?
- A. Always — dataclasses are deprecated
- B. When you need runtime validation of data crossing a trust boundary (HTTP, config files)
- C. When you want faster attribute access
- D. When the object has fewer than 5 fields

**10.** Which pytest built-in fixture gives each test a unique temporary directory as a `pathlib.Path`?
- A. `tmpdir`
- B. `tmp_path`
- C. `monkeypatch`
- D. `capsys`

---

## Answer key

| # | Answer | Source |
|---|---|---|
| 1 | C | [PEP 518](https://peps.python.org/pep-0518/) |
| 2 | C | [PEP 621](https://peps.python.org/pep-0621/) |
| 3 | B | [Packaging User Guide — src layout vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) |
| 4 | B | [uv — Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/) |
| 5 | C | [Ruff — Formatter](https://docs.astral.sh/ruff/formatter/), [Ruff — Rules](https://docs.astral.sh/ruff/rules/) |
| 6 | B | [pytest — conftest.py](https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files) |
| 7 | C | [pytest — Parametrizing tests](https://docs.pytest.org/en/stable/how-to/parametrize.html) |
| 8 | B | [pre-commit — `.pre-commit-config.yaml`](https://pre-commit.com/#pre-commit-configyaml---hooks) |
| 9 | B | [Pydantic — Models](https://docs.pydantic.dev/latest/concepts/models/), [`dataclasses`](https://docs.python.org/3/library/dataclasses.html) |
| 10 | B | [pytest — `tmp_path`](https://docs.pytest.org/en/stable/how-to/tmp_path.html) |
