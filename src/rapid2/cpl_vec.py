#!/usr/bin/env python3
# *****************************************************************************
# cpl_vec.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2025


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import csv
import numpy as np
import numpy.typing as npt
import sys


# *****************************************************************************
# Connectivity function
# *****************************************************************************
def cpl_vec(
            cpl_csv: str
            ) -> tuple[
                       npt.NDArray[np.int32],
                       npt.NDArray[np.float64],
                       npt.NDArray[np.int32],
                       npt.NDArray[np.int32]
                       ]:
    '''Read coupling file.

    Create arrays for river IDs, catchment area, i, and j indices.

    Parameters
    ----------
    cpl_csv : str
        Path to the coupling file.

    Returns
    -------
    IV_riv_tot : ndarray[int32]
        The river IDs of the domain.
    ZV_riv_skm : ndarray[float64]
        The areas of contributing catchments to each river ID.
    IV_riv_1bi : ndarray[float64]
        The 1-based i index corresponding to each river ID in the LSM grid.
    IV_riv_1bj : ndarray[float64]
        The 1-based j index corresponding to each river ID in the LSM grid.

    Examples
    --------
    >>> cpl_csv = './input/Sandbox/rapid_coupling_Sandbox.csv'
    >>> cpl_vec(cpl_csv) # doctest: +NORMALIZE_WHITESPACE
    (array([10, 20, 30, 40, 50], dtype=int32),\
     array([1., 1., 1., 1., 1.]),\
     array([1, 1, 1, 1, 1], dtype=int32),\
     array([2, 2, 2, 1, 1], dtype=int32))
    '''

    # -------------------------------------------------------------------------
    # Count the number of elements
    # -------------------------------------------------------------------------
    try:
        with open(cpl_csv, 'r') as csvfile:
            IS_riv_tot = sum(1 for _ in csvfile)
    except IOError:
        print(f'ERROR - Unable to open {cpl_csv}')
        sys.exit(1)

    # -------------------------------------------------------------------------
    # Allocate array sizes
    # -------------------------------------------------------------------------
    IV_riv_tot = np.empty(IS_riv_tot, dtype=np.int32)
    ZV_riv_skm = np.empty(IS_riv_tot, dtype=np.float64)
    IV_riv_1bi = np.empty(IS_riv_tot, dtype=np.int32)
    IV_riv_1bj = np.empty(IS_riv_tot, dtype=np.int32)

    # -------------------------------------------------------------------------
    # Populate arrays
    # -------------------------------------------------------------------------
    try:
        with open(cpl_csv, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for JS_riv_tot, row in enumerate(csvreader):
                IV_riv_tot[JS_riv_tot] = np.int32(row[0])
                ZV_riv_skm[JS_riv_tot] = np.float64(row[1])
                IV_riv_1bi[JS_riv_tot] = np.int32(row[2])
                IV_riv_1bj[JS_riv_tot] = np.int32(row[3])
    except IOError:
        print(f'ERROR - Unable to open {cpl_csv}')
        sys.exit(1)

    return IV_riv_tot, ZV_riv_skm, IV_riv_1bi, IV_riv_1bj


# *****************************************************************************
# End
# *****************************************************************************
