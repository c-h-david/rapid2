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

import netCDF4  # type: ignore[import-untyped]
from tqdm import tqdm  # type: ignore[import-untyped]

from rapid2 import __version__
from rapid2.bas_vec import bas_vec
from rapid2.ccc_mat import ccc_mat
from rapid2.chk_ids import chk_ids
from rapid2.chk_top import chk_top
from rapid2.con_vec import con_vec
from rapid2.hsh_tbl import hsh_tbl
from rapid2.k_x_vec import k_x_vec
from rapid2.mus_rte import mus_rte
from rapid2.net_mat import net_mat
from rapid2.nml_cfg import nml_cfg
from rapid2.Qfi_new import Qfi_new
from rapid2.Qou_new import Qou_new
from rapid2.rte_mat import rte_mat
from rapid2.std_mdt import std_mdt
from rapid2.stp_cor import stp_cor


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
            "  rapid2 -nl namelist_Sandbox.yml\n"
            "  rapid2 --namelist namelist_Sandbox.yml"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    parser.add_argument(
        "-nl",
        "--namelist",
        type=str,
        required=True,
        help="specify the namelist file",
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    nml_yml = args.namelist

    print(f"Namelist file: {nml_yml}")

    # -------------------------------------------------------------------------
    # Read namelist into a dictionary and assign to local variables
    # -------------------------------------------------------------------------
    AT_cfg = nml_cfg(nml_yml)

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
    IV_riv_tot, IV_dwn_tot = con_vec(con_csv)
    IV_riv_bas = bas_vec(bas_csv)
    IT_idx_tot, IT_idx_bas, IV_idx_bas = hsh_tbl(IV_riv_tot, IV_riv_bas)
    ZM_Net = net_mat(IV_dwn_tot, IT_idx_tot, IV_riv_bas, IT_idx_bas)

    # -------------------------------------------------------------------------
    # Model parameters
    # -------------------------------------------------------------------------
    ZV_kpr_bas, ZV_xpr_bas = k_x_vec(kpr_csv, xpr_csv, IV_idx_bas)
    ZM_C1m, ZM_C2m, ZM_C3m = ccc_mat(ZV_kpr_bas, ZV_xpr_bas, IS_dtR)
    ZM_Lin, ZM_Qex, ZM_Qou = rte_mat(ZM_Net, ZM_C1m, ZM_C2m, ZM_C3m)

    # -------------------------------------------------------------------------
    # Extract metadata of external inflow, get time step correspondance
    # -------------------------------------------------------------------------
    (
        IV_riv_tmp,
        ZV_lon_tot,
        ZV_lat_tot,
        IV_tim_all,
        IM_tim_all,
    ) = std_mdt(Qex_ncf)

    if IM_tim_all is None:
        print("ERROR - std_mdt returned None for IM_tim_all")
        sys.exit(1)

    IS_tim_all = len(IV_tim_all)
    IS_TaR = IM_tim_all[0, 1] - IM_tim_all[0, 0]
    # Using IM_tim_all rather than IV_tim_all which may have only one timestep

    if IS_TaR == 0:
        print("ERROR - Values of time_bnds lead to IS_TaR = 0")
        sys.exit(1)

    IS_mus = stp_cor(IS_TaR, IS_dtR)

    # -------------------------------------------------------------------------
    # Check river IDs and upstream to downstream topology
    # -------------------------------------------------------------------------
    chk_ids(IV_riv_tot, IV_riv_tmp)
    chk_top(IV_riv_bas, IT_idx_bas, IV_riv_tot, IV_dwn_tot, IT_idx_tot)

    # -------------------------------------------------------------------------
    # Populate metadata for discharge output files
    # -------------------------------------------------------------------------
    Qou_new(
        IV_riv_tot[IV_idx_bas],
        ZV_lon_tot[IV_idx_bas],
        ZV_lat_tot[IV_idx_bas],
        Qou_ncf,
    )
    Qfi_new(
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
    ZV_Qou_ini = e.variables["Qout"][0, IV_idx_bas]

    # -------------------------------------------------------------------------
    # Run simulations
    # -------------------------------------------------------------------------
    for JS_tim_all in tqdm(range(IS_tim_all), desc="Computing discharge"):
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Compute Qout
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        ZV_Qex_avg = f.variables["Qext"][JS_tim_all][IV_idx_bas]

        ZV_Qou_avg, ZV_Qou_fin = mus_rte(
            ZM_Lin, ZM_Qex, ZM_Qou, IS_mus, ZV_Qou_ini, ZV_Qex_avg
        )
        ZV_Qou_ini = ZV_Qou_fin

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Populate Qout, time, and time_bnds
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        g.variables["Qout"][JS_tim_all, :] = ZV_Qou_avg[:]
        g.variables["time"][JS_tim_all] = IV_tim_all[JS_tim_all]
        g.variables["time_bnds"][JS_tim_all, :] = IM_tim_all[JS_tim_all, :]

    # -------------------------------------------------------------------------
    # Save final discharge state
    # -------------------------------------------------------------------------
    h.variables["Qout"][0, IV_idx_bas] = ZV_Qou_fin[:]

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
