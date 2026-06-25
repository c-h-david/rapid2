# CLI formatting standard

Every command-line tool in rapid2 lives under `src/rapid2/cli/` in a
file named `_<tool>.py` and follows the structure below. Mirror
[`_rapid2.py`][R2] exactly: it is the canonical example and this file
only describes the rules it embodies. If the two ever disagree,
`_rapid2.py` wins.

## File skeleton

```python
#!/usr/bin/env python3
# *****************************************************************************
# _new_tool.py
# *****************************************************************************

# Author:
# <Your Name>, <YYYY>-<YYYY>


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse

import netCDF4
import numpy as np

from rapid2 import __version__


# *****************************************************************************
# Main
# *****************************************************************************
def main() -> None:
    # -------------------------------------------------------------------------
    # Initialize the argument parser
    # -------------------------------------------------------------------------
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


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == "__main__":
    main()


# *****************************************************************************
# End
# *****************************************************************************
```

## Structure rules

- Banner comment lines and the in-`main()` section dividers span a
  total width of 79 characters, exactly as in `_rapid2.py`.
- Imports form three blocks with one blank line between each: standard
  library, then third-party, then `from rapid2 import ...`.
- All work happens inside `def main() -> None:`. The module ends with
  the `if __name__ == "__main__":` guard and a closing `End` banner.
- Argument flags use the 3-letter short / descriptive long convention
  (`-nml` / `--namelist`, `-phs` / `--phase`). Booleans read off
  `args` are named `BS_<short-flag-name>` per [`NOMENCLATURE.md`][NOM].

## Registering the CLI

Add an entry under `[project.scripts]` in [`pyproject.toml`][PRJ] so the
tool installs as a console command:

```toml
[project.scripts]
new_tool = "rapid2.cli._new_tool:main"
```

[R2]: src/rapid2/cli/_rapid2.py
[NOM]: NOMENCLATURE.md
[PRJ]: pyproject.toml
