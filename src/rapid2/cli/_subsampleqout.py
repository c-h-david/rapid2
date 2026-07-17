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

import netCDF4
import numpy as np
from tqdm import tqdm

from rapid2 import (
    __version__,
    make_0bi_tbl,
    prep_Qou_ncf,
    read_riv_vec,
    read_std_vec,
)


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
        print(f"WARNING - File already exists {Qme_ncf}. Exit without error")
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Execute main logic
    # -------------------------------------------------------------------------
    try:
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Read observational gauge IDs
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print("- Read observation file")
        IV_riv_avl = read_riv_vec(obs_pqt)
        IS_riv_avl = len(IV_riv_avl)
        print(f"  . Found {IS_riv_avl} observation locations")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Extract metadata from Qou_ncf and check spatial topology
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print("- Extract metadata from Qou file")
        (
            IV_riv_bas,
            ZV_lon_bas,
            ZV_lat_bas,
            IV_tim_all,
            IM_tim_all,
        ) = read_std_vec(Qou_ncf)

        if IM_tim_all is None:
            raise ValueError(f"time_bnds is missing in {Qou_ncf}")

        # Map the observation IDs to their 0-based indices in the Qou file
        _, _, IV_0bi_avl = make_0bi_tbl(IV_riv_bas, IV_riv_avl)

        # Spatially subset coordinates
        ZV_lon_avl = ZV_lon_bas[IV_0bi_avl]
        ZV_lat_avl = ZV_lat_bas[IV_0bi_avl]

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Determine temporal ratios
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print("- Check temporal consistency")
        IS_dtE = IM_tim_all[0, 1] - IM_tim_all[0, 0]
        IS_tim_all = len(IV_tim_all)

        if IS_dtO % IS_dtE != 0:
            raise ValueError(
                f"Target timestep ({IS_dtO}) is not a multiple of the "
                f"input timestep ({IS_dtE})"
            )

        IS_rat_Qob = IS_dtO // IS_dtE
        IS_tim_Qob = IS_tim_all // IS_rat_Qob

        print(f"  . Input time step: {IS_dtE}s")
        print(f"  . Output time step: {IS_dtO}s")
        print(f"  . Averaging {IS_rat_Qob} timesteps per output frame")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Create Qme file
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print("- Create Qme file")
        prep_Qou_ncf(IV_riv_avl, ZV_lon_avl, ZV_lat_avl, Qme_ncf)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Sub-sample data
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print("- Sub-sample data")

        g = netCDF4.Dataset(Qou_ncf, "r")
        m = netCDF4.Dataset(Qme_ncf, "a")

        for JS_tim_Qob in tqdm(range(IS_tim_Qob), desc="Averaging discharge"):
            JS_tim_now = JS_tim_Qob * IS_rat_Qob

            # Extract the chunk and apply spatial filter simultaneously
            ZM_Qou_tmp = g.variables["Qout"][
                JS_tim_now : JS_tim_now + IS_rat_Qob, IV_0bi_avl
            ]

            # Calculate temporal mean across the specified window (axis 0)
            ZV_Qme_avg = np.mean(ZM_Qou_tmp, axis=0)

            # Write to Qme output
            m.variables["Qout"][JS_tim_Qob, :] = ZV_Qme_avg[:]

            # Write aligned time and bounds
            m.variables["time"][JS_tim_Qob] = g.variables["time"][JS_tim_now]
            m.variables["time_bnds"][JS_tim_Qob, 0] = g.variables["time_bnds"][
                JS_tim_now, 0
            ]
            m.variables["time_bnds"][JS_tim_Qob, 1] = g.variables["time_bnds"][
                JS_tim_now + IS_rat_Qob - 1, 1
            ]

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Copy some global attributes
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        m.setncattr("title", g.getncattr("title"))
        m.setncattr("institution", g.getncattr("institution"))

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Close files
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        g.close()
        m.close()

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
