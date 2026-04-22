#!/usr/bin/env python3
# *****************************************************************************
# read_cpl_vec.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2025


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
def read_cpl_vec(
    cpl_csv: str,
) -> tuple[
    npt.NDArray[np.int32],
    npt.NDArray[np.float64],
    npt.NDArray[np.int32],
    npt.NDArray[np.int32],
]:
    """Read coupling file.

    Create arrays for river IDs, catchment area, i, and j indices.

    Parameters
    ----------
    cpl_csv : str
        Path to the coupling file.

    Returns
    -------
    IV_riv_tot : ndarray[int32]
        The river IDs of the domain.
    ZV_skm_tot : ndarray[float64]
        The areas of contributing catchments to each river ID.
    IV_1bi_tot : ndarray[int32]
        The 1-based i index corresponding to each river ID in the LSM grid.
    IV_1bj_tot : ndarray[int32]
        The 1-based j index corresponding to each river ID in the LSM grid.

    Examples
    --------
    >>> cpl_csv = './input/Sandbox/rapid_coupling_Sandbox.csv'
    >>> read_cpl_vec(cpl_csv) # doctest: +NORMALIZE_WHITESPACE
    (array([10, 20, 30, 40, 50], dtype=int32),\
     array([1., 1., 1., 1., 1.]),\
     array([1, 1, 1, 1, 1], dtype=int32),\
     array([2, 2, 2, 1, 1], dtype=int32))
    """

    # -------------------------------------------------------------------------
    # Read CSV and populate arrays
    # -------------------------------------------------------------------------
    try:
        read_options = pv.ReadOptions(
            column_names=["riv", "skm", "1bi", "1bj"]
        )
        table = pv.read_csv(cpl_csv, read_options=read_options)

        IV_riv_tot = table.column("riv").to_numpy().astype(np.int32)
        ZV_skm_tot = table.column("skm").to_numpy().astype(np.float64)
        IV_1bi_tot = table.column("1bi").to_numpy().astype(np.int32)
        IV_1bj_tot = table.column("1bj").to_numpy().astype(np.int32)

    except IOError:
        print(f"ERROR - Unable to open {cpl_csv}")
        sys.exit(1)

    return IV_riv_tot, ZV_skm_tot, IV_1bi_tot, IV_1bj_tot


# *****************************************************************************
# End
# *****************************************************************************
