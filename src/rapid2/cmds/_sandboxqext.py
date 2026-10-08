#!/usr/bin/env python3
# *****************************************************************************
# _sandboxqext.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse
import os
import sys

import numpy as np

from rapid2 import __version__, prep


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
            "  sandboxqext --scale 5 5 5 10 10 --average 10 10 10 "
            "20 20 --bias 0 0 0 0 0 --standard_deviation 0 0 0 0 0 "
            "--external_inflow Qext_Sandbox.nc"
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
        "-bia",
        "--bias",
        dest="bia",
        metavar="BIAS",
        type=float,
        required=False,
        nargs=5,
        default=[1e20, 1e20, 1e20, 1e20, 1e20],
        help="specify five bias error values: b1 b2 b3 b4 b5",
    )

    parser.add_argument(
        "-sdv",
        "--standard_deviation",
        dest="sdv",
        metavar="STANDARD_DEVIATION",
        type=float,
        required=False,
        nargs=5,
        default=[1e20, 1e20, 1e20, 1e20, 1e20],
        help="specify five standard deviation error values: s1 s2 s3 s4 s5",
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
    ZV_bia_tot = np.array(args.bia, dtype=np.float32)
    ZV_sdv_tot = np.array(args.sdv, dtype=np.float32)
    Qex_ncf = args.Qex

    print("Creating (from/to):")
    print(f" - {ZV_Qex_avg}")
    print(f" - {ZV_scl_tot}")
    print(f" - {Qex_ncf}")

    # -------------------------------------------------------------------------
    # Skip if file already exists
    # -------------------------------------------------------------------------
    if os.path.isfile(Qex_ncf):
        print(f"WARNING - File already exists {Qex_ncf}. Skipping.")
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Execute main logic
    # -------------------------------------------------------------------------
    try:
        prep.sandbox(
            ZV_scl_tot=ZV_scl_tot,
            ZV_Qex_avg=ZV_Qex_avg,
            Qex_ncf=Qex_ncf,
            ZV_bia_tot=ZV_bia_tot,
            ZV_sdv_tot=ZV_sdv_tot,
        )
    except (IOError, ValueError, KeyError, FileExistsError) as err:
        print(f"ERROR - {err}", file=sys.stderr)


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == "__main__":
    main()


# *****************************************************************************
# End
# *****************************************************************************
