#!/usr/bin/env python3
# *****************************************************************************
# _cmpncf.py
# *****************************************************************************

# Author:
# Cedric H. David, 2016-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse
import sys

import netCDF4  # type: ignore[import-untyped]
import numpy as np
from numpy.ma import MaskedArray

from rapid2 import __version__
from rapid2.make_0bi_tbl import make_0bi_tbl
from rapid2.read_std_vec import read_std_vec


# *****************************************************************************
# Main
# *****************************************************************************
def main() -> None:

    # -------------------------------------------------------------------------
    # Initialize the argument parser and add valid arguments
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description=(
            "Compare RAPID input/output netCDF files for numerical regression "
            "testing."
        ),
        epilog=(
            "examples:\n"
            "  cmpncf "
            "--prv input/Tutorial/Qinit_GLDAS_2.1_VIC_2010-01_GOLD.nc4 "
            "--now input/Tutorial/Qinit_GLDAS_2.1_VIC_2010-01.nc4 "
            "--rtl 1e-6 --atl 1e-3\n"
            "  cmpncf "
            "--prv input/Tutorial/Qext_GLDAS_2.1_VIC_2010-01_GOLD.nc4 "
            "--now input/Tutorial/Qext_GLDAS_2.1_VIC_2010-01.nc4 "
            "--rtl 1e-6 --atl 1e-3"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    parser.add_argument(
        "--prv",
        type=str,
        required=True,
        help="specify the old netCDF file",
    )

    parser.add_argument(
        "--now",
        type=str,
        required=True,
        help="specify the new netCDF file",
    )

    parser.add_argument(
        "--rtl",
        type=str,
        required=False,
        default="0",
        help="specify the relative tolerance",
    )

    parser.add_argument(
        "--atl",
        type=str,
        required=False,
        default="0",
        help="specify the absolute tolerance",
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    prv_ncf = args.prv
    now_ncf = args.now
    YS_rtl = args.rtl
    YS_atl = args.atl

    print(
        f"Comparing {prv_ncf} "
        f"with {now_ncf} "
        f"relative tolerance {YS_rtl} "
        f"absolute tolerance {YS_atl}"
    )

    ZS_rtl = np.float64(YS_rtl)
    ZS_atl = np.float64(YS_atl)

    # -------------------------------------------------------------------------
    # Get metadata in netCDF files
    # -------------------------------------------------------------------------
    (
        IV_riv_prv,
        ZV_lon_prv,
        ZV_lat_prv,
        IV_tim_prv,
        IM_tim_prv,
    ) = read_std_vec(prv_ncf)

    (
        IV_riv_now,
        ZV_lon_now,
        ZV_lat_now,
        IV_tim_now,
        IM_tim_now,
    ) = read_std_vec(now_ncf)

    # -------------------------------------------------------------------------
    # Compare dimension sizes
    # -------------------------------------------------------------------------
    if len(IV_riv_prv) == len(IV_riv_now):
        IS_riv_tot = len(IV_riv_prv)
        print(f"Common number of river reaches: {IS_riv_tot}")
    else:
        print(
            f"ERROR - The number of river reaches differs: "
            f"{len(IV_riv_prv)} <> {len(IV_riv_now)}"
        )
        sys.exit(1)

    if len(IV_tim_prv) == len(IV_tim_now):
        IS_tim = len(IV_tim_prv)
        print(f"Common number of time steps   : {IS_tim}")
    else:
        print(
            f"ERROR - The number of time steps differs: "
            f"{len(IV_tim_prv)} <> {len(IV_tim_now)}"
        )
        sys.exit(1)

    # -------------------------------------------------------------------------
    # Compare rivid values
    # -------------------------------------------------------------------------
    if np.array_equal(IV_riv_prv, IV_riv_now):
        print("The rivids and their sort are both the same")
    else:
        if np.array_equal(np.sort(IV_riv_prv), np.sort(IV_riv_now)):
            print("WARNING - The rivids are the same, but sorted differently")
            _, _, IV_0bi_prv = make_0bi_tbl(IV_riv_now, IV_riv_prv)
        else:
            print("ERROR - The rivids differ")
            sys.exit(1)

    # -------------------------------------------------------------------------
    # Compare other metadata values
    # -------------------------------------------------------------------------
    if np.array_equal(ZV_lon_prv, ZV_lon_now):
        print("The longitude values are the same")
    else:
        print("ERROR - The longitude values differ")
        sys.exit(1)

    if np.array_equal(ZV_lat_prv, ZV_lat_now):
        print("The latitude values are the same")
    else:
        print("ERROR - The latitude values differ")
        sys.exit(1)

    if np.array_equal(IV_tim_prv, IV_tim_now):
        print("The time values are the same")
    else:
        print("ERROR - The time values differ")
        sys.exit(1)

    if (IM_tim_prv is None) != (IM_tim_now is None):
        print("ERROR - time_bnds present in only one file")
        sys.exit(1)

    if (IM_tim_prv is not None) and (IM_tim_now is not None):
        if np.array_equal(IM_tim_prv, IM_tim_now):
            print("The time_bnds values are the same")
        else:
            print("ERROR - The time_bnds values differ")
            sys.exit(1)
    else:
        print("WARNING - time_bnds variable missing: skipping comparison")

    # -------------------------------------------------------------------------
    # Get main variable in netCDF files
    # -------------------------------------------------------------------------
    p = netCDF4.Dataset(prv_ncf, "r")
    n = netCDF4.Dataset(now_ncf, "r")

    com_var = set(p.variables) & set(n.variables)

    if "Qext" in com_var:
        ncf_var = "Qext"
    elif "Qout" in com_var:
        ncf_var = "Qout"
    else:
        print("ERROR - Neither Qext nor Qout is common variable")
        sys.exit(1)
    print(f"The main variable names are the same: {ncf_var}")

    # -------------------------------------------------------------------------
    # Compute differences
    # -------------------------------------------------------------------------
    ZS_rdf_max = 0
    ZS_adf_max = 0
    BS_fll_prv = False
    BS_fll_now = False

    for JS_tim in range(IS_tim):
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Initializing
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        ZS_rdf = 0
        ZS_adf = 0

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Getting values
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        ZV_val_prv = p.variables[ncf_var][JS_tim, :]
        ZV_val_now = n.variables[ncf_var][JS_tim, :]
        if "IV_0bi_prv" in locals():
            ZV_val_now = ZV_val_now[IV_0bi_prv]

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Converting masked values to -9999
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if isinstance(ZV_val_prv, MaskedArray) and np.any(ZV_val_prv.mask):
            ZV_val_prv = ZV_val_prv.filled(fill_value=-9999)  # type: ignore
            # 'filled triggers mypy
            BS_fll_prv = True
        if isinstance(ZV_val_now, MaskedArray) and np.any(ZV_val_now.mask):
            ZV_val_now = ZV_val_now.filled(fill_value=-9999)  # type: ignore
            # 'filled triggers mypy
            BS_fll_now = True

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Comparing difference values
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Tried computations with regular Python lists but they are very slow.
        # Also tried using map(operator.sub,V,W) or [x-y for x,y in zip(V,W)],
        # but this still results in slow computations.
        # The best performance seems to be with Numpy.
        ZV_adf_tmp = np.absolute(ZV_val_prv - ZV_val_now)
        ZS_adf_max = max(np.max(ZV_adf_tmp), ZS_adf_max)

        ZS_rdf = np.sqrt(
            np.sum(ZV_adf_tmp * ZV_adf_tmp) / np.sum(ZV_val_prv * ZV_val_prv)
        )
        ZS_rdf_max = max(ZS_rdf, ZS_rdf_max)

    # ------------------------------------------------------------------------
    # Print difference values and compare to tolerances
    # ------------------------------------------------------------------------
    if BS_fll_prv:
        print(f"WARNING - masked values replaced by -9999 in {prv_ncf}")
    if BS_fll_now:
        print(f"WARNING - masked values replaced by -9999 in {now_ncf}")
    if BS_fll_prv or BS_fll_now:
        print("-------------------------------")

    print("Max relative difference       :" + "{0:.2e}".format(ZS_rdf_max))
    print("Max absolute difference       :" + "{0:.2e}".format(ZS_adf_max))
    print("-------------------------------")

    if ZS_rdf_max > ZS_rtl:
        print("Unacceptable rel. difference!!!")
        print("-------------------------------")
        sys.exit(1)

    if ZS_adf_max > ZS_atl:
        print("Unacceptable abs. difference!!!")
        print("-------------------------------")
        sys.exit(1)

    print("netCDF files similar!!!")
    print("-------------------------------")


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == "__main__":
    main()


# *****************************************************************************
# End
# *****************************************************************************
