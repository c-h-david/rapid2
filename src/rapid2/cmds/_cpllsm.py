#!/usr/bin/env python3
# *****************************************************************************
# _cpllsm.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2025


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse
import os.path
import sys

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
            "Transform Land Surface Model data into RAPID external inflow "
            "input."
        ),
        epilog=(
            "examples:\n"
            "  cpllsm "
            "--land_surface_model "
            "input/Tutorial/GLDAS_2.1_VIC_2010-01.nc4 "
            "--connectivity "
            "input/Tutorial/rapid_connect_pfaf_74.parquet "
            "--coordinates "
            "input/Tutorial/coords_pfaf_74.parquet "
            "--coupling "
            "input/Tutorial/rapid_coupling_pfaf_74_GLDAS.parquet "
            "--external_inflow "
            "input/Tutorial/Qext_GLDAS_2.1_VIC_2010-01.nc4"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    parser.add_argument(
        "-lsm",
        "--land_surface_model",
        dest="lsm",
        metavar="LAND_SURFACE_MODEL",
        type=str,
        required=True,
        help="specify the LSM file",
    )

    parser.add_argument(
        "-con",
        "--connectivity",
        dest="con",
        metavar="CONNECTIVITY",
        type=str,
        required=True,
        help="specify the connectivity file",
    )

    parser.add_argument(
        "-crd",
        "--coordinates",
        dest="crd",
        metavar="COORDINATES",
        type=str,
        required=True,
        help="specify the coordinates",
    )

    parser.add_argument(
        "-cpl",
        "--coupling",
        dest="cpl",
        metavar="COUPLING",
        type=str,
        required=True,
        help="specify the coupling file",
    )

    parser.add_argument(
        "-Qex",
        "--external_inflow",
        dest="Qex",
        metavar="EXTERNAL_INFLOW",
        type=str,
        required=True,
        help="specify the file name",
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    lsm_ncf = args.lsm
    con_pqt = args.con
    crd_pqt = args.crd
    cpl_pqt = args.cpl
    Qex_ncf = args.Qex

    print(
        f"Transforming data from  {lsm_ncf} "
        f"for {con_pqt} "
        f"with {crd_pqt} "
        f"and {cpl_pqt} "
        f"as {Qex_ncf}"
    )

    # -------------------------------------------------------------------------
    # Skip if file already exists
    # -------------------------------------------------------------------------
    if os.path.exists(Qex_ncf):
        print(f"WARNING - File already exists {Qex_ncf}. Skipping.")
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Execute main logic
    # -------------------------------------------------------------------------
    try:
        prep.couple(lsm_ncf, con_pqt, crd_pqt, cpl_pqt, Qex_ncf)
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
