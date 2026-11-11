#!/usr/bin/env python3
# *****************************************************************************
# chck_Kal.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import warnings

import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import LinearOperator, eigs, eigsh

from rapid2.base.updt_Mus_Qou import updt_Mus_Qou


# *****************************************************************************
# Check Kalman filter assimilation matrices
# *****************************************************************************
def chck_Kal(
    ZM_SA0: csc_matrix,
    ZM_SAe: csc_matrix,
    ZM_dQe: csc_matrix,
    ZM_dQo: csc_matrix,
    ZM_Kal: csc_matrix,
    ZM_ICN: csc_matrix,
    ZM_Qex: csc_matrix,
    ZM_Qou: csc_matrix,
    IS_rat_Qob: np.int32,
) -> None:
    """Diagnose theoretical stability and plausibility of Data Assimilation.

    Evaluates the physical controllability, gauge interference, filter
    aggressiveness, and absolute numerical stability of the closed-loop
    routing system before runtime.

    Parameters
    ----------
    ZM_SA0 : scipy.sparse.spmatrix
        The selection-multiplied initial-to-state average matrix.
    ZM_SAe : scipy.sparse.spmatrix
        The selection-multiplied input-to-state average matrix.
    ZM_dQe : scipy.sparse.spmatrix
        The background error covariance matrix.
    ZM_dQo : scipy.sparse.spmatrix
        The observation error covariance matrix.
    ZM_Kal : scipy.sparse.spmatrix
        The computed Kalman Gain matrix.
    ZM_ICN : scipy.sparse.spmatrix
        The linear system matrix for the basin in matrix-based Muskingum.
    ZM_Qex : scipy.sparse.spmatrix
        The multiplicand matrix for ZV_Qex for the basin in right-hand side.
    ZM_Qou : scipy.sparse.spmatrix
        The multiplicand matrix for ZV_Qou for the basin in right-hand side.
    IS_rat_Qob : np.int32
        The number of routing time steps within one assimilation window.

    Returns
    -------
    None

    Examples
    --------
    """

    # -------------------------------------------------------------------------
    # 1. Physical Controllability: Old Water Index
    # -------------------------------------------------------------------------
    ZV_SA0_tmp = np.sum(np.abs(ZM_SA0.toarray()), axis=1)
    ZV_SAe_tmp = np.sum(np.abs(ZM_SAe.toarray()), axis=1)

    ZV_scl = np.divide(
        ZV_SA0_tmp,
        ZV_SAe_tmp,
        out=np.full_like(ZV_SA0_tmp, np.inf),
        where=(ZV_SAe_tmp > 1e-12),
    )

    ZS_scl_max = np.max(ZV_scl)

    print(f"\n[DEBUG] Max Old Water Index (SA0/SAe): {ZS_scl_max:.2f}x")

    if ZS_scl_max >= 5.0:
        raise ValueError(
            f"Observability limit exceeded: Max 'old water' index "
            f"({ZS_scl_max:.2f}x) is critically high. The assimilation "
            "window is too short relative to the routing inertia."
        )
    elif ZS_scl_max > 2.0:
        warnings.warn(
            f"High 'old water' index ({ZS_scl_max:.2f}x). Gauges are "
            "heavily dominated by routing inertia. External forcing "
            "corrections may be artificially inflated.",
            stacklevel=2,
        )

    # -------------------------------------------------------------------------
    # 2. Gauge Interference: Innovation Condition Number
    # -------------------------------------------------------------------------
    ZM_den = ZM_SAe @ ZM_dQe @ ZM_SAe.T + ZM_dQo

    # Get the single (k=1) largest magnitude (which='LM') absolute eigen value
    ZS_val_max = np.float64(
        np.abs(eigsh(ZM_den, k=1, which="LM", return_eigenvectors=False)[0])
    )

    # Use shift-invert (sigma=0.0) to find the eigenvalue closest to zero
    try:
        ZS_val_min = np.float64(
            np.abs(
                eigsh(
                    ZM_den,
                    k=1,
                    sigma=0.0,
                    which="LM",
                    return_eigenvectors=False,
                )[0]
            )
        )
    except Exception:
        ZS_val_min = np.float64(0.0)

    if ZS_val_min == 0.0:
        ZS_scl = np.inf
    else:
        ZS_scl = ZS_val_max / ZS_val_min

    print(f"[DEBUG] Innovation Matrix Condition Number: {ZS_scl:.2e}")

    if ZS_scl > 1e6:
        warnings.warn(
            f"High innovation condition number ({ZS_scl:.2e}). "
            "Gauges are likely interfering with each other due to "
            "overlapping spatial covariance radii (ZS_lkm_cov).",
            stacklevel=2,
        )

    # -------------------------------------------------------------------------
    # 3. Filter Aggressiveness: DA Amplification Ratio
    # -------------------------------------------------------------------------
    ZV_scl = np.sum(np.abs(ZM_Kal.toarray()), axis=0)
    ZS_scl_max = np.max(ZV_scl)

    print(f"[DEBUG] Max DA Amplification Ratio: {ZS_scl_max:.2f}x")

    if ZS_scl_max >= 10.0:
        raise ValueError(
            f"Data assimilation instability: max amplification ratio "
            f"({ZS_scl_max:.2f}x) exceeds critical threshold (10.0)."
        )
    elif ZS_scl_max > 5.0:
        warnings.warn(
            f"High data assimilation amplification ratio "
            f"({ZS_scl_max:.2f}x). Spatial covariance radius may "
            "exceed routing constraints.",
            stacklevel=2,
        )

    # -------------------------------------------------------------------------
    # 4. Absolute Stability: Closed-Loop Spectral Radius
    # -------------------------------------------------------------------------
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Linear Operator mapping initial state to final state across the window
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def mv_CLp(ZV_Qou_prv: np.ndarray) -> np.ndarray:
        # 1. Compute the autonomous feedback correction from the initial state
        ZV_dQe = -(ZM_Kal @ (ZM_SA0 @ ZV_Qou_prv))

        # 2. Route the state forward using the exact Muskingum solver
        _, ZV_Qou_now = updt_Mus_Qou(
            ZM_ICN, ZM_Qex, ZM_Qou, IS_rat_Qob, ZV_Qou_prv, ZV_dQe
        )

        return np.asarray(ZV_Qou_now)

    IS_riv_bas = ZM_ICN.shape[0]
    LO_CLp = LinearOperator(
        (IS_riv_bas, IS_riv_bas), matvec=mv_CLp, dtype=np.float64
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Extract dominant eigenvalue using Arnoldi iteration (eigs for asymmetric)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ZS_rad_max = np.float64(
        np.abs(
            eigs(LO_CLp, k=1, which="LM", tol=1e-2, return_eigenvectors=False)[
                0
            ]
        )
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Evaluate numerical stability limits
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    print(f"[DEBUG] Max Closed-Loop Spectral Radius: {ZS_rad_max:.4f}\n")

    if ZS_rad_max >= 1.0:
        raise ValueError(
            f"Catastrophic DA Instability: Closed-loop spectral radius "
            f"({ZS_rad_max:.4f}) is >= 1.0. The filter feedback loop "
            "will generate infinite mass."
        )
    elif ZS_rad_max > 0.95:
        warnings.warn(
            f"High closed-loop spectral radius ({ZS_rad_max:.4f}). "
            "The assimilation feedback is dangerously close to "
            "numerical instability.",
            stacklevel=2,
        )


# *****************************************************************************
# End
# *****************************************************************************
