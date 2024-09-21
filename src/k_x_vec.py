#!/usr/bin/env python3
# *****************************************************************************
# k_x_vec.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import csv
import numpy as np
import numpy.typing as npt


# *****************************************************************************
# Muskingum k and x function
# *****************************************************************************
def k_x_vec(
            kpr_csv: str,
            xpr_csv: str,
            IV_bas_tot: npt.NDArray[np.int32]
            ) -> tuple[
                       npt.NDArray[np.float64],
                       npt.NDArray[np.float64]
                       ]:
    '''Read k and x parameter files.

    Create two arrays for parameters k and x in the basin.

    Parameters
    ----------
    kpr_csv : str
        Path to the k parameter file.
    xpr_csv : str
        Path to the x parameter file.
    IV_bas_tot : ndarray[int32]
        The index in domain for river IDs in basin.

    Returns
    -------
    ZV_kpr_bas : ndarray[float64]
        The values of k in the basin.
    ZV_xpr_bas : ndarray[float64]
        The values of x in the basin.

    Examples
    --------
    >>> kpr_csv = '../input/Test/k_Test.csv'
    >>> xpr_csv = '../input/Test/x_Test.csv'
    >>> IV_bas_tot = np.array([0, 1, 2, 3, 4], dtype=np.int32)
    >>> k_x_vec(kpr_csv, xpr_csv, IV_bas_tot) # doctest: +NORMALIZE_WHITESPACE
    (array([12600., 12600., 12600., 12600., 12600.]),\
     array([0.3, 0.3, 0.3, 0.3, 0.3]))
    '''

    ZV_kpr_tot = np.empty(0, dtype=np.float64)
    with open(kpr_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            ZV_kpr_tot = np.append(ZV_kpr_tot, np.float64(row[0]))
    ZV_kpr_bas = ZV_kpr_tot[IV_bas_tot]

    ZV_xpr_tot = np.empty(0, dtype=np.float64)
    with open(xpr_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            ZV_xpr_tot = np.append(ZV_xpr_tot, np.float64(row[0]))
    ZV_xpr_bas = ZV_xpr_tot[IV_bas_tot]

    return ZV_kpr_bas, ZV_xpr_bas


# *****************************************************************************
# End
# *****************************************************************************
