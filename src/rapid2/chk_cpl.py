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
def chk_cpl(
    ZV_riv_skm: npt.NDArray[np.float64],
    IV_riv_1bi: npt.NDArray[np.int32],
    IV_riv_1bj: npt.NDArray[np.int32],
) -> None:
    """Check coupling values.

    Check that the coupling arrays are consistent.

    Parameters
    ----------
    ZV_riv_skm : ndarray[float64]
        The areas of contributing catchments to each river ID.
    IV_riv_1bi : ndarray[float64]
        The 1-based i index corresponding to each river ID in the LSM grid.
    IV_riv_1bj : ndarray[float64]
        The 1-based j index corresponding to each river ID in the LSM grid.

    Returns
    -------
    None

    Examples
    --------
    >>> ZV_riv_skm = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
    >>> IV_riv_1bi = np.array([1, 1, 1, 1, 1], dtype=np.int32)
    >>> IV_riv_1bj = np.array([2, 2, 2, 1, 1], dtype=np.int32)
    >>> chk_cpl(ZV_riv_skm, IV_riv_1bi, IV_riv_1bj)
    >>> IV_riv_1bj = np.array([2, 2, 2, 1, 0], dtype=np.int32)
    >>> chk_cpl(ZV_riv_skm, IV_riv_1bi, IV_riv_1bj)
    Traceback (most recent call last):
    ValueError: The locations where i and j both equal zero differ
    >>> IV_riv_1bi = np.array([1, 1, 1, 1, 0], dtype=np.int32)
    >>> chk_cpl(ZV_riv_skm, IV_riv_1bi, IV_riv_1bj)
    Traceback (most recent call last):
    ValueError: Non-null area found for null i index
    >>> ZV_riv_skm = np.array([1.0, 1.0, 1.0, 1.0, 0.0])
    >>> chk_cpl(ZV_riv_skm, IV_riv_1bi, IV_riv_1bj)
    """

    if ZV_riv_skm.size != IV_riv_1bi.size:
        raise ValueError("The arrays have different sizes")

    if ZV_riv_skm.size != IV_riv_1bj.size:
        raise ValueError("The arrays have different sizes")

    IV_1bi_000 = (IV_riv_1bi == 0).astype(np.int32)
    IV_1bj_000 = (IV_riv_1bj == 0).astype(np.int32)
    # These two lists contain 1 where the 1-based index is null, 0 otherwise

    if not np.array_equal(IV_1bi_000, IV_1bj_000):
        raise ValueError("The locations where i and j both equal zero differ")
    # Check that zero positions match

    if np.any((IV_riv_1bi == 0) & (ZV_riv_skm != 0.0)):
        raise ValueError("Non-null area found for null i index")
    # Check that every null i index also has null area

    if np.any((IV_riv_1bj == 0) & (ZV_riv_skm != 0.0)):
        raise ValueError("Non-null area found for null j index")
    # Check that every null i index also has null area


# *****************************************************************************
# End
# *****************************************************************************
