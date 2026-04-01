#!/usr/bin/env python3
# *****************************************************************************
# make_CCC_mat.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
import numpy.typing as npt
from scipy.sparse import (
    csc_matrix,
    diags,
)


# *****************************************************************************
# Muskingum C1, C2, C3 function
# *****************************************************************************
def make_CCC_mat(
    ZV_kpr_bas: npt.NDArray[np.float64],
    ZV_xpr_bas: npt.NDArray[np.float64],
    IS_dtR: np.int32,
) -> tuple[csc_matrix, csc_matrix, csc_matrix]:
    """Create parameter matrices.

    Create C1, C2, and C3 parameter matrices for basin within domain.

    Parameters
    ----------
    ZV_kpr_bas : ndarray[float64]
        The values of k in the basin.
    ZV_xpr_bas : ndarray[float64]
        The values of x in the basin.
    IS_dtR : int32
        The routing time step of Muskingum method.

    Returns
    -------
    ZM_C1p : scipy.sparse.spmatrix
        The C1 parameter matrix for the basin.
    ZM_C2p : scipy.sparse.spmatrix
        The C2 parameter matrix for the basin.
    ZM_C3p : scipy.sparse.spmatrix
        The C3 parameter matrix for the basin.

    Examples
    --------
    >>> ZV_kpr_bas = np.array([9000.0, 9000.0, 9000.0, 9000.0, 9000.0])
    >>> ZV_xpr_bas = np.array([0.25, 0.25, 0.25, 0.25, 0.25])
    >>> IS_dtR = 900
    >>> ZM_C1p, ZM_C2p, ZM_C3p = make_CCC_mat(ZV_kpr_bas, ZV_xpr_bas, IS_dtR)
    >>> ZM_C1p.toarray()
    array([[-0.25,  0.  ,  0.  ,  0.  ,  0.  ],
           [ 0.  , -0.25,  0.  ,  0.  ,  0.  ],
           [ 0.  ,  0.  , -0.25,  0.  ,  0.  ],
           [ 0.  ,  0.  ,  0.  , -0.25,  0.  ],
           [ 0.  ,  0.  ,  0.  ,  0.  , -0.25]])
    >>> ZM_C2p.toarray()
    array([[0.375, 0.   , 0.   , 0.   , 0.   ],
           [0.   , 0.375, 0.   , 0.   , 0.   ],
           [0.   , 0.   , 0.375, 0.   , 0.   ],
           [0.   , 0.   , 0.   , 0.375, 0.   ],
           [0.   , 0.   , 0.   , 0.   , 0.375]])
    >>> ZM_C3p.toarray()
    array([[0.875, 0.   , 0.   , 0.   , 0.   ],
           [0.   , 0.875, 0.   , 0.   , 0.   ],
           [0.   , 0.   , 0.875, 0.   , 0.   ],
           [0.   , 0.   , 0.   , 0.875, 0.   ],
           [0.   , 0.   , 0.   , 0.   , 0.875]])
    >>> (ZM_C1p + ZM_C2p + ZM_C3p).toarray()
    array([[1., 0., 0., 0., 0.],
           [0., 1., 0., 0., 0.],
           [0., 0., 1., 0., 0.],
           [0., 0., 0., 1., 0.],
           [0., 0., 0., 0., 1.]])
    """

    ZV_den = IS_dtR / 2 + ZV_kpr_bas * (1 - ZV_xpr_bas)

    ZV_C1p = IS_dtR / 2 - ZV_kpr_bas * ZV_xpr_bas
    ZV_C1p = ZV_C1p / ZV_den
    ZM_C1p = diags(ZV_C1p, format="csc", dtype=np.float64)

    ZV_C2p = IS_dtR / 2 + ZV_kpr_bas * ZV_xpr_bas
    ZV_C2p = ZV_C2p / ZV_den
    ZM_C2p = diags(ZV_C2p, format="csc", dtype=np.float64)

    ZV_C3p = -IS_dtR / 2 + ZV_kpr_bas * (1 - ZV_xpr_bas)
    ZV_C3p = ZV_C3p / ZV_den
    ZM_C3p = diags(ZV_C3p, format="csc", dtype=np.float64)

    return ZM_C1p, ZM_C2p, ZM_C3p


# *****************************************************************************
# End
# *****************************************************************************
