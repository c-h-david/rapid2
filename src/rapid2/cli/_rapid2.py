#!/usr/bin/env python3
# *****************************************************************************
# _rapid2.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import sys

from rapid2 import __version__
from rapid2.cli import _cmpncf, _run


# *****************************************************************************
# Main
# *****************************************************************************
def main() -> None:
    # -------------------------------------------------------------------------
    # Provide base help if no arguments are passed
    # -------------------------------------------------------------------------
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help", "--version"]:
        print(f"RAPID2 {__version__} - Unified Command Line Interface")
        print("\nUsage: rapid2 <group> <command> [options]")
        print("\nAvailable commands:")
        print("  run            Execute the core matrix-based routing model")
        print("  comp netcdf    Compare NetCDF outputs for regression")
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Parse the group and command
    # -------------------------------------------------------------------------
    YS_grp = sys.argv[1]
    YS_cmd = sys.argv[2] if len(sys.argv) > 2 else ""

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 run
    # -------------------------------------------------------------------------
    if YS_grp == "run":
        # Rewrite sys.argv so argparse prints the correct usage string
        sys.argv = ["rapid2 run"] + sys.argv[2:]
        _run.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 comp netcdf
    # -------------------------------------------------------------------------
    elif YS_grp == "comp" and YS_cmd == "netcdf":
        # Rewrite sys.argv so argparse prints the correct usage string
        sys.argv = ["rapid2 comp netcdf"] + sys.argv[3:]
        _cmpncf.main()

    # -------------------------------------------------------------------------
    # Handle unknown commands
    # -------------------------------------------------------------------------
    else:
        YS_err = f"{YS_grp} {YS_cmd}".strip()
        print(f"ERROR - Unknown command: rapid2 {YS_err}", file=sys.stderr)
        sys.exit(1)


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == "__main__":
    main()


# *****************************************************************************
# End
# *****************************************************************************
