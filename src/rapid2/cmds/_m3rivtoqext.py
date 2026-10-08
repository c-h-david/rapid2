#!/usr/bin/env python3
# *****************************************************************************
# _m3rivtoqext.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2025


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse
import os
import sys

import netCDF4
from tqdm import tqdm

from rapid2 import (
    __version__,
    prep_Qex_ncf,
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
            "Convert external inflow volume (m3_riv) to external inflow "
            "rate (Qext)."
        ),
        epilog=(
            "examples:\n"
            "  m3rivtoqext --inflow_volume m3_riv_San_Guad.nc4 "
            "--external_inflow Qext_San_Guad.nc4"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    parser.add_argument(
        "-m3r",
        "--external_volume",
        dest="m3r",
        metavar="EXTERNAL_VOLUME",
        type=str,
        required=True,
        help="specify the input m3_riv file",
    )

    parser.add_argument(
        "-Qex",
        "--external_inflow",
        dest="Qex",
        metavar="EXTERNAL_INFLOW",
        type=str,
        required=True,
        help="specify the output Qext file",
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    m3r_ncf = args.m3r
    Qex_ncf = args.Qex

    print("Converting (from/to):")
    print(f" - {m3r_ncf}")
    print(f" - {Qex_ncf}")

    # -------------------------------------------------------------------------
    # Skip if file already exists
    # -------------------------------------------------------------------------
    if os.path.isfile(Qex_ncf):
        print(f"WARNING - File already exists {Qex_ncf}. Skipping.")
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Execute main logic
    # -------------------------------------------------------------------------
    try:
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Get metadata from m3_riv file
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        d = netCDF4.Dataset(m3r_ncf, "r")

        if "m3_riv" not in d.variables:
            raise ValueError(f"m3_riv variable does not exist in {m3r_ncf}")

        if "rivid" not in d.variables:
            raise ValueError(f"rivid variable does not exist in {m3r_ncf}")

        if "lon" not in d.variables:
            raise ValueError(f"lon variable does not exist in {m3r_ncf}")

        if "lat" not in d.variables:
            raise ValueError(f"lat variable does not exist in {m3r_ncf}")

        if "time" not in d.variables:
            raise ValueError(f"time variable does not exist in {m3r_ncf}")

        if "time_bnds" not in d.variables:
            raise ValueError(f"time_bnds variable does not exist in {m3r_ncf}")

        IV_riv_tot = d.variables["rivid"][:]
        ZV_lon_tot = d.variables["lon"][:]
        ZV_lat_tot = d.variables["lat"][:]

        IV_tim_all = d.variables["time"][:]
        IM_tim_all = d.variables["time_bnds"][:]

        IS_tim_all = len(IV_tim_all)
        IS_dtE = IM_tim_all[0, 1] - IM_tim_all[0, 0]

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Create Qex file
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print(f"The transformation will divide by the value: {IS_dtE}")

        prep_Qex_ncf(IV_riv_tot, ZV_lon_tot, ZV_lat_tot, Qex_ncf)

        f = netCDF4.Dataset(Qex_ncf, "a")

        f.variables["time"][:] = IV_tim_all
        f.variables["time_bnds"][:] = IM_tim_all

        for JS_tim_all in tqdm(
            range(IS_tim_all), desc="Converting inflow volume"
        ):
            f.variables["Qext"][JS_tim_all, :] = (
                d.variables["m3_riv"][JS_tim_all, :] / IS_dtE
            )

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Close files
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        d.close()
        f.close()

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
