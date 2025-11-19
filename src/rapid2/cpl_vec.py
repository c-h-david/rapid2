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
     array([0, 0, 0, 0, 0], dtype=int32),\
     array([1, 1, 1, 0, 0], dtype=int32))
    '''

    IV_riv_tot = np.empty(0, dtype=np.int32)
    ZV_riv_skm = np.empty(0, dtype=np.float64)
    IV_riv_1bi = np.empty(0, dtype=np.int32)
    IV_riv_1bj = np.empty(0, dtype=np.int32)
    try:
        with open(cpl_csv, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                IV_riv_tot = np.append(IV_riv_tot, np.int32(row[0]))
                ZV_riv_skm = np.append(ZV_riv_skm, np.float64(row[1]))
                IV_riv_1bi = np.append(IV_riv_1bi, np.int32(row[2]))
                IV_riv_1bj = np.append(IV_riv_1bj, np.int32(row[3]))
    except IOError:
        print('ERROR - Unable to open '+cpl_csv)
        raise SystemExit(22)

    return IV_riv_tot, ZV_riv_skm, IV_riv_1bi, IV_riv_1bj


# *****************************************************************************
# End
# *****************************************************************************
