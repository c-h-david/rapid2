#!/usr/bin/env python3
# *****************************************************************************
# _rapid2.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2025


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse

import netCDF4
import numpy as np
from tqdm import tqdm

from rapid2 import (
    __version__,
    chck_bas,
    make_0bi_tbl,
    make_CCC_mat,
    make_Mus_mat,
    make_Net_mat,
    prep_Qfi_ncf,
    prep_Qou_ncf,
    read_bas_vec,
    read_con_vec,
    read_kpr_vec,
    read_nml_tbl,
    read_std_vec,
    read_xpr_vec,
    updt_Mus_Qou,
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
            "Routing Application for Programmed Integration of Discharge "
            "(RAPID)."
        ),
        epilog=(
            "examples:\n"
            "  rapid2 --namelist input/Sandbox/namelist_Sandbox.yml\n"
            "  rapid2 --namelist input/Tutorial/namelist_Tutorial.yml"
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
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    nml_yml = args.nml

    print(f"Namelist file: {nml_yml}")

    # -------------------------------------------------------------------------
    # Read namelist into a dictionary and assign to local variables
    # -------------------------------------------------------------------------
    AT_nml = read_nml_tbl(nml_yml)

    Q00_ncf = AT_nml["Q00_ncf"]
    Qex_ncf = AT_nml["Qex_ncf"]

    con_pqt = AT_nml["con_pqt"]
    kpr_pqt = AT_nml["kpr_pqt"]
    xpr_pqt = AT_nml["xpr_pqt"]

    bas_pqt = AT_nml["bas_pqt"]

    IS_dtR = AT_nml["IS_dtR"]

    Qou_ncf = AT_nml["Qou_ncf"]
    Qfi_ncf = AT_nml["Qfi_ncf"]

    # -------------------------------------------------------------------------
    # River network
    # -------------------------------------------------------------------------
    IV_riv_tot, IV_dwn_tot = read_con_vec(con_pqt)
    IV_riv_bas = read_bas_vec(bas_pqt)
    IT_0bi_tot, IT_0bi_bas, IV_0bi_bas = make_0bi_tbl(IV_riv_tot, IV_riv_bas)
    ZM_Net = make_Net_mat(IV_dwn_tot, IT_0bi_tot, IV_riv_bas, IT_0bi_bas)

    # -------------------------------------------------------------------------
    # Model parameters
    # -------------------------------------------------------------------------
    IV_riv_tmp, ZV_kpr_bas = read_kpr_vec(kpr_pqt, IV_0bi_bas)
    np.testing.assert_array_equal(IV_riv_bas, IV_riv_tmp)

    IV_riv_tmp, ZV_xpr_bas = read_xpr_vec(xpr_pqt, IV_0bi_bas)
    np.testing.assert_array_equal(IV_riv_bas, IV_riv_tmp)

    ZM_C1p, ZM_C2p, ZM_C3p = make_CCC_mat(ZV_kpr_bas, ZV_xpr_bas, IS_dtR)
    ZM_ICN, ZM_Qex, ZM_Qou = make_Mus_mat(ZM_Net, ZM_C1p, ZM_C2p, ZM_C3p)

    # -------------------------------------------------------------------------
    # Extract metadata of initial value and check IDs
    # -------------------------------------------------------------------------
    IV_riv_tmp, _, _, _, _ = read_std_vec(Q00_ncf)
    np.testing.assert_array_equal(IV_riv_tot, IV_riv_tmp)

    # -------------------------------------------------------------------------
    # Extract metadata of external inflow and check IDs
    # -------------------------------------------------------------------------
    (
        IV_riv_tmp,
        ZV_lon_tot,
        ZV_lat_tot,
        IV_tim_all,
        IM_tim_all,
    ) = read_std_vec(Qex_ncf)
    np.testing.assert_array_equal(IV_riv_tot, IV_riv_tmp)

    # -------------------------------------------------------------------------
    # Get time step correspondance
    # -------------------------------------------------------------------------
    IS_tim_all = len(IV_tim_all)

    if IM_tim_all is None:
        raise ValueError("read_std_vec returned None for IM_tim_all")

    IS_dtE = IM_tim_all[0, 1] - IM_tim_all[0, 0]
    # Using IM_tim_all rather than IV_tim_all which may have only one timestep

    if IS_dtE == 0:
        raise ValueError("Values of time_bnds lead to IS_dtE = 0")

    if IS_dtE % IS_dtR == 0:
        IS_rat_Qex = IS_dtE // IS_dtR
    else:
        raise ValueError("IS_dtE is not a multiple of IS_dtR")

    # -------------------------------------------------------------------------
    # Check upstream to downstream topology
    # -------------------------------------------------------------------------
    chck_bas(IV_riv_bas, IT_0bi_bas, IV_riv_tot, IV_dwn_tot, IT_0bi_tot)

    # -------------------------------------------------------------------------
    # Populate metadata for discharge output files
    # -------------------------------------------------------------------------
    prep_Qou_ncf(
        IV_riv_tot[IV_0bi_bas],
        ZV_lon_tot[IV_0bi_bas],
        ZV_lat_tot[IV_0bi_bas],
        Qou_ncf,
    )
    prep_Qfi_ncf(
        IV_riv_tot,
        ZV_lon_tot,
        ZV_lat_tot,
        Qfi_ncf,
    )

    # -------------------------------------------------------------------------
    # Open files
    # -------------------------------------------------------------------------
    e = netCDF4.Dataset(Q00_ncf, "r")
    f = netCDF4.Dataset(Qex_ncf, "r")
    g = netCDF4.Dataset(Qou_ncf, "a")
    h = netCDF4.Dataset(Qfi_ncf, "a")

    # -------------------------------------------------------------------------
    # Read initial discharge state
    # -------------------------------------------------------------------------
    ZV_Qou_prv = e.variables["Qout"][0, IV_0bi_bas]

    # -------------------------------------------------------------------------
    # Run simulations
    # -------------------------------------------------------------------------
    for JS_tim_all in tqdm(range(IS_tim_all), desc="Computing discharge"):
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Compute Qout
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        ZV_Qex_avg = f.variables["Qext"][JS_tim_all][IV_0bi_bas]

        ZV_Qou_avg, ZV_Qou_now = updt_Mus_Qou(
            ZM_ICN, ZM_Qex, ZM_Qou, IS_rat_Qex, ZV_Qou_prv, ZV_Qex_avg
        )
        ZV_Qou_prv = ZV_Qou_now

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Populate Qout, time, and time_bnds
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        g.variables["Qout"][JS_tim_all, :] = ZV_Qou_avg[:]
        g.variables["time"][JS_tim_all] = IV_tim_all[JS_tim_all]
        g.variables["time_bnds"][JS_tim_all, :] = IM_tim_all[JS_tim_all, :]

    # -------------------------------------------------------------------------
    # Save final discharge state
    # -------------------------------------------------------------------------
    h.variables["Qout"][0, IV_0bi_bas] = ZV_Qou_now[:]
    h.variables["time"][0] = IM_tim_all[-1, 1]

    # -------------------------------------------------------------------------
    # Copy some global attributes
    # -------------------------------------------------------------------------
    g.setncattr("title", f.getncattr("title"))
    g.setncattr("institution", f.getncattr("institution"))
    h.setncattr("title", f.getncattr("title"))
    h.setncattr("institution", f.getncattr("institution"))

    # -------------------------------------------------------------------------
    # Close files
    # -------------------------------------------------------------------------
    e.close()
    f.close()
    g.close()
    h.close()

    # -------------------------------------------------------------------------
    # Done
    # -------------------------------------------------------------------------
    print("Done")


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == "__main__":
    main()


# *****************************************************************************
# End
# *****************************************************************************
