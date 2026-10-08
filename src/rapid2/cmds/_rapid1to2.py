#!/usr/bin/env python3
# *****************************************************************************
# _rapid1to2.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse
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
        description="Convert legacy RAPID1 files to RAPID2 files",
        epilog=(
            "examples:\n"
            "  rapid1to2 "
            "--connectivity input/Sandbox/rapid_connect.csv "
            "--basin input/Sandbox/riv_bas_id.csv"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    parser.add_argument(
        "-con",
        "--connectivity",
        dest="con",
        metavar="CONNECTIVITY",
        type=str,
        required=True,
        help="specify the legacy connectivity CSV file",
    )

    parser.add_argument(
        "-bas",
        "--basin",
        dest="bas",
        metavar="BASIN",
        type=str,
        required=False,
        help="specify the legacy basin CSV file",
    )

    parser.add_argument(
        "-kpr",
        "--k_parameter",
        dest="kpr",
        metavar="K_PARAMETER",
        type=str,
        required=False,
        help="specify the legacy k parameter CSV file",
    )

    parser.add_argument(
        "-xpr",
        "--x_parameter",
        dest="xpr",
        metavar="X_PARAMETER",
        type=str,
        required=False,
        help="specify the legacy x parameter CSV file",
    )

    parser.add_argument(
        "-crd",
        "--coordinates",
        dest="crd",
        metavar="COORDINATES",
        type=str,
        required=False,
        help="specify the legacy coordinates CSV file",
    )

    parser.add_argument(
        "-cpl",
        "--coupling",
        dest="cpl",
        metavar="COUPLING",
        type=str,
        required=False,
        help="specify the legacy coupling CSV file",
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    con_csv = args.con
    bas_csv = args.bas
    kpr_csv = args.kpr
    xpr_csv = args.xpr
    crd_csv = args.crd
    cpl_csv = args.cpl

    print("Converting legacy files (from/to):")

    # -------------------------------------------------------------------------
    # Execute main logic
    # -------------------------------------------------------------------------
    try:
        v1v2.static(
            con_csv=con_csv,
            bas_csv=bas_csv,
            kpr_csv=kpr_csv,
            xpr_csv=xpr_csv,
            crd_csv=crd_csv,
            cpl_csv=cpl_csv,
        )
        print("Conversion complete.")

    except (IOError, ValueError, KeyError, FileExistsError) as err:
        print(f"ERROR - {err}", file=sys.stderr)
         sys.exit(1)


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == "__main__":
    main()


# *****************************************************************************
# End
# *****************************************************************************
