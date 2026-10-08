#!/usr/bin/env python3
# *****************************************************************************
# calc_Kal_mat.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve


# *****************************************************************************
# Kalman Gain matrix
# *****************************************************************************
def calc_Kal_mat(
    ZM_SAe: csc_matrix,
    ZM_dQe: csc_matrix,
    ZM_dQo: csc_matrix,
) -> csc_matrix:
    """Calculate the Kalman Gain matrix using a sparse linear system solver.

    Computes the Kalman Gain (K) used to distribute observation innovations
    back into the background state. Because the control variable being updated
    is the external inflow, the observation operator (H) is exactly the
    selection-multiplied input-to-state matrix (SAe). 
    
    The function bypasses explicit matrix inversion by solving the linear
    system S * X = SAe * Pb (where S is the innovation covariance) and
    transposing the result to yield K = Pb * SAe^T * S^-1.

    Parameters
    ----------
    ZM_SAe : scipy.sparse.spmatrix
        The explicit input to selected state matrix (Sel * Aex).
    ZM_dQe : scipy.sparse.spmatrix
        The background error covariance matrix (Pb).
    ZM_dQo : scipy.sparse.spmatrix
        The observation error covariance matrix (R).

    Returns
    -------
    ZM_Kal : scipy.sparse.spmatrix
        The Kalman Gain matrix (K).

    Examples
    --------
    >>> import numpy as np
    >>> ZM_SAe = csc_matrix([[-0.0156, -0.0156,  0.0625,  0.    ,  0.    ],\
                             [ 0.0039,  0.0039, -0.0156, -0.0156,  0.0625]])
    >>> ZM_dQe = csc_matrix([[100.  ,   3.33,   0.  ,   0.  ,   0.  ],\
                             [  3.33, 100.  ,   0.  ,   0.  ,   0.  ],\
                             [  0.  ,   0.  , 100.  ,   1.48,   0.  ],\
                             [  0.  ,   0.  ,   1.48,  25.  ,   0.  ],\
                             [  0.  ,   0.  ,   0.  ,   0.  ,  25.  ]])
    >>> ZM_dQo = csc_matrix([[0., 0.],\
                             [0., 0.]])
    >>> ZM_Kal = calc_Kal_mat(ZM_SAe, ZM_dQe, ZM_dQo)
    >>> np.round(ZM_Kal.toarray(), 4)
    array([[-3.6674, -0.0453],
           [-3.6674, -0.0453],
           [14.1693, -0.0226],
           [-0.7403, -3.7566],
           [ 3.8095, 15.0624]])
    """

    # -------------------------------------------------------------------------
    # Denominator (Innovation covariance S)
    # -------------------------------------------------------------------------
    # S = H * Pb * H^T + R
    ZM_den = ZM_SAe @ ZM_dQe @ ZM_SAe.T + ZM_dQo

    # -------------------------------------------------------------------------
    # Solve linear system to avoid explicit inversion of S
    # -------------------------------------------------------------------------
    # We want K = Pb * H^T * S^-1
    # Because S and Pb are symmetric, we can solve the transposed system:
    # S * X = H * Pb  -->  X = S^-1 * H * Pb  -->  X^T = Pb * H^T * S^-1
    ZM_rhs = ZM_SAe @ ZM_dQe

    # spsolve returns a dense array or a CSR matrix depending on inputs.
    # We cast back to CSC to maintain pipeline consistency.
    ZM_tmp = spsolve(ZM_den, ZM_rhs)
    ZM_Kal = csc_matrix(ZM_tmp.T)

    return ZM_Kal


# *****************************************************************************
# End
# *****************************************************************************
