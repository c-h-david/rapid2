#!/usr/bin/env python3
# *****************************************************************************
# crd_vec.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2025


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import csv
import sys

import numpy as np
import numpy.typing as npt


# *****************************************************************************
# Connectivity function
# *****************************************************************************
def crd_vec(
            crd_csv: str
            ) -> tuple[
                       npt.NDArray[np.int32],
                       npt.NDArray[np.float64],
                       npt.NDArray[np.float64]
                       ]:
    '''Read coordinates file.

    Create arrays for river IDs, longitude, and latitude from coordinate file.

    Parameters
    ----------
    crd_csv : str
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
    >>> crd_csv = './input/Sandbox/coords_Sandbox.csv'
    >>> crd_vec(crd_csv) # doctest: +NORMALIZE_WHITESPACE
    (array([10, 20, 30, 40, 50], dtype=int32),\
     array([4.3 , 5.94, 5.12, 6.55, 4.3 ]),\
     array([8.2 , 8.2 , 5.12, 4.3 , 2.04]))
    '''

    # -------------------------------------------------------------------------
    # Count the number of elements
    # -------------------------------------------------------------------------
    try:
        with open(crd_csv, 'r') as csvfile:
            IS_riv_tot = sum(1 for _ in csvfile)
    except IOError:
        print(f'ERROR - Unable to open {crd_csv}')
        sys.exit(1)

    # -------------------------------------------------------------------------
    # Allocate array sizes
    # -------------------------------------------------------------------------
    IV_riv_tot = np.empty(IS_riv_tot, dtype=np.int32)
    ZV_lon_tot = np.empty(IS_riv_tot, dtype=np.float64)
    ZV_lat_tot = np.empty(IS_riv_tot, dtype=np.float64)

    # -------------------------------------------------------------------------
    # Populate arrays
    # -------------------------------------------------------------------------
    try:
        with open(crd_csv, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for JS_riv_tot, row in enumerate(csvreader):
                IV_riv_tot[JS_riv_tot] = np.int32(row[0])
                ZV_lon_tot[JS_riv_tot] = np.float64(row[1])
                ZV_lat_tot[JS_riv_tot] = np.float64(row[2])
    except IOError:
        print(f'ERROR - Unable to open {crd_csv}')
        sys.exit(1)

    return IV_riv_tot, ZV_lon_tot, ZV_lat_tot


# *****************************************************************************
# End
# *****************************************************************************
