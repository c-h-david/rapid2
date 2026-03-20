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

import netCDF4  # type: ignore[import-untyped]
import numpy as np
from tqdm import tqdm  # type: ignore[import-untyped]

from rapid2 import __version__
from rapid2.read_bas_vec import read_bas_vec
from rapid2.make_CCC_mat import make_CCC_mat
from rapid2.read_con_vec import read_con_vec
from rapid2.make_0bi_tbl import make_0bi_tbl
from rapid2.read_kpr_vec import read_kpr_vec
from rapid2.mus_rte import mus_rte
from rapid2.make_Net_mat import make_Net_mat
from rapid2.read_nml_tbl import read_nml_tbl
from rapid2.prep_Qfi_ncf import prep_Qfi_ncf
from rapid2.prep_Qou_ncf import prep_Qou_ncf
from rapid2.make_Mus_mat import make_Mus_mat
from rapid2.read_std_vec import read_std_vec
from rapid2.top_chk import top_chk
from rapid2.read_xpr_vec import read_xpr_vec


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
            "  rapid2 --nml input/Sandbox/namelist_Sandbox.yml\n"
            "  rapid2 --nml input/Tutorial/namelist_Tutorial.yml"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    parser.add_argument(
        "--nml",
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
    AT_cfg = read_nml_tbl(nml_yml)

    Q00_ncf = AT_cfg["Q00_ncf"]
    Qex_ncf = AT_cfg["Qex_ncf"]

    con_csv = AT_cfg["con_csv"]
    kpr_csv = AT_cfg["kpr_csv"]
    xpr_csv = AT_cfg["xpr_csv"]

    bas_csv = AT_cfg["bas_csv"]

    IS_dtR = AT_cfg["IS_dtR"]

    Qou_ncf = AT_cfg["Qou_ncf"]
    Qfi_ncf = AT_cfg["Qfi_ncf"]

    # -------------------------------------------------------------------------
    # River network
    # -------------------------------------------------------------------------
    IV_riv_tot, IV_dwn_tot = read_con_vec(con_csv)
    IV_riv_bas = read_bas_vec(bas_csv)
    IT_idx_tot, IT_idx_bas, IV_idx_bas = make_0bi_tbl(IV_riv_tot, IV_riv_bas)
    ZM_Net = make_Net_mat(IV_dwn_tot, IT_idx_tot, IV_riv_bas, IT_idx_bas)

    # -------------------------------------------------------------------------
    # Model parameters
    # -------------------------------------------------------------------------
    ZV_kpr_bas = read_kpr_vec(kpr_csv, IV_idx_bas)
    ZV_xpr_bas = read_xpr_vec(xpr_csv, IV_idx_bas)
    ZM_C1m, ZM_C2m, ZM_C3m = make_CCC_mat(ZV_kpr_bas, ZV_xpr_bas, IS_dtR)
    ZM_Lin, ZM_Qex, ZM_Qou = make_Mus_mat(ZM_Net, ZM_C1m, ZM_C2m, ZM_C3m)

    # -------------------------------------------------------------------------
    # Extract metadata of external inflow
    # -------------------------------------------------------------------------
    (
        IV_riv_tmp,
        ZV_lon_tot,
        ZV_lat_tot,
        IV_tim_all,
        IM_tim_all,
    ) = read_std_vec(Qex_ncf)

    # -------------------------------------------------------------------------
    # Get time step correspondance
    # -------------------------------------------------------------------------
    IS_tim_all = len(IV_tim_all)

    if IM_tim_all is None:
        raise ValueError("read_std_vec returned None for IM_tim_all")

    IS_TaR = IM_tim_all[0, 1] - IM_tim_all[0, 0]
    # Using IM_tim_all rather than IV_tim_all which may have only one timestep

    if IS_TaR == 0:
        raise ValueError("Values of time_bnds lead to IS_TaR = 0")

    if IS_TaR % IS_dtR == 0:
        IS_mus = IS_TaR // IS_dtR
    else:
        raise ValueError("IS_TaR is not a multiple of IS_dtR")

    # -------------------------------------------------------------------------
    # Check river IDs and upstream to downstream topology
    # -------------------------------------------------------------------------
    np.testing.assert_array_equal(IV_riv_tot, IV_riv_tmp)
    top_chk(IV_riv_bas, IT_idx_bas, IV_riv_tot, IV_dwn_tot, IT_idx_tot)

    # -------------------------------------------------------------------------
    # Populate metadata for discharge output files
    # -------------------------------------------------------------------------
    prep_Qou_ncf(
        IV_riv_tot[IV_idx_bas],
        ZV_lon_tot[IV_idx_bas],
        ZV_lat_tot[IV_idx_bas],
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
    ZV_Qou_prv = e.variables["Qout"][0, IV_idx_bas]

    # -------------------------------------------------------------------------
    # Run simulations
    # -------------------------------------------------------------------------
    for JS_tim_all in tqdm(range(IS_tim_all), desc="Computing discharge"):
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Compute Qout
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        ZV_Qex_avg = f.variables["Qext"][JS_tim_all][IV_idx_bas]

        ZV_Qou_avg, ZV_Qou_now = mus_rte(
            ZM_Lin, ZM_Qex, ZM_Qou, IS_mus, ZV_Qou_prv, ZV_Qex_avg
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
    h.variables["Qout"][0, IV_idx_bas] = ZV_Qou_now[:]

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
