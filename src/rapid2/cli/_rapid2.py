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
from rapid2.cli import (
    _cmpncf,
    _cpllsm,
    _dgldas2,
    _dsandbox,
    _hydrographs,
    _ltir_cor,
    _ltir_scl,
    _m3rivtoqext,
    _rapid1to2,
    _run,
    _sandboxqext,
    _subsampleqout,
    _zeroqinit,
)


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
        print("  core run         Run the core matrix routing model")
        print("  core ltir        Apply inflow bias correction")
        print("  pull sandbox     Download Sandbox data")
        print("  pull gldas2      Download raw GLDAS2 data")
        print("  prep gldas2      Reformat GLDAS2 time and units")
        print("  prep couple      Map LSM grids to river networks")
        print("  prep sandbox     Generate synthetic inflow")
        print("  prep coldinit    Generate cold-start states")
        print("  prep sample      Align NetCDF data to gauges")
        print("  prep ltir        Compute LTIR scalars")
        print("  eval graph       Generate SVG hydrographs")
        print("  eval cmpncf      Compare NetCDF files")
        print("  v1v2 static      Upgrade RAPID1 CSV to Parquet")
        print("  v1v2 inflow      Convert volumes to flow rates")
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Parse the group and command
    # -------------------------------------------------------------------------
    YS_grp = sys.argv[1]
    YS_cmd = sys.argv[2] if len(sys.argv) > 2 else ""

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 core run
    # -------------------------------------------------------------------------
    if YS_grp == "core" and YS_cmd == "run":
        # Rewrite sys.argv so argparse prints the correct usage string
        sys.argv = ["rapid2 core run"] + sys.argv[3:]
        _run.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 core ltir
    # -------------------------------------------------------------------------
    elif YS_grp == "core" and YS_cmd == "ltir":
        sys.argv = ["rapid2 core ltir"] + sys.argv[3:]
        _ltir_cor.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 pull sandbox
    # -------------------------------------------------------------------------
    elif YS_grp == "pull" and YS_cmd == "sandbox":
        sys.argv = ["rapid2 pull sandbox"] + sys.argv[3:]
        _dsandbox.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 pull gldas2
    # -------------------------------------------------------------------------
    elif YS_grp == "pull" and YS_cmd == "gldas2":
        sys.argv = ["rapid2 pull gldas2"] + sys.argv[3:]
        _dgldas2.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 prep gldas2
    # -------------------------------------------------------------------------
    elif YS_grp == "prep" and YS_cmd == "gldas2":
        sys.argv = ["rapid2 prep gldas2"] + sys.argv[3:]
        _dgldas2.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 prep couple
    # -------------------------------------------------------------------------
    elif YS_grp == "prep" and YS_cmd == "couple":
        sys.argv = ["rapid2 prep couple"] + sys.argv[3:]
        _cpllsm.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 prep sandbox
    # -------------------------------------------------------------------------
    elif YS_grp == "prep" and YS_cmd == "sandbox":
        sys.argv = ["rapid2 prep sandbox"] + sys.argv[3:]
        _sandboxqext.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 prep coldinit
    # -------------------------------------------------------------------------
    elif YS_grp == "prep" and YS_cmd == "coldinit":
        sys.argv = ["rapid2 prep coldinit"] + sys.argv[3:]
        _zeroqinit.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 prep sample
    # -------------------------------------------------------------------------
    elif YS_grp == "prep" and YS_cmd == "sample":
        sys.argv = ["rapid2 prep sample"] + sys.argv[3:]
        _subsampleqout.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 prep ltir
    # -------------------------------------------------------------------------
    elif YS_grp == "prep" and YS_cmd == "ltir":
        sys.argv = ["rapid2 prep ltir"] + sys.argv[3:]
        _ltir_scl.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 eval graph
    # -------------------------------------------------------------------------
    elif YS_grp == "eval" and YS_cmd == "graph":
        sys.argv = ["rapid2 eval graph"] + sys.argv[3:]
        _hydrographs.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 eval cmpncf
    # -------------------------------------------------------------------------
    elif YS_grp == "eval" and YS_cmd == "cmpncf":
        # Rewrite sys.argv so argparse prints the correct usage string
        sys.argv = ["rapid2 eval cmpncf"] + sys.argv[3:]
        _cmpncf.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 v1v2 static
    # -------------------------------------------------------------------------
    elif YS_grp == "v1v2" and YS_cmd == "static":
        sys.argv = ["rapid2 v1v2 static"] + sys.argv[3:]
        _rapid1to2.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 v1v2 inflow
    # -------------------------------------------------------------------------
    elif YS_grp == "v1v2" and YS_cmd == "inflow":
        sys.argv = ["rapid2 v1v2 inflow"] + sys.argv[3:]
        _m3rivtoqext.main()

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
