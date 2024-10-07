#!/usr/bin/env python3
# *****************************************************************************
# chk_ids.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
import numpy.typing as npt


# *****************************************************************************
# Check topology
# *****************************************************************************
def chk_top(
            IV_riv_bas: npt.NDArray[np.int32],
            IM_hsh_bas: dict[np.int32, int],
            IV_riv_tot: npt.NDArray[np.int32],
            IV_dwn_tot: npt.NDArray[np.int32],
            IM_hsh_tot: dict[np.int32, int]
            ) -> None:
    '''Check topology.

    Check missing connections upstream and downstream as well as adequate sort.

    Parameters
    ----------
    IV_riv_bas : ndarray[int32]
        The river IDs of the basin.
    IM_hsh_bas : dict[int32, int]
        The link from river ID to index in basin.
    IV_riv_tot : ndarray[int32]
        The river IDs of the domain.
    IV_dwn_tot : ndarray[int32]
        The river IDs downstream of the river IDs in domain.
    IM_hsh_tot : dict[int32, int]
        The link from river ID to index in domain.

    Returns
    -------
    None

    Examples
    --------
    >>> IV_riv_bas = np.array([10, 20, 30, 40, 50], dtype=np.int32)
    >>> IM_hsh_bas = {np.int32(10): 0,\
                      np.int32(20): 1,\
                      np.int32(30): 2,\
                      np.int32(40): 3,\
                      np.int32(50): 4}
    >>> IV_riv_tot = np.array([10, 20, 30, 40, 50], dtype=np.int32)
    >>> IV_dwn_tot = np.array([30, 30, 50, 50, 0], dtype=np.int32)
    >>> IM_hsh_tot = {np.int32(10): 0,\
                      np.int32(20): 1,\
                      np.int32(30): 2,\
                      np.int32(40): 3,\
                      np.int32(50): 4}
    >>> chk_top(IV_riv_bas, IM_hsh_bas, IV_riv_tot, IV_dwn_tot, IM_hsh_tot)
    >>> IV_riv_bas = np.array([10, 20, 30, 40], dtype=np.int32)
    >>> IM_hsh_bas = {np.int32(10): 0,\
                      np.int32(20): 1,\
                      np.int32(30): 2,\
                      np.int32(40): 3}
    >>> chk_top(IV_riv_bas, IM_hsh_bas, IV_riv_tot, IV_dwn_tot, IM_hsh_tot)
    WARNING - connectivity: 50 is downstream of 30 but is not in basin file
    WARNING - connectivity: 50 is downstream of 40 but is not in basin file
    >>> IV_riv_bas = np.array([20, 30, 40, 50], dtype=np.int32)
    >>> IM_hsh_bas = {np.int32(20): 0,\
                      np.int32(30): 1,\
                      np.int32(40): 2,\
                      np.int32(50): 3}
    >>> chk_top(IV_riv_bas, IM_hsh_bas, IV_riv_tot, IV_dwn_tot, IM_hsh_tot)
    WARNING - connectivity: 10 is upstream of 30 but is not in basin file
    >>> IV_riv_bas = np.array([50, 40, 30, 20, 10], dtype=np.int32)
    >>> IM_hsh_bas = {np.int32(50): 0,\
                      np.int32(40): 1,\
                      np.int32(30): 2,\
                      np.int32(20): 3,\
                      np.int32(10): 4}
    >>> chk_top(IV_riv_bas, IM_hsh_bas, IV_riv_tot, IV_dwn_tot,\
                IM_hsh_tot) # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ValueError: Sorting problem: 50 is downstream of 40 but is located above in
    basin file
    '''

    # -------------------------------------------------------------------------
    # Check for missing connections upstream
    # -------------------------------------------------------------------------
    IS_riv_tot = len(IV_riv_tot)
    for JS_riv_tot in range(IS_riv_tot):
        IS_riv = IV_riv_tot[JS_riv_tot]
        IS_dwn = IV_dwn_tot[JS_riv_tot]
        if IS_dwn != 0:
            if IS_dwn in IM_hsh_bas and IS_riv not in IM_hsh_bas:
                print('WARNING - connectivity: ' + str(IS_riv) +
                      ' is upstream of ' + str(IS_dwn) +
                      ' but is not in basin file')

    # -------------------------------------------------------------------------
    # Check for missing connections downstream
    # -------------------------------------------------------------------------
    for IS_riv in IV_riv_bas:
        IS_dwn = IV_dwn_tot[IM_hsh_tot[IS_riv]]
        if IS_dwn != 0:
            if IS_dwn not in IM_hsh_bas:
                print('WARNING - connectivity: ' + str(IS_dwn) +
                      ' is downstream of ' + str(IS_riv) +
                      ' but is not in basin file')

    # -------------------------------------------------------------------------
    # Check sorting from upstream to downstream
    # -------------------------------------------------------------------------
    for IS_riv in IV_riv_bas:
        IS_dwn = IV_dwn_tot[IM_hsh_tot[IS_riv]]
        if IS_dwn != 0:
            if IS_dwn in IM_hsh_bas:
                if IM_hsh_bas[IS_dwn] < IM_hsh_bas[IS_riv]:
                    raise ValueError('Sorting problem: ' + str(IS_dwn) +
                                     ' is downstream of ' + str(IS_riv) +
                                     ' but is located above in basin file')


# *****************************************************************************
# End
# *****************************************************************************
