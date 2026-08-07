#!/usr/bin/env python3
# *****************************************************************************
# make_SAe_mat.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
from typing import cast

import numpy as np
from scipy.sparse import csc_matrix


# *****************************************************************************
# Matrices for selection-multiplied average over a window
# *****************************************************************************
def make_SAe_mat(
    ZM_Sel: csc_matrix,
    ZM_Mus: csc_matrix,
    ZM_Qex: csc_matrix,
    ZM_Qou: csc_matrix,
    IS_rat_Qob: np.int32,
) -> csc_matrix:
    """Create selection-multiplied input-to-state average matrix over a window.

    Create a single matrix such that ZM_SAe = ZM_Sel @ ZM_Aem without having
    to build the full, memory-intensive ZM_Aem matrix. This leverages the
    smaller row-size of the selection matrix and factors out the constant right
    multiplier to minimize floating point operations.

    Parameters
    ----------
    ZM_Sel : scipy.sparse.spmatrix
        The selection matrix mapping active observations to river reaches.
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
    ZM_SAe : scipy.sparse.spmatrix
        The explicit input to selected state matrix (Sel * Aex).

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.sparse import csc_matrix
    >>> ZM_Sel = csc_matrix(np.array([[0., 0., 1., 0., 0.],\
                                      [0., 0., 0., 0., 1.]]))
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
    >>> ZM_SAe = make_SAe_mat(ZM_Sel, ZM_Mus, ZM_Qex, ZM_Qou, IS_rat_Qob)
    >>> ZM_SAe.toarray()
    array([[-0.015625  , -0.015625  ,  0.0625    ,  0.        ,  0.        ],
           [ 0.00390625,  0.00390625, -0.015625  , -0.015625  ,  0.0625    ]])
    """

    # -------------------------------------------------------------------------
    # Start with some initial variables
    # -------------------------------------------------------------------------
    IS_riv_act = ZM_Sel.shape[0]
    IS_riv_bas = ZM_Mus.shape[0]

    ZM_Alp = ZM_Mus @ ZM_Qou
    ZM_Bet = ZM_Mus @ ZM_Qex

    # -------------------------------------------------------------------------
    # Computation of SAe
    # -------------------------------------------------------------------------
    ZM_SAe = csc_matrix((IS_riv_act, IS_riv_bas), dtype=np.float64)

    ZM_tmp = ZM_Sel

    for JS_rat_Qob in range(IS_rat_Qob):
        ZM_SAe = ZM_SAe + (IS_rat_Qob - 1 - JS_rat_Qob) * ZM_tmp
        ZM_tmp = ZM_tmp @ ZM_Alp

    ZM_SAe = cast(csc_matrix, (ZM_SAe @ ZM_Bet) / IS_rat_Qob)

    # -------------------------------------------------------------------------
    # Explanations
    # -------------------------------------------------------------------------
    # We avoid computing the massive ZM_Aex matrix by distributing ZM_Sel
    # inside the summation and factoring out ZM_Bet to the right:
    # ZM_SAe = (
    #             (IS_rat_Qob - 1 - 0) * (ZM_Sel)
    #           + (IS_rat_Qob - 1 - 1) * (ZM_Sel @ ZM_Alp)
    #           + (IS_rat_Qob - 1 - 2) * (ZM_Sel @ ZM_Alp^2)
    #           + ...
    #           ) @ ZM_Bet / IS_rat_Qob

    return ZM_SAe


# *****************************************************************************
# End
# *****************************************************************************
