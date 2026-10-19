#!/usr/bin/env python3
# *****************************************************************************
# _run.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2025


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse
import os
import sys

from rapid2 import __version__, base, core


# *****************************************************************************
# Main
# *****************************************************************************
def main() -> None:
    # -------------------------------------------------------------------------
    # Initialize the argument parser and add valid arguments
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description=(
            "Routing Application for Programmed Integration of Discharge "
            "(RAPID)."
        ),
        epilog=(
            "examples:\n"
            "  run --namelist input/Sandbox/nml_Sandbox_OL.yml\n"
            "  run --namelist input/Sandbox/nml_Sandbox_TR.yml\n"
            "\n"
            "citation:\n"
            "  If using RAPID2, please cite:\n"
            "  https://doi.org/10.1175/2011JHM1345.1\n"
            "  See CITATION.cff for full citation details."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    parser.add_argument(
        "-nml",
        "--namelist",
        dest="nml",
        metavar="NAMELIST",
        type=str,
        required=True,
        help="specify the namelist file",
    )

    # -------------------------------------------------------------------------
    # Show help if no arguments provided
    # -------------------------------------------------------------------------
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    nml_yml = args.nml

    print(f"Namelist file: {nml_yml}")

    # -------------------------------------------------------------------------
    # Execute main logic
    # -------------------------------------------------------------------------
    try:
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Read namelist into a dictionary and assign to local variables
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        AT_nml = base.read_nml_tbl(nml_yml)

        Q00_ncf = AT_nml["Q00_ncf"]
        Qex_ncf = AT_nml["Qex_ncf"]

        con_pqt = AT_nml["con_pqt"]
        kpr_pqt = AT_nml["kpr_pqt"]
        xpr_pqt = AT_nml["xpr_pqt"]

        bas_pqt = AT_nml["bas_pqt"]

        IS_dtR = AT_nml["IS_dtR"]

        Qou_ncf = AT_nml["Qou_ncf"]
        Qfi_ncf = AT_nml["Qfi_ncf"]

        Qob_ncf = None
        ZS_scl_inf = None
        ZS_scl_sdv = None
        ZS_lkm_cov = None

        if "Qob_ncf" in AT_nml:
            Qob_ncf = AT_nml["Qob_ncf"]
            ZS_scl_inf = AT_nml["ZS_scl_inf"]
            ZS_scl_sdv = AT_nml["ZS_scl_sdv"]
            ZS_lkm_cov = AT_nml["ZS_lkm_cov"]

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Skip if file already exists
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if os.path.exists(Qou_ncf):
            print(f"WARNING - File already exists {Qou_ncf}. Skipping.")
            sys.exit(0)

        if os.path.exists(Qfi_ncf):
            print(f"WARNING - File already exists {Qfi_ncf}. Skipping.")
            sys.exit(0)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Execute core function
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        core.run(
            Q00_ncf,
            Qex_ncf,
            con_pqt,
            kpr_pqt,
            xpr_pqt,
            bas_pqt,
            IS_dtR,
            Qou_ncf,
            Qfi_ncf,
            Qob_ncf,
            ZS_scl_inf,
            ZS_scl_sdv,
            ZS_lkm_cov,
        )
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
