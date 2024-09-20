#!/usr/bin/env python3
# *****************************************************************************
# hsh_tbl.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
import numpy.typing as npt


# *****************************************************************************
# Hash tables function
# *****************************************************************************
def hsh_tbl(
            IV_riv_tot: npt.NDArray[np.int32],
            IV_riv_bas: npt.NDArray[np.int32]
            ) -> tuple[
                       dict[np.int32, int],
                       dict[np.int32, int],
                       npt.NDArray[np.int32]
                       ]:
    '''Create two hash tables and an indexing array.

    Create one hash table linking river ID to index in connectivity file,
    create one hash table linking river ID to index in basin file, and create
    one array with the index in connectivity file corresponding to each river
    ID in the basin file.

    Parameters
    ----------
    arg1 : ndarray[int32]
        Path to the basin file.
    arg2 : ndarray[int32]
        Path to the basin file.

    Returns
    -------
    ndarray[int32]
        The river IDs of the basin.

    Examples
    --------
    >>> IV_riv_tot = np.array([10, 20, 30, 40, 50], dtype=np.int32)
    >>> IV_riv_bas = np.array([10, 20, 30, 40, 50], dtype=np.int32)
    >>> hsh_tbl(IV_riv_tot, IV_riv_bas) # doctest: +NORMALIZE_WHITESPACE
     ({np.int32(10): 0,\
       np.int32(20): 1,\
       np.int32(30): 2,\
       np.int32(40): 3,\
       np.int32(50): 4},\
      {np.int32(10): 0,\
       np.int32(20): 1,\
       np.int32(30): 2,\
       np.int32(40): 3,\
       np.int32(50): 4},\
      array([0, 1, 2, 3, 4], dtype=int32))

    '''

    IS_riv_tot = len(IV_riv_tot)
    IM_hsh_tot = {}
    for JS_riv_tot in range(IS_riv_tot):
        IM_hsh_tot[IV_riv_tot[JS_riv_tot]] = JS_riv_tot
    # IM_hsh_tot[IS_riv] = JS_riv_tot

    IS_riv_bas = len(IV_riv_bas)
    IM_hsh_bas = {}
    for JS_riv_bas in range(IS_riv_bas):
        IM_hsh_bas[IV_riv_bas[JS_riv_bas]] = JS_riv_bas
    # IM_hsh_bas[IS_riv] = JS_riv_bas

    IV_bas_tot = np.zeros(IS_riv_bas, dtype=np.int32)
    for JS_riv_bas in range(IS_riv_bas):
        IV_bas_tot[JS_riv_bas] = IM_hsh_tot[IV_riv_bas[JS_riv_bas]]
    # This array allows for index mapping such that IV_riv_tot[JS_riv_tot]
    #                                             = IV_riv_bas[JS_riv_bas]
    # IV_bas_tot[JS_riv_bas] = JS_riv_tot

    return IM_hsh_tot, IM_hsh_bas, IV_bas_tot


# *****************************************************************************
# End
# *****************************************************************************
