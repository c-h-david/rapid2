#!/usr/bin/env python3
# *****************************************************************************
# ltir.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import netCDF4
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from rapid2.base import (
    calc_scl_vec,
    make_0bi_tbl,
    make_Net_mat,
    make_Sel_mat,
    read_con_vec,
    read_riv_vec,
    read_std_vec,
)


# *****************************************************************************
# Compute LTIR Scaling Factors
# *****************************************************************************
def ltir(
    con_pqt: str,
    bas_pqt: str,
    Qex_ncf: str,
    Qob_ncf: str,
    scl_pqt: str,
) -> None:
    """Compute Long-Term Inverse Routing (LTIR) scaling factors.

    Computes a static scaling vector for external inflows based on the
    long-term temporal averages of simulated external inflows and observed
    gauge discharges, exporting the resulting scalars to a Parquet file.

    Parameters
    ----------
    con_pqt : str
        Path to the input connectivity Parquet file.
    bas_pqt : str
        Path to the input basin Parquet file.
    Qex_ncf : str
        Path to the input external inflow (Qex) NetCDF file.
    Qob_ncf : str
        Path to the input observations (Qob) NetCDF file.
    scl_pqt : str
        Path to the output scalar (scl) Parquet file.

    Returns
    -------
    None

    Examples
    --------
    >>> con_pqt = "input/Sandbox/con_Sandbox.parquet"
    >>> bas_pqt = "input/Sandbox/bas_Sandbox_ascend.parquet"
    >>> Qex_ncf = "input/Sandbox/Qex_Sandbox_19700101_19700110_FG.nc4"
    >>> Qob_ncf = "input/Sandbox/Qob_Sandbox_19700101_19700110_TR.nc4"
    >>> scl_pqt = "output/Sandbox/scl_Sandbox_tst.parquet"
    >>> ltir(con_pqt, bas_pqt, Qex_ncf, Qob_ncf, scl_pqt)
    >>> import os
    >>> os.path.exists(scl_pqt)
    True
    >>> os.remove(scl_pqt)
    """

    # -------------------------------------------------------------------------
    # River network
    # -------------------------------------------------------------------------
    IV_riv_tot, IV_dwn_tot = read_con_vec(con_pqt)
    IV_riv_bas = read_riv_vec(bas_pqt)

    IT_0bi_tot, IT_0bi_bas, IV_0bi_bas = make_0bi_tbl(IV_riv_tot, IV_riv_bas)
    ZM_Net = make_Net_mat(IV_dwn_tot, IT_0bi_tot, IV_riv_bas, IT_0bi_bas)

    # -------------------------------------------------------------------------
    # External inflows
    # -------------------------------------------------------------------------
    IV_riv_tmp, _, _, IV_tim_all, IM_tim_all = read_std_vec(Qex_ncf)

    if not np.array_equal(IV_riv_tot, IV_riv_tmp):
        raise ValueError(f"River IDs in {Qex_ncf} must match {con_pqt}")

    # -------------------------------------------------------------------------
    # Observational locations
    # -------------------------------------------------------------------------
    IV_riv_avl, _, _, IV_tim_tmp, IM_tim_tmp = read_std_vec(Qob_ncf)

    IV_riv_act = IV_riv_avl[np.isin(IV_riv_avl, IV_riv_bas)]
    if len(IV_riv_act) == 0:
        raise ValueError("No valid overlapping gauges found in the basin")

    _, _, IV_0bi_act = make_0bi_tbl(IV_riv_avl, IV_riv_act)
    ZM_Sel = make_Sel_mat(IV_riv_act, IT_0bi_bas)

    # -------------------------------------------------------------------------
    # Validate temporal alignment
    # -------------------------------------------------------------------------
    IS_tim_all = IM_tim_all[0, 0] if IM_tim_all is not None else IV_tim_all[0]
    IS_tim_tmp = IM_tim_tmp[0, 0] if IM_tim_tmp is not None else IV_tim_tmp[0]
    if IS_tim_all != IS_tim_tmp:
        raise ValueError(
            f"Start times differ. Qex: {IS_tim_all}, Qob: {IS_tim_tmp}"
        )

    IS_tim_all = (
        IM_tim_all[-1, 1] if IM_tim_all is not None else IV_tim_all[-1]
    )
    IS_tim_tmp = (
        IM_tim_tmp[-1, 1] if IM_tim_tmp is not None else IV_tim_tmp[-1]
    )
    if IS_tim_all != IS_tim_tmp:
        raise ValueError(
            f"End times differ. Qex: {IS_tim_all}, Qob: {IS_tim_tmp}"
        )

    # -------------------------------------------------------------------------
    # Average external inflows
    # -------------------------------------------------------------------------
    try:
        f = netCDF4.Dataset(Qex_ncf, "r")
    except IOError as err:
        raise IOError(f"Unable to open {Qex_ncf}") from err

    ZV_Qex_avg = np.mean(f.variables["Qext"][:, IV_0bi_bas], axis=0)
    f.close()

    # -------------------------------------------------------------------------
    # Average observations
    # -------------------------------------------------------------------------
    try:
        o = netCDF4.Dataset(Qob_ncf, "r")
    except IOError as err:
        raise IOError(f"Unable to open {Qob_ncf}") from err

    ZV_Qob_avg = np.mean(o.variables["Qout"][:, IV_0bi_act], axis=0)
    o.close()

    # -------------------------------------------------------------------------
    # Compute LTIR Scaling Factors
    # -------------------------------------------------------------------------
    ZV_scl_bas = calc_scl_vec(ZM_Net, ZM_Sel, ZV_Qex_avg, ZV_Qob_avg)

    # -------------------------------------------------------------------------
    # Export scalars to Parquet
    # -------------------------------------------------------------------------
    ZV_scl_tot = np.full_like(IV_riv_tot, np.nan, dtype=np.float64)
    ZV_scl_tot[IV_0bi_bas] = ZV_scl_bas

    table = pa.table([IV_riv_tot, ZV_scl_tot], names=["riv", "scl"])

    schema = pa.schema(
        [
            field.with_nullable(False) if field.name == "riv" else field
            for field in table.schema
        ]
    )
    table = table.cast(schema)

    try:
        pq.write_table(table, scl_pqt)
    except IOError as err:
        raise IOError(f"Unable to write to {scl_pqt}") from err


# *****************************************************************************
# End
# *****************************************************************************
