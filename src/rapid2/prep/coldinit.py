#!/usr/bin/env python3
# *****************************************************************************
# coldinit.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import os

import netCDF4

from rapid2.base import prep_Qfi_ncf


# *****************************************************************************
# Generate Cold-Start State
# *****************************************************************************
def coldinit(
    Qex_ncf: str,
    Q00_ncf: str,
) -> None:
    """Create an initial discharge file with zero values for cold start.

    Parameters
    ----------
    Qex_ncf : str
        Path to the input external inflow NetCDF file.
    Q00_ncf : str
        Path to the output initial discharge NetCDF file.

    Returns
    -------
    None

    Examples
    --------
    >>> Qex_ncf = "./input/Sandbox/Qex_Sandbox_19700101_19700110_TR.nc4"
    >>> Q00_ncf = "./input/Sandbox/Q00_Sandbox_19700101_19700110_tst.nc4"
    >>> coldinit(Qex_ncf, Q00_ncf)
    >>> import netCDF4
    >>> e = netCDF4.Dataset(Q00_ncf, "r")
    >>> e.variables["Qout"][0, :].filled()
    array([0., 0., 0., 0., 0.])
    >>> e.close()
    >>> import os
    >>> os.remove(Q00_ncf)
    """

    # -------------------------------------------------------------------------
    # Overwrite protection
    # -------------------------------------------------------------------------
    if os.path.exists(Q00_ncf):
        raise FileExistsError(f"File already exists: {Q00_ncf}")

    # -------------------------------------------------------------------------
    # Open external inflow file
    # -------------------------------------------------------------------------
    try:
        f = netCDF4.Dataset(Qex_ncf, "r")
    except IOError as err:
        raise IOError(f"Unable to open {Qex_ncf}") from err

    # -------------------------------------------------------------------------
    # Get metadata from external inflow file
    # -------------------------------------------------------------------------
    if "rivid" not in f.variables:
        raise ValueError(f"rivid variable does not exist in {Qex_ncf}")

    if "lon" not in f.variables:
        raise ValueError(f"lon variable does not exist in {Qex_ncf}")

    if "lat" not in f.variables:
        raise ValueError(f"lat variable does not exist in {Qex_ncf}")

    if "time" not in f.variables:
        raise ValueError(f"time variable does not exist in {Qex_ncf}")

    IV_riv_tot = f.variables["rivid"][:]
    ZV_lon_tot = f.variables["lon"][:]
    ZV_lat_tot = f.variables["lat"][:]

    IV_tim_all = f.variables["time"][:]

    # -------------------------------------------------------------------------
    # Create initial discharge file
    # -------------------------------------------------------------------------
    prep_Qfi_ncf(IV_riv_tot, ZV_lon_tot, ZV_lat_tot, Q00_ncf)

    try:
        e = netCDF4.Dataset(Q00_ncf, "a")
    except IOError as err:
        raise IOError(f"Unable to open {Q00_ncf}") from err

    e.variables["time"][0] = IV_tim_all[0]
    e.variables["Qout"][0, :] = 0

    # -------------------------------------------------------------------------
    # Copy global attributes
    # -------------------------------------------------------------------------
    e.setncattr("title", f.getncattr("title"))
    e.setncattr("institution", f.getncattr("institution"))

    # -------------------------------------------------------------------------
    # Close files
    # -------------------------------------------------------------------------
    e.close()
    f.close()


# *****************************************************************************
# End
# *****************************************************************************
