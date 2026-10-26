#!/usr/bin/env python3
# *****************************************************************************
# gldas2.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import math
import os
import warnings

import earthaccess
import netCDF4
from tqdm import tqdm


# *****************************************************************************
# Download and Preprocess GLDAS-2
# *****************************************************************************
def gldas2(
    YS_phs: str,
    YS_mod: str,
    YS_tim: str,
    lsm_ncf: str,
) -> None:
    """Download and preprocess GLDAS-2 land surface model data.

    Downloads 3-hourly Land Surface Model (LSM) data from NASA EarthData,
    verifies file sizes, concatenates the temporal segments into a single
    NetCDF file, and normalizes the time and flux units.

    Parameters
    ----------
    YS_phs : str
        The phase number of GLDAS-2 (e.g., '2.1').
    YS_mod : str
        The land surface model used (e.g., 'VIC').
    YS_tim : str
        The target month formatted as 'yyyy-mm'.
    lsm_ncf : str
        Path to the output LSM NetCDF file.

    Returns
    -------
    None

    Examples
    --------
    >>> YS_phs = "2.1"
    >>> YS_mod = "VIC"
    >>> YS_tim = "2010-01"
    >>> lsm_ncf = "input/Tutorial/GLDAS_2.1_VIC_2010-01.nc4"
    >>> gldas2(YS_phs, YS_mod, YS_tim, lsm_ncf)  # doctest: +SKIP
    # TODO: Replace +SKIP & add chck_lsm() to validate sch, dim, and var.
    """

    # -------------------------------------------------------------------------
    # Login
    # -------------------------------------------------------------------------
    earthaccess.login()

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------
    YS_exp = "GLDAS"
    YS_res = "10"
    YS_frq = "3H"

    YS_nam = YS_exp + "_" + YS_mod + YS_res + "_" + YS_frq

    AV_rem = earthaccess.search_data(
        short_name=YS_nam,
        version=YS_phs,
        temporal=(YS_tim, YS_tim),
        count=2928,  # limiting to one year of 3-hourly out of the box
    )

    # -------------------------------------------------------------------------
    # Download
    # -------------------------------------------------------------------------
    YS_dir = os.path.dirname(lsm_ncf)

    earthaccess.download(AV_rem, YS_dir)

    # -------------------------------------------------------------------------
    # Check files
    # -------------------------------------------------------------------------
    IS_rem = len(AV_rem)
    YV_loc = []

    for JS_rem in tqdm(range(IS_rem), desc="Verifying LSM files"):
        YS_rem = AV_rem[JS_rem]["meta"]["native-id"].split(":", 1)[1]
        ZS_rem = AV_rem[JS_rem]["size"]
        tmp_ncf = os.path.join(YS_dir, YS_rem)

        if not os.path.exists(tmp_ncf):
            raise ValueError(f"file not downloaded: {tmp_ncf}")
        else:
            ZS_loc = os.path.getsize(tmp_ncf) / 1024**2
            YV_loc.append(tmp_ncf)

        # Check files
        if not math.isclose(ZS_rem, ZS_loc, abs_tol=1e-3):
            raise ValueError(
                f"Remote file {YS_rem}, "
                f"Local file {tmp_ncf}, "
                f"Remote size {ZS_rem}, "
                f"Local size {ZS_loc}"
            )

    # -------------------------------------------------------------------------
    # Concatenate files
    # -------------------------------------------------------------------------
    YV_loc = sorted(YV_loc)
    YV_yes = {"time", "time_bnds", "lon", "lat", "Qs_acc", "Qsb_acc"}

    tmp_ncf = YV_loc[0]
    try:
        with (
            netCDF4.Dataset(tmp_ncf, "r") as t,
            netCDF4.Dataset(lsm_ncf, "w") as c,
        ):
            # Copy global attributes
            c.setncatts({attr: t.getncattr(attr) for attr in t.ncattrs()})

            # Copy dimensions (time should be unlimited)
            for name, dim in t.dimensions.items():
                c.createDimension(
                    name, None if dim.isunlimited() else len(dim)
                )

            # Copy variables that are in YV_yes (and their attributes)
            for name, var in t.variables.items():
                if name in YV_yes:
                    c.createVariable(
                        name, var.datatype, var.dimensions
                    ).setncatts(
                        {attr: var.getncattr(attr) for attr in var.ncattrs()}
                    )
    except IOError as err:
        raise IOError(f"Unable to process {tmp_ncf} or {lsm_ncf}") from err

    try:
        c = netCDF4.Dataset(lsm_ncf, "a")
    except IOError as err:
        raise IOError(f"Unable to open {lsm_ncf} for appending") from err

    JS_tim = 0
    for tmp_ncf in tqdm(YV_loc, desc="Concatenating LSM files"):
        try:
            t = netCDF4.Dataset(tmp_ncf, "r")
        except IOError as err:
            raise IOError(f"Unable to process {tmp_ncf}") from err

        IS_siz = t.dimensions["time"].size
        for name, var in t.variables.items():
            if name in YV_yes:
                if "time" in var.dimensions:
                    JS_idx_beg = JS_tim
                    JS_idx_end = JS_tim + IS_siz
                    c.variables[name][JS_idx_beg:JS_idx_end] = var[:]
                else:
                    c.variables[name][:] = var[:]
        JS_tim += IS_siz
        t.close()

    c.close()

    # -------------------------------------------------------------------------
    # Update time
    # -------------------------------------------------------------------------
    try:
        with netCDF4.Dataset(lsm_ncf, "a") as c:
            if YS_phs == "2.0":
                c.variables["time"][:] = (
                    c.variables["time"][:] * 60 - 694299600
                )
                c.variables["time_bnds"][:] = (
                    c.variables["time_bnds"][:] * 60 - 694299600
                )

            if YS_phs == "2.1":
                c.variables["time"][:] = (
                    c.variables["time"][:] * 60 + 946695600
                )
                c.variables["time_bnds"][:] = (
                    c.variables["time_bnds"][:] * 60 + 946695600
                )

            c.variables[
                "time"
            ].units = "second since 1970-01-01 00:00:00 +00:00"
    except IOError as err:
        raise IOError(f"Unable to process time in {lsm_ncf}") from err

    # -------------------------------------------------------------------------
    # Convert accumulated depth to depth rate
    # -------------------------------------------------------------------------
    try:
        with netCDF4.Dataset(lsm_ncf, "a") as c:
            # 1. Calculate the exact duration of the first time step in seconds
            IS_dtE = (
                c.variables["time_bnds"][0, 1] - c.variables["time_bnds"][0, 0]
            )

            # 2. If duration is less than a month (e.g., 3-hourly is 10,800s),
            #    the GLDAS data is an accumulation and must be divided by time.
            if IS_dtE < 100000:
                # Divide data by the time step duration
                c.variables["Qs_acc"][:] = c.variables["Qs_acc"][:] / IS_dtE
                c.variables["Qsb_acc"][:] = c.variables["Qsb_acc"][:] / IS_dtE

                # Update the standard units in the netCDF metadata
                c.variables["Qs_acc"].units = "kg m-2 s-1"
                c.variables["Qsb_acc"].units = "kg m-2 s-1"
    except IOError as err:
        raise IOError(f"Unable to process rates in {lsm_ncf}") from err

    # -------------------------------------------------------------------------
    # Delete files
    # -------------------------------------------------------------------------
    for tmp_ncf in YV_loc:
        try:
            os.remove(tmp_ncf)
        except OSError as e:
            warnings.warn(
                f"Error deleting {tmp_ncf}: {e}",
                stacklevel=2,
            )


# *****************************************************************************
# End
# *****************************************************************************
