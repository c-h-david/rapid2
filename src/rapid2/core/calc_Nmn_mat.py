#!/usr/bin/env python3
# *****************************************************************************
# calc_Lum_mat.py
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
# Neumann series inverse network matrix
# *****************************************************************************
def calc_Nmn_mat(
    ZM_nlp: csc_matrix,
) -> csc_matrix:
    """Calculate (I - ZM_nlp)^-1 using the Neumann series expansion

    For a nilpotent matrix of a Directed Acyclic Graph (e.g. a river network),
    the infinite series converges exactly in a finite number of steps:
    (I - ZM_nlp)^-1 = I + ZM_nlp + ZM_nlp^2 + ... + ZM_nlp^k

    Parameters
    ----------
    ZM_nlp : scipy.sparse.csc_matrix
        The nilpotent sparse matrix (e.g. ZM_Net or ZM_C1m*ZM_Net)

    Returns
    -------
    ZM_Nmn : scipy.sparse.csc_matrix
        The precomputed lumped routing inverse matrix.

    Examples
    --------
    >>> ZM_Net = csc_matrix(np.array([[0, 0, 0, 0, 0],\
                                      [0, 0, 0, 0, 0],\
                                      [1, 1, 0, 0, 0],\
                                      [0, 0, 0, 0, 0],\
                                      [0, 0, 1, 1, 0]], dtype=np.float64))
    >>> ZM_Lmp = calc_Nmn_mat(ZM_Net)
    >>> ZM_Lmp.toarray()
    array([[1., 0., 0., 0., 0.],
           [0., 1., 0., 0., 0.],
           [1., 1., 1., 0., 0.],
           [0., 0., 0., 1., 0.],
           [1., 1., 1., 1., 1.]])
    """

    # -------------------------------------------------------------------------
    # Start with some initial variables
    # -------------------------------------------------------------------------
    IS_riv_bas = ZM_nlp.shape[0]
    ZM_Idt = identity(IS_riv_bas, format="csc", dtype=np.float64)

    # -------------------------------------------------------------------------
    # Compute Neumann series expansion
    # -------------------------------------------------------------------------
    ZM_Nmn = ZM_Idt.copy()
    ZM_tmp = ZM_nlp.copy()

    for _ in range(IS_riv_bas):
        if ZM_tmp.nnz == 0:
            break
        ZM_Nmn = ZM_Nmn + ZM_tmp
        ZM_tmp = ZM_tmp @ ZM_nlp

    return ZM_Nmn


# *****************************************************************************
# End
# *****************************************************************************
