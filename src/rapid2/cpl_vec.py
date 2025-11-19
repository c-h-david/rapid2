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
    ZV_riv_km2 : ndarray[float64]
        The areas of contributing catchments to each river ID.
    IV_riv_iii : ndarray[float64]
        The i index corresponding to each river ID in the LSM grid.
    IV_riv_jjj : ndarray[float64]
        The j index corresponding to each river ID in the LSM grid.

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
    ZV_riv_km2 = np.empty(0, dtype=np.float64)
    IV_riv_iii = np.empty(0, dtype=np.int32)
    IV_riv_jjj = np.empty(0, dtype=np.int32)
    try:
        with open(cpl_csv, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                IV_riv_tot = np.append(IV_riv_tot, np.int32(row[0]))
                ZV_riv_km2 = np.append(ZV_riv_km2, np.float64(row[1]))
                IV_riv_iii = np.append(IV_riv_iii, np.int32(row[2]))
                IV_riv_jjj = np.append(IV_riv_jjj, np.int32(row[3]))
    except IOError:
        print('ERROR - Unable to open '+cpl_csv)
        raise SystemExit(22)

    return IV_riv_tot, ZV_riv_km2, IV_riv_iii, IV_riv_jjj


# *****************************************************************************
# End
# *****************************************************************************
