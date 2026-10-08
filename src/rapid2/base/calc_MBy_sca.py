#!/usr/bin/env python3
# *****************************************************************************
# calc_MBy_sca.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
from scipy.sparse import csc_matrix


# *****************************************************************************
# Memory footprint calculation
# *****************************************************************************
def calc_MBy_sca(
    ZM_Net: csc_matrix,
) -> np.float64:
    """Calculate the memory footprint of a sparse matrix in megabytes.

    Computes the total memory footprint of a SciPy CSC matrix by summing
    the sizes of its underlying data, indices, and indptr arrays, and
    returns the size in megabytes (MB).

    Parameters
    ----------
    ZM_Net : scipy.sparse.spmatrix
        The sparse matrix whose memory footprint is to be calculated.

    Returns
    -------
    ZS_MBy : np.float64
        The memory footprint of the sparse matrix in megabytes (MB).

    Examples
    --------
    >>> ZM_Net = csc_matrix(np.array([[0, 0, 0, 0, 0],\
                                      [0, 0, 0, 0, 0],\
                                      [1, 1, 0, 0, 0],\
                                      [0, 0, 0, 0, 0],\
                                      [0, 0, 1, 1, 0]], dtype=np.float64))
    >>> ZS_MBy = calc_MBy_sca(ZM_Net)
    >>> round(ZS_MBy * 1024**2) in [72, 112]
    True
    """

    # -------------------------------------------------------------------------
    # Calculate footprint in megabytes
    # -------------------------------------------------------------------------
    ZS_MBy = np.float64(
        (ZM_Net.data.nbytes + ZM_Net.indices.nbytes + ZM_Net.indptr.nbytes)
        / (1024**2)
    )

    return ZS_MBy


# *****************************************************************************
# End
# *****************************************************************************
