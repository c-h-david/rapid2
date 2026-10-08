#!/usr/bin/env python3
# *****************************************************************************
# make_dQe_mat.py
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
from scipy.spatial import cKDTree

from rapid2 import calc_GCt_vec


# *****************************************************************************
# Background error covariance matrix (Pb)
# *****************************************************************************
def make_dQe_mat(
    ZV_Qex_sdv: npt.NDArray[np.float64],
    ZV_lon_bas: npt.NDArray[np.float64],
    ZV_lat_bas: npt.NDArray[np.float64],
    ZS_lkm_cov: np.float64,
) -> csc_matrix:
    """Create the background error covariance matrix for external inflow.

    Create a sparse covariance matrix from the standard deviation of the
    external inflow error. Spatial correlation is computed using a 5th-order
    Gaspari-Cohn tapering function over the spherical surface distance between
    reaches. The Gaspari-Cohn half-width parameter (c) is calculated from the
    e-folding length scale (L) via second-order curvature matching
    (c = sqrt(5/3) * L), smoothly dropping to zero at a cutoff distance of 2c.
    Reaches with missing data (NoData) for standard deviation of the external
    inflow error are mathematically isolated by forcing their variance to 0.0.

    Parameters
    ----------
    ZV_Qex_sdv : ndarray[float64]
        The standard deviation of external inflow errors for the basin.
    ZV_lon_bas : ndarray[float64]
        The longitudes related to river IDs in the basin.
    ZV_lat_bas : ndarray[float64]
        The latitudes related to river IDs in the basin.
    ZS_lkm_cov : float64
        The e-folding correlation length scale (L) in kilometers.

    Returns
    -------
    ZM_dQe : scipy.sparse.spmatrix
        The background error covariance matrix.

    Examples
    --------
    >>> ZV_Qex_sdv = np.array([10.0, 10.0, 10.0, 5.0, 5.0], dtype=np.float64)
    >>> ZV_lon_bas = np.array([4.30, 5.94, 5.12, 6.55, 4.30])
    >>> ZV_lat_bas = np.array([8.20, 8.20, 5.12, 4.30, 2.04])
    >>> ZS_lkm_cov = np.float64(0)
    >>> ZM_dQe_0 = make_dQe_mat(ZV_Qex_sdv, ZV_lon_bas, ZV_lat_bas, ZS_lkm_cov)
    >>> np.round(ZM_dQe_0.toarray(), 2)
    array([[100.,   0.,   0.,   0.,   0.],
           [  0., 100.,   0.,   0.,   0.],
           [  0.,   0., 100.,   0.,   0.],
           [  0.,   0.,   0.,  25.,   0.],
           [  0.,   0.,   0.,   0.,  25.]])
    >>> ZS_lkm_cov = np.float64(100.0)
    >>> ZM_dQe = make_dQe_mat(ZV_Qex_sdv, ZV_lon_bas, ZV_lat_bas, ZS_lkm_cov)
    >>> np.round(ZM_dQe.toarray(), 2)
    array([[100.  ,   3.33,   0.  ,   0.  ,   0.  ],
           [  3.33, 100.  ,   0.  ,   0.  ,   0.  ],
           [  0.  ,   0.  , 100.  ,   1.48,   0.  ],
           [  0.  ,   0.  ,   1.48,  25.  ,   0.  ],
           [  0.  ,   0.  ,   0.  ,   0.  ,  25.  ]])
    >>> ZV_eig = np.linalg.eigvalsh(ZM_dQe.toarray())
    >>> bool(np.min(ZV_eig) > 0.0)
    True
    """

    # -------------------------------------------------------------------------
    # Clean NoData values to 0.0 variance
    # -------------------------------------------------------------------------
    ZV_sdv_tmp = np.where(ZV_Qex_sdv == 1e20, 0.0, ZV_Qex_sdv)

    # -------------------------------------------------------------------------
    # Skip rest and return diagonal of variances if zero length of correlation
    # -------------------------------------------------------------------------
    if ZS_lkm_cov == 0.0:
        ZM_dQe = diags(ZV_sdv_tmp**2, format="csc", dtype=np.float64)
        return ZM_dQe

    # -------------------------------------------------------------------------
    # Arithmetic mean of WGS84 ellipsoid radius
    # -------------------------------------------------------------------------
    # semi-major axis in km (6378.137 is for WGS84)
    ZS_a = 6378.137
    # flatening (298.257223563 is for WGS84)
    ZS_f = 1 / 298.257223563
    # arithmetic mean of ellipsoid radius
    ZS_rad_ear = ZS_a * (1 - ZS_f / 3)

    # -------------------------------------------------------------------------
    # Calculate 3D Cartesian coordinates of river reaches on a spherical Earth
    # -------------------------------------------------------------------------
    coords = ZS_rad_ear * np.column_stack(
        (
            np.cos(np.radians(ZV_lat_bas)) * np.cos(np.radians(ZV_lon_bas)),
            np.cos(np.radians(ZV_lat_bas)) * np.sin(np.radians(ZV_lon_bas)),
            np.sin(np.radians(ZV_lat_bas)),
        )
    )

    # -------------------------------------------------------------------------
    # Gaspari-Cohn parameter (GC equation goes to zero at two half-widths)
    # -------------------------------------------------------------------------
    # Half-width (c) from e-folding length (L) via 2nd-order curvature matching
    ZS_c = np.sqrt(5.0 / 3.0) * ZS_lkm_cov

    # -------------------------------------------------------------------------
    # Sparse matrix with distances separating reaches (using spatial indexing)
    # -------------------------------------------------------------------------
    # Convert surface distance cutoff to 3D straight-line distance:
    # cKDTree computes the straight-line (chord) distance between 3D Cartesian
    # coordinates. However, the Gaspari-Cohn polynomial requires the surface
    # distance (arc length) and mathematically drops to zero at exactly 2*c.
    # To rigorously enforce this surface cutoff using the 3D KD-Tree search,
    # we map the target arc length (s = 2*c) to its equivalent chord length (C)
    # using the spherical geometry formula:
    # C = 2 * R * sin(s / (2 * R)).
    ZS_tmp = 2.0 * ZS_rad_ear * np.sin(2.0 * ZS_c / (2.0 * ZS_rad_ear))

    # Sparse matrix of chord distances separating reaches:
    # We query the KD-Tree to build an IS_riv_bas x IS_riv_bas sparse matrix,
    # where the element at (i, j) is the chord distance between reach i and j.
    # Requesting the "coo_matrix" (Coordinate format) directly exposes the flat
    # .row, .col, and .data arrays. This bypasses the overhead of CSC column
    # compression, allowing for blazing-fast vectorized math in the next steps.
    tree = cKDTree(coords)
    ZM_lkm = tree.sparse_distance_matrix(
        tree, max_distance=ZS_tmp, output_type="coo_matrix"
    )

    # Convert chord distances to arc lengths directly in the matrix
    # s = 2*R*arcsin(C / (2*R)). Clip to prevent rounding errors > 1.0
    ZM_lkm.data = (
        2.0
        * ZS_rad_ear
        * np.arcsin(np.clip(ZM_lkm.data / (2.0 * ZS_rad_ear), -1.0, 1.0))
    )

    # -------------------------------------------------------------------------
    # Gaspari-Cohn Tapering and Covariance Assembly (In-Place)
    # -------------------------------------------------------------------------
    # 1. Overwrite arc lengths with Gaspari-Cohn tapering weights (Alpha)
    ZM_lkm.data = calc_GCt_vec(ZM_lkm.data / ZS_c)

    # 2. Multiply weights by the standard deviations at (row, col) coordinates
    ZM_lkm.data *= ZV_sdv_tmp[ZM_lkm.row] * ZV_sdv_tmp[ZM_lkm.col]

    # Cast the populated COO matrix to CSC for downstream routing math
    ZM_dQe = ZM_lkm.tocsc()

    return ZM_dQe


# *****************************************************************************
# End
# *****************************************************************************
