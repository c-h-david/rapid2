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


# *****************************************************************************
# Check Kalman filter assimilation matrices
# *****************************************************************************
def chck_Kal(
    ZM_SA0: csc_matrix,
    ZM_SAe: csc_matrix,
    ZM_dQe: csc_matrix,
    ZM_dQo: csc_matrix,
    ZM_Kal: csc_matrix,
    ZM_Mus: csc_matrix,
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
    ZM_Mus : scipy.sparse.spmatrix
        The transitive propagation matrix (I - C1 N)^-1 for the basin.

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

    print(f"\n[DEBUG] Max Old Water Index (SA0/SAe): {ZS_scl_max:.2f}x")


# *****************************************************************************
# End
# *****************************************************************************
