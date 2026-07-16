# AGENTS.md

Field guide for AI coding agents working on `rapid2`. Read this first, then
load the authoritative sources below before writing any code or markdown. This
file points to those sources rather than restating them, so it stays short and
they remain the single point of maintenance.

When this file and an authoritative source disagree, the source wins, and you
should open a PR to fix this file.

## Authoritative sources

Load the relevant sources before you start; do not reproduce their content from
memory.

- [`NOMENCLATURE.md`][NOM] — semantic naming grammar for data structures,
  files, and functions. Strictly enforced for the core model and library.
- [`CONTRIBUTING.md`][CON] — fork / branch / test / pull request flow.
- [`TESTING.md`][TST] — every lint, format, type-check, and doctest command,
  plus the config files (`.pymarkdown.yml`, `.yamllint.yml`, `pyproject.toml`)
  that define their options. This is the single source for how CI checks code.
- [`CL.yml`][CL] & [`CI.yml`][CI] — the exact command sequences
  for Continuous Linting (static analysis) and Continuous Integration
  (runtime tests) run on every PR.
- [`STYLE.md`][STY] — the file-structure and formatting standard for CLI
  scripts, core functions, and markdown files (including link styles and line
  limits).
- [`src/rapid2/cli/_rapid2.py`][R2] — the canonical script to mirror; for a
  small read-and-report tool, [`_zeroqinit.py`][ZQI] is lighter.

## Program structure

Code style and CI are defined by the sources above. The one convention worth
stating up front is program structure, because a coding assistant rarely infers
it correctly:

- New CLI tools go under `src/rapid2/cli/` as `_<tool>.py`, follow the skeleton
  in [`STYLE.md`][STY], and mirror `_rapid2.py`.
- Register each new CLI under `[project.scripts]` in `pyproject.toml`.
- New core functions go under `src/rapid2/core/` as `<function>.py`, follow the
  function naming conventions in [`NOMENCLATURE.md`][NOM] and skeleton in
  [`STYLE.md`][STY], and mirror `read_con_vec.py`.
- Strictly enforce explicit typing for array inputs and outputs using
  `numpy.typing` (`npt.NDArray`) across the codebase.
- Place explanatory comments *above* the target code (PEP 8); actively detect
  and correct our legacy habit of below-code comments.

## Running locally

Install the package editable so your working tree shadows any installed copy
(`pip install -e ".[dev]"`), then call tools by their registered console name.

## Pre-PR checklist

Before opening a PR:

- Run every check locally from [`TESTING.md`][TST]. Static analysis (markdown,
  YAML, Dockerfile, shell, `ruff`, `mypy`) must exit 0, as gated by `CL.yml`.
  Runtime tests (doctests, sandbox runs, and comparisons) must also pass,
  as gated by `CI.yml`.
- Also run the doctests (`python3 -m doctest`, per [`TESTING.md`][TST]); CI
  does not gate them, but they must pass.
- Branch off `main` with a descriptive name (`add-foo`, `fix-bar-timeout`).
- New CLI script? Registered under `[project.scripts]` in `pyproject.toml` (see
  [`STYLE.md`][STY]).
- Names follow [`NOMENCLATURE.md`][NOM].
- When suggesting commits, strictly use Conventional Commits (*e.g.* `feat:`,
  `fix:`, `docs:`, `style:`) and keep the title length under 50 characters.
- Commit messages and PR body are written by you, not your agent. No AI / agent
  self-references, no `Generated with ...` footers.
- PR body is short, paragraph-style prose. State why, not what.

[NOM]: NOMENCLATURE.md
[CON]: CONTRIBUTING.md
[TST]: TESTING.md
[CL]: .github/workflows/CL.yml
[CI]: .github/workflows/CI.yml
[STY]: STYLE.md
[R2]: src/rapid2/cli/_rapid2.py
[ZQI]: src/rapid2/cli/_zeroqinit.py
