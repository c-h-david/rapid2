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
from pathlib import Path

import pooch  # type: ignore[import-untyped]

from rapid2 import __version__


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

    # -------------------------------------------------------------------------
    # Publication message
    # -------------------------------------------------------------------------
    print("********************")
    print("Downloading files from:   https://doi.org/10.5281/zenodo.21085813")
    print("These are under a Creative Commons Attribution (CC BY) license.")
    print("Please cite the DOI if using these files for your publications.")
    print("********************")

    # -------------------------------------------------------------------------
    # Location of the dataset
    # -------------------------------------------------------------------------
    doi = "doi:10.5281/zenodo.21085813/"

    # -------------------------------------------------------------------------
    # Download input files
    # -------------------------------------------------------------------------
    files = [
        "con_Sandbox.parquet",
        "Qex_Sandbox_19700101_19700110_TR.nc4",
        "Q00_Sandbox_19700101_19700110_TR.nc4",
        "kpr_Sandbox.parquet",
        "xpr_Sandbox.parquet",
        "bas_Sandbox_ascend.parquet",
        "nml_Sandbox.yml",
        "cpl_Sandbox.parquet",
        "crd_Sandbox.parquet",
        "obs_Sandbox.parquet",
        "Qob_Sandbox_19700101_19700110_TR.nc4",
        "Qex_Sandbox_19700101_19700110_FG.nc4",
        "Q00_Sandbox_19700101_19700110_FG.nc4",
    ]

    fetcher = pooch.create(
        path=Path("input/Sandbox"),
        base_url=doi,
        registry={f: None for f in files},
    )

    try:
        print("- Downloading input files...")
        for file in files:
            fetcher.fetch(file)
    except Exception as e:
        print(f"ERROR - Problem downloading files: {e}", file=sys.stderr)
        sys.exit(44)

    # -------------------------------------------------------------------------
    # Download output files
    # -------------------------------------------------------------------------
    files = [
        "Qou_Sandbox_19700101_19700110_TR.nc4",
        "Qfi_Sandbox_19700101_19700110_TR.nc4",
        "Qou_Sandbox_19700101_19700110_OL.nc4",
        "Qfi_Sandbox_19700101_19700110_OL.nc4",
    ]

    fetcher = pooch.create(
        path=Path("output/Sandbox"),
        base_url=doi,
        registry={f: None for f in files},
    )

    try:
        print("- Downloading output files...")
        for file in files:
            fetcher.fetch(file)
    except Exception as e:
        print(f"ERROR - Problem downloading files: {e}", file=sys.stderr)
        sys.exit(44)

    # -------------------------------------------------------------------------
    # End
    # -------------------------------------------------------------------------
    print("Done")
    sys.exit(0)


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == "__main__":
    main()


# *****************************************************************************
# End
# *****************************************************************************
