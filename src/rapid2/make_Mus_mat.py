#!/usr/bin/env python3
# *****************************************************************************
# make_Mus_mat.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


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
def make_Mus_mat(
    ZM_Net: csc_matrix,
    ZM_C1p: csc_matrix,
    ZM_C2p: csc_matrix,
    ZM_C3p: csc_matrix,
) -> tuple[csc_matrix, csc_matrix, csc_matrix]:
    """Create routing matrices.

    Create the three matrices used in the matrix-based Muskingum method.

    Parameters
    ----------
    ZM_Net : scipy.sparse.spmatrix
        The network matrix for the basin.
    ZM_C1p : scipy.sparse.spmatrix
        The C1 parameter matrix for the basin.
    ZM_C2p : scipy.sparse.spmatrix
        The C2 parameter matrix for the basin.
    ZM_C3p : scipy.sparse.spmatrix
        The C3 parameter matrix for the basin.

    Returns
    -------
    ZM_ICN : scipy.sparse.spmatrix
        The linear system matrix for the basin in matrix-based Muskingum.
    ZM_Qex : scipy.sparse.spmatrix
        The multiplicand matrix for ZV_Qex for the basin in right-hand side.
    ZM_Qou : scipy.sparse.spmatrix
        The multiplicand matrix for ZV_Qou for the basin in right-hand side.

    Examples
    --------
    >>> ZM_Net = csc_matrix(np.array([[0, 0, 0, 0, 0],\
                                      [0, 0, 0, 0, 0],\
                                      [1, 1, 0, 0, 0],\
                                      [0, 0, 0, 0, 0],\
                                      [0, 0, 1, 1, 0]]))
    >>> ZM_C1p = csc_matrix(np.array([[-0.25,  0.  ,  0.  ,  0.  ,  0.  ],\
                                      [ 0.  , -0.25,  0.  ,  0.  ,  0.  ],\
                                      [ 0.  ,  0.  , -0.25,  0.  ,  0.  ],\
                                      [ 0.  ,  0.  ,  0.  , -0.25,  0.  ],\
                                      [ 0.  ,  0.  ,  0.  ,  0.  , -0.25]]))
    >>> ZM_C2p = csc_matrix(np.array([[0.375, 0.   , 0.   , 0.   , 0.   ],\
                                      [0.   , 0.375, 0.   , 0.   , 0.   ],\
                                      [0.   , 0.   , 0.375, 0.   , 0.   ],\
                                      [0.   , 0.   , 0.   , 0.375, 0.   ],\
                                      [0.   , 0.   , 0.   , 0.   , 0.375]]))
    >>> ZM_C3p = csc_matrix(np.array([[0.875, 0.   , 0.   , 0.   , 0.   ],\
                                      [0.   , 0.875, 0.   , 0.   , 0.   ],\
                                      [0.   , 0.   , 0.875, 0.   , 0.   ],\
                                      [0.   , 0.   , 0.   , 0.875, 0.   ],\
                                      [0.   , 0.   , 0.   , 0.   , 0.875]]))
    >>> ZM_ICN, ZM_Qex, ZM_Qou = make_Mus_mat(ZM_Net, ZM_C1p, ZM_C2p, ZM_C3p)
    >>> ZM_ICN.toarray()
    array([[1.  , 0.  , 0.  , 0.  , 0.  ],
           [0.  , 1.  , 0.  , 0.  , 0.  ],
           [0.25, 0.25, 1.  , 0.  , 0.  ],
           [0.  , 0.  , 0.  , 1.  , 0.  ],
           [0.  , 0.  , 0.25, 0.25, 1.  ]])
    >>> ZM_Qex.toarray()
    array([[0.125, 0.   , 0.   , 0.   , 0.   ],
           [0.   , 0.125, 0.   , 0.   , 0.   ],
           [0.   , 0.   , 0.125, 0.   , 0.   ],
           [0.   , 0.   , 0.   , 0.125, 0.   ],
           [0.   , 0.   , 0.   , 0.   , 0.125]])
    >>> ZM_Qou.toarray()
    array([[0.875, 0.   , 0.   , 0.   , 0.   ],
           [0.   , 0.875, 0.   , 0.   , 0.   ],
           [0.375, 0.375, 0.875, 0.   , 0.   ],
           [0.   , 0.   , 0.   , 0.875, 0.   ],
           [0.   , 0.   , 0.375, 0.375, 0.875]])
    """

    IS_riv_bas = ZM_Net.shape[0]
    ZM_Idt = identity(IS_riv_bas, format="csc", dtype=np.float64)

    ZM_ICN = ZM_Idt - ZM_C1p @ ZM_Net
    ZM_Qex = ZM_C1p + ZM_C2p
    ZM_Qou = ZM_C3p + ZM_C2p @ ZM_Net

    return ZM_ICN, ZM_Qex, ZM_Qou


# *****************************************************************************
# End
# *****************************************************************************
