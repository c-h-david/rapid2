#!/usr/bin/env python3
# *****************************************************************************
# _ltir_scl.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


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
    # Initialize the argument parser
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description=(
            "Compute Long-Term Inverse Routing (LTIR) scaling factors for "
            "external inflows using gauge observations."
        ),
        epilog=(
            "examples:\n"
            "  ltir_scl --connectivity con_Sandbox.parquet "
            "--basin bas_Sandbox_ascend.parquet "
            "--external_inflow Qex_historic.nc4 "
            "--observations Qob_historic.nc4 "
            "--scalar scl_historic.parquet"
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
        help="specify the input con_pqt file",
    )

    parser.add_argument(
        "-bas",
        "--basin",
        dest="bas",
        metavar="BASIN",
        type=str,
        required=True,
        help="specify the input bas_pqt file",
    )

    parser.add_argument(
        "-Qex",
        "--external_inflow",
        dest="Qex",
        metavar="EXTERNAL_INFLOW",
        type=str,
        required=True,
        help="specify the input Qex_ncf file",
    )

    parser.add_argument(
        "-Qob",
        "--observations",
        dest="Qob",
        metavar="OBSERVATIONS",
        type=str,
        required=True,
        help="specify the input Qob_ncf file",
    )

    parser.add_argument(
        "-scl",
        "--scalar",
        dest="scl",
        metavar="SCALAR",
        type=str,
        required=True,
        help="specify the output scl_pqt file",
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    con_pqt = args.con
    bas_pqt = args.bas
    Qex_ncf = args.Qex
    Qob_ncf = args.Qob
    scl_pqt = args.scl

    # -------------------------------------------------------------------------
    # Skip if file already exists
    # -------------------------------------------------------------------------
    if os.path.exists(scl_pqt):
        print(f"WARNING - File already exists {scl_pqt}. Skipping.")
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Execute main logic
    # -------------------------------------------------------------------------
    try:
        prep.ltir(con_pqt, bas_pqt, Qex_ncf, Qob_ncf, scl_pqt)
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
