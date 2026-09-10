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
import sys

import netCDF4
import numpy as np
from tqdm import tqdm

from rapid2 import (
    __version__,
    calc_Nmn_mat,
    chck_bas,
    make_0bi_tbl,
    make_CCC_mat,
    make_Msk_mat,
    make_Net_mat,
    make_SA0_mat,
    make_SAe_mat,
    make_Sel_mat,
    prep_Qfi_ncf,
    prep_Qou_ncf,
    read_con_vec,
    read_kpr_vec,
    read_nml_tbl,
    read_riv_vec,
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
            "  rapid2 --namelist input/Sandbox/nml_Sandbox_OL.yml\n"
            "  rapid2 --namelist input/Sandbox/nml_Sandbox_TR.yml\n"
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

        if "Qob_ncf" in AT_nml:
            Qob_ncf = AT_nml["Qob_ncf"]
            ZS_scl_inf = AT_nml["ZS_scl_inf"]
            ZS_scl_sdv = AT_nml["ZS_scl_sdv"]
            ZS_lkm_cov = AT_nml["ZS_lkm_cov"]

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # River network
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        IV_riv_tot, IV_dwn_tot = read_con_vec(con_pqt)
        IV_riv_bas = read_riv_vec(bas_pqt)
        IT_0bi_tot, IT_0bi_bas, IV_0bi_bas = make_0bi_tbl(
            IV_riv_tot, IV_riv_bas
        )
        ZM_Net = make_Net_mat(IV_dwn_tot, IT_0bi_tot, IV_riv_bas, IT_0bi_bas)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Model parameters
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        IV_riv_tmp, ZV_kpr_bas = read_kpr_vec(kpr_pqt, IV_0bi_bas)
        np.testing.assert_array_equal(IV_riv_bas, IV_riv_tmp)

        IV_riv_tmp, ZV_xpr_bas = read_xpr_vec(xpr_pqt, IV_0bi_bas)
        np.testing.assert_array_equal(IV_riv_bas, IV_riv_tmp)

        ZM_C1p, ZM_C2p, ZM_C3p = make_CCC_mat(ZV_kpr_bas, ZV_xpr_bas, IS_dtR)
        ZM_ICN, ZM_Qex, ZM_Qou = make_Msk_mat(ZM_Net, ZM_C1p, ZM_C2p, ZM_C3p)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Extract metadata of external inflow and check IDs
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        (
            IV_riv_tmp,
            ZV_lon_tot,
            ZV_lat_tot,
            IV_tim_all,
            IM_tim_all,
        ) = read_std_vec(Qex_ncf)
        np.testing.assert_array_equal(IV_riv_tot, IV_riv_tmp)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Extract metadata of initial value and check IDs and time
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        IV_riv_tmp, _, _, IV_tim_tmp, _ = read_std_vec(Q00_ncf)
        np.testing.assert_array_equal(IV_riv_tot, IV_riv_tmp)
        np.testing.assert_equal(IV_tim_all[0], IV_tim_tmp[0])

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Get time step correspondance
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        IS_tim_all = len(IV_tim_all)

        if IM_tim_all is None:
            raise ValueError("read_std_vec returned None for IM_tim_all")
        # Use IM_tim_all instead of IV_tim_all which may have only one timestep
        IS_dtE = IM_tim_all[0, 1] - IM_tim_all[0, 0]

        if IS_dtE == 0:
            raise ValueError("Values of time_bnds lead to IS_dtE = 0")

        if IS_dtE % IS_dtR == 0:
            IS_rat_Qex = IS_dtE // IS_dtR
        else:
            raise ValueError("IS_dtE is not a multiple of IS_dtR")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Check upstream to downstream topology
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        chck_bas(IV_riv_bas, IT_0bi_bas, IV_riv_tot, IV_dwn_tot, IT_0bi_tot)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Populate metadata for discharge output files
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
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

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Data Assimilation: Static setup for observations
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if "Qob_ncf" in locals():
            # Extract metadata of observed flows
            (
                IV_riv_avl,
                _,
                _,
                IV_tim_obs,
                IM_tim_obs,
            ) = read_std_vec(Qob_ncf)

            # Find gauges that physically intersect the simulated basin
            IV_riv_act = IV_riv_avl[np.isin(IV_riv_avl, IV_riv_bas)]
            if len(IV_riv_act) == 0:
                raise ValueError(
                    "No valid overlapping gauges found in the basin"
                )

            # Get 0-based indices of active gauges relative to observations
            _, _, IV_0bi_act = make_0bi_tbl(IV_riv_avl, IV_riv_act)

            # Build the Selection matrix mapping active gauges to basin reaches
            ZM_Sel = make_Sel_mat(IV_riv_act, IT_0bi_bas)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Data Assimilation: Validate temporal alignment
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if "Qob_ncf" in locals():
            # Check for existence of time bounds
            if IM_tim_obs is None:
                raise ValueError("time_bnds is missing in Qob_ncf")

            # Check start times
            if IM_tim_all[0, 0] != IM_tim_obs[0, 0]:
                raise ValueError(
                    f"Start times differ. Sim: {IM_tim_all[0, 0]}, "
                    f"Obs: {IM_tim_obs[0, 0]}"
                )

            # Check time step of observations
            IS_dtO = IM_tim_obs[0, 1] - IM_tim_obs[0, 0]

            if IS_dtO == 0:
                raise ValueError("Values of time_bnds lead to IS_dtO = 0")

            if IS_dtO % IS_dtE != 0:
                raise ValueError("IS_dtO is not a multiple of IS_dtE")

            if IS_dtO % IS_dtR == 0:
                IS_rat_Qob = IS_dtO // IS_dtR
            else:
                raise ValueError("IS_dtO is not a multiple of IS_dtR")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Data Assimilation: Build observation matrices
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if "Qob_ncf" in locals():
            # Compute the Muskingum operator (I - C1*N)^-1
            ZM_Mus = calc_Nmn_mat(ZM_C1p @ ZM_Net)

            # Compute the selection-multiplied input-to-state average matrix
            ZM_SAe = make_SAe_mat(ZM_Sel, ZM_Mus, ZM_Qex, ZM_Qou, IS_rat_Qob)

            # Compute the selection-multiplied initial-to-state average matrix
            ZM_SA0 = make_SA0_mat(ZM_Sel, ZM_Mus, ZM_Qou, IS_rat_Qob)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Open files
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        e = netCDF4.Dataset(Q00_ncf, "r")
        f = netCDF4.Dataset(Qex_ncf, "r")
        g = netCDF4.Dataset(Qou_ncf, "a")
        h = netCDF4.Dataset(Qfi_ncf, "a")
        if "Qob_ncf" in locals():
            o = netCDF4.Dataset(Qob_ncf, "r")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Read initial discharge state
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        ZV_Qou_prv = e.variables["Qout"][0, IV_0bi_bas]

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Run simulations
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        for JS_tim_all in tqdm(range(IS_tim_all), desc="Computing discharge"):
            # Read external inflow
            ZV_Qex_avg = f.variables["Qext"][JS_tim_all][IV_0bi_bas]

            # Data Assimilation
            if "Qob_ncf" in locals() and JS_tim_all % (IS_dtO // IS_dtE) == 0:
                JS_tim_obs = JS_tim_all // (IS_dtO // IS_dtE)
                ZV_Qob_now = o.variables["Qout"][JS_tim_obs, IV_0bi_act]
                ZV_Qex_tmp = f.variables["Qext"][
                    JS_tim_all : JS_tim_all + (IS_dtO // IS_dtE), IV_0bi_bas
                ].mean(axis=0)
                ZV_Qme_tmp = ZM_SAe @ ZV_Qex_tmp + ZM_SA0 @ ZV_Qou_prv

            # Compute Qout
            ZV_Qou_avg, ZV_Qou_now = updt_Mus_Qou(
                ZM_ICN, ZM_Qex, ZM_Qou, IS_rat_Qex, ZV_Qou_prv, ZV_Qex_avg
            )
            ZV_Qou_prv = ZV_Qou_now

            # Populate Qout, time, and time_bnds
            g.variables["Qout"][JS_tim_all, :] = ZV_Qou_avg[:]
            g.variables["time"][JS_tim_all] = IV_tim_all[JS_tim_all]
            g.variables["time_bnds"][JS_tim_all, :] = IM_tim_all[JS_tim_all, :]

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Save final discharge state
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        h.variables["Qout"][0, IV_0bi_bas] = ZV_Qou_now[:]
        h.variables["time"][0] = IM_tim_all[-1, 1]

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Copy some global attributes
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        g.setncattr("title", f.getncattr("title"))
        g.setncattr("institution", f.getncattr("institution"))
        h.setncattr("title", f.getncattr("title"))
        h.setncattr("institution", f.getncattr("institution"))

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Close files
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        e.close()
        f.close()
        g.close()
        h.close()
        if "Qob_ncf" in locals():
            o.close()

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Done
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
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
