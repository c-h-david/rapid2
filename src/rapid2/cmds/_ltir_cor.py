#!/usr/bin/env python3
# *****************************************************************************
# _ltir_cor.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse
import os
import sys

from rapid2 import __version__, core


# *****************************************************************************
# Main
# *****************************************************************************
def main() -> None:
    # -------------------------------------------------------------------------
    # Initialize the argument parser
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description=(
            "Apply Long-Term Inverse Routing (LTIR) scaling factors to an "
            "external inflow (Qex) file."
        ),
        epilog=(
            "examples:\n"
            "  ltir_cor --previous Qex_historic_FG.nc4 "
            "--scalar scl_historic.parquet "
            "--now Qex_historic_BC.nc4"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    parser.add_argument(
        "-prv",
        "--previous",
        dest="prv",
        metavar="PREVIOUS",
        type=str,
        required=True,
        help="specify the uncorrected input Qex_ncf file",
    )

    parser.add_argument(
        "-scl",
        "--scalar",
        dest="scl",
        metavar="SCALAR",
        type=str,
        required=True,
        help="specify the input scl_pqt scaling file",
    )

    parser.add_argument(
        "-now",
        "--now",
        dest="now",
        metavar="NOW",
        type=str,
        required=True,
        help="specify the corrected output Qex_ncf file",
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    prv_ncf = args.prv
    scl_pqt = args.scl
    now_ncf = args.now

    print(
        f"Applying LTIR scalars\n"
        f" - Previous : {prv_ncf}\n"
        f" - Scalar   : {scl_pqt}\n"
        f"   -> {now_ncf}"
    )

    # -------------------------------------------------------------------------
    # Skip if file already exists
    # -------------------------------------------------------------------------
    if os.path.exists(now_ncf):
        print(f"WARNING - File already exists {now_ncf}. Skipping.")
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Execute main logic
    # -------------------------------------------------------------------------
    try:
        core.ltir(prv_ncf, scl_pqt, now_ncf)
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
