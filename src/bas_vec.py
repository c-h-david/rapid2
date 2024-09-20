#!/usr/bin/env python3
# *****************************************************************************
# bas_vec.py
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
# Basin function
# *****************************************************************************
def bas_vec(
            bas_csv: str
            ) -> npt.NDArray[np.int32]:
    '''Read basin file.

    Create one array of river IDs based on basin file.

    Parameters
    ----------
    arg1 : str
        Path to the basin file.

    Returns
    -------
    ndarray[int32]
        The river IDs of the basin.

    Examples
    --------
    >>> bas_vec('../input/Test/riv_bas_id_Test.csv')
    array([10, 20, 30, 40, 50], dtype=int32)

    '''

    IV_riv_bas = np.empty(0, dtype=np.int32)
    with open(bas_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            IV_riv_bas = np.append(IV_riv_bas, np.int32(row[0]))

    return IV_riv_bas


# *****************************************************************************
# End
# *****************************************************************************
