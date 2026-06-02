# AGENTS.md

Field guide for AI coding agents working on rapid2. Read this first to
produce code and documentation that passes CI on the first try and
conforms to the project's naming grammar. Authoritative sources are
linked below; this file is the operational companion, not a substitute.

When this file and an authoritative source disagree, the authoritative
source wins. Open a PR to fix this file.

## Authoritative sources

- [`NOMENCLATURE.md`][NOM] — semantic naming grammar, strictly enforced
  for the core model and library.
- [`CONTRIBUTING.md`][CON] — fork / branch / test / pull request flow.
- [`.github/workflows/CL.yml`][CL] — the nine CI lint commands run on
  every PR. This file's checklist mirrors them.

## CI lint gates

CI runs nine commands in order. Any non-zero exit fails the build. Run
all nine locally before opening a PR; see the Pre-PR checklist below
for the full block.

### 1. Markdown lint

```bash
pymarkdown scan *.md
```

Config: [`.pymarkdown.yml`][PYM] — `line_length: 79`,
`code_block_line_length: 79`, `strict: true`. Code blocks are length
checked, not just prose.

Common trips:

- **Long inline URL (MD013).** Move the URL to a reference link block
  at the end of the file, and wrap the block in a pyml line-length
  disable directive. Same idiom as `CONTRIBUTING.md`:

  ```markdown
  See the [tutorial][URL_TUT] for details.

  <!-- pyml disable-num-lines 3 line-length -->
  [URL_TUT]: https://example.org/some/very/long/path/to/page/
  ```

- **Trailing whitespace, hard tabs, missing blank line around a
  fenced code block.** Retype the offending line.

### 2. YAML lint

```bash
yamllint .*.yml .github/*/*.yml
```

Config: `.yamllint.yml` — `max: 79`, `spaces: 2`,
`indent-sequences: true`.

Common trips:

- Missing `---` document start.
- Wrong indent (use 2 spaces; sequences are indented).
- Boolean-like keys (`on:`) need the inline escape
  `# yamllint disable-line rule:truthy`.

### 3. Dockerfile lint

```bash
hadolint --ignore DL3008 --ignore SC2046 Dockerfile
wc -L Dockerfile | awk '{exit $1 > 79}'
awk 'length>79 {print FILENAME ":"FNR">79"; exit 1}' Dockerfile
```

Common trips:

- Any line >79 chars. Break with `\` line continuations.
- Untagged `FROM image`. Use `FROM image:tag`.

### 4. Python lint

```bash
ruff check .
```

Config: [`pyproject.toml`][PRJ] — `select = ["E", "F", "I", "B"]`.

Common trips:

- **Import order (`I001`).** Three groups, blank line between each:
  stdlib, then third-party, then `from rapid2 import ...`.
- **Unused import (`F401`).** Remove it, or add to `__all__`.
- **Mutable default (`B006`).** Use `None` and assign inside the body.

### 5. Python format

```bash
ruff format . --check
```

Config: `pyproject.toml` — `line-length = 79`, `quote-style = "double"`,
`line-ending = "lf"`, `docstring-code-format = true`.

Common trips:

- Single quotes. Use `"double quotes"`.
- Lines over 79 chars. Run `ruff format .` (without `--check`) to
  rewrite them before committing.

### 6. Type check

```bash
mypy .
```

Config: `pyproject.toml` — `python_version = "3.11"`, `strict = true`.

Common trips:

- **Untyped function signature.** Every function needs explicit
  annotations including `-> None` for procedures.
- **Optional return.** Guard with an explicit `raise` before use.
  The canonical pattern is:

  ```python
  IM_tim_all: int | None = some_call()
  if IM_tim_all is None:
      raise RuntimeError("IM_tim_all is None")
  # safe to use IM_tim_all as int below
  ```

- Stubs already declared in `[project.optional-dependencies].dev`:
  `types-PyYAML`, `scipy-stubs`, `types-tqdm`, `pyarrow-stubs`.

### 7. Shell lint

```bash
shellcheck *.sh tst/*.sh
awk 'length>79 {print FILENAME ":"FNR">79"; exit 1}' *.sh tst/*.sh
```

Common trips:

- Unquoted variable expansion (`SC2086`). Quote with `"$VAR"`.
- Lines >79 chars. Break with `\` continuations.

## Python file template

Every CLI script under `src/rapid2/cli/` starts with this skeleton
(see `_rapid2.py` for the canonical example). Banner lines are 79
characters total; section dividers inside `main()` start with `#`,
then a space, then 77 dashes:

```python
#!/usr/bin/env python3
# ****************************************************************************
# _new_tool.py
# ****************************************************************************

# Author:
# <Your Name>, <YYYY>-<YYYY>


# ****************************************************************************
# Import Python modules
# ****************************************************************************
import argparse

import netCDF4
import numpy as np

from rapid2 import __version__


# ****************************************************************************
# Main
# ****************************************************************************
def main() -> None:
    # ------------------------------------------------------------------------
    # Initialize the argument parser
    # ------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description="One sentence summary.",
        epilog="examples:\n  new_tool --foo bar",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    # Add flags here using the 3-letter short / descriptive long
    # convention: -nml / --namelist, -phs / --phase, -skd /
    # --skip-download.

    args = parser.parse_args()
    print(args)


# ****************************************************************************
# If executed as a script
# ****************************************************************************
if __name__ == "__main__":
    main()


# ****************************************************************************
# End
# ****************************************************************************
```

Register new CLIs under `[project.scripts]` in `pyproject.toml`.

## Nomenclature quick reference

The full grammar is in `NOMENCLATURE.md`. The summary below is enough
for most additions; cross-check the file before inventing a new
triplet or quadruplet.

### Enforcement scope (verbatim from NOMENCLATURE.md)

> These guidelines are strictly enforced for the core routing model
> (`_rapid2.py`), the `rapid2` library, and all internal data
> utilities (e.g., `_cmpncf.py`, `_cpllsm.py`).
>
> The download utility (`_dgldas2.py`) is formally exempt from strict
> checking to accommodate external API terminology.

### Data structure names

Pattern: `<type><structure>_<quantity>_[<qualifier>]`.

- `<type>` = one of `I` (integer), `J` (integer loop index),
  `Z` (float), `Y` (string), `B` (boolean), `A` (any).
- `<structure>` = one of `S` (scalar), `V` (1-D vector),
  `M` (2-D matrix), `T` (table / dict).
- `<quantity>` and `<qualifier>` = triplets defined in
  `NOMENCLATURE.md` (`riv`, `tim`, `Qex`, `lat`, `tot`, ...).

Examples:

- `IV_riv_tot` — integer vector of all river IDs.
- `ZV_lat_tot` — float vector of all latitudes.
- `ZM_Net` — float matrix, network connectivity.
- `BS_vrb` — boolean scalar, e.g. a verbose CLI flag value read
  from `args.vrb`. Boolean flags extracted from `args` follow
  `BS_<short-flag-name>`.

### File names

Pattern: `<dataset>_<format>`. `<format>` is the extension triplet
(`ncf`, `csv`, `yml`, `pqt`). Examples: `Qex_ncf`, `nml_yml`.

### Function names

Pattern: `<verb>_<dataset>_<format>()` or
`<verb>_<concept>_<quantity>()`.

Verbs: `read`, `make`, `prep`, `chck`, `calc`, `updt`, `assm`.

Examples: `read_bas_vec()`, `chck_bas()`, `make_Net_mat()`.

## Pre-PR checklist

Run all nine commands locally from the repo root; every one must
exit 0:

```bash
pymarkdown scan *.md
yamllint .*.yml .github/*/*.yml
hadolint --ignore DL3008 --ignore SC2046 Dockerfile
wc -L Dockerfile | awk '{exit $1 > 79}'
awk 'length>79 {print FILENAME ":"FNR">79"; exit 1}' Dockerfile
ruff check .
ruff format . --check
mypy .
shellcheck *.sh tst/*.sh
awk 'length>79 {print FILENAME ":"FNR">79"; exit 1}' *.sh tst/*.sh
```

Then:

- Branched off `main` with a descriptive branch name
  (`add-foo`, `fix-bar-timeout`).
- New CLI script? Registered under `[project.scripts]` in
  `pyproject.toml`.
- Commit messages and PR body are written by you, not your agent.
  No AI / agent self-references, no `Generated with ...` footers.
- PR body is short, paragraph-style prose. State why, not what.

<!-- pyml disable-num-lines 6 line-length -->
[NOM]: NOMENCLATURE.md
[CON]: CONTRIBUTING.md
[CL]: .github/workflows/CL.yml
[PYM]: .pymarkdown.yml
[PRJ]: pyproject.toml
