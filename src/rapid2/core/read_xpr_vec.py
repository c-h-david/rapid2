#!/usr/bin/env python3
# *****************************************************************************
# read_xpr_vec.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
import numpy.typing as npt
import pyarrow.parquet as pq


# *****************************************************************************
# Muskingum x function
# *****************************************************************************
def read_xpr_vec(
    xpr_pqt: str, IV_0bi_bas: npt.NDArray[np.int32]
) -> tuple[npt.NDArray[np.int32], npt.NDArray[np.float64]]:
    """Read x parameter file.

    Create arrays for river IDs and parameters x in the basin.

    Parameters
    ----------
    xpr_pqt : str
        Path to the x parameter file.
    IV_0bi_bas : ndarray[int32]
        The index in domain for river IDs in basin.

    Returns
    -------
    IV_riv_bas : ndarray[int32]
        The river IDs of the basin from the parameter file.
    ZV_xpr_bas : ndarray[float64]
        The values of x in the basin.

    Examples
    --------
    >>> xpr_pqt = "./input/Sandbox/xpr_Sandbox.parquet"
    >>> IV_0bi_bas = np.array([0, 1, 2, 3, 4], dtype=np.int32)
    >>> read_xpr_vec(xpr_pqt, IV_0bi_bas)  # doctest: +NORMALIZE_WHITESPACE
    (array([10, 20, 30, 40, 50], dtype=int32),\
     array([0.25, 0.25, 0.25, 0.25, 0.25]))
    """

    # -------------------------------------------------------------------------
    # Read Parquet and populate array
    # -------------------------------------------------------------------------
    try:
        table = pq.read_table(xpr_pqt, columns=["riv", "xpr"])

        IV_riv_tot = table.column("riv").to_numpy().astype(np.int32)
        ZV_xpr_tot = table.column("xpr").to_numpy().astype(np.float64)

        IV_riv_bas = IV_riv_tot[IV_0bi_bas]
        ZV_xpr_bas = ZV_xpr_tot[IV_0bi_bas]

    except IOError as e:
        raise IOError(f"Unable to open {xpr_pqt}") from e

    return IV_riv_bas, ZV_xpr_bas


# *****************************************************************************
# End
# *****************************************************************************
