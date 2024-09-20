#!/usr/bin/env python3
# *****************************************************************************
# con_vec.py
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
# Connectivity function
# *****************************************************************************
def con_vec(
            con_csv: str
            ) -> tuple[
                       npt.NDArray[np.int32],
                       npt.NDArray[np.int32]
                       ]:
    '''Read connectivity file.

    Create two arrays of river IDs based on connectivity file.

    Parameters
    ----------
    arg1 : str
        Path to the connectivity file.

    Returns
    -------
    ndarray[int32]
        The river IDs of the domain.
    ndarray[int32]
        The river IDs downstream.

    Examples
    --------
    >>> con_csv = '../input/Test/rapid_connect_Test.csv'
    >>> con_vec(con_csv) # doctest: +NORMALIZE_WHITESPACE
    (array([10, 20, 30, 40, 50], dtype=int32),\
     array([30, 30, 50, 50,  0], dtype=int32))

    '''

    IV_riv_tot = np.empty(0, dtype=np.int32)
    IV_dwn_tot = np.empty(0, dtype=np.int32)
    with open(con_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            IV_riv_tot = np.append(IV_riv_tot, np.int32(row[0]))
            IV_dwn_tot = np.append(IV_dwn_tot, np.int32(row[1]))

    return IV_riv_tot, IV_dwn_tot


# *****************************************************************************
# End
# *****************************************************************************
