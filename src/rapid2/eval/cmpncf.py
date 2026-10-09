#!/usr/bin/env python3
# *****************************************************************************
# cmpncf.py
# *****************************************************************************

# Author:
# Cedric H. David, 2016-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import warnings

import netCDF4
import numpy as np
from numpy.ma import MaskedArray

from rapid2.base import make_0bi_tbl, read_std_vec


# *****************************************************************************
# Compare NetCDF files
# *****************************************************************************
def cmpncf(
    prv_ncf: str,
    now_ncf: str,
    ZS_rtl: np.float64,
    ZS_atl: np.float64,
) -> None:
    """Compare RAPID input/output netCDF files for regression testing.

    Reads metadata and data arrays from two NetCDF files to ensure they share
    matching dimensions, river IDs, coordinates, and time bounds. Evaluates
    the absolute and relative differences of their core data variable against
    provided thresholds, failing loudly if tolerances are exceeded.

    Parameters
    ----------
    prv_ncf : str
        Path to the previous/baseline netCDF file.
    now_ncf : str
        Path to the current/new netCDF file to evaluate.
    ZS_rtl : np.float64
        Acceptable relative tolerance threshold.
    ZS_atl : np.float64
        Acceptable absolute tolerance threshold.

    Returns
    -------
    None

    Examples
    --------
    >>> prv_ncf = "input/Sandbox/Qex_Sandbox_19700101_19700110_TR.nc4"
    >>> now_ncf = "input/Sandbox/Qex_Sandbox_19700101_19700110_TR.nc4"
    >>> ZS_rtl = np.float64(1e-10)
    >>> ZS_atl = np.float64(1e-10)
    >>> cmpncf(p_ncf, n_ncf, ZS_rtl, ZS_atl)
    """

    # -------------------------------------------------------------------------
    # Get metadata in netCDF files
    # -------------------------------------------------------------------------
    (
        IV_riv_prv,
        ZV_lon_prv,
        ZV_lat_prv,
        IV_tim_prv,
        IM_tim_prv,
    ) = read_std_vec(prv_ncf)

    (
        IV_riv_now,
        ZV_lon_now,
        ZV_lat_now,
        IV_tim_now,
        IM_tim_now,
    ) = read_std_vec(now_ncf)

    # -------------------------------------------------------------------------
    # Compare dimension sizes
    # -------------------------------------------------------------------------
    if len(IV_riv_prv) == len(IV_riv_now):
        IS_riv_tot = len(IV_riv_prv)
    else:
        raise ValueError(
            f"The number of river reaches differs: "
            f"{len(IV_riv_prv)} <> {len(IV_riv_now)}"
        )

    if len(IV_tim_prv) == len(IV_tim_now):
        IS_tim = len(IV_tim_prv)
    else:
        raise ValueError(
            f"The number of time steps differs: "
            f"{len(IV_tim_prv)} <> {len(IV_tim_now)}"
        )

    # -------------------------------------------------------------------------
    # Compare rivid values
    # -------------------------------------------------------------------------
    if np.array_equal(IV_riv_prv, IV_riv_now):
        pass
    else:
        if np.array_equal(np.sort(IV_riv_prv), np.sort(IV_riv_now)):
            warnings.warn("The rivids are the same, but sorted differently")
            _, _, IV_0bi_prv = make_0bi_tbl(IV_riv_now, IV_riv_prv)
        else:
            raise ValueError("The rivids differ")

    # -------------------------------------------------------------------------
    # Compare other metadata values
    # -------------------------------------------------------------------------
    if np.array_equal(ZV_lon_prv, ZV_lon_now):
        pass
    else:
        raise ValueError("The longitude values differ")

    if np.array_equal(ZV_lat_prv, ZV_lat_now):
        pass
    else:
        raise ValueError("The latitude values differ")

    if np.array_equal(IV_tim_prv, IV_tim_now):
        pass
    else:
        raise ValueError("The time values differ")

    if (IM_tim_prv is None) != (IM_tim_now is None):
        raise ValueError("time_bnds present in only one file")

    if (IM_tim_prv is not None) and (IM_tim_now is not None):
        if np.array_equal(IM_tim_prv, IM_tim_now):
            pass
        else:
            raise ValueError("The time_bnds values differ")

    # -------------------------------------------------------------------------
    # Get main variable in netCDF files
    # -------------------------------------------------------------------------
    try:
        p = netCDF4.Dataset(prv_ncf, "r")
    except IOError as err:
        raise IOError(f"Unable to open {prv_ncf}") from err

    try:
        n = netCDF4.Dataset(now_ncf, "r")
    except IOError as err:
        raise IOError(f"Unable to open {now_ncf}") from err

    if "Qext" in p.variables and "Qext" in n.variables:
        YS_val_tmp = "Qext"
    elif "Qout" in p.variables and "Qout" in n.variables:
        YS_val_tmp = "Qout"
    else:
        raise ValueError("Neither Qext nor Qout is common variable")

    # -------------------------------------------------------------------------
    # Compute differences
    # -------------------------------------------------------------------------
    ZS_rdf_max = 0
    ZS_adf_max = 0
    BS_fll_prv = False
    BS_fll_now = False

    for JS_tim in range(IS_tim):
        # Initializing
        ZS_rdf = 0
        ZS_adf = 0

        # Getting values
        ZV_val_prv = p.variables[YS_val_tmp][JS_tim, :]
        ZV_val_now = n.variables[YS_val_tmp][JS_tim, :]
        if "IV_0bi_prv" in locals():
            ZV_val_now = ZV_val_now[IV_0bi_prv]

        # Converting masked values to -9999
        if isinstance(ZV_val_prv, MaskedArray) and np.any(ZV_val_prv.mask):
            ZV_val_prv = ZV_val_prv.filled(fill_value=-9999)
            BS_fll_prv = True
        if isinstance(ZV_val_now, MaskedArray) and np.any(ZV_val_now.mask):
            ZV_val_now = ZV_val_now.filled(fill_value=-9999)
            BS_fll_now = True

        # Comparing difference values
        ZV_adf_tmp = np.absolute(ZV_val_prv - ZV_val_now)
        ZS_adf_max = max(np.max(ZV_adf_tmp), ZS_adf_max)

        ZS_rdf = np.sqrt(
            np.sum(ZV_adf_tmp * ZV_adf_tmp) / np.sum(ZV_val_prv * ZV_val_prv)
        )
        ZS_rdf_max = max(ZS_rdf, ZS_rdf_max)

    # -------------------------------------------------------------------------
    # Compare to tolerances and handle closures
    # -------------------------------------------------------------------------
    if BS_fll_prv:
        warnings.warn(f"masked values replaced by -9999 in {prv_ncf}")
    if BS_fll_now:
        warnings.warn(f"masked values replaced by -9999 in {now_ncf}")

    if ZS_rdf_max > ZS_rtl:
        raise ValueError("Unacceptable rel. difference!!!")

    if ZS_adf_max > ZS_atl:
        raise ValueError("Unacceptable abs. difference!!!")

    p.close()
    n.close()


# *****************************************************************************
# End
# *****************************************************************************
