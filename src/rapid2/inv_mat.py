#!/usr/bin/env python3
# *****************************************************************************
# inv_mat.py
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


# *****************************************************************************
# Muskingum routing matrices
# *****************************************************************************
def inv_mat(
            ZM_Net: csc_matrix,
            ZM_C1m: csc_matrix,
            ) -> csc_matrix:
    '''Create inverse Muskingum matrix.

    Create the inverse of the matrix used in matrix-based Muskingum method.

    Parameters
    ----------
    ZM_Net : scipy.sparse.spmatrix
        The network matrix for the basin.
    ZM_C1m : scipy.sparse.spmatrix
        The C1 parameter matrix for the basin.

    Returns
    -------
    ZM_Inv : scipy.sparse.spmatrix
        The inverse of the matrix used in matrix-based Muskingum method.

    Examples
    --------
    >>> ZM_Net = csc_matrix(np.array([[0, 0, 0, 0, 0],\
                                      [0, 0, 0, 0, 0],\
                                      [1, 1, 0, 0, 0],\
                                      [0, 0, 0, 0, 0],\
                                      [0, 0, 1, 1, 0]]))
    >>> ZM_C1m = csc_matrix(np.array([[-0.25,  0.  ,  0.  ,  0.  ,  0.  ],\
                                      [ 0.  , -0.25,  0.  ,  0.  ,  0.  ],\
                                      [ 0.  ,  0.  , -0.25,  0.  ,  0.  ],\
                                      [ 0.  ,  0.  ,  0.  , -0.25,  0.  ],\
                                      [ 0.  ,  0.  ,  0.  ,  0.  , -0.25]]))
    >>> ZM_Inv = inv_mat(ZM_Net, ZM_C1m)
    >>> ZM_Inv.toarray()
    array([[ 1.    ,  0.    ,  0.    ,  0.    ,  0.    ],
           [ 0.    ,  1.    ,  0.    ,  0.    ,  0.    ],
           [-0.25  , -0.25  ,  1.    ,  0.    ,  0.    ],
           [ 0.    ,  0.    ,  0.    ,  1.    ,  0.    ],
           [ 0.0625,  0.0625, -0.25  , -0.25  ,  1.    ]])
    '''

    IS_riv_bas = ZM_Net.shape[0]
    ZM_Idt = identity(IS_riv_bas, format='csc', dtype=np.float64)

    ZM_C1N = ZM_C1m @ ZM_Net

    ZM_Inv = ZM_Idt
    ZM_inc = ZM_C1N
    for _ in range(IS_riv_bas):
        ZM_Inv = ZM_Inv + ZM_inc
        ZM_inc = ZM_inc @ ZM_C1N

    # Compute (I-C1N)^-1 using Equation (10) in David et al. (2013, WRR).

    return ZM_Inv


# *****************************************************************************
# End
# *****************************************************************************
