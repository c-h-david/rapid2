#!/usr/bin/env python3
# *****************************************************************************
# read_kpr_vec.py
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
# Muskingum k function
# *****************************************************************************
def read_kpr_vec(
    kpr_csv: str, IV_0bi_bas: npt.NDArray[np.int32]
) -> npt.NDArray[np.float64]:
    """Read k parameter file.

    Create an array for parameters k in the basin.

    Parameters
    ----------
    kpr_csv : str
        Path to the k parameter file.
    IV_0bi_bas : ndarray[int32]
        The index in domain for river IDs in basin.

    Returns
    -------
    ZV_kpr_bas : ndarray[float64]
        The values of k in the basin.

    Examples
    --------
    >>> kpr_csv = "./input/Sandbox/k_Sandbox.csv"
    >>> IV_0bi_bas = np.array([0, 1, 2, 3, 4], dtype=np.int32)
    >>> read_kpr_vec(kpr_csv, IV_0bi_bas)  # doctest: +NORMALIZE_WHITESPACE
    array([9000., 9000., 9000., 9000., 9000.])
    """

    # -------------------------------------------------------------------------
    # Read CSV and populate array
    # -------------------------------------------------------------------------
    try:
        read_options = pv.ReadOptions(column_names=["kpr"])
        table = pv.read_csv(kpr_csv, read_options=read_options)

        ZV_kpr_tot = table.column("kpr").to_numpy().astype(np.float64)
        ZV_kpr_bas = ZV_kpr_tot[IV_0bi_bas]

    except IOError:
        print(f"ERROR - Unable to open {kpr_csv}")
        sys.exit(1)

    return ZV_kpr_bas


# *****************************************************************************
# End
# *****************************************************************************
