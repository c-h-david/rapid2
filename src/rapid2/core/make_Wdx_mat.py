#!/usr/bin/env python3
# *****************************************************************************
# make_Wdx_mat.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
from scipy.sparse import (
    csc_matrix,
    identity,
)


# *****************************************************************************
# Matrices for explicit average over a window
# *****************************************************************************
def make_Wdx_mat(
    ZM_Net: csc_matrix,
    ZM_Qex: csc_matrix,
    IS_rat_Qob: np.int32,
) -> tuple[
    csc_matrix,
    csc_matrix,
]:
    """Create explicit routing matrices for average discharge over a window.

    Create two explicit matrices such that Qbar = ZM_Aex @ Qebar + ZM_A00 @ Q0
    for assimilation over a given window of time steps, utilizing the
    time-lagged semi-implicit Muskingum method to completely avoid matrix
    inversions.

    Parameters
    ----------
    ZM_Net : scipy.sparse.spmatrix
        The network matrix for the basin.
    ZM_Qex : scipy.sparse.spmatrix
        The multiplicand matrix for ZV_Qex for the basin (represents Crm).
    IS_rat_Qob : np.int32
        The number of consecutive time steps in the assimilation window.

    Returns
    -------
    ZM_Aex : scipy.sparse.spmatrix
        The explicit input to state matrix.
    ZM_A00 : scipy.sparse.spmatrix
        The explicit initial condition to state matrix.

    Examples
    --------
    >>> ZM_Net = csc_matrix(np.array([[0, 0, 0, 0, 0],\
                                      [0, 0, 0, 0, 0],\
                                      [1, 1, 0, 0, 0],\
                                      [0, 0, 0, 0, 0],\
                                      [0, 0, 1, 1, 0]]))
    >>> ZM_Qex = csc_matrix(np.array([[0.125, 0.   , 0.   , 0.   , 0.   ],\
                                      [0.   , 0.125, 0.   , 0.   , 0.   ],\
                                      [0.   , 0.   , 0.125, 0.   , 0.   ],\
                                      [0.   , 0.   , 0.   , 0.125, 0.   ],\
                                      [0.   , 0.   , 0.   , 0.   , 0.125]]))
    >>> IS_rat_Qob = 2
    >>> ZM_Aex, ZM_A00 = make_Wdx_mat(ZM_Net, ZM_Qex, IS_rat_Qob)
    >>> ZM_Aex.toarray()
    array([[0.0625, 0.    , 0.    , 0.    , 0.    ],
           [0.    , 0.0625, 0.    , 0.    , 0.    ],
           [0.    , 0.    , 0.0625, 0.    , 0.    ],
           [0.    , 0.    , 0.    , 0.0625, 0.    ],
           [0.    , 0.    , 0.    , 0.    , 0.0625]])
    >>> ZM_A00.toarray()
    array([[0.9375, 0.    , 0.    , 0.    , 0.    ],
           [0.    , 0.9375, 0.    , 0.    , 0.    ],
           [0.0625, 0.0625, 0.9375, 0.    , 0.    ],
           [0.    , 0.    , 0.    , 0.9375, 0.    ],
           [0.    , 0.    , 0.0625, 0.0625, 0.9375]])
    >>> ZV_Qou_prv = np.array([0, 0, 0, 0, 0])
    >>> ZV_Qex_avg = np.array([1, 1, 1, 1, 1])
    >>> ZV_Qou_avg = ZM_Aex @ ZV_Qex_avg + ZM_A00 @ ZV_Qou_prv
    >>> ZV_Qou_avg
    array([0.0625, 0.0625, 0.0625, 0.0625, 0.0625])
    >>> ZV_Qou_prv = np.array([1, 1, 3, 1, 5])
    >>> ZV_Qex_avg = np.array([1, 1, 1, 1, 1])
    >>> ZV_Qou_avg = ZM_Aex @ ZV_Qex_avg + ZM_A00 @ ZV_Qou_prv
    >>> ZV_Qou_avg
    array([1., 1., 3., 1., 5.])
    """

    # -------------------------------------------------------------------------
    # Start with some initial variables
    # -------------------------------------------------------------------------
    IS_riv_bas = ZM_Net.shape[0]
    ZM_Idt = identity(IS_riv_bas, format="csc", dtype=np.float64)

    # -------------------------------------------------------------------------
    # Construct the explicit operators (Alpha and Beta)
    # ZM_Qex acts as the modified Courant matrix (Crm = C1 + C2)
    # -------------------------------------------------------------------------
    ZM_Alp = ZM_Idt - ZM_Qex + ZM_Qex @ ZM_Net
    ZM_Bet = ZM_Qex

    # -------------------------------------------------------------------------
    # Computation of Aex
    # -------------------------------------------------------------------------
    ZM_Aex = csc_matrix((IS_riv_bas, IS_riv_bas), dtype=np.float64)
    ZM_Aex_tmp = ZM_Bet
    for JS_rat_Qob in range(IS_rat_Qob):
        ZM_Aex = ZM_Aex + (IS_rat_Qob - 1 - JS_rat_Qob) * ZM_Aex_tmp
        ZM_Aex_tmp = ZM_Alp @ ZM_Aex_tmp
    ZM_Aex = ZM_Aex / IS_rat_Qob

    # -------------------------------------------------------------------------
    # Computation of A00
    # -------------------------------------------------------------------------
    ZM_A00 = csc_matrix((IS_riv_bas, IS_riv_bas), dtype=np.float64)
    ZM_A00_tmp = ZM_Idt
    for _ in range(IS_rat_Qob):
        ZM_A00 = ZM_A00 + ZM_A00_tmp
        ZM_A00_tmp = ZM_Alp @ ZM_A00_tmp
    ZM_A00 = ZM_A00 / IS_rat_Qob

    # -------------------------------------------------------------------------
    # Explanations
    # -------------------------------------------------------------------------
    # ZM_Alp = ZM_Idt - ZM_Crm + ZM_Crm @ ZM_Net
    # ZM_Bet = ZM_Crm
    # ZM_A00 = (ZM_Idt + ZM_Alp + ZM_Alp^2 + ...
    #           + ZM_Alp^(IS_rat_Qob-1)) / IS_rat_Qob
    # ZM_Aex = (
    #             (IS_rat_Qob - 1 - 0) * ZM_Bet
    #           + (IS_rat_Qob - 1 - 1) * ZM_Alp @ ZM_Bet
    #           + (IS_rat_Qob - 1 - 2) * ZM_Alp^2 @ ZM_Bet
    #           + ...
    #           + (IS_rat_Qob - 1 - IS_rat_Qob + 2) * ZM_Alp^(IS_rat_Qob-2)
    #             @ ZM_Bet
    #           ) / IS_rat_Qob
    #
    # The inverse (ZM_ICN)^(-1) is completely bypassed.
    # The recurrence relies strictly on sparse matrix multiplication (@) which
    # is significantly more memory and compute efficient than spsolve.
    # ZM_A00_tmp stores ZM_Alp^(JS_rat_Qob) for the A00 computation.
    # ZM_Aex_tmp stores ZM_Alp^(JS_rat_Qob) @ ZM_Bet for the Aex computation.

    return ZM_Aex, ZM_A00


# *****************************************************************************
# End
# *****************************************************************************
