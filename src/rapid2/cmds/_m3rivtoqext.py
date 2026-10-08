#!/usr/bin/env python3
# *****************************************************************************
# _m3rivtoqext.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse
import os
import sys

from rapid2 import __version__, v1v2


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
            "  m3rivtoqext --inflow_volume m3_riv_San_Guad.nc4 "
            "--external_inflow Qext_San_Guad.nc4"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    parser.add_argument(
        "-m3r",
        "--external_volume",
        dest="m3r",
        metavar="EXTERNAL_VOLUME",
        type=str,
        required=True,
        help="specify the input m3_riv file",
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

    m3r_ncf = args.m3r
    Qex_ncf = args.Qex

    print("Converting (from/to):")
    print(f" - {m3r_ncf}")
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
        v1v2.inflow(m3r_ncf, Qex_ncf)
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
