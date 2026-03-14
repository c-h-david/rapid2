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

import netCDF4  # type: ignore[import-untyped]
import numpy as np
from tqdm import tqdm  # type: ignore[import-untyped]

from rapid2 import __version__
from rapid2.chk_cpl import chk_cpl
from rapid2.chk_ids import chk_ids
from rapid2.con_vec import con_vec
from rapid2.cpl_vec import cpl_vec
from rapid2.crd_vec import crd_vec
from rapid2.Qex_new import Qex_new


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
            "  cpllsm --lsm input/Tutorial/GLDAS_2.1_VIC_2010-01.nc4 "
            "--con input/Tutorial/rapid_connect_pfaf_74.csv "
            "--crd input/Tutorial/coords_pfaf_74.csv "
            "--cpl input/Tutorial/rapid_coupling_pfaf_74_GLDAS.csv "
            "--Qex input/Tutorial/Qext_GLDAS_2.1_VIC_2010-01.nc4"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    parser.add_argument(
        "--lsm", type=str, required=True, help="specify the LSM file"
    )

    parser.add_argument(
        "--con",
        type=str,
        required=True,
        help="specify the connectivity file",
    )

    parser.add_argument(
        "--crd",
        type=str,
        required=True,
        help="specify the coordinates",
    )

    parser.add_argument(
        "--cpl",
        type=str,
        required=True,
        help="specify the coupling file",
    )

    parser.add_argument(
        "--Qex", type=str, required=True, help="specify the file name"
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    lsm_ncf = args.lsm
    con_csv = args.con
    crd_csv = args.crd
    cpl_csv = args.cpl
    Qex_ncf = args.Qex

    print(
        f"Transforming data from  {lsm_ncf} "
        f"for {con_csv} "
        f"with {crd_csv} "
        f"and {cpl_csv} "
        f"as {Qex_ncf}"
    )

    # -------------------------------------------------------------------------
    # Skip if file already exists
    # -------------------------------------------------------------------------
    if os.path.exists(Qex_ncf):
        print(f"WARNING - File already exists {Qex_ncf}. Exit without error")
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Check if files exist
    # -------------------------------------------------------------------------
    try:
        with open(lsm_ncf):
            pass
    except IOError:
        print(f"ERROR - Unable to open {lsm_ncf}")
        sys.exit(1)

    # -------------------------------------------------------------------------
    # Read connectivity file
    # -------------------------------------------------------------------------
    print("- Read connectivity file")

    IV_riv_tot, IV_dwn_tot = con_vec(con_csv)
    IS_riv_tot = len(IV_riv_tot)
    print(
        "  . The number of river reaches in connectivity file is: "
        f"{IS_riv_tot}"
    )

    # -------------------------------------------------------------------------
    # Read coordinate file
    # -------------------------------------------------------------------------
    print("- Read coordinate file")

    IV_riv_tmp, ZV_lon_tot, ZV_lat_tot = crd_vec(crd_csv)
    chk_ids(IV_riv_tot, IV_riv_tmp)
    print("  . The river reaches are the same as in connectivity file")

    # -------------------------------------------------------------------------
    # Read coupling file
    # -------------------------------------------------------------------------
    print("- Read coupling file")

    IV_riv_tmp, ZV_skm_tot, IV_1bi_tot, IV_1bj_tot = cpl_vec(cpl_csv)
    chk_ids(IV_riv_tot, IV_riv_tmp)
    print("  . The river reaches are the same as in connectivity file")

    # -------------------------------------------------------------------------
    # Check consistency of coupling file
    # -------------------------------------------------------------------------
    print("- Check consisitency of coupling file")

    chk_cpl(ZV_skm_tot, IV_1bi_tot, IV_1bj_tot)
    print(" . OK")

    # -------------------------------------------------------------------------
    # Read LSM metadata
    # -------------------------------------------------------------------------
    print("- Read LSM metadata")

    c = netCDF4.Dataset(lsm_ncf, "r")

    IS_lon_lsm = len(c.dimensions["lon"])
    print(f"  . The number of longitudes is: {IS_lon_lsm}")

    IS_lat_lsm = len(c.dimensions["lat"])
    print(f"  . The number of latitudes is: {IS_lat_lsm}")

    IS_tim_all = len(c.dimensions["time"])
    print(f"  . The number of time steps is: {IS_tim_all}")

    ZS_fll_rsf = netCDF4.default_fillvals["f4"]
    if "Qs_acc" in c.variables:
        var = c.variables["Qs_acc"]
        if "_FillValue" in var.ncattrs():
            ZS_fll_rsf = var._FillValue
            print(f"  . The fill value for Qs_acc is: {ZS_fll_rsf}")
    else:
        raise ValueError("Qs_acc variable missing")

    ZS_fll_rsb = netCDF4.default_fillvals["f4"]
    if "Qsb_acc" in c.variables:
        var = c.variables["Qsb_acc"]
        if "_FillValue" in var.ncattrs():
            ZS_fll_rsb = var._FillValue
            print(f"  . The fill value for Qsb_acc is: {ZS_fll_rsb}")
    else:
        raise ValueError("Qsb_acc variable missing")

    # -------------------------------------------------------------------------
    # Create Qext file
    # -------------------------------------------------------------------------
    print("- Create Qext file")

    Qex_new(IV_riv_tot, ZV_lon_tot, ZV_lat_tot, Qex_ncf)

    f = netCDF4.Dataset(Qex_ncf, "a")
    Qex = f.variables["Qext"]
    time = f.variables["time"]
    time_bnds = f.variables["time_bnds"]

    # -------------------------------------------------------------------------
    # Populate dynamic data
    # -------------------------------------------------------------------------
    print("- Populate dynamic data")

    ZV_scl_tot = 1000 * ZV_skm_tot
    # Scale by 1000: the multiplication of 0.001 m/mm and 1,000,000 m2/km2

    # TODO: check scaling for time step duration to make flow units.

    IV_0bi_tot = IV_1bi_tot - 1
    IV_0bj_tot = IV_1bj_tot - 1
    # Shift to 0-based indexing; entries becoming −1 have 0 area (chk_cpl.py).

    for JS_tim_all in tqdm(range(IS_tim_all), desc="Processing LSM data"):
        ZM_rsf_lsm = c.variables["Qs_acc"][JS_tim_all][:][:]
        ZM_rsb_lsm = c.variables["Qsb_acc"][JS_tim_all][:][:]
        # netCDF data are stored following: c.variables[var][time][lat][lon]
        ZM_run_lsm = ZM_rsf_lsm + ZM_rsb_lsm
        # ZM_run_lsm is of type 'np.ma.core.MaskedArray' or 'np.ndarray'
        # The units of runoff in GLDAS2 are kg*m-2, which is equivalent to mm

        ZV_Qex_tot = ZM_run_lsm[IV_0bj_tot, IV_0bi_tot]
        # This uses the multidimensional list-of-locations indexing capability.
        # All values at given i and j indices can be obtained by giving two
        # lists of j and i indices.
        ZV_Qex_tot = ZV_Qex_tot * ZV_scl_tot
        # Scaling accounting for area and units.

        if isinstance(ZV_Qex_tot, np.ma.MaskedArray):
            ZV_Qex_tot = np.where(ZV_Qex_tot.mask, 0, ZV_Qex_tot.data)
        # Make sure the masked values are replaced by 0
        Qex[JS_tim_all, :] = ZV_Qex_tot[:]
        # netCDF data are stored following: g.variables[m3_riv][time][rivid]

    time[:] = c.variables["time"][:]
    time_bnds[:] = c.variables["time_bnds"][:]
    # From the LSM netCDF file
    c.close()


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == "__main__":
    main()


# *****************************************************************************
# End
# *****************************************************************************
