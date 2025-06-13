#!/usr/bin/env python3
# *****************************************************************************
# stp_cor.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np


# *****************************************************************************
# Time step correspondance
# *****************************************************************************
def stp_cor(
            IS_TaR: np.int32,
            IS_dtR: np.int32
            ) -> int:
    '''Read basin file.

    Create one array of river IDs based on basin file.

    Parameters
    ----------
    IS_TaR : int32
       The time step of the lateral inflow volume file.
    IS_dtR : int32
       The time step of Muskingum routing.

    Returns
    -------
    IS_mus : int
        The number of Muskingum time steps per lateral inflow time step.

    Examples
    --------
    >>> IS_TaR = np.int32(10800)
    >>> IS_dtR = np.int32(900)
    >>> stp_cor(IS_TaR, IS_dtR)
    12
    >>> IS_TaR = np.int32(10800)
    >>> IS_dtR = np.int32(800)
    >>> stp_cor(IS_TaR, IS_dtR)
    Traceback (most recent call last):
    ValueError: quotient of time steps is not an integer
    '''

    if round(IS_TaR/IS_dtR) == IS_TaR/IS_dtR:
        IS_mus = round(IS_TaR/IS_dtR)
    else:
        raise ValueError('quotient of time steps is not an integer')

    return IS_mus


# *****************************************************************************
# End
# *****************************************************************************
