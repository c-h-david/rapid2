#!/usr/bin/env python3
# *****************************************************************************
# make_Sel_mat.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
import numpy.typing as npt
from scipy.sparse import csc_matrix


# *****************************************************************************
# Selection matrix function
# *****************************************************************************
def make_Sel_mat(
    IV_riv_act: npt.NDArray[np.int32],
    IT_0bi_bas: dict[np.int32, int],
) -> csc_matrix:
    """Create selection matrix for active observations.

    Create a selection matrix mapping the active observation gauges to their
    corresponding indices within the simulated basin.

    Parameters
    ----------
    IV_riv_act : ndarray[int32]
        The river IDs of the active observations within the basin.
    IT_0bi_bas : dict[int32, int]
        The link from river ID to 0-based index in the simulated basin.

    Returns
    -------
    ZM_Sel : scipy.sparse.spmatrix
        The selection matrix mapping active observations to basin reaches.

    Examples
    --------
    >>> IV_riv_act = np.array([30, 50], dtype=np.int32)
    >>> IT_0bi_bas = {np.int32(10): 0, np.int32(20): 1, np.int32(30): 2, \\
    ...               np.int32(40): 3, np.int32(50): 4}
    >>> ZM_Sel = make_Sel_mat(IV_riv_act, IT_0bi_bas)
    >>> ZM_Sel.toarray()
    array([[0., 0., 1., 0., 0.],
           [0., 0., 0., 0., 1.]])
    """

    IS_riv_act = len(IV_riv_act)
    IS_riv_bas = len(IT_0bi_bas)

    IV_row = np.arange(IS_riv_act, dtype=np.int32)
    IV_col = np.array(
        [IT_0bi_bas[IS_riv] for IS_riv in IV_riv_act], dtype=np.int32
    )
    ZV_val = np.ones(IS_riv_act, dtype=np.float64)

    ZM_Sel = csc_matrix(
        (ZV_val, (IV_row, IV_col)),
        shape=(IS_riv_act, IS_riv_bas),
    )

    return ZM_Sel


# *****************************************************************************
# End
# *****************************************************************************
