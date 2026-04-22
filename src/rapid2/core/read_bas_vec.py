#!/usr/bin/env python3
# *****************************************************************************
# read_bas_vec.py
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
# Basin function
# *****************************************************************************
def read_bas_vec(bas_csv: str) -> npt.NDArray[np.int32]:
    """Read basin file.

    Create one array of river IDs based on basin file.

    Parameters
    ----------
    bas_csv : str
        Path to the basin file.

    Returns
    -------
    IV_riv_bas : ndarray[int32]
        The river IDs of the basin.

    Examples
    --------
    >>> bas_csv = "./input/Sandbox/riv_bas_id_Sandbox.csv"
    >>> read_bas_vec(bas_csv)
    array([10, 20, 30, 40, 50], dtype=int32)
    """

    # -------------------------------------------------------------------------
    # Read CSV and populate array
    # -------------------------------------------------------------------------
    try:
        read_options = pv.ReadOptions(column_names=["riv"])
        table = pv.read_csv(bas_csv, read_options=read_options)

        IV_riv_bas = table.column("riv").to_numpy().astype(np.int32)

    except IOError:
        print(f"ERROR - Unable to open {bas_csv}")
        sys.exit(1)

    return IV_riv_bas


# *****************************************************************************
# End
# *****************************************************************************
