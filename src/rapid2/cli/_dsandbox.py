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
    print("Downloading files from:   https://doi.org/10.5281/zenodo.23044811")
    print("These are under a Creative Commons Attribution (CC BY) license.")
    print("Please cite the DOI if using these files for your publications.")
    print("********************")

    # -------------------------------------------------------------------------
    # Location of the dataset
    # -------------------------------------------------------------------------
    doi = "doi:10.5281/zenodo.23044811/"

    # -------------------------------------------------------------------------
    # Execute main logic
    # -------------------------------------------------------------------------
    try:
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Download input files
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        files = [
            "bas_Sandbox_ascend.parquet",
            "con_Sandbox.parquet",
            "cpl_Sandbox.parquet",
            "crd_Sandbox.parquet",
            "kpr_Sandbox.parquet",
            "nml_Sandbox_BC.yml",
            "nml_Sandbox_DA.yml",
            "nml_Sandbox_OL.yml",
            "nml_Sandbox_HY.yml",
            "nml_Sandbox_TR.yml",
            "obs_Sandbox.parquet",
            "Q00_Sandbox_19700101_19700110_FG.nc4",
            "Q00_Sandbox_19700101_19700110_TR.nc4",
            "Qex_Sandbox_19700101_19700110_BC.nc4",
            "Qex_Sandbox_19700101_19700110_FG.nc4",
            "Qex_Sandbox_19700101_19700110_TR.nc4",
            "Qob_Sandbox_19700101_19700110_TR.nc4",
            "scl_Sandbox.parquet",
            "xpr_Sandbox.parquet",
        ]

        fetcher = pooch.create(
            path=Path("input/Sandbox"),
            base_url=doi,
            registry={f: None for f in files},
        )

        print("- Downloading input files...")
        for file in files:
            fetcher.fetch(file)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Download output files
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        files = [
            "Qfi_Sandbox_19700101_19700110_BC.nc4",
            "Qfi_Sandbox_19700101_19700110_DA.nc4",
            "Qfi_Sandbox_19700101_19700110_HY.nc4",
            "Qfi_Sandbox_19700101_19700110_OL.nc4",
            "Qfi_Sandbox_19700101_19700110_TR.nc4",
            "Qme_Sandbox_19700101_19700110_BC.nc4",
            "Qme_Sandbox_19700101_19700110_DA.nc4",
            "Qme_Sandbox_19700101_19700110_HY.nc4",
            "Qme_Sandbox_19700101_19700110_OL.nc4",
            "Qou_Sandbox_19700101_19700110_BC.nc4",
            "Qou_Sandbox_19700101_19700110_DA.nc4",
            "Qou_Sandbox_19700101_19700110_HY.nc4",
            "Qou_Sandbox_19700101_19700110_OL.nc4",
            "Qou_Sandbox_19700101_19700110_TR.nc4",
        ]

        fetcher = pooch.create(
            path=Path("output/Sandbox"),
            base_url=doi,
            registry={f: None for f in files},
        )

        print("- Downloading output files...")
        for file in files:
            fetcher.fetch(file)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # End
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
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
