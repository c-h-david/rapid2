#!/usr/bin/env python3
# *****************************************************************************
# read_con_vec.py
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
# Connectivity function
# *****************************************************************************
def read_con_vec(
    con_pqt: str,
) -> tuple[npt.NDArray[np.int32], npt.NDArray[np.int32]]:
    """Read connectivity file.

    Create two arrays of river IDs based on connectivity file.

    Parameters
    ----------
    con_pqt : str
        Path to the connectivity file: a Parquet file with two
        integer columns, riv (the river ID) and dwn (its downstream
        river ID, 0 for an outlet with no downstream reach).

    Returns
    -------
    IV_riv_tot : ndarray[int32]
        The river IDs of the domain.
    IV_dwn_tot : ndarray[int32]
        The river IDs downstream of the river IDs in domain.

    Examples
    --------
    >>> con_pqt = './input/Sandbox/con_Sandbox.parquet'
    >>> read_con_vec(con_pqt) # doctest: +NORMALIZE_WHITESPACE
    (array([10, 20, 30, 40, 50], dtype=int32),\
     array([30, 30, 50, 50,  0], dtype=int32))
    """

    # -------------------------------------------------------------------------
    # Read Parquet and populate arrays
    # -------------------------------------------------------------------------
    try:
        table = pq.read_table(con_pqt, columns=["riv", "dwn"])

        IV_riv_tot = table.column("riv").to_numpy().astype(np.int32)
        IV_dwn_tot = table.column("dwn").to_numpy().astype(np.int32)

    except IOError as e:
        raise IOError(f"Unable to open {con_pqt}") from e

    return IV_riv_tot, IV_dwn_tot


# *****************************************************************************
# End
# *****************************************************************************
