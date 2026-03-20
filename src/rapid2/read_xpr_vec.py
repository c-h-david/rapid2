#!/usr/bin/env python3
# *****************************************************************************
# read_xpr_vec.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import csv
import sys

import numpy as np
import numpy.typing as npt


# *****************************************************************************
# Muskingum x function
# *****************************************************************************
def read_xpr_vec(
    xpr_csv: str, IV_idx_bas: npt.NDArray[np.int32]
) -> npt.NDArray[np.float64]:
    """Read x parameter file.

    Create an array for parameters x in the basin.

    Parameters
    ----------
    xpr_csv : str
        Path to the x parameter file.
    IV_idx_bas : ndarray[int32]
        The index in domain for river IDs in basin.

    Returns
    -------
    ZV_xpr_bas : ndarray[float64]
        The values of x in the basin.

    Examples
    --------
    >>> xpr_csv = "./input/Sandbox/x_Sandbox.csv"
    >>> IV_idx_bas = np.array([0, 1, 2, 3, 4], dtype=np.int32)
    >>> read_xpr_vec(xpr_csv, IV_idx_bas)  # doctest: +NORMALIZE_WHITESPACE
    array([0.25, 0.25, 0.25, 0.25, 0.25])
    """

    # -------------------------------------------------------------------------
    # Count the number of elements
    # -------------------------------------------------------------------------
    try:
        with open(xpr_csv, "r") as csvfile:
            IS_riv_tot = sum(1 for _ in csvfile)
    except IOError:
        print(f"ERROR - Unable to open {xpr_csv}")
        sys.exit(1)

    # -------------------------------------------------------------------------
    # Allocate array sizes
    # -------------------------------------------------------------------------
    ZV_xpr_tot = np.empty(IS_riv_tot, dtype=np.float64)

    # -------------------------------------------------------------------------
    # Populate arrays
    # -------------------------------------------------------------------------
    try:
        with open(xpr_csv, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            for JS_riv_tot, row in enumerate(csvreader):
                ZV_xpr_tot[JS_riv_tot] = np.float64(row[0])
    except IOError:
        print(f"ERROR - Unable to open {xpr_csv}")
        sys.exit(1)
    ZV_xpr_bas = ZV_xpr_tot[IV_idx_bas]

    return ZV_xpr_bas


# *****************************************************************************
# End
# *****************************************************************************
