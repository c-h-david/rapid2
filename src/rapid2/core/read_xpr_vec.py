#!/usr/bin/env python3
# *****************************************************************************
# read_xpr_vec.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import sys

import numpy as np
import numpy.typing as npt
import pyarrow.parquet as pq


# *****************************************************************************
# Muskingum x function
# *****************************************************************************
def read_xpr_vec(
    xpr_pqt: str, IV_0bi_bas: npt.NDArray[np.int32]
) -> npt.NDArray[np.float64]:
    """Read x parameter file.

    Create an array for parameters x in the basin.

    Parameters
    ----------
    xpr_pqt : str
        Path to the x parameter file.
    IV_0bi_bas : ndarray[int32]
        The index in domain for river IDs in basin.

    Returns
    -------
    ZV_xpr_bas : ndarray[float64]
        The values of x in the basin.

    Examples
    --------
    >>> xpr_pqt = "./input/Sandbox/x_Sandbox.parquet"
    >>> IV_0bi_bas = np.array([0, 1, 2, 3, 4], dtype=np.int32)
    >>> read_xpr_vec(xpr_pqt, IV_0bi_bas)  # doctest: +NORMALIZE_WHITESPACE
    array([0.25, 0.25, 0.25, 0.25, 0.25])
    """

    # -------------------------------------------------------------------------
    # Read Parquet and populate array
    # -------------------------------------------------------------------------
    try:
        table = pq.read_table(xpr_pqt, columns=["xpr"])

        ZV_xpr_tot = table.column("xpr").to_numpy().astype(np.float64)
        ZV_xpr_bas = ZV_xpr_tot[IV_0bi_bas]

    except IOError:
        print(f"ERROR - Unable to open {xpr_pqt}")
        sys.exit(1)

    return ZV_xpr_bas


# *****************************************************************************
# End
# *****************************************************************************
