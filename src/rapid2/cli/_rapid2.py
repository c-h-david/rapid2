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
        print("  run              Execute the core matrix-based routing model")
        print("  fetch sandbox    Download Sandbox synthetic experiment files")
        print("  fetch gldas2     Download remote GLDAS-2 data")
        print("  inflow lsm       Map prepped LSM grids to river networks")
        print("  inflow sandbox   Generate synthetic sine-wave inflow")
        print("  init zero        Generate cold-start initial discharge files")
        print("  sample spacetime Align NetCDF data to match gauges")
        print("  bias learn       Compute LTIR scalars to learn the bias")
        print("  bias correct     Apply the learned scalars to correct inflow")
        print("  plot hydro       Generate SVG hydrograph visualizations")
        print("  comp netcdf      Compare NetCDF files for regression testing")
        print("  legacy static    Upgrade RAPID1 CSV files to Parquet")
        print("  legacy inflow    Convert legacy external volumes to flows")
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
    # Dispatch to: rapid2 fetch sandbox
    # -------------------------------------------------------------------------
    elif YS_grp == "fetch" and YS_cmd == "sandbox":
        sys.argv = ["rapid2 fetch sandbox"] + sys.argv[3:]
        _dsandbox.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 fetch gldas2
    # -------------------------------------------------------------------------
    elif YS_grp == "fetch" and YS_cmd == "gldas2":
        sys.argv = ["rapid2 fetch gldas2"] + sys.argv[3:]
        _dgldas2.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 inflow lsm
    # -------------------------------------------------------------------------
    elif YS_grp == "inflow" and YS_cmd == "lsm":
        sys.argv = ["rapid2 inflow lsm"] + sys.argv[3:]
        _cpllsm.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 inflow sandbox
    # -------------------------------------------------------------------------
    elif YS_grp == "inflow" and YS_cmd == "sandbox":
        sys.argv = ["rapid2 inflow sandbox"] + sys.argv[3:]
        _sandboxqext.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 init zero
    # -------------------------------------------------------------------------
    elif YS_grp == "init" and YS_cmd == "zero":
        sys.argv = ["rapid2 init zero"] + sys.argv[3:]
        _zeroqinit.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 sample spacetime
    # -------------------------------------------------------------------------
    elif YS_grp == "sample" and YS_cmd == "spacetime":
        sys.argv = ["rapid2 sample spacetime"] + sys.argv[3:]
        _subsampleqout.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 bias learn
    # -------------------------------------------------------------------------
    elif YS_grp == "bias" and YS_cmd == "learn":
        sys.argv = ["rapid2 bias learn"] + sys.argv[3:]
        _ltir_scl.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 bias correct
    # -------------------------------------------------------------------------
    elif YS_grp == "bias" and YS_cmd == "correct":
        sys.argv = ["rapid2 bias correct"] + sys.argv[3:]
        _ltir_cor.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 plot hydro
    # -------------------------------------------------------------------------
    elif YS_grp == "plot" and YS_cmd == "hydro":
        sys.argv = ["rapid2 plot hydro"] + sys.argv[3:]
        _hydrographs.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 legacy static
    # -------------------------------------------------------------------------
    elif YS_grp == "legacy" and YS_cmd == "static":
        sys.argv = ["rapid2 legacy static"] + sys.argv[3:]
        _rapid1to2.main()

    # -------------------------------------------------------------------------
    # Dispatch to: rapid2 legacy inflow
    # -------------------------------------------------------------------------
    elif YS_grp == "legacy" and YS_cmd == "inflow":
        sys.argv = ["rapid2 legacy inflow"] + sys.argv[3:]
        _m3rivtoqext.main()

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
