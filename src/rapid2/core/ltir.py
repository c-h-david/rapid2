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
import pyarrow.parquet as pq
from tqdm import tqdm

from rapid2.base import prep_Qex_ncf, read_std_vec


# *****************************************************************************
# Apply Long-Term Inverse Routing (LTIR) Scaling Factors
# *****************************************************************************
def ltir(prv_ncf: str, scl_pqt: str, now_ncf: str) -> None:
    """Apply Long-Term Inverse Routing (LTIR) scaling to external inflow.

    Reads a file containing scaling factors and applies them multiplicatively
    to an existing uncorrected external inflow dataset across all timesteps,
    saving the bias-corrected values to a new file.

    Parameters
    ----------
    prv_ncf : str
        Path to the uncorrected input external inflow (Qex) NetCDF file.
    scl_pqt : str
        Path to the input scalar (scl) Parquet file containing scaling factors.
    now_ncf : str
        Path to the output corrected external inflow (Qex) NetCDF file.

    Returns
    -------
    None

    Examples
    --------
    >>> prv_ncf = "input/Sandbox/Qex_Sandbox_19700101_19700110_FG.nc4"
    >>> scl_pqt = "input/Sandbox/scl_Sandbox.parquet"
    >>> now_ncf = "output/Sandbox/Qex_Sandbox_19700101_19700110_BC_tst.nc4"
    >>> ltir(prv_ncf, scl_pqt, now_ncf)
    >>> import os
    >>> os.path.exists(now_ncf)
    True
    >>> os.remove(now_ncf)
    """

    # -------------------------------------------------------------------------
    # Validate metadata alignment between files
    # -------------------------------------------------------------------------
    (
        IV_riv_tot,
        ZV_lon_tot,
        ZV_lat_tot,
        IV_tim_all,
        IM_tim_all,
    ) = read_std_vec(prv_ncf)
    IS_tim_all = len(IV_tim_all)

    try:
        table = pq.read_table(scl_pqt, columns=["riv", "scl"])
    except IOError as err:
        raise IOError(f"Unable to open {scl_pqt}") from err

    IV_riv_tmp = table.column("riv").to_numpy().astype(np.int32)

    if not np.array_equal(IV_riv_tot, IV_riv_tmp):
        raise ValueError(f"River IDs in {scl_pqt} must match {prv_ncf}")

    # -------------------------------------------------------------------------
    # Load scalars and handle NoData padding
    # -------------------------------------------------------------------------
    ZV_scl_tot = table.column("scl").to_numpy().astype(np.float64)
    ZV_scl_tot = np.nan_to_num(ZV_scl_tot, nan=1.0)

    # -------------------------------------------------------------------------
    # Prepare the new netCDF file
    # -------------------------------------------------------------------------
    prep_Qex_ncf(IV_riv_tot, ZV_lon_tot, ZV_lat_tot, now_ncf)

    try:
        p = netCDF4.Dataset(prv_ncf, "r")
    except IOError as err:
        raise IOError(f"Unable to open {prv_ncf}") from err

    try:
        n = netCDF4.Dataset(now_ncf, "a")
    except IOError as err:
        raise IOError(f"Unable to open {now_ncf} for appending") from err

    # Copy time and time bounds
    n.variables["time"][:] = IV_tim_all
    if IM_tim_all is not None:
        n.variables["time_bnds"][:] = IM_tim_all

    # -------------------------------------------------------------------------
    # Apply scaling factors
    # -------------------------------------------------------------------------
    for JS_tim_all in tqdm(range(IS_tim_all), desc="Scaling external inflow"):
        ZV_Qex_tmp = p.variables["Qext"][JS_tim_all, :]
        n.variables["Qext"][JS_tim_all, :] = ZV_Qex_tmp * ZV_scl_tot

    # -------------------------------------------------------------------------
    # Copy global attributes
    # -------------------------------------------------------------------------
    for attr in ["title", "institution"]:
        if attr in p.ncattrs():
            n.setncattr(attr, p.getncattr(attr))

    # -------------------------------------------------------------------------
    # Close files
    # -------------------------------------------------------------------------
    p.close()
    n.close()


# *****************************************************************************
# End
# *****************************************************************************
