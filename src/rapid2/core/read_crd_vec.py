#!/usr/bin/env python3
# *****************************************************************************
# read_crd_vec.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2025


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import sys

import numpy as np
import numpy.typing as npt
import pyarrow.parquet as pq


# *****************************************************************************
# Connectivity function
# *****************************************************************************
def read_crd_vec(
    crd_pqt: str,
) -> tuple[
    npt.NDArray[np.int32], npt.NDArray[np.float64], npt.NDArray[np.float64]
]:
    """Read coordinates file.

    Create arrays for river IDs, longitude, and latitude from coordinate file.

    Parameters
    ----------
    crd_pqt : str
        Path to the coordinate file.

    Returns
    -------
    IV_riv_tot : ndarray[int32]
        The river IDs of the domain.
    ZV_lon_tot : ndarray[float64]
        The longitudes of individual points related to each river ID.
    ZV_lat_tot : ndarray[float64]
        The latitudes of individual points related to each river ID.

    Examples
    --------
    >>> crd_pqt = './input/Sandbox/crd_Sandbox.parquet'
    >>> read_crd_vec(crd_pqt) # doctest: +NORMALIZE_WHITESPACE
    (array([10, 20, 30, 40, 50], dtype=int32),\
     array([4.3 , 5.94, 5.12, 6.55, 4.3 ]),\
     array([8.2 , 8.2 , 5.12, 4.3 , 2.04]))
    """

    # -------------------------------------------------------------------------
    # Read Parquet and populate arrays
    # -------------------------------------------------------------------------
    try:
        table = pq.read_table(crd_pqt, columns=["riv", "lon", "lat"])

        IV_riv_tot = table.column("riv").to_numpy().astype(np.int32)
        ZV_lon_tot = table.column("lon").to_numpy().astype(np.float64)
        ZV_lat_tot = table.column("lat").to_numpy().astype(np.float64)

    except IOError:
        print(f"ERROR - Unable to open {crd_pqt}")
        sys.exit(1)

    return IV_riv_tot, ZV_lon_tot, ZV_lat_tot


# *****************************************************************************
# End
# *****************************************************************************
