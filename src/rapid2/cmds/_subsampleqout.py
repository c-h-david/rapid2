#!/usr/bin/env python3
# *****************************************************************************
# _subsampleqout.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


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
            "Spatially and temporally sub-sample a discharge output (Qou) "
            "file to create model equivalents (Qme) for observations."
        ),
        epilog=(
            "examples:\n"
            "  subsampleqout "
            "--outflow input/Sandbox/Qou_Sandbox.nc4 "
            "--observations input/Sandbox/obs_Sandbox.parquet "
            "--time_step 86400 "
            "--model_equivalent output/Sandbox/Qme_Sandbox.nc4"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    parser.add_argument(
        "-Qou",
        "--outflow",
        dest="Qou",
        metavar="OUTFLOW",
        type=str,
        required=True,
        help="specify the input Qou_ncf file",
    )

    parser.add_argument(
        "-obs",
        "--observations",
        dest="obs",
        metavar="OBSERVATIONS",
        type=str,
        required=True,
        help="specify the input obs_pqt file containing river IDs for gauges",
    )

    parser.add_argument(
        "-dtO",
        "--time_step",
        dest="dtO",
        metavar="TIME_STEP",
        type=int,
        required=True,
        help="specify the observational time cadence in seconds (e.g., 86400)",
    )

    parser.add_argument(
        "-Qme",
        "--model_equivalent",
        dest="Qme",
        metavar="MODEL_EQUIVALENT",
        type=str,
        required=True,
        help="specify the output Qme_ncf file",
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    Qou_ncf = args.Qou
    obs_pqt = args.obs
    IS_dtO = np.int32(args.dtO)
    Qme_ncf = args.Qme

    print(
        f"Sub-sampling {Qou_ncf} "
        f"using {obs_pqt} "
        f"at cadence {IS_dtO}s "
        f"to create {Qme_ncf}"
    )

    # -------------------------------------------------------------------------
    # Skip if file already exists
    # -------------------------------------------------------------------------
    if os.path.exists(Qme_ncf):
        print(f"WARNING - File already exists {Qme_ncf}. Skipping.")
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Execute main logic
    # -------------------------------------------------------------------------
    try:
        prep.sample(Qou_ncf, obs_pqt, IS_dtO, Qme_ncf)
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
