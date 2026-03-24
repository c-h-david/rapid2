#!/usr/bin/env python3
# *****************************************************************************
# make_Wdw_mat.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2025


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
from scipy.sparse import (  # type: ignore[import-untyped]
    csc_matrix,
    identity,
)
from scipy.sparse.linalg import (  # type: ignore[import-untyped]
    spsolve,
)


# *****************************************************************************
# Matrices for average over a window
# *****************************************************************************
def make_Wdw_mat(
    ZM_ICN: csc_matrix,
    ZM_Qex: csc_matrix,
    ZM_Qou: csc_matrix,
    IS_wdw: np.int32,
) -> tuple[
    csc_matrix,
    csc_matrix,
]:
    """Create routing matrices for average discharge over a given window.

    Create two matrices such that Qbar = ZM_Aex @ Qebar + ZM_A00 @ Q0 for
    assimilation over a given window of time steps.

    Parameters
    ----------
    ZM_ICN : scipy.sparse.spmatrix
        The linear system matrix for the basin in matrix-based Muskingum.
    ZM_Qex : scipy.sparse.spmatrix
        The multiplicand matrix for ZV_Qex for the basin in right-hand side.
    ZM_Qou : scipy.sparse.spmatrix
        The multiplicand matrix for ZV_Qou for the basin in right-hand side.
    IS_wdw : np.int32
        The number of consecutive time steps in the assimilation window.

    Returns
    -------
    ZM_Aex : scipy.sparse.spmatrix
        The input to state matrix.
    ZM_A00 : scipy.sparse.spmatrix
        The initial condition to state matrix.

    Examples
    --------
    >>> ZM_ICN = csc_matrix(np.array([[1.  , 0.  , 0.  , 0.  , 0.  ],\
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
    >>> IS_wdw = 2
    >>> ZM_Aex, ZM_A00 = make_Wdw_mat(ZM_ICN, ZM_Qex, ZM_Qou, IS_wdw)
    >>> ZM_Aex.toarray()
    array([[ 0.0625    ,  0.        ,  0.        ,  0.        ,  0.        ],
           [ 0.        ,  0.0625    ,  0.        ,  0.        ,  0.        ],
           [-0.015625  , -0.015625  ,  0.0625    ,  0.        ,  0.        ],
           [ 0.        ,  0.        ,  0.        ,  0.0625    ,  0.        ],
           [ 0.00390625,  0.00390625, -0.015625  , -0.015625  ,  0.0625    ]])
    >>> ZM_A00.toarray()
    array([[ 0.9375    ,  0.        ,  0.        ,  0.        ,  0.        ],
           [ 0.        ,  0.9375    ,  0.        ,  0.        ,  0.        ],
           [ 0.078125  ,  0.078125  ,  0.9375    ,  0.        ,  0.        ],
           [ 0.        ,  0.        ,  0.        ,  0.9375    ,  0.        ],
           [-0.01953125, -0.01953125,  0.078125  ,  0.078125  ,  0.9375    ]])
    >>> ZV_Qou_ini = np.array([0, 0, 0, 0, 0])
    >>> ZV_Qex_avg = np.array([1, 1, 1, 1, 1])
    >>> ZV_Qou_avg = ZM_Aex @ ZV_Qex_avg + ZM_A00 @ ZV_Qou_ini
    >>> ZV_Qou_avg
    array([0.0625   , 0.0625   , 0.03125  , 0.0625   , 0.0390625])
    >>> ZV_Qou_ini = np.array([1, 1, 1, 1, 1])
    >>> ZV_Qex_avg = np.array([1, 1, 1, 1, 1])
    >>> ZV_Qou_avg = ZM_Aex @ ZV_Qex_avg + ZM_A00 @ ZV_Qou_ini
    >>> ZV_Qou_avg
    array([1.     , 1.     , 1.125  , 1.     , 1.09375])
    """

    # -------------------------------------------------------------------------
    # Start with some initial variables
    # -------------------------------------------------------------------------
    IS_riv_bas = ZM_ICN.shape[0]
    ZM_Idt = identity(IS_riv_bas, format="csc", dtype=np.float64)
    ZM_Bet = spsolve(ZM_ICN, ZM_Qex)

    # -------------------------------------------------------------------------
    # Computation of Ae
    # -------------------------------------------------------------------------
    ZM_Aex = csc_matrix((IS_riv_bas, IS_riv_bas))
    ZM_Aex_tmp = ZM_Bet
    for JS_wdw in range(IS_wdw):
        ZM_Aex = ZM_Aex + (IS_wdw - 1 - JS_wdw) * ZM_Aex_tmp
        ZM_Aex_tmp = spsolve(ZM_ICN, ZM_Qou @ ZM_Aex_tmp)
    ZM_Aex = ZM_Aex / IS_wdw

    # -------------------------------------------------------------------------
    # Computation of A0
    # -------------------------------------------------------------------------
    ZM_A00 = csc_matrix((IS_riv_bas, IS_riv_bas))
    ZM_A00_tmp = ZM_Idt
    for _ in range(IS_wdw):
        ZM_A00 = ZM_A00 + ZM_A00_tmp
        ZM_A00_tmp = spsolve(ZM_ICN, ZM_Qou @ ZM_A00_tmp)
    ZM_A00 = ZM_A00 / IS_wdw

    # -------------------------------------------------------------------------
    # Explanations
    # -------------------------------------------------------------------------
    # ZM_Alp = (ZM_ICN)^(-1) @ ZM_Qou
    # ZM_Bet = (ZM_ICN)^(-1) @ ZM_Qex
    # ZM_A00 = (ZM_Idt + ZM_Alp + ZM_Alp^2 + ... + ZM_Alp^(IS_wdw-1))/IS_wdw
    # ZM_Aex = (
    #             (IS_wdw - 1 - 0) * ZM_Bet
    #           + (IS_wdw - 1 - 1) * ZM_Alp @ ZM_Bet
    #           + (IS_wdw - 1 - 2) * ZM_Alp^2 @ ZM_Bet
    #           + ...
    #           + (IS_wdw - 1 - IS_wdw +2) * ZM_Alp^(IS_wdw-2) @ ZM_Bet
    #           ) / IS_wdw
    #
    # The inverse (ZM_ICN)^(-1) is never actually computed, relying instead on
    # the following linear system solver applied to matrices:
    # ZM_ICN @ ZM_Alp^(JS_wdw+1) = ZM_Qou @ ZM_Alp^(JS_wdw)
    # ZM_A00_tmp stores ZM_Alp^(JS_wdw) for the computation of A00.
    # ZM_Aex_tmp stores ZM_Alp^(JS_wdw) @ ZM_Bet for the computation of Aex.
    # The recurrence for ZM_A00 is initialized with ZM_Alp^0 = ZM_Idt
    # The recurrence for ZM_Aex is initialized with ZM_Alp^0 @ ZM_Bet = ZM_Bet
    # Note that spsolve_triangular cannot be used on sparse matrices. It could
    # be used on dense matrices but densifying the lower triangular matrices
    # would not be sustainable for memory usage when dealing with networks
    # composed of 100k-200k river reaches.
    #
    # This implementation explicitly constructs entire Ae and A0 matrices
    # (sparse versions of them) using repeated sparse solves. It is intended as
    # a reference version. More memory- and compute-efficient formulations
    # (e.g. row-restricted construction of S @ Ae) should be considered.

    return ZM_Aex, ZM_A00


# *****************************************************************************
# End
# *****************************************************************************
