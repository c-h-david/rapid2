#!/usr/bin/env python3
# *****************************************************************************
# ccc_mat.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
import numpy.typing as npt
from scipy.sparse import (  # type: ignore[import-untyped]
    csc_matrix,
    diags,
)


# *****************************************************************************
# Muskingum C1, C2, C3 function
# *****************************************************************************
def ccc_mat(
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
    ZM_C1m : scipy.sparse.spmatrix
        The C1 parameter matrix for the basin.
    ZM_C2m : scipy.sparse.spmatrix
        The C2 parameter matrix for the basin.
    ZM_C3m : scipy.sparse.spmatrix
        The C3 parameter matrix for the basin.

    Examples
    --------
    >>> ZV_kpr_bas = np.array([9000.0, 9000.0, 9000.0, 9000.0, 9000.0])
    >>> ZV_xpr_bas = np.array([0.25, 0.25, 0.25, 0.25, 0.25])
    >>> IS_dtR = 900
    >>> ZM_C1m, ZM_C2m, ZM_C3m = ccc_mat(ZV_kpr_bas, ZV_xpr_bas, IS_dtR)
    >>> ZM_C1m.toarray()
    array([[-0.25,  0.  ,  0.  ,  0.  ,  0.  ],
           [ 0.  , -0.25,  0.  ,  0.  ,  0.  ],
           [ 0.  ,  0.  , -0.25,  0.  ,  0.  ],
           [ 0.  ,  0.  ,  0.  , -0.25,  0.  ],
           [ 0.  ,  0.  ,  0.  ,  0.  , -0.25]])
    >>> ZM_C2m.toarray()
    array([[0.375, 0.   , 0.   , 0.   , 0.   ],
           [0.   , 0.375, 0.   , 0.   , 0.   ],
           [0.   , 0.   , 0.375, 0.   , 0.   ],
           [0.   , 0.   , 0.   , 0.375, 0.   ],
           [0.   , 0.   , 0.   , 0.   , 0.375]])
    >>> ZM_C3m.toarray()
    array([[0.875, 0.   , 0.   , 0.   , 0.   ],
           [0.   , 0.875, 0.   , 0.   , 0.   ],
           [0.   , 0.   , 0.875, 0.   , 0.   ],
           [0.   , 0.   , 0.   , 0.875, 0.   ],
           [0.   , 0.   , 0.   , 0.   , 0.875]])
    >>> (ZM_C1m + ZM_C2m + ZM_C3m).toarray()
    array([[1., 0., 0., 0., 0.],
           [0., 1., 0., 0., 0.],
           [0., 0., 1., 0., 0.],
           [0., 0., 0., 1., 0.],
           [0., 0., 0., 0., 1.]])
    """

    ZV_den = IS_dtR / 2 + ZV_kpr_bas * (1 - ZV_xpr_bas)

    ZV_C1m = IS_dtR / 2 - ZV_kpr_bas * ZV_xpr_bas
    ZV_C1m = ZV_C1m / ZV_den
    ZM_C1m = diags(ZV_C1m, format="csc", dtype=np.float64)

    ZV_C2m = IS_dtR / 2 + ZV_kpr_bas * ZV_xpr_bas
    ZV_C2m = ZV_C2m / ZV_den
    ZM_C2m = diags(ZV_C2m, format="csc", dtype=np.float64)

    ZV_C3m = -IS_dtR / 2 + ZV_kpr_bas * (1 - ZV_xpr_bas)
    ZV_C3m = ZV_C3m / ZV_den
    ZM_C3m = diags(ZV_C3m, format="csc", dtype=np.float64)

    return ZM_C1m, ZM_C2m, ZM_C3m


# *****************************************************************************
# End
# *****************************************************************************
