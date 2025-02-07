#!/usr/bin/env python3
# *****************************************************************************
# chk_ids.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
import numpy.typing as npt


# *****************************************************************************
# Check IDs
# *****************************************************************************
def chk_ids(
            IV_riv_tot: npt.NDArray[np.int32],
            IV_m3r_tot: npt.NDArray[np.int32]
            ) -> None:
    '''Check river IDs.

    Check that the array of river IDs in domain and in lateral inflow volume
    file are exactly the same and in the same order.

    Parameters
    ----------
    IV_riv_tot : ndarray[int32]
        The river IDs of the domain.
    IV_m3r_tot : ndarray[int32]
        The river IDs of the lateral inflow volume file.

    Returns
    -------
    None

    Examples
    --------
    >>> IV_riv_tot = np.array([10, 20, 30, 40, 50], dtype=np.int32)
    >>> IV_m3r_tot = np.array([10, 20, 30, 40, 50], dtype=np.int32)
    >>> chk_ids(IV_riv_tot, IV_m3r_tot)
    >>> IV_m3r_tot = np.array([10, 20], dtype=np.int32)
    >>> chk_ids(IV_riv_tot, IV_m3r_tot)
    Traceback (most recent call last):
    ValueError: The arrays have different sizes
    >>> IV_m3r_tot = np.array([50, 40, 30, 20, 10], dtype=np.int32)
    >>> chk_ids(IV_riv_tot, IV_m3r_tot)
    Traceback (most recent call last):
    ValueError: The river IDs in con_csv and m3r_ncf differ
    '''

    if IV_riv_tot.size != IV_m3r_tot.size:
        raise ValueError('The arrays have different sizes')

    if not np.all(IV_riv_tot - IV_m3r_tot == 0):
        raise ValueError('The river IDs in con_csv and m3r_ncf differ')


# *****************************************************************************
# End
# *****************************************************************************
