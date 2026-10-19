#!/usr/bin/env python3
# *****************************************************************************
# _hydrographs.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse
import sys
from pathlib import Path

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
            "Plot hydrographs comparing observations (Qob) to model "
            "equivalents (Qme) and save as individual SVG files."
        ),
        epilog=(
            "examples:\n"
            "  hydrographs "
            "--observations input/Sandbox/"
            "Qob_Sandbox_19700101_19700110_TR.nc4 "
            "--model_equivalent output/Sandbox/"
            "Qme_Sandbox_19700101_19700110_OL.nc4 "
            "--hyd_svg output/Sandbox/hyd.svg"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
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
        "-Qme",
        "--model_equivalent",
        dest="Qme",
        metavar="MODEL_EQUIVALENT",
        type=str,
        required=True,
        help="specify the input Qme_ncf file",
    )

    parser.add_argument(
        "-max",
        "--maximum",
        dest="max",
        metavar="MAXIMUM",
        type=float,
        required=True,
        help="specify a maximum value for the y-axis to standardize scales",
    )

    parser.add_argument(
        "-hyd",
        "--hyd_svg",
        dest="hyd",
        metavar="HYD_SVG",
        type=str,
        required=True,
        help="specify the output SVG file (e.g., hyd.svg), which will be "
        "modified to append river IDs (e.g., hyd_10.svg)",
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    Qob_ncf = args.Qob
    Qme_ncf = args.Qme
    hyd_svg = args.hyd
    ZS_Qou_max = args.max

    trg_dir = str(Path(hyd_svg).parent)
    YS_hyd_tmp = str(Path(hyd_svg).stem)

    print("Plotting hydrographs (from/to):")
    print(f" - {Qob_ncf}")
    print(f" - {Qme_ncf}")
    print(f"   -> {Path(trg_dir) / f'{YS_hyd_tmp}_<rivid>.svg'}")

    # -------------------------------------------------------------------------
    # Execute main logic
    # -------------------------------------------------------------------------
    try:
        eval.graph(Qob_ncf, Qme_ncf, ZS_Qou_max, hyd_svg)
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
