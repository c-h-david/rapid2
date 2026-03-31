#!/usr/bin/env python3
# *****************************************************************************
# _sandboxqext.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2025


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse
import os
import sys

import netCDF4
import numpy as np

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
            "Generate synthetic external inflow data for the RAPID Sandbox."
        ),
        epilog=(
            "examples:\n"
            "  sandboxqext --scale 1 1 1 2 2 --average 10 10 10 "
            "20 20 --external_inflow Qext_Sandbox.nc"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    parser.add_argument(
        "-scl",
        "--scale",
        dest="scl",
        metavar="SCALE",
        type=float,
        required=True,
        nargs=5,
        help="specify five unit-amplitude scaling values: s1 s2 s3 s4 s5",
    )

    parser.add_argument(
        "-avg",
        "--average",
        dest="avg",
        metavar="AVERAGE",
        type=float,
        required=True,
        nargs=5,
        help="specify five average values: a1 a2 a3 a4 a5",
    )

    parser.add_argument(
        "-Qex",
        "--external_inflow",
        dest="Qex",
        metavar="EXTERNAL_INFLOW",
        type=str,
        required=True,
        help="specify the output Qext file",
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    ZV_Qex_avg = np.array(args.avg, dtype=np.float32)
    ZV_scl_tot = np.array(args.scl, dtype=np.float32)
    Qex_ncf = args.Qex

    print("Creating (from/to):")
    print(f" - {ZV_Qex_avg}")
    print(f" - {ZV_scl_tot}")
    print(f" - {Qex_ncf}")

    # -------------------------------------------------------------------------
    # Skip if file already exists
    # -------------------------------------------------------------------------
    if os.path.isfile(Qex_ncf):
        print(f"WARNING - File already exists {Qex_ncf}. Exit without error")
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Hardcoded Sandbox values
    # -------------------------------------------------------------------------
    IV_riv_tot = np.array([10, 20, 30, 40, 50], dtype=np.int32)
    ZV_lon_tot = np.array([4.30, 5.94, 5.12, 6.55, 4.30])
    ZV_lat_tot = np.array([8.20, 8.20, 5.12, 4.30, 2.04])
    IV_tim_all = np.array(range(80), dtype=np.int32) * np.int32(10800)

    # -------------------------------------------------------------------------
    # Array sizes
    # -------------------------------------------------------------------------
    IS_riv_tot = len(IV_riv_tot)
    IS_tim_all = len(IV_tim_all)

    # -------------------------------------------------------------------------
    # Check size of provided unit-amplitude scaling and average arrays
    # -------------------------------------------------------------------------
    if len(ZV_scl_tot) != IS_riv_tot:
        print("ERROR - Unit-amplitude scaling array not of size 5.")
        sys.exit(1)

    if len(ZV_Qex_avg) != IS_riv_tot:
        print("ERROR - Average array not of size 5.")
        sys.exit(1)

    # -------------------------------------------------------------------------
    # Create Qext file
    # -------------------------------------------------------------------------
    prep_Qex_ncf(IV_riv_tot, ZV_lon_tot, ZV_lat_tot, Qex_ncf)

    # -------------------------------------------------------------------------
    # Populate Qext file
    # -------------------------------------------------------------------------
    f = netCDF4.Dataset(Qex_ncf, "a")

    f.variables["time"][:] = IV_tim_all[:]

    f.variables["time_bnds"][:, 0] = IV_tim_all[:]
    f.variables["time_bnds"][:, 1] = IV_tim_all[:] + np.int32(10800)

    for JS_tim_all in range(IS_tim_all):
        ZV_Qex_tmp = np.sign(
            np.sin(np.pi / 86400 * IV_tim_all[JS_tim_all] + 1e-7)
        )
        ZV_Qex_tmp = ZV_Qex_tmp * ZV_scl_tot
        ZV_Qex_tmp = ZV_Qex_tmp + ZV_Qex_avg
        f.variables["Qext"][JS_tim_all, :] = ZV_Qex_tmp[:]
    # The 1e-7 avoids np.sign(0) = 0

    f.title = "Sandbox dataset for RAPID2"
    f.institution = (
        "Jet Propulsion Laboratory, California Institute of Technology"
    )

    # -------------------------------------------------------------------------
    # Close file
    # -------------------------------------------------------------------------
    f.close()


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == "__main__":
    main()


# *****************************************************************************
# End
# *****************************************************************************
