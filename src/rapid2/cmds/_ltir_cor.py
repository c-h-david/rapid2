#!/usr/bin/env python3
# *****************************************************************************
# _ltir_cor.py
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
import pyarrow.parquet as pq
from tqdm import tqdm

from rapid2 import (
    __version__,
    prep_Qex_ncf,
    read_std_vec,
)


# *****************************************************************************
# Main
# *****************************************************************************
def main() -> None:
    # -------------------------------------------------------------------------
    # Initialize the argument parser
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description=(
            "Apply Long-Term Inverse Routing (LTIR) scaling factors to an "
            "external inflow (Qex) file."
        ),
        epilog=(
            "examples:\n"
            "  ltir_cor --previous Qex_historic_FG.nc4 "
            "--scalar scl_historic.parquet "
            "--now Qex_historic_BC.nc4"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    parser.add_argument(
        "-prv",
        "--previous",
        dest="prv",
        metavar="PREVIOUS",
        type=str,
        required=True,
        help="specify the uncorrected input Qex_ncf file",
    )

    parser.add_argument(
        "-scl",
        "--scalar",
        dest="scl",
        metavar="SCALAR",
        type=str,
        required=True,
        help="specify the input scl_pqt scaling file",
    )

    parser.add_argument(
        "-now",
        "--now",
        dest="now",
        metavar="NOW",
        type=str,
        required=True,
        help="specify the corrected output Qex_ncf file",
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    prv_ncf = args.prv
    scl_pqt = args.scl
    now_ncf = args.now

    print(
        f"Applying LTIR scalars\n"
        f" - Previous : {prv_ncf}\n"
        f" - Scalar   : {scl_pqt}\n"
        f"   -> {now_ncf}"
    )

    # -------------------------------------------------------------------------
    # Skip if file already exists
    # -------------------------------------------------------------------------
    if os.path.exists(now_ncf):
        print(f"WARNING - File already exists {now_ncf}. Skipping.")
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Execute main logic
    # -------------------------------------------------------------------------
    try:
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Validate metadata alignment between files
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print("- Validating files")
        (
            IV_riv_tot,
            ZV_lon_tot,
            ZV_lat_tot,
            IV_tim_all,
            IM_tim_all,
        ) = read_std_vec(prv_ncf)
        IS_tim_all = len(IV_tim_all)

        table = pq.read_table(scl_pqt, columns=["riv", "scl"])
        IV_riv_tmp = table.column("riv").to_numpy().astype(np.int32)

        if not np.array_equal(IV_riv_tot, IV_riv_tmp):
            raise ValueError(f"River IDs in {scl_pqt} must match {prv_ncf}")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Load scalars and handle NoData padding
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print("- Loading and padding scalars")
        # Extract the scalar array and replace explicitly stored NaNs with 1.0
        ZV_scl_tot = table.column("scl").to_numpy().astype(np.float64)
        ZV_scl_tot = np.nan_to_num(ZV_scl_tot, nan=1.0)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Prepare the new netCDF file
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print("- Preparing corrected file structure")
        prep_Qex_ncf(IV_riv_tot, ZV_lon_tot, ZV_lat_tot, now_ncf)

        p = netCDF4.Dataset(prv_ncf, "r")
        n = netCDF4.Dataset(now_ncf, "a")

        # Copy time and time bounds
        n.variables["time"][:] = IV_tim_all
        if IM_tim_all is not None:
            n.variables["time_bnds"][:] = IM_tim_all

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Apply scaling factors
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print("- Applying scaling factors")
        for JS_tim_all in tqdm(
            range(IS_tim_all), desc="Scaling external inflow"
        ):
            # Scale the entire domain simultaneously at each timestep
            ZV_Qex_tmp = p.variables["Qext"][JS_tim_all, :]
            n.variables["Qext"][JS_tim_all, :] = ZV_Qex_tmp * ZV_scl_tot

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Copy global attributes
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if "title" in p.ncattrs():
            n.setncattr("title", p.getncattr("title"))
        if "institution" in p.ncattrs():
            n.setncattr("institution", p.getncattr("institution"))

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Close files
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        p.close()
        n.close()

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
