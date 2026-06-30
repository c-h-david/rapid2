# AGENTS.md

Field guide for AI coding agents working on rapid2. Read this first,
then load the authoritative sources below before writing any code or
markdown. This file points to those sources rather than restating them,
so it stays short and they remain the single point of maintenance.

When this file and an authoritative source disagree, the source wins.
Open a PR to fix this file.

## Authoritative sources

Load the relevant ones before you start; do not reproduce their content
from memory.

- [`NOMENCLATURE.md`][NOM] — semantic naming grammar for data
  structures, files, and functions. Strictly enforced for the core
  model and library.
- [`CONTRIBUTING.md`][CON] — fork / branch / test / pull request flow.
- [`TESTING.md`][TST] — every lint, format, type-check, and doctest
  command, plus the config files (`.pymarkdown.yml`, `.yamllint.yml`,
  `pyproject.toml`) that define their options. This is the single
  source for how CI checks code.
- [`.github/workflows/CL.yml`][CL] — the exact command sequence CI runs
  on every PR (the static-analysis checks in `TESTING.md`).
- [`CLI_STYLE.md`][CLI] — the file-structure and formatting standard for
  CLI scripts, and how to register a CLI in `pyproject.toml`.
- [`src/rapid2/cli/_rapid2.py`][R2] — the canonical script to mirror;
  for a small read-and-report tool, [`_zeroqinit.py`][ZQI] is lighter.

## Program structure

Code style and CI are defined by the sources above. The one convention
worth stating up front is program structure, because a coding assistant
rarely infers it correctly:

- New CLI tools go under `src/rapid2/cli/` as `_<tool>.py`, follow the
  skeleton in [`CLI_STYLE.md`][CLI], and mirror `_rapid2.py`.
- Register each new CLI under `[project.scripts]` in `pyproject.toml`.

## Running locally

Install the package editable so your working tree shadows any installed
copy (`pip install -e ".[dev]"`), then call tools by their registered
console name.

## Pre-PR checklist

Before opening a PR:

- Run every CI gate locally from [`TESTING.md`][TST]: markdown, YAML,
  Dockerfile, shell, `ruff` lint, `ruff` format, and `mypy`. Each must
  exit 0 — CI (`CL.yml`) runs exactly these.
- Also run the doctests (`python3 -m doctest`, per [`TESTING.md`][TST]);
  CI does not gate them, but they must pass.
- Branch off `main` with a descriptive name (`add-foo`,
  `fix-bar-timeout`).
- New CLI script? Registered under `[project.scripts]` in
  `pyproject.toml` (see [`CLI_STYLE.md`][CLI]).
- Names follow [`NOMENCLATURE.md`][NOM].
- Commit messages and PR body are written by you, not your agent. No
  AI / agent self-references, no `Generated with ...` footers.
- PR body is short, paragraph-style prose. State why, not what.

[NOM]: NOMENCLATURE.md
[CON]: CONTRIBUTING.md
[TST]: TESTING.md
[CL]: .github/workflows/CL.yml
[CLI]: CLI_STYLE.md
[R2]: src/rapid2/cli/_rapid2.py
[ZQI]: src/rapid2/cli/_zeroqinit.py
