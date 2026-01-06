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
    bas_csv : str
        Path to the basin file.

    Returns
    -------
    IV_riv_bas : ndarray[int32]
        The river IDs of the basin.

    Examples
    --------
    >>> bas_csv = './input/Sandbox/riv_bas_id_Sandbox.csv'
    >>> bas_vec(bas_csv)
    array([10, 20, 30, 40, 50], dtype=int32)
    '''

    IV_riv_bas = np.empty(0, dtype=np.int32)
    try:
        with open(bas_csv, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                IV_riv_bas = np.append(IV_riv_bas, np.int32(row[0]))
    except IOError:
        print('ERROR - Unable to open '+bas_csv)
        sys.exit(1)

    return IV_riv_bas


# *****************************************************************************
# End
# *****************************************************************************
