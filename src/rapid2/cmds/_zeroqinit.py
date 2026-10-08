#!/usr/bin/env python3
# *****************************************************************************
# _zeroqinit.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse
import os
import sys

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
            "Create an initial discharge file with zero values for cold start "
            "of model."
        ),
        epilog=(
            "examples:\n"
            "  zeroqinit "
            "--external_inflow "
            "input/Tutorial/Qext_GLDAS_2.1_VIC_2010-01.nc4 "
            "--initial_outflow "
            "input/Tutorial/Qinit_GLDAS_2.1_VIC_2010-01.nc4"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    parser.add_argument(
        "-Qex",
        "--external_inflow",
        dest="Qex",
        metavar="EXTERNAL_INFLOW",
        type=str,
        required=True,
        help="specify the input Qext file",
    )

    parser.add_argument(
        "-Q00",
        "--initial_outflow",
        dest="Q00",
        metavar="INITIAL_OUTFLOW",
        type=str,
        required=True,
        help="specify the output Qinit file",
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    Qex_ncf = args.Qex
    Q00_ncf = args.Q00

    print("Creating (from/to):")
    print(f" - {Qex_ncf}")
    print(f" - {Q00_ncf}")

    # -------------------------------------------------------------------------
    # Skip if file already exists
    # -------------------------------------------------------------------------
    if os.path.isfile(Q00_ncf):
        print(f"WARNING - File already exists {Q00_ncf}. Skipping.")
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Execute main logic
    # -------------------------------------------------------------------------
    try:
        prep.coldinit(Qex_ncf, Q00_ncf)
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
