#!/usr/bin/env python3
# *****************************************************************************
# read_kpr_vec.py
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
# Muskingum k function
# *****************************************************************************
def read_kpr_vec(
    kpr_csv: str, IV_idx_bas: npt.NDArray[np.int32]
) -> npt.NDArray[np.float64]:
    """Read k parameter file.

    Create an array for parameters k in the basin.

    Parameters
    ----------
    kpr_csv : str
        Path to the k parameter file.
    IV_idx_bas : ndarray[int32]
        The index in domain for river IDs in basin.

    Returns
    -------
    ZV_kpr_bas : ndarray[float64]
        The values of k in the basin.

    Examples
    --------
    >>> kpr_csv = './input/Sandbox/k_Sandbox.csv'
    >>> IV_idx_bas = np.array([0, 1, 2, 3, 4], dtype=np.int32)
    >>> read_kpr_vec(kpr_csv, IV_idx_bas) # doctest: +NORMALIZE_WHITESPACE
    array([9000., 9000., 9000., 9000., 9000.])
    """

    # -------------------------------------------------------------------------
    # Count the number of elements
    # -------------------------------------------------------------------------
    try:
        with open(kpr_csv, "r") as csvfile:
            IS_riv_tot = sum(1 for _ in csvfile)
    except IOError:
        print(f"ERROR - Unable to open {kpr_csv}")
        sys.exit(1)

    # -------------------------------------------------------------------------
    # Allocate array sizes
    # -------------------------------------------------------------------------
    ZV_kpr_tot = np.empty(IS_riv_tot, dtype=np.float64)

    # -------------------------------------------------------------------------
    # Populate arrays
    # -------------------------------------------------------------------------
    try:
        with open(kpr_csv, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            for JS_riv_tot, row in enumerate(csvreader):
                ZV_kpr_tot[JS_riv_tot] = np.float64(row[0])
    except IOError:
        print(f"ERROR - Unable to open {kpr_csv}")
        sys.exit(1)
    ZV_kpr_bas = ZV_kpr_tot[IV_idx_bas]

    return ZV_kpr_bas


# *****************************************************************************
# End
# *****************************************************************************
