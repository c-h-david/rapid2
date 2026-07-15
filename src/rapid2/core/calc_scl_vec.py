#!/usr/bin/env python3
# *****************************************************************************
# calc_scl_vec.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
import numpy.typing as npt
from scipy.sparse import (
    csc_matrix,
    identity,
)
from scipy.sparse.linalg import spsolve


# *****************************************************************************
# Long-Term Inverse Routing (LTIR) Scaling Factor
# *****************************************************************************
def calc_scl_vec(
    ZM_Net: csc_matrix,
    ZM_Sel: csc_matrix,
    ZV_Qex_avg: npt.NDArray[np.float64],
    ZV_Qob_avg: npt.NDArray[np.float64],
) -> npt.NDArray[np.float64]:
    """Calculate the multiplicative scaling factors for Inverse Routing.

    Using the Long-Term Inverse Routing (LTIR) methodology, compute the static
    scaling vector for external inflows based on the long-term temporal
    averages of simulated external inflows and observed gauge discharges.

    Parameters
    ----------
    ZM_Net : scipy.sparse.spmatrix
        The network matrix for the basin.
    ZM_Sel : scipy.sparse.spmatrix
        The selection matrix mapping active observations to river reaches.
    ZV_Qex_avg : ndarray[float64]
        The temporal average of the external inflow for the basin.
    ZV_Qob_avg : ndarray[float64]
        The temporal average of the observed discharge for the active gauges.

    Returns
    -------
    ZV_scl_bas : ndarray[float64]
        The computed multiplicative scaling factor for each reach in the basin.

    Examples
    --------
    >>> ZM_Net = csc_matrix(np.array([[0, 0, 0, 0, 0],\
                                      [0, 0, 0, 0, 0],\
                                      [1, 1, 0, 0, 0],\
                                      [0, 0, 0, 0, 0],\
                                      [0, 0, 1, 1, 0]], dtype=np.float64))
    >>> ZM_Sel = csc_matrix(np.array([[0, 0, 1, 0, 0],\
                                      [0, 0, 0, 0, 1]], dtype=np.float64))
    >>> ZV_Qex_avg = np.array([15.0, 15.0, 15.0, 5.0, 5.0])
    >>> ZV_Qob_avg = np.array([30.0, 70.0])
    >>> calc_scl_vec(ZM_Net, ZM_Sel, ZV_Qex_avg, \
                     ZV_Qob_avg) # doctest: +NORMALIZE_WHITESPACE
    array([0.66666667, 0.66666667, 0.66666667, 4.        , 4.        ])
    """

    # -------------------------------------------------------------------------
    # Start with some initial variables
    # -------------------------------------------------------------------------
    IS_riv_bas = ZM_Net.shape[0]
    ZM_Idt = identity(IS_riv_bas, format="csc", dtype=np.float64)

    # -------------------------------------------------------------------------
    # 1. Independent Subbasin Inflows
    # -------------------------------------------------------------------------
    ZM_ImN = ZM_Idt - ZM_Net

    # Implicitly build (I - N)^-1 * S^T (converted to CSC) and solve for q^e
    ZV_lqe_avg = spsolve(
        ZM_Sel @ spsolve(ZM_ImN, ZM_Sel.T.tocsc()), ZV_Qob_avg
    )

    # -------------------------------------------------------------------------
    # 2. Disconnected Network and Routing
    # -------------------------------------------------------------------------
    ZM_Dis = ZM_Net - ZM_Net @ ZM_Sel.T @ ZM_Sel
    ZM_ImD = ZM_Idt - ZM_Dis

    ZV_Qdi_avg = spsolve(ZM_ImD, ZV_Qex_avg)

    # -------------------------------------------------------------------------
    # 3. Compute Scaling Factors
    # -------------------------------------------------------------------------
    ZV_Qdi_act = ZM_Sel @ ZV_Qdi_avg

    # Calculate active scalars (little-lambda): safely handling zero division
    ZV_scl_act = np.divide(
        ZV_lqe_avg,
        ZV_Qdi_act,
        out=np.ones_like(ZV_lqe_avg),
        where=(ZV_Qdi_act != 0),
    )

    # Distribute subbasin scalars to individual reaches (big-Lambda)
    ZV_scl_bas = np.ones(IS_riv_bas, dtype=np.float64)
    ZV_scl_bas[:] = spsolve(ZM_ImD.T, ZM_Sel.T @ (ZV_scl_act - 1.0)) + 1.0

    return ZV_scl_bas


# *****************************************************************************
# End
# *****************************************************************************
