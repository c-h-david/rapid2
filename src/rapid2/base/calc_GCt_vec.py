#!/usr/bin/env python3
# *****************************************************************************
# calc_GCt_vec.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
import numpy.typing as npt


# *****************************************************************************
# Gaspari-Cohn tapering function
# *****************************************************************************
def calc_GCt_vec(
    ZV_Omg: npt.NDArray[np.float64],
) -> npt.NDArray[np.float64]:
    """Calculate the 5th-order Gaspari-Cohn tapering values.

    Computes the Gaspari-Cohn piecewise polynomial for an array of normalized
    distances (Omega = distance / half-width). The function evaluates to 1.0
    at distance 0, drops smoothly to 0.0 at distance 2.0, and remains 0.0
    for all distances strictly greater than 2.0.

    Parameters
    ----------
    ZV_Omg : ndarray[float64]
        The normalized distances (Omega) to be evaluated.

    Returns
    -------
    ZV_Alp : ndarray[float64]
        The Gaspari-Cohn tapering weights (Alpha), bound between 0.0 and 1.0.

    Examples
    --------
    >>> ZV_Omg = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 2.5], dtype=np.float64)
    >>> ZV_Alp = calc_GCt_vec(ZV_Omg)
    >>> np.round(ZV_Alp, 4)
    array([ 1.    ,  0.6849,  0.2083,  0.0165, -0.    ,  0.    ])
    """

    ZV_Alp = np.zeros_like(ZV_Omg)

    # -------------------------------------------------------------------------
    # Piecewise Condition 1: 0 <= Omega <= 1
    # -------------------------------------------------------------------------
    BV_tmp = ZV_Omg <= 1.0
    ZV_Alp[BV_tmp] = (
        1.0
        - (1.0 / 4.0) * ZV_Omg[BV_tmp] ** 5
        + (1.0 / 2.0) * ZV_Omg[BV_tmp] ** 4
        + (5.0 / 8.0) * ZV_Omg[BV_tmp] ** 3
        - (5.0 / 3.0) * ZV_Omg[BV_tmp] ** 2
    )

    # -------------------------------------------------------------------------
    # Piecewise Condition 2: 1 < Omega <= 2
    # -------------------------------------------------------------------------
    # Division by zero is inherently avoided because Omega > 1.0
    BV_tmp = (ZV_Omg > 1.0) & (ZV_Omg <= 2.0)
    ZV_Alp[BV_tmp] = (
        (1.0 / 12.0) * ZV_Omg[BV_tmp] ** 5
        - (1.0 / 2.0) * ZV_Omg[BV_tmp] ** 4
        + (5.0 / 8.0) * ZV_Omg[BV_tmp] ** 3
        + (5.0 / 3.0) * ZV_Omg[BV_tmp] ** 2
        - 5.0 * ZV_Omg[BV_tmp]
        + 4.0
        - (2.0 / 3.0) / ZV_Omg[BV_tmp]
    )

    # -------------------------------------------------------------------------
    # Note: Omega > 2.0 remains 0.0 from the initial zeros_like array.
    # -------------------------------------------------------------------------

    return ZV_Alp


# *****************************************************************************
# End
# *****************************************************************************
