#!/usr/bin/env python3
# *****************************************************************************
# _dgldas2.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2025


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse
import os
import sys

import earthaccess
import netCDF4

from rapid2 import __version__


# *****************************************************************************
# Main
# *****************************************************************************
def main() -> None:

    # -------------------------------------------------------------------------
    # Initialize the argument parser and add valid arguments
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description=(
            "Download and preprocess GLDAS-2 land surface model data from "
            "NASA EarthData."
        ),
        epilog=(
            "examples:\n"
            "  dgldas2 --phase 2.1 --model VIC --time 2010-01 "
            "--land_surface_model "
            "input/Tutorial/GLDAS_2.1_VIC_2010-01.nc4"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    parser.add_argument(
        "-phs",
        "--phase",
        dest="phs",
        metavar="PHASE",
        type=str,
        required=True,
        help="specify the phase number",
    )

    parser.add_argument(
        "-mod",
        "--model",
        dest="mod",
        metavar="MODEL",
        type=str,
        required=True,
        help="specify the land surface model",
    )

    parser.add_argument(
        "-tim",
        "--time",
        dest="tim",
        metavar="TIME",
        type=str,
        required=True,
        help="specify the month in yyyy-mm",
    )

    parser.add_argument(
        "-lsm",
        "--land_surface_model",
        dest="lsm",
        metavar="LAND_SURFACE_MODEL",
        type=str,
        required=True,
        help="specify the LSM file name",
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    YS_phs = args.phs
    YS_mod = args.mod
    YS_tim = args.tim
    lsm_ncf = args.lsm

    print(
        f"Download data from GLDAS{YS_phs} "
        f"for {YS_mod} "
        f"and {YS_tim} "
        f"as {lsm_ncf}"
    )

    # -------------------------------------------------------------------------
    # Skip if file already exists
    # -------------------------------------------------------------------------
    if os.path.exists(lsm_ncf):
        print(f"WARNING - File already exists {lsm_ncf}. Exit without error")
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Login
    # -------------------------------------------------------------------------
    print("- Login")
    earthaccess.login()

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------
    YS_exp = "GLDAS"
    YS_res = "10"
    YS_frq = "3H"

    YS_nam = YS_exp + "_" + YS_mod + YS_res + "_" + YS_frq

    print(f"- Search {YS_nam} {YS_phs} {YS_tim} max=300")

    AV_rem = earthaccess.search_data(
        short_name=YS_nam,
        version=YS_phs,
        temporal=(YS_tim, YS_tim),
        count=300,
    )

    # -------------------------------------------------------------------------
    # Download
    # -------------------------------------------------------------------------
    print(f"- Download {len(AV_rem)} files")

    YS_dir = os.path.dirname(lsm_ncf)
    earthaccess.download(AV_rem, YS_dir)

    # -------------------------------------------------------------------------
    # Check files
    # -------------------------------------------------------------------------
    print("- Check files")

    IS_rem = len(AV_rem)

    YV_loc = []
    for JS_rem in range(IS_rem):
        YS_rem = AV_rem[JS_rem]["meta"]["native-id"].split(":", 1)[1]
        ZS_rem = AV_rem[JS_rem]["size"]
        tmp_ncf = os.path.join(YS_dir, YS_rem)

        if not os.path.exists(tmp_ncf):
            print(f"ERROR - file not downloaded: {tmp_ncf}")
            sys.exit(1)
        else:
            ZS_loc = os.path.getsize(tmp_ncf) / 1024**2
            YV_loc.append(tmp_ncf)

        if abs(ZS_rem - ZS_loc) >= 1e-15:
            print(
                f"ERROR - "
                f"Remote file {YS_rem}, "
                f"Local file {tmp_ncf}, "
                f"Remote size {ZS_rem}, "
                f"Local size {ZS_loc}"
            )
            sys.exit(1)

    # -------------------------------------------------------------------------
    # Concatenate files
    # -------------------------------------------------------------------------
    print("- Concatenate file")

    YV_loc = sorted(YV_loc)
    YV_yes = {"time", "time_bnds", "lon", "lat", "Qs_acc", "Qsb_acc"}

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Open first file to create the output structure
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    tmp_ncf = YV_loc[0]
    with (
        netCDF4.Dataset(tmp_ncf, "r") as t,
        netCDF4.Dataset(lsm_ncf, "w") as c,
    ):
        # Copy global attributes
        c.setncatts({attr: t.getncattr(attr) for attr in t.ncattrs()})

        # Copy dimensions (time should be unlimited)
        for name, dim in t.dimensions.items():
            c.createDimension(name, None if dim.isunlimited() else len(dim))

        # Copy variables that are in YV_yes (and their attributes)
        for name, var in t.variables.items():
            if name in YV_yes:
                c.createVariable(name, var.datatype, var.dimensions).setncatts(
                    {attr: var.getncattr(attr) for attr in var.ncattrs()}
                )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Append data from all files
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    JS_tim = 0
    for tmp_ncf in YV_loc:
        with (
            netCDF4.Dataset(tmp_ncf, "r") as t,
            netCDF4.Dataset(lsm_ncf, "a") as c,
        ):
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

    # -------------------------------------------------------------------------
    # Update time
    # -------------------------------------------------------------------------
    with netCDF4.Dataset(lsm_ncf, "a") as c:
        if YS_phs == "2.0":
            c.variables["time"][:] = c.variables["time"][:] * 60 - 694299600
            c.variables["time_bnds"][:] = (
                c.variables["time_bnds"][:] * 60 - 694299600
            )

        if YS_phs == "2.1":
            c.variables["time"][:] = c.variables["time"][:] * 60 + 946695600
            c.variables["time_bnds"][:] = (
                c.variables["time_bnds"][:] * 60 + 946695600
            )

        c.variables["time"].units = "second since 1970-01-01 00:00:00 +00:00"

    # -------------------------------------------------------------------------
    # Convert accumulated depth to depth rate
    # -------------------------------------------------------------------------
    print("- Convert accumulated depth to depth rate")

    with netCDF4.Dataset(lsm_ncf, "a") as c:
        # 1. Calculate the exact duration of the first time step in seconds
        IS_dtE = (
            c.variables["time_bnds"][0, 1] - c.variables["time_bnds"][0, 0]
        )

        # 2. If the duration is less than a month (e.g., 3-hourly is 10,800s),
        #    the GLDAS data is an accumulation and must be divided by time.
        if IS_dtE < 100000:
            print(f"  . Dividing accumulations by IS_dtE: {IS_dtE} seconds")

            # Divide data by the time step duration
            c.variables["Qs_acc"][:] = c.variables["Qs_acc"][:] / IS_dtE
            c.variables["Qsb_acc"][:] = c.variables["Qsb_acc"][:] / IS_dtE

            # Update the standard units in the netCDF metadata
            c.variables["Qs_acc"].units = "kg m-2 s-1"
            c.variables["Qsb_acc"].units = "kg m-2 s-1"
        else:
            print("  . Data appears to be monthly; assuming flux units.")

    # -------------------------------------------------------------------------
    # Delete files
    # -------------------------------------------------------------------------
    print("- Delete files")

    for tmp_ncf in YV_loc:
        try:
            os.remove(tmp_ncf)
        except OSError as e:
            print(f"Error deleting {tmp_ncf}: {e}")


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == "__main__":
    main()


# *****************************************************************************
# End
# *****************************************************************************
