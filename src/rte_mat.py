#!/usr/bin/env python3
# *****************************************************************************
# rte_mat.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
from scipy.sparse import identity  # type: ignore
from scipy.sparse import csc_matrix


# *****************************************************************************
# Muskingum routing matrices
# *****************************************************************************
def rte_mat(
            ZM_Net: csc_matrix,
            ZM_C1m: csc_matrix,
            ZM_C2m: csc_matrix,
            ZM_C3m: csc_matrix
            ) -> tuple[
                       csc_matrix,
                       csc_matrix,
                       csc_matrix
                       ]:
    '''Create routing matrices.

    Create the three matrices used in the matrix-based Muskingum method.

    Parameters
    ----------
    ZM_Net : scipy.sparse.spmatrix
        The network matrix for the basin.
    ZM_C1m : scipy.sparse.spmatrix
        The C1 parameter matrix for the basin.
    ZM_C2m : scipy.sparse.spmatrix
        The C2 parameter matrix for the basin.
    ZM_C3m : scipy.sparse.spmatrix
        The C3 parameter matrix for the basin.

    Returns
    -------
    ZM_Lin : scipy.sparse.spmatrix
        The linear system matrix for the basin in matrix-based Muskingum.
    ZM_Qex : scipy.sparse.spmatrix
        The multiplicand matrix for ZV_Qex for the basin in right-hand side.
    ZM_Qou : scipy.sparse.spmatrix
        The multiplicand matrix for ZV_Qou for the basin in left-hand side.

    Examples
    --------
    >>> ZM_Net= [[0, 0, 0, 0, 0],\
                 [0, 0, 0, 0, 0],\
                 [1, 1, 0, 0, 0],\
                 [0, 0, 0, 0, 0],\
                 [0, 0, 1, 1, 0]]
    >>> ZM_Net= csc_matrix(np.array(ZM_Net))
    >>> ZM_C1m= [[-0.3592233,  0.       ,  0.       ,  0.       ,  0.       ],\
                 [ 0.       , -0.3592233,  0.       ,  0.       ,  0.       ],\
                 [ 0.       ,  0.       , -0.3592233,  0.       ,  0.       ],\
                 [ 0.       ,  0.       ,  0.       , -0.3592233,  0.       ],\
                 [ 0.       ,  0.       ,  0.       ,  0.       , -0.3592233]]
    >>> ZM_C1m= csc_matrix(np.array(ZM_C1m))
    >>> ZM_C2m= [[0.45631068, 0.        , 0.        , 0.        , 0.        ],\
                 [0.        , 0.45631068, 0.        , 0.        , 0.        ],\
                 [0.        , 0.        , 0.45631068, 0.        , 0.        ],\
                 [0.        , 0.        , 0.        , 0.45631068, 0.        ],\
                 [0.        , 0.        , 0.        , 0.        , 0.45631068]]
    >>> ZM_C2m= csc_matrix(np.array(ZM_C2m))
    >>> ZM_C3m= [[0.90291262, 0.        , 0.        , 0.        , 0.        ],\
                 [0.        , 0.90291262, 0.        , 0.        , 0.        ],\
                 [0.        , 0.        , 0.90291262, 0.        , 0.        ],\
                 [0.        , 0.        , 0.        , 0.90291262, 0.        ],\
                 [0.        , 0.        , 0.        , 0.        , 0.90291262]]
    >>> ZM_C3m= csc_matrix(np.array(ZM_C3m))
    >>> ZM_Lin, ZM_Qex, ZM_Qou= rte_mat(ZM_Net, ZM_C1m, ZM_C2m, ZM_C3m)
    >>> ZM_Lin.toarray()
    array([[1.       , 0.       , 0.       , 0.       , 0.       ],
           [0.       , 1.       , 0.       , 0.       , 0.       ],
           [0.3592233, 0.3592233, 1.       , 0.       , 0.       ],
           [0.       , 0.       , 0.       , 1.       , 0.       ],
           [0.       , 0.       , 0.3592233, 0.3592233, 1.       ]])
    >>> ZM_Qex.toarray()
    array([[0.09708738, 0.        , 0.        , 0.        , 0.        ],
           [0.        , 0.09708738, 0.        , 0.        , 0.        ],
           [0.        , 0.        , 0.09708738, 0.        , 0.        ],
           [0.        , 0.        , 0.        , 0.09708738, 0.        ],
           [0.        , 0.        , 0.        , 0.        , 0.09708738]])

    >>> ZM_Qou.toarray()
    array([[0.90291262, 0.        , 0.        , 0.        , 0.        ],
           [0.        , 0.90291262, 0.        , 0.        , 0.        ],
           [0.45631068, 0.45631068, 0.90291262, 0.        , 0.        ],
           [0.        , 0.        , 0.        , 0.90291262, 0.        ],
           [0.        , 0.        , 0.45631068, 0.45631068, 0.90291262]])
    '''

    IS_riv_bas = ZM_Net.shape[0]
    ZM_Idt = identity(IS_riv_bas, format='csc', dtype=np.int32)

    ZM_Lin = ZM_Idt - ZM_C1m * ZM_Net
    ZM_Qex = ZM_C1m + ZM_C2m
    ZM_Qou = ZM_C3m + ZM_C2m * ZM_Net

    return ZM_Lin, ZM_Qex, ZM_Qou


# *****************************************************************************
# End
# *****************************************************************************
