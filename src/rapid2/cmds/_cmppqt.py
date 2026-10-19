#!/usr/bin/env python3
# *****************************************************************************
# _cmppqt.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse
import sys

import numpy as np

from rapid2 import __version__, eval


# *****************************************************************************
# Main
# *****************************************************************************
def main() -> None:

    # -------------------------------------------------------------------------
    # Initialize the argument parser and add valid arguments
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description=(
            "Compare RAPID input/output Parquet files for numerical "
            "regression testing."
        ),
        epilog=(
            "examples:\n"
            "  cmppqt "
            "--previous "
            "input/Sandbox/kpr_Sandbox.parquet "
            "--now "
            "input/Sandbox/kpr_Sandbox.parquet "
            "--relative_tolerance 1e-6 "
            "--absolute_tolerance 1e-3"
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
        help="specify the old Parquet file",
    )

    parser.add_argument(
        "-now",
        "--now",
        dest="now",
        metavar="NOW",
        type=str,
        required=True,
        help="specify the new Parquet file",
    )

    parser.add_argument(
        "-rtl",
        "--relative_tolerance",
        dest="rtl",
        metavar="RELATIVE_TOLERANCE",
        type=str,
        required=False,
        default="0",
        help="specify the relative tolerance",
    )

    parser.add_argument(
        "-atl",
        "--absolute_tolerance",
        dest="atl",
        metavar="ABSOLUTE_TOLERANCE",
        type=str,
        required=False,
        default="0",
        help="specify the absolute tolerance",
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    prv_pqt = args.prv
    now_pqt = args.now
    YS_rtl = args.rtl
    YS_atl = args.atl

    print(
        f"Comparing {prv_pqt} "
        f"with {now_pqt} "
        f"relative tolerance {YS_rtl} "
        f"absolute tolerance {YS_atl}"
    )

    ZS_rtl = np.float64(YS_rtl)
    ZS_atl = np.float64(YS_atl)

    # -------------------------------------------------------------------------
    # Execute main logic
    # -------------------------------------------------------------------------
    try:
        eval.cmppqt(prv_pqt, now_pqt, ZS_rtl, ZS_atl)
        print("Parquet files similar!!!")
        print("-------------------------------")

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
