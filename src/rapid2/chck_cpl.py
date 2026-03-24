#!/usr/bin/env python3
# *****************************************************************************
# chck_cpl.py
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
def chck_cpl(
    ZV_skm_tot: npt.NDArray[np.float64],
    IV_1bi_tot: npt.NDArray[np.int32],
    IV_1bj_tot: npt.NDArray[np.int32],
) -> None:
    """Check coupling values.

    Check that the coupling arrays are consistent.

    Parameters
    ----------
    ZV_skm_tot : ndarray[float64]
        The areas of contributing catchments to each river ID.
    IV_1bi_tot : ndarray[int32]
        The 1-based i index corresponding to each river ID in the LSM grid.
    IV_1bj_tot : ndarray[int32]
        The 1-based j index corresponding to each river ID in the LSM grid.

    Returns
    -------
    None

    Examples
    --------
    >>> ZV_skm_tot = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
    >>> IV_1bi_tot = np.array([1, 1, 1, 1, 1], dtype=np.int32)
    >>> IV_1bj_tot = np.array([2, 2, 2, 1, 1], dtype=np.int32)
    >>> chck_cpl(ZV_skm_tot, IV_1bi_tot, IV_1bj_tot)
    >>> IV_1bj_tot = np.array([2, 2, 2, 1, 0], dtype=np.int32)
    >>> chck_cpl(ZV_skm_tot, IV_1bi_tot, IV_1bj_tot)
    Traceback (most recent call last):
    ValueError: The locations where i and j both equal zero differ
    >>> IV_1bi_tot = np.array([1, 1, 1, 1, 0], dtype=np.int32)
    >>> chck_cpl(ZV_skm_tot, IV_1bi_tot, IV_1bj_tot)
    Traceback (most recent call last):
    ValueError: Non-null area found for null i index
    >>> ZV_skm_tot = np.array([1.0, 1.0, 1.0, 1.0, 0.0])
    >>> chck_cpl(ZV_skm_tot, IV_1bi_tot, IV_1bj_tot)
    """

    if ZV_skm_tot.size != IV_1bi_tot.size:
        raise ValueError("The arrays have different sizes")

    if ZV_skm_tot.size != IV_1bj_tot.size:
        raise ValueError("The arrays have different sizes")

    BV_1bi_tmp = IV_1bi_tot == 0
    BV_1bj_tmp = IV_1bj_tot == 0
    # These lists contain True where the 1-based index is null, False otherwise

    if not np.array_equal(BV_1bi_tmp, BV_1bj_tmp):
        raise ValueError("The locations where i and j both equal zero differ")
    # Check that zero positions match

    if np.any((IV_1bi_tot == 0) & (ZV_skm_tot != 0.0)):
        raise ValueError("Non-null area found for null i index")
    # Check that every null i index also has null area

    if np.any((IV_1bj_tot == 0) & (ZV_skm_tot != 0.0)):
        raise ValueError("Non-null area found for null j index")
    # Check that every null i index also has null area


# *****************************************************************************
# End
# *****************************************************************************
