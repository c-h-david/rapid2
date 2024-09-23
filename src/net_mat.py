#!/usr/bin/env python3
# *****************************************************************************
# net_mat.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
import numpy.typing as npt
from scipy.sparse import csc_matrix  # type: ignore


# *****************************************************************************
# Network matrix function
# *****************************************************************************
def net_mat(
            IV_dwn_tot: npt.NDArray[np.int32],
            IM_hsh_tot: dict[np.int32, int],
            IV_riv_bas: npt.NDArray[np.int32],
            IM_hsh_bas: dict[np.int32, int]
            ) -> csc_matrix:
    '''Create network matrix.

    Create network matrix for basin within domain.

    Parameters
    ----------
    IV_dwn_tot : ndarray[int32]
        The river IDs downstream of the river IDs in domain.
    IM_hsh_tot : dict[int32, int]
        The link from river ID to index in domain.
    IV_riv_bas : ndarray[int32]
        The river IDs of the basin.
    IM_hsh_bas : dict[int32, int]
        The link from river ID to index in basin.

    Returns
    -------
    ZM_Net : scipy.sparse.spmatrix
        The network matrix for the basin.

    Examples
    --------
    >>> IV_dwn_tot = np.array([30, 30, 50, 50, 0], dtype=np.int32)
    >>> IM_hsh_tot = {np.int32(10): 0,\
                      np.int32(20): 1,\
                      np.int32(30): 2,\
                      np.int32(40): 3,\
                      np.int32(50): 4}
    >>> IV_riv_bas = np.array([10, 20, 30, 40, 50], dtype=np.int32)
    >>> IM_hsh_bas = {np.int32(10): 0,\
                      np.int32(20): 1,\
                      np.int32(30): 2,\
                      np.int32(40): 3,\
                      np.int32(50): 4}
    >>> net_mat(IV_dwn_tot, IM_hsh_tot, IV_riv_bas, IM_hsh_bas).toarray()
    array([[0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [1, 1, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 1, 1, 0]])
    '''

    IS_riv_bas = len(IV_riv_bas)
    IV_row = []
    IV_col = []
    ZV_val = []
    for JS_riv_bas in range(IS_riv_bas):
        JS_riv_tot = IM_hsh_tot[IV_riv_bas[JS_riv_bas]]
        IS_dwn = IV_dwn_tot[JS_riv_tot]
        if IS_dwn != 0 and IS_dwn in IM_hsh_bas:
            JS_riv_ba2 = IM_hsh_bas[IS_dwn]
            IV_row.append(JS_riv_ba2)
            IV_col.append(JS_riv_bas)
            ZV_val.append(1)

    ZM_Net = csc_matrix((ZV_val, (IV_row, IV_col)),
                        shape=(IS_riv_bas, IS_riv_bas),
                        )

    return ZM_Net


# *****************************************************************************
# End
# *****************************************************************************
