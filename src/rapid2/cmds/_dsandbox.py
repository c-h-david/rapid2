#!/usr/bin/env python3
# *****************************************************************************
# _dsandbox.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse
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
            "Download all files for the RAPID Sandbox synthetic experiment. "
            "Files are saved to input/Sandbox/ and output/Sandbox/ in the "
            "current working directory."
        ),
        epilog=("examples:\n  dsandbox\n"),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    parser.add_argument(
        "-tgt",
        "--target_directory",
        dest="tgt",
        metavar="TARGET_DIRECTORY",
        type=str,
        required=False,
        default=".",
        help="specify the target directory (defaults to current directory)",
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()
    YS_tgt = args.tgt

    # -------------------------------------------------------------------------
    # Publication message
    # -------------------------------------------------------------------------
    print("********************")
    print("Downloading files from:   https://doi.org/10.5281/zenodo.23044811")
    print("These are under a Creative Commons Attribution (CC BY) license.")
    print("Please cite the DOI if using these files for your publications.")
    print("********************")

    # -------------------------------------------------------------------------
    # Execute main logic
    # -------------------------------------------------------------------------
    try:
        print(f"- Downloading files to {YS_tgt}...")
        pull.sandbox(YS_tgt)
        print("Done")

    except Exception as e:
        print(f"ERROR - Problem downloading files: {e}", file=sys.stderr)
        sys.exit(1)


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == "__main__":
    main()


# *****************************************************************************
# End
# *****************************************************************************
