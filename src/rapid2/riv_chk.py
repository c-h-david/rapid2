#!/usr/bin/env python3
# *****************************************************************************
# riv_chk.py
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
def riv_chk(
    IV_riv_tot: npt.NDArray[np.int32],
    IV_riv_tmp: npt.NDArray[np.int32],
) -> None:
    """Check river IDs.

    Check that the array of river IDs in domain and in lateral inflow volume
    file are exactly the same and in the same order.

    Parameters
    ----------
    IV_riv_tot : ndarray[int32]
        The river IDs of the domain.
    IV_riv_tmp : ndarray[int32]
        The river IDs of the domain, but from a different source.

    Returns
    -------
    None

    Examples
    --------
    >>> IV_riv_tot = np.array([10, 20, 30, 40, 50], dtype=np.int32)
    >>> IV_riv_tmp = np.array([10, 20, 30, 40, 50], dtype=np.int32)
    >>> riv_chk(IV_riv_tot, IV_riv_tmp)
    >>> IV_riv_tmp = np.array([10, 20], dtype=np.int32)
    >>> riv_chk(IV_riv_tot, IV_riv_tmp)
    Traceback (most recent call last):
    ValueError: The river ID arrays have different sizes
    >>> IV_riv_tmp = np.array([50, 40, 30, 20, 10], dtype=np.int32)
    >>> riv_chk(IV_riv_tot, IV_riv_tmp)
    Traceback (most recent call last):
    ValueError: The river ID arrays have different elements
    """

    if IV_riv_tot.size != IV_riv_tmp.size:
        raise ValueError("The river ID arrays have different sizes")

    if not np.all(IV_riv_tot - IV_riv_tmp == 0):
        raise ValueError("The river ID arrays have different elements")


# *****************************************************************************
# End
# *****************************************************************************
