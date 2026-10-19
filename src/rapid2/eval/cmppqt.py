#!/usr/bin/env python3
# *****************************************************************************
# cmppqt.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
import pyarrow.parquet as pq


# *****************************************************************************
# Compare Parquet files
# *****************************************************************************
def cmppqt(
    prv_pqt: str,
    now_pqt: str,
    ZS_rtl: np.float64,
    ZS_atl: np.float64,
) -> None:
    """Compare RAPID input/output Parquet files for regression testing.

    Reads data from two Parquet files to ensure they share matching columns
    and row counts. Evaluates the absolute and relative differences of their
    numerical columns against provided thresholds, failing loudly if tolerances
    are exceeded.

    Parameters
    ----------
    prv_pqt : str
        Path to the previous/baseline Parquet file.
    now_pqt : str
        Path to the current/new Parquet file to evaluate.
    ZS_rtl : np.float64
        Acceptable relative tolerance threshold.
    ZS_atl : np.float64
        Acceptable absolute tolerance threshold.

    Returns
    -------
    None

    Examples
    --------
    >>> prv_pqt = "input/Sandbox/kpr_Sandbox.parquet"
    >>> now_pqt = "input/Sandbox/kpr_Sandbox.parquet"
    >>> ZS_rtl = np.float64(1e-10)
    >>> ZS_atl = np.float64(1e-10)
    >>> cmppqt(prv_pqt, now_pqt, ZS_rtl, ZS_atl)
    """

    # -------------------------------------------------------------------------
    # Open Parquet files
    # -------------------------------------------------------------------------
    try:
        p = pq.read_table(prv_pqt)
    except IOError as err:
        raise IOError(f"Unable to open {prv_pqt}") from err

    try:
        n = pq.read_table(now_pqt)
    except IOError as err:
        raise IOError(f"Unable to open {now_pqt}") from err

    # -------------------------------------------------------------------------
    # Compare schema and row counts
    # -------------------------------------------------------------------------
    if p.num_rows != n.num_rows:
        raise ValueError(
            f"The number of rows differs: {p.num_rows} <> {n.num_rows}"
        )

    if p.column_names != n.column_names:
        raise ValueError(
            f"The columns differ: {p.column_names} <> {n.column_names}"
        )

    # -------------------------------------------------------------------------
    # Compute differences for each column
    # -------------------------------------------------------------------------
    for YS_col in p.column_names:
        AV_val_prv = p.column(YS_col).to_numpy()
        AV_val_now = n.column(YS_col).to_numpy()

        # Handle numeric comparisons
        if np.issubdtype(AV_val_prv.dtype, np.number) and np.issubdtype(
            AV_val_now.dtype, np.number
        ):
            ZV_val_prv = AV_val_prv.astype(np.float64)
            ZV_val_now = AV_val_now.astype(np.float64)

            ZV_adf_tmp = np.absolute(ZV_val_prv - ZV_val_now)
            ZS_adf_max = np.max(ZV_adf_tmp)

            ZS_den = np.sum(ZV_val_prv * ZV_val_prv)
            if ZS_den == 0.0:
                ZS_rdf_max = np.float64(0.0) if ZS_adf_max == 0.0 else np.inf
            else:
                ZS_rdf_max = np.sqrt(np.sum(ZV_adf_tmp * ZV_adf_tmp) / ZS_den)

            if ZS_rdf_max > ZS_rtl:
                raise ValueError(
                    f"Unacceptable rel. difference in column {YS_col}!!!"
                )

            if ZS_adf_max > ZS_atl:
                raise ValueError(
                    f"Unacceptable abs. difference in column {YS_col}!!!"
                )

        # Handle non-numeric comparisons (exact match required)
        else:
            if not np.array_equal(AV_val_prv, AV_val_now):
                raise ValueError(f"Values in column {YS_col} differ strictly!")


# *****************************************************************************
# End
# *****************************************************************************
