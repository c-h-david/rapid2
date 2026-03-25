#!/usr/bin/env python3
# *****************************************************************************
# _m3rivtoqext.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2025


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse
import os
import sys

import netCDF4  # type: ignore[import-untyped]

from rapid2 import __version__
from rapid2.prep_Qex_ncf import prep_Qex_ncf


# *****************************************************************************
# Main
# *****************************************************************************
def main() -> None:

    # -------------------------------------------------------------------------
    # Initialize the argument parser and add valid arguments
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description=(
            "Convert external inflow volume (m3_riv) to external inflow "
            "rate (Qext)."
        ),
        epilog=(
            "examples:\n"
            "  m3rivtoqext --m3r m3_riv_San_Guad.nc4 --Qex Qext_San_Guad.nc4"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    parser.add_argument(
        "--m3r",
        type=str,
        required=True,
        help="specify the input m3_riv file",
    )

    parser.add_argument(
        "--Qex",
        type=str,
        required=True,
        help="specify the output Qext file",
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    m3r_ncf = args.m3r
    Qex_ncf = args.Qex

    print("Converting (from/to):")
    print(f" - {m3r_ncf}")
    print(f" - {Qex_ncf}")

    # -------------------------------------------------------------------------
    # Skip if file already exists
    # -------------------------------------------------------------------------
    if os.path.isfile(Qex_ncf):
        print(f"WARNING - File already exists {Qex_ncf}. Exit without error")
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Get metadata from m3_riv file
    # -------------------------------------------------------------------------
    d = netCDF4.Dataset(m3r_ncf, "r")

    if "m3_riv" not in d.variables:
        print(f"ERROR - m3_riv variable does not exist in {m3r_ncf}")
        sys.exit(1)

    if "rivid" not in d.variables:
        print(f"ERROR - rivid variable does not exist in {m3r_ncf}")
        sys.exit(1)

    if "lon" not in d.variables:
        print(f"ERROR - lon variable does not exist in {m3r_ncf}")
        sys.exit(1)

    if "lat" not in d.variables:
        print(f"ERROR - lat variable does not exist in {m3r_ncf}")
        sys.exit(1)

    if "time" not in d.variables:
        print(f"ERROR - time variable does not exist in {m3r_ncf}")
        sys.exit(1)

    if "time_bnds" not in d.variables:
        print(f"ERROR - time_bnds variable does not exist in {m3r_ncf}")
        sys.exit(1)

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
    print(f"The transformation will divide by the value: {IS_dtE}")

    prep_Qex_ncf(IV_riv_tot, ZV_lon_tot, ZV_lat_tot, Qex_ncf)

    f = netCDF4.Dataset(Qex_ncf, "a")

    f.variables["time"][:] = IV_tim_all
    f.variables["time_bnds"][:] = IM_tim_all

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
# If executed as a script
# *****************************************************************************
if __name__ == "__main__":
    main()


# *****************************************************************************
# End
# *****************************************************************************
