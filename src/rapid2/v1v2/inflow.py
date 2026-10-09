#!/usr/bin/env python3
# *****************************************************************************
# inflow.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import os

import netCDF4

from rapid2.base import prep_Qex_ncf


# *****************************************************************************
# Convert External Inflow Volume to External Inflow Rate
# *****************************************************************************
def inflow(
    m3r_ncf: str,
    Qex_ncf: str,
) -> None:
    """Convert legacy external inflow volume (m3_riv) to inflow rate (Qext).

    Parameters
    ----------
    m3r_ncf : str
        Path to the input external inflow volume NetCDF file.
    Qex_ncf : str
        Path to the output external inflow rate NetCDF file.

    Returns
    -------
    None

    Examples
    --------
    >>> m3r_ncf = "./input/Sandbox/m3_riv_Sandbox.nc4"
    >>> Qex_ncf = "./input/Sandbox/Qex_Sandbox_tst.nc4"
    >>> inflow(m3r_ncf, Qex_ncf)  # doctest: +SKIP
    """

    # -------------------------------------------------------------------------
    # Overwrite protection
    # -------------------------------------------------------------------------
    if os.path.exists(Qex_ncf):
        raise FileExistsError(f"File already exists: {Qex_ncf}")

    # -------------------------------------------------------------------------
    # Open input external volume file
    # -------------------------------------------------------------------------
    try:
        d = netCDF4.Dataset(m3r_ncf, "r")
    except IOError as err:
        raise IOError(f"Unable to open {m3r_ncf}") from err

    # -------------------------------------------------------------------------
    # Get metadata from m3_riv file
    # -------------------------------------------------------------------------
    if "m3_riv" not in d.variables:
        raise ValueError(f"m3_riv variable does not exist in {m3r_ncf}")

    if "rivid" not in d.variables:
        raise ValueError(f"rivid variable does not exist in {m3r_ncf}")

    if "lon" not in d.variables:
        raise ValueError(f"lon variable does not exist in {m3r_ncf}")

    if "lat" not in d.variables:
        raise ValueError(f"lat variable does not exist in {m3r_ncf}")

    if "time" not in d.variables:
        raise ValueError(f"time variable does not exist in {m3r_ncf}")

    if "time_bnds" not in d.variables:
        raise ValueError(f"time_bnds variable does not exist in {m3r_ncf}")

    IV_riv_tot = d.variables["rivid"][:]
    ZV_lon_tot = d.variables["lon"][:]
    ZV_lat_tot = d.variables["lat"][:]

    IV_tim_all = d.variables["time"][:]
    IM_tim_all = d.variables["time_bnds"][:]

    IS_tim_all = len(IV_tim_all)
    IS_dtE = IM_tim_all[0, 1] - IM_tim_all[0, 0]

    # -------------------------------------------------------------------------
    # Create Qex file
    # -------------------------------------------------------------------------
    prep_Qex_ncf(IV_riv_tot, ZV_lon_tot, ZV_lat_tot, Qex_ncf)

    try:
        f = netCDF4.Dataset(Qex_ncf, "a")
    except IOError as err:
        raise IOError(f"Unable to open {Qex_ncf}") from err

    f.variables["time"][:] = IV_tim_all
    f.variables["time_bnds"][:] = IM_tim_all

    # -------------------------------------------------------------------------
    # Convert inflow volume to rate
    # -------------------------------------------------------------------------
    for JS_tim_all in range(IS_tim_all):
        f.variables["Qext"][JS_tim_all, :] = (
            d.variables["m3_riv"][JS_tim_all, :] / IS_dtE
        )

    # -------------------------------------------------------------------------
    # Close files
    # -------------------------------------------------------------------------
    d.close()
    f.close()


# *****************************************************************************
# End
# *****************************************************************************
