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

- [`NOMENCLATURE.md`][LOC_NOMENC] — semantic naming grammar for data
  structures, files, and functions. Strictly enforced for the core model and
  library.
- [`CONTRIBUTING.md`][LOC_CONTRI] — fork / branch / test / pull request flow.
- [`TESTING.md`][LOC_TSTING] — every lint, format, type-check, and doctest
  command, plus the config files (`.pymarkdown.yml`, `.yamllint.yml`,
  `pyproject.toml`) that define their options. This is the single source for
  how CI checks code.
- [`CL.yml`][LOC_CLWORK] & [`CI.yml`][LOC_CIWORK] — the exact command sequences
  for Continuous Linting (static analysis) and Continuous Integration
  (runtime tests) run on every PR.
- [`STYLE.md`][LOC__STYLE] — the file-structure and formatting standard for CLI
  scripts, core functions, and markdown files (including link styles and line
  limits).
- [`src/rapid2/cli/_rapid2.py`][LOC_RAPID2] — the canonical script to mirror;
  for a small read-and-report tool, [`_zeroqinit.py`][LOC_ZEROQI] is lighter.

## Program structure

Code style and CI are defined by the sources above. The one convention worth
stating up front is program structure, because a coding assistant rarely infers
it correctly:

- New CLI tools go under `src/rapid2/cli/` as `_<tool>.py`, follow the skeleton
  in [`STYLE.md`][LOC__STYLE], and mirror `_rapid2.py`.
- Register each new CLI under `[project.scripts]` in `pyproject.toml`.
- New core functions go under `src/rapid2/core/` as `<function>.py`, follow the
  function naming conventions in [`NOMENCLATURE.md`][LOC_NOMENC] and skeleton
  in [`STYLE.md`][LOC__STYLE], and mirror `read_con_vec.py`.
- Strictly enforce explicit typing for array inputs and outputs using
  `numpy.typing` (`npt.NDArray`) across the codebase.
- Place explanatory comments *above* the target code (PEP 8); actively detect
  and correct our legacy habit of below-code comments.

## Running locally

Install the package editable so your working tree shadows any installed copy
(`pip install -e ".[dev]"`), then call tools by their registered console name.

## Pre-PR checklist

Before opening a PR:

- Run every check locally from [`TESTING.md`][LOC_TSTING]. Static analysis
  (markdown, YAML, Dockerfile, shell, `ruff`, `mypy`) must exit 0, as gated by
  `CL.yml`. Runtime tests (doctests, sandbox runs, and comparisons) must also
  pass, as gated by `CI.yml`.
- Branch off `main` with a descriptive name (`add-foo`, `fix-bar-timeout`).
- New CLI script? Registered under `[project.scripts]` in `pyproject.toml` (see
  [`STYLE.md`][LOC__STYLE]).
- Names follow [`NOMENCLATURE.md`][LOC_NOMENC].
- When suggesting commits, strictly use Conventional Commits (*e.g.* `feat:`,
  `fix:`, `docs:`, `style:`) and keep the title length under 50 characters.
- Commit messages and PR body are written by you, not your agent. No AI / agent
  self-references, no `Generated with ...` footers.
- PR body is short, paragraph-style prose. State why, not what.

[LOC_NOMENC]: NOMENCLATURE.md
[LOC_CONTRI]: CONTRIBUTING.md
[LOC_TSTING]: TESTING.md
[LOC_CLWORK]: .github/workflows/CL.yml
[LOC_CIWORK]: .github/workflows/CI.yml
[LOC__STYLE]: STYLE.md
[LOC_RAPID2]: src/rapid2/cli/_rapid2.py
[LOC_ZEROQI]: src/rapid2/cli/_zeroqinit.py
