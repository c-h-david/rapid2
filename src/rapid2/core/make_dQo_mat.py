#!/usr/bin/env python3
# *****************************************************************************
# make_dQo_mat.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


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
# Observation error covariance matrix (R)
# *****************************************************************************
def make_dQo_mat(
    ZV_Qob_sdv: npt.NDArray[np.float64],
) -> csc_matrix:
    """Create the observation error covariance matrix.

    Create a sparse, purely diagonal covariance matrix from the standard
    deviation of the observed discharge errors. Because individual gauge
    measurement errors are assumed to be spatially independent, no off-diagonal
    correlation tapering is applied.

    Parameters
    ----------
    ZV_Qob_sdv : ndarray[float64]
        The standard deviation of observation errors for the active gauges.

    Returns
    -------
    ZM_dQo : scipy.sparse.spmatrix
        The observation error covariance matrix.

    Examples
    --------
    >>> ZV_Qob_sdv = np.array([0.0, 0.0], dtype=np.float64)
    >>> ZM_dQo = make_dQo_mat(ZV_Qob_sdv)
    >>> ZM_dQo.toarray()
    array([[0., 0.],
           [0., 0.]])
    >>> ZV_Qob_sdv = np.array([1.0, 2.0], dtype=np.float64)
    >>> ZM_dQo = make_dQo_mat(ZV_Qob_sdv)
    >>> ZM_dQo.toarray()
    array([[1., 0.],
           [0., 4.]])
    """

    # -------------------------------------------------------------------------
    # Build pure diagonal covariance matrix
    # -------------------------------------------------------------------------
    # Squaring the standard deviation provides the variance for the diagonal
    # R matrix. Note that if ZV_Qob_sdv contains NoData values (1e20), they
    # will safely square to 1e40 in float64. Because the observation error
    # covariance matrix (R) is inverted in the Kalman gain equation (acting
    # as a denominator), this effectively infinite variance mathematically
    # forces the resulting gain for that specific gauge to exactly zero.
    # This cleanly ignores the missing observation without complex masking.
    ZM_dQo = diags(ZV_Qob_sdv**2, format="csc", dtype=np.float64)

    return ZM_dQo


# *****************************************************************************
# End
# *****************************************************************************
