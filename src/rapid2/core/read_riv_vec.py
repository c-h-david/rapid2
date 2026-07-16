#!/usr/bin/env python3
# *****************************************************************************
# read_riv_vec.py
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
# Basin function
# *****************************************************************************
def read_riv_vec(riv_pqt: str) -> npt.NDArray[np.int32]:
    """Read river ID file.

    Create one array of river IDs based on a single-column parquet file.

    Parameters
    ----------
    riv_pqt : str
        Path to the parquet file containing river IDs (e.g., bas_pqt, obs_pqt).

    Returns
    -------
    IV_riv : ndarray[int32]
        The river IDs from the file.

    Examples
    --------
    >>> riv_pqt = "./input/Sandbox/bas_Sandbox_ascend.parquet"
    >>> read_riv_vec(riv_pqt)
    array([10, 20, 30, 40, 50], dtype=int32)
    """

    # -------------------------------------------------------------------------
    # Read Parquet and populate array
    # -------------------------------------------------------------------------
    try:
        table = pq.read_table(riv_pqt, columns=["riv"])

        IV_riv = table.column("riv").to_numpy().astype(np.int32)

    except IOError:
        raise IOError(f"Unable to open {riv_pqt}")

    return IV_riv


# *****************************************************************************
# End
# *****************************************************************************
