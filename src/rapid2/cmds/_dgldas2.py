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

from rapid2 import __version__, pull


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
        print(f"WARNING - File already exists {lsm_ncf}. Skipping.")
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Execute main logic
    # -------------------------------------------------------------------------
    try:
        pull.gldas2(YS_phs, YS_mod, YS_tim, lsm_ncf)
        print("Done")

    except (IOError, ValueError, KeyError) as e:
        print(f"ERROR - {e}", file=sys.stderr)
        sys.exit(1)


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == "__main__":
    main()


# *****************************************************************************
# End
# *****************************************************************************
