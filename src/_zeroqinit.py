#!/usr/bin/env python3
# *****************************************************************************
# _zeroqinit.py
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
from rapid2.Qfi_new import Qfi_new


# *****************************************************************************
# Main
# *****************************************************************************
def main() -> None:

    # -------------------------------------------------------------------------
    # Initialize the argument parser and add valid arguments
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description=(
            "Create an initial discharge file with zero values for cold start "
            "of model."
        ),
        epilog=(
            "examples:\n"
            "  zeroqinit -i Qext_file.nc -o Qinit_zeros.nc\n"
            "  zeroqinit --input Qext.nc --output Qinit.nc"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="specify the input Qext file",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="specify the output Qinit file",
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    Qex_ncf = args.input
    Q00_ncf = args.output

    print("Creating (from/to):")
    print(f" - {Qex_ncf}")
    print(f" - {Q00_ncf}")

    # -------------------------------------------------------------------------
    # Skip if file already exists
    # -------------------------------------------------------------------------
    if os.path.isfile(Q00_ncf):
        print(f"WARNING - File already exists {Q00_ncf}. Exit without error")
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Get metadata from m3_riv file
    # -------------------------------------------------------------------------
    f = netCDF4.Dataset(Qex_ncf, "r")

    if "rivid" not in f.variables:
        print(f"ERROR - rivid variable does not exist in {Qex_ncf}")
        sys.exit(1)

    if "lon" not in f.variables:
        print(f"ERROR - lon variable does not exist in {Qex_ncf}")
        sys.exit(1)

    if "lat" not in f.variables:
        print(f"ERROR - lat variable does not exist in {Qex_ncf}")
        sys.exit(1)

    if "time" not in f.variables:
        print(f"ERROR - time variable does not exist in {Qex_ncf}")
        sys.exit(1)

    IV_Qex_tot = f.variables["rivid"][:]
    ZV_lon_tot = f.variables["lon"][:]
    ZV_lat_tot = f.variables["lat"][:]

    IV_Qex_tim = f.variables["time"][:]

    # -------------------------------------------------------------------------
    # Create Qfi file
    # -------------------------------------------------------------------------
    Qfi_new(IV_Qex_tot, ZV_lon_tot, ZV_lat_tot, Q00_ncf)

    e = netCDF4.Dataset(Q00_ncf, "a")

    time = e.variables["time"]
    time[0] = IV_Qex_tim[0]

    Q00 = e.variables["Qout"]
    Q00[0, :] = 0

    # -------------------------------------------------------------------------
    # Copy some global attributes
    # -------------------------------------------------------------------------
    e.setncattr("title", f.getncattr("title"))
    e.setncattr("institution", f.getncattr("institution"))

    # -------------------------------------------------------------------------
    # Close files
    # -------------------------------------------------------------------------
    e.close()
    f.close()


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == "__main__":
    main()


# *****************************************************************************
# End
# *****************************************************************************
