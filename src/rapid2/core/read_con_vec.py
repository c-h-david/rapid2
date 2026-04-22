#!/usr/bin/env python3
# *****************************************************************************
# read_con_vec.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import sys

import numpy as np
import numpy.typing as npt
import pyarrow.csv as pv


# *****************************************************************************
# Connectivity function
# *****************************************************************************
def read_con_vec(
    con_csv: str,
) -> tuple[npt.NDArray[np.int32], npt.NDArray[np.int32]]:
    """Read connectivity file.

    Create two arrays of river IDs based on connectivity file.

    Parameters
    ----------
    con_csv : str
        Path to the connectivity file.

    Returns
    -------
    IV_riv_tot : ndarray[int32]
        The river IDs of the domain.
    IV_dwn_tot : ndarray[int32]
        The river IDs downstream of the river IDs in domain.

    Examples
    --------
    >>> con_csv = './input/Sandbox/rapid_connect_Sandbox.csv'
    >>> read_con_vec(con_csv) # doctest: +NORMALIZE_WHITESPACE
    (array([10, 20, 30, 40, 50], dtype=int32),\
     array([30, 30, 50, 50,  0], dtype=int32))
    """

    # -------------------------------------------------------------------------
    # Read CSV and populate arrays
    # -------------------------------------------------------------------------
    try:
        read_options = pv.ReadOptions(column_names=["riv", "dwn"])
        table = pv.read_csv(con_csv, read_options=read_options)

        IV_riv_tot = table.column("riv").to_numpy().astype(np.int32)
        IV_dwn_tot = table.column("dwn").to_numpy().astype(np.int32)

    except IOError:
        print(f"ERROR - Unable to open {con_csv}")
        sys.exit(1)

    return IV_riv_tot, IV_dwn_tot


# *****************************************************************************
# End
# *****************************************************************************
