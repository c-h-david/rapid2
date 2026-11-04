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
    # Process in chunks to prevent temporary math array bloat
    # -------------------------------------------------------------------------
    IS_Omg_chn = 2000000
    for JS_Omg_chn in range(0, len(ZV_Omg), IS_Omg_chn):
        JS_Omg_max = JS_Omg_chn + IS_Omg_chn
        ZV_Omg_chn = ZV_Omg[JS_Omg_chn:JS_Omg_max]
        ZV_Alp_chn = np.zeros_like(ZV_Omg_chn)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Piecewise Condition 1: 0 <= Omega <= 1
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        BV_tmp = ZV_Omg_chn <= 1.0
        ZV_tmp = ZV_Omg_chn[BV_tmp]

        if len(ZV_tmp) > 0:
            ZV_val = 1.0 - (5.0 / 3.0) * ZV_tmp ** 2
            ZV_val += (5.0 / 8.0) * ZV_tmp ** 3
            ZV_val += (1.0 / 2.0) * ZV_tmp ** 4
            ZV_val -= (1.0 / 4.0) * ZV_tmp ** 5

            ZV_Alp_chn[BV_tmp] = ZV_val

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Piecewise Condition 2: 1 < Omega <= 2
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Division by zero is inherently avoided because Omega > 1.0
        BV_tmp = (ZV_Omg_chn > 1.0) & (ZV_Omg_chn <= 2.0)
        ZV_tmp = ZV_Omg_chn[BV_tmp]

        if len(ZV_tmp) > 0:
            ZV_val = 4.0 - (2.0 / 3.0) / ZV_tmp
            ZV_val -= 5.0 * ZV_tmp
            ZV_val += (5.0 / 3.0) * ZV_tmp ** 2
            ZV_val += (5.0 / 8.0) * ZV_tmp ** 3
            ZV_val -= (1.0 / 2.0) * ZV_tmp ** 4
            ZV_val += (1.0 / 12.0) * ZV_tmp ** 5

            ZV_Alp_chn[BV_tmp] = ZV_val

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Note: Omega > 2.0 remains 0.0 from the initial zeros_like array.
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # Write the processed chunk back to the main array
        ZV_Alp[JS_Omg_chn:JS_Omg_max] = ZV_Alp_chn

    return ZV_Alp


# *****************************************************************************
# End
# *****************************************************************************
