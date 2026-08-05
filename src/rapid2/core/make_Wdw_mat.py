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
from scipy.sparse import (
    csc_matrix,
    identity,
)


# *****************************************************************************
# Matrices for average over a window
# *****************************************************************************
def make_Wdw_mat(
    ZM_Mus: csc_matrix,
    ZM_Qex: csc_matrix,
    ZM_Qou: csc_matrix,
    IS_rat_Qob: np.int32,
) -> tuple[
    csc_matrix,
    csc_matrix,
]:
    """Create routing matrices for average discharge over a given window.

    Create two matrices such that Qbar = ZM_Aex @ Qebar + ZM_A00 @ Q0 for
    assimilation over a given window of time steps.

    Parameters
    ----------
    ZM_Mus : scipy.sparse.spmatrix
        The transitive propagation matrix (I - C1 N)^-1 for the basin.
    ZM_Qex : scipy.sparse.spmatrix
        The multiplicand matrix for ZV_Qex for the basin in right-hand side.
    ZM_Qou : scipy.sparse.spmatrix
        The multiplicand matrix for ZV_Qou for the basin in right-hand side.
    IS_rat_Qob : np.int32
        The number of consecutive time steps in the assimilation window.

    Returns
    -------
    ZM_Aex : scipy.sparse.spmatrix
        The input to state matrix.
    ZM_A00 : scipy.sparse.spmatrix
        The initial condition to state matrix.

    Examples
    --------
    >>> ZM_Mus = csc_matrix(np.array([[ 1.    ,  0.    ,  0.  ,  0.  ,  0. ],\
                                      [ 0.    ,  1.    ,  0.  ,  0.  ,  0. ],\
                                      [-0.25  , -0.25  ,  1.  ,  0.  ,  0. ],\
                                      [ 0.    ,  0.    ,  0.  ,  1.  ,  0. ],\
                                      [ 0.0625,  0.0625, -0.25, -0.25,  1. ]]))
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
    >>> IS_rat_Qob = 2
    >>> ZM_Aex, ZM_A00 = make_Wdw_mat(ZM_Mus, ZM_Qex, ZM_Qou, IS_rat_Qob)
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
    >>> ZV_Qou_prv = np.array([0, 0, 0, 0, 0])
    >>> ZV_Qex_avg = np.array([1, 1, 1, 1, 1])
    >>> ZV_Qou_avg = ZM_Aex @ ZV_Qex_avg + ZM_A00 @ ZV_Qou_prv
    >>> ZV_Qou_avg
    array([0.0625   , 0.0625   , 0.03125  , 0.0625   , 0.0390625])
    >>> ZV_Qou_prv = np.array([1, 1, 3, 1, 5])
    >>> ZV_Qex_avg = np.array([1, 1, 1, 1, 1])
    >>> ZV_Qou_avg = ZM_Aex @ ZV_Qex_avg + ZM_A00 @ ZV_Qou_prv
    >>> ZV_Qou_avg
    array([1., 1., 3., 1., 5.])
    """

    # -------------------------------------------------------------------------
    # Start with some initial variables
    # -------------------------------------------------------------------------
    IS_riv_bas = ZM_Mus.shape[0]
    ZM_Idt = identity(IS_riv_bas, format="csc", dtype=np.float64)
    ZM_Bet = ZM_Mus @ ZM_Qex

    # -------------------------------------------------------------------------
    # Computation of Ae
    # -------------------------------------------------------------------------
    ZM_Aex = csc_matrix((IS_riv_bas, IS_riv_bas), dtype=np.float64)
    ZM_Aex_tmp = ZM_Bet
    for JS_rat_Qob in range(IS_rat_Qob):
        ZM_Aex = ZM_Aex + (IS_rat_Qob - 1 - JS_rat_Qob) * ZM_Aex_tmp
        ZM_Aex_tmp = ZM_Mus @ (ZM_Qou @ ZM_Aex_tmp)
    ZM_Aex = ZM_Aex / IS_rat_Qob

    # -------------------------------------------------------------------------
    # Computation of A0
    # -------------------------------------------------------------------------
    ZM_A00 = csc_matrix((IS_riv_bas, IS_riv_bas), dtype=np.float64)
    ZM_A00_tmp = ZM_Idt
    for _ in range(IS_rat_Qob):
        ZM_A00 = ZM_A00 + ZM_A00_tmp
        ZM_A00_tmp = ZM_Mus @ (ZM_Qou @ ZM_A00_tmp)
    ZM_A00 = ZM_A00 / IS_rat_Qob

    # -------------------------------------------------------------------------
    # Explanations
    # -------------------------------------------------------------------------
    # ZM_Alp = ZM_Mus @ ZM_Qou
    # ZM_Bet = ZM_Mus @ ZM_Qex
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
    # The precomputed ZM_Mus matrix = (I - C1 N)^-1 is passed directly,
    # replacing spsolve calls with fast sparse matrix multiplication (@).

    return ZM_Aex, ZM_A00


# *****************************************************************************
# End
# *****************************************************************************
