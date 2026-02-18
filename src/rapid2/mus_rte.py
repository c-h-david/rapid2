#!/usr/bin/env python3
# *****************************************************************************
# mus_rte.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
import numpy.typing as npt
from scipy.sparse import csc_matrix  # type: ignore[import-untyped]
from scipy.sparse.linalg import (  # type: ignore[import-untyped]
    spsolve_triangular,
)


# *****************************************************************************
# Muskingum routing
# *****************************************************************************
def mus_rte(
    ZM_Lin: csc_matrix,
    ZM_Qex: csc_matrix,
    ZM_Qou: csc_matrix,
    IS_mus: int,
    ZV_Qou_ini: npt.NDArray[np.float64],
    ZV_Qex_avg: npt.NDArray[np.float64],
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    """Perform matrix-based Muskingum routing for a given number of timesteps.

    Given the three matrices of the matrix-based Muskingum method, a number of
    timesteps, initial values of discharge, and lateral inflow; compute the
    average values of discharge and the final values of discharge after
    Muskingum timesteps.

    Parameters
    ----------
    ZM_Lin : scipy.sparse.spmatrix
        The linear system matrix for the basin in matrix-based Muskingum.
    ZM_Qex : scipy.sparse.spmatrix
        The multiplicand matrix for ZV_Qex for the basin in right-hand side.
    ZM_Qou : scipy.sparse.spmatrix
        The multiplicand matrix for ZV_Qou for the basin in right-hand side.
    IS_mus : int32
        The given number of Muskingum routing timesteps.
    ZV_Qou_ini : ndarray[float64]
        The initial value of discharge in the basin.
    ZV_Qex_avg : ndarray[float64]
        The lateral inflow in the basin.

    Returns
    -------
    ZV_Qou_avg : ndarray[float64]
        The average value of discharge in the basin after Muskingum timesteps.
    ZV_Qou_fin : ndarray[float64]
        The final value of discharge in the basin after Muskingum timesteps.

    Examples
    --------
    >>> ZM_Lin = csc_matrix(np.array([[1.  , 0.  , 0.  , 0.  , 0.  ],\
                                      [0.  , 1.  , 0.  , 0.  , 0.  ],\
                                      [0.25, 0.25, 1.  , 0.  , 0.  ],\
                                      [0.  , 0.  , 0.  , 1.  , 0.  ],\
                                      [0.  , 0.  , 0.25, 0.25, 1.  ]]))
    >>> ZM_Qex = csc_matrix(np.array([[0.125, 0.   , 0.   , 0.   , 0.   ],\
                                      [0.   , 0.125, 0.   , 0.   , 0.   ],\
                                      [0.   , 0.   , 0.125, 0.   , 0.   ],\
                                      [0.   , 0.   , 0.   , 0.125, 0.   ],\
                                      [0.   , 0.   , 0.   , 0.   , 0.125]]))
    >>> ZM_Qou = csc_matrix(np.array([[0.875, 0.   , 0.   , 0.   , 0.   ],\
                                      [0.   , 0.875, 0.   , 0.   , 0.   ],\
                                      [0.375, 0.375, 0.875, 0.   , 0.   ],\
                                      [0.   , 0.   , 0.   , 0.875, 0.   ],\
                                      [0.   , 0.   , 0.375, 0.375, 0.875]]))
    >>> IS_mus = 2
    >>> ZV_Qou_ini = np.array([0, 0, 0, 0, 0])
    >>> ZV_Qex_avg = np.array([1, 1, 1, 1, 1])
    >>> ZV_Qou_avg, ZV_Qou_fin = mus_rte(ZM_Lin, ZM_Qex, ZM_Qou, IS_mus,\
                                         ZV_Qou_ini, ZV_Qex_avg\
                                         )
    >>> ZV_Qou_avg
    array([0.0625   , 0.0625   , 0.03125  , 0.0625   , 0.0390625])
    >>> ZV_Qou_fin
    array([0.234375  , 0.234375  , 0.15625   , 0.234375  , 0.16601562])
    >>> ZV_Qou_ini = np.array([1, 1, 1, 1, 1])
    >>> ZV_Qex_avg = np.array([1, 1, 1, 1, 1])
    >>> ZV_Qou_avg, ZV_Qou_fin = mus_rte(ZM_Lin, ZM_Qex, ZM_Qou, IS_mus,\
                                         ZV_Qou_ini, ZV_Qex_avg\
                                         )
    >>> ZV_Qou_avg
    array([1.     , 1.     , 1.125  , 1.     , 1.09375])
    >>> ZV_Qou_fin
    array([1.      , 1.      , 1.46875 , 1.      , 1.390625])
    """

    ZV_Qou = ZV_Qou_ini
    ZV_avg = np.zeros(len(ZV_Qou_ini))
    ZV_rh1 = ZM_Qex @ ZV_Qex_avg

    for _ in range(IS_mus):
        # ---------------------------------------------------------------------
        # Updating average before routing to remain in [0, IS_mus - 1] range
        # ---------------------------------------------------------------------
        ZV_avg = ZV_avg + ZV_Qou

        # ---------------------------------------------------------------------
        # Updating instantaneous value of right-hand side
        # ---------------------------------------------------------------------
        ZV_rhs = ZV_rh1 + ZM_Qou @ ZV_Qou

        # ---------------------------------------------------------------------
        # Routing
        # ---------------------------------------------------------------------
        ZV_Qou = spsolve_triangular(
            ZM_Lin, ZV_rhs, lower=True, unit_diagonal=True
        )
    ZV_avg = ZV_avg / IS_mus

    ZV_Qou_avg = ZV_avg
    ZV_Qou_fin = ZV_Qou

    return ZV_Qou_avg, ZV_Qou_fin


# *****************************************************************************
# End
# *****************************************************************************
