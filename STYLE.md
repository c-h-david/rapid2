# Code Formatting Standards

This document defines the structural and formatting standards for Python files
in RAPID2. It complements our
[`NOMENCLATURE.md`](NOMENCLATURE.md)
and our
[`TESTING.md`](TESTING.md).

## 1. Command-Line Interface (`cli/`)

Every command-line tool in `rapid2` lives under `src/rapid2/cli/` in a file
named `_<tool>.py` and follows the structure below. Mirror `_rapid2.py`
exactly: it is the canonical example. For a small read-input and report tool,
`_zeroqinit.py` is a lighter example to mirror.

### Structure Rules

- **Banners:** Banner comment lines and the in-`main()` section dividers
  span a total width of 79 characters.
- **Imports:** Imports form three blocks with one blank line between each:
  standard library, then third-party, then `from rapid2 import ...`.
- **Execution:** All work happens inside `def main() -> None:`. The module ends
  with the `if __name__ == "__main__":` guard and a closing `End` banner.
- **Arguments:** Argument flags use the 3-letter short / descriptive long
  convention (`-nml` / `--namelist`, `-con` / `--connectivity`). Booleans
  read off `args` are named `BS_<short-flag-name>`.
- **Registration:** Add an entry under `[project.scripts]` in
  `pyproject.toml` so the tool installs as a console command.

### CLI Skeleton

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

    args = parser.parse_args()


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == "__main__":
    main()


# *****************************************************************************
# End
# *****************************************************************************
```

## 2. Core Library (`core/`)

Every internal function lives under `src/rapid2/core/` in a file named using
the standard `verb_dataset_format` nomenclature (e.g., `read_crd_vec.py`,
`chck_bas.py`).

### Structure Rules

- **Banners:** File headers, function headers (`# ***...`), and internal logic
  steps (`# ---...`) span exactly 79 characters.
- **Typing:** Strict type hinting is enforced. Use `numpy.typing`
  (`npt.NDArray`) for all array inputs and outputs.
- **Docstrings:** Every function must have a strict NumPy-style docstring
  containing a summary, `Parameters`, `Returns`, and `Examples` section.
- **Doctests:** The `Examples` section in the docstring must contain executable
  Python code (`>>>`) that serves as an automated test for `doctest`.

### Core Skeleton

```python
#!/usr/bin/env python3
# *****************************************************************************
# new_core_func.py
# *****************************************************************************

# Author:
# <Your Name>, <YYYY>-<YYYY>


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
import numpy.typing as npt


# *****************************************************************************
# Description of the function group
# *****************************************************************************
def new_core_func(
    IV_arg: npt.NDArray[np.int32],
) -> npt.NDArray[np.float64]:
    """Short summary of the function.

    Extended description of what the function does and how it integrates 
    with the matrix-based routing or I/O.

    Parameters
    ----------
    IV_arg : ndarray[int32]
        Description of the input array.

    Returns
    -------
    ZV_out : ndarray[float64]
        Description of the output array.

    Examples
    --------
    >>> IV_arg = np.array([1, 2, 3], dtype=np.int32)
    >>> new_core_func(IV_arg)
    array([1., 2., 3.])
    """

    # -------------------------------------------------------------------------
    # Description of logical step
    # -------------------------------------------------------------------------
    ZV_out = IV_arg.astype(np.float64)

    return ZV_out


# *****************************************************************************
# End
# *****************************************************************************
```
