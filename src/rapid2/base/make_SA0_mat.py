#!/usr/bin/env python3
# *****************************************************************************
# make_SA0_mat.py
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
def make_SA0_mat(
    ZM_Sel: csc_matrix,
    ZM_Mus: csc_matrix,
    ZM_Qou: csc_matrix,
    IS_rat_Qob: np.int32,
) -> csc_matrix:
    """Create selection-multiplied initial condition matrix over a window.

    Create a single matrix such that ZM_SA0 = ZM_Sel @ ZM_A00 without having
    to build the full, memory-intensive ZM_A00 matrix. This leverages the
    smaller row-size of the selection matrix to minimize floating point
    operations.

    Parameters
    ----------
    ZM_Sel : scipy.sparse.spmatrix
        The selection matrix mapping active observations to river reaches.
    ZM_Mus : scipy.sparse.spmatrix
        The transitive propagation matrix (I - C1 N)^-1 for the basin.
    ZM_Qou : scipy.sparse.spmatrix
        The multiplicand matrix for ZV_Qou for the basin in right-hand side.
    IS_rat_Qob : np.int32
        The number of consecutive time steps in the assimilation window.

    Returns
    -------
    ZM_SA0 : scipy.sparse.spmatrix
        The explicit initial condition to selected state matrix (Sel * A00).

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
    >>> ZM_Qou = csc_matrix(np.array([[0.875, 0.   , 0.   , 0.   , 0.   ],\
                                      [0.   , 0.875, 0.   , 0.   , 0.   ],\
                                      [0.375, 0.375, 0.875, 0.   , 0.   ],\
                                      [0.   , 0.   , 0.   , 0.875, 0.   ],\
                                      [0.   , 0.   , 0.375, 0.375, 0.875]]))
    >>> IS_rat_Qob = 2
    >>> ZM_SA0 = make_SA0_mat(ZM_Sel, ZM_Mus, ZM_Qou, IS_rat_Qob)
    >>> ZM_SA0.toarray()
    array([[ 0.078125  ,  0.078125  ,  0.9375    ,  0.        ,  0.        ],
           [-0.01953125, -0.01953125,  0.078125  ,  0.078125  ,  0.9375    ]])
    """

    # -------------------------------------------------------------------------
    # Start with some initial variables
    # -------------------------------------------------------------------------
    IS_riv_act = ZM_Sel.shape[0]
    IS_riv_bas = ZM_Mus.shape[0]

    ZM_Alp = ZM_Mus @ ZM_Qou

    # -------------------------------------------------------------------------
    # Computation of SA0
    # -------------------------------------------------------------------------
    ZM_SA0 = csc_matrix((IS_riv_act, IS_riv_bas), dtype=np.float64)

    ZM_tmp = ZM_Sel.copy()

    for _ in range(IS_rat_Qob):
        ZM_SA0 = ZM_SA0 + ZM_tmp
        ZM_tmp = ZM_tmp @ ZM_Alp

    ZM_SA0 = cast(csc_matrix, ZM_SA0 / IS_rat_Qob)

    # -------------------------------------------------------------------------
    # Explanations
    # -------------------------------------------------------------------------
    # We avoid computing the massive ZM_A00 matrix by distributing ZM_Sel
    # inside the summation:
    # ZM_SA0 = (
    #               ZM_Sel
    #             + ZM_Sel @ ZM_Alp
    #             + ZM_Sel @ ZM_Alp^2
    #             + ...
    #           ) / IS_rat_Qob

    return ZM_SA0


# *****************************************************************************
# End
# *****************************************************************************
