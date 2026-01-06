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

from rapid2.nml_cfg import nml_cfg
from rapid2.con_vec import con_vec
from rapid2.bas_vec import bas_vec
from rapid2.hsh_tbl import hsh_tbl
from rapid2.net_mat import net_mat
from rapid2.k_x_vec import k_x_vec
from rapid2.ccc_mat import ccc_mat
from rapid2.rte_mat import rte_mat
from rapid2.Qex_mdt import Qex_mdt
from rapid2.stp_cor import stp_cor
from rapid2.chk_ids import chk_ids
from rapid2.chk_top import chk_top
from rapid2.Qou_new import Qou_new
from rapid2.Qfi_new import Qfi_new
from rapid2.mus_rte import mus_rte


# *****************************************************************************
# Main
# *****************************************************************************
def main() -> None:
    # -------------------------------------------------------------------------
    # Initialize the argument parser and add valid arguments
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description='This is RAPID2')

    parser.add_argument('-nl', '--namelist', type=str, required=True,
                        help='Specify the namelist value')

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    nml_yml = args.namelist

    print('Namelist file: '+nml_yml)

    # -------------------------------------------------------------------------
    # Read namelist into a dictionary and assign to local variables
    # -------------------------------------------------------------------------
    nml_dic = nml_cfg(nml_yml)

    Q00_ncf = nml_dic['Q00_ncf']
    Qex_ncf = nml_dic['Qex_ncf']

    con_csv = nml_dic['con_csv']
    kpr_csv = nml_dic['kpr_csv']
    xpr_csv = nml_dic['xpr_csv']

    bas_csv = nml_dic['bas_csv']

    IS_dtR = nml_dic['IS_dtR']

    Qou_ncf = nml_dic['Qou_ncf']
    Qfi_ncf = nml_dic['Qfi_ncf']

    # -------------------------------------------------------------------------
    # River network
    # -------------------------------------------------------------------------
    IV_riv_tot, IV_dwn_tot = con_vec(con_csv)
    IV_riv_bas = bas_vec(bas_csv)
    IM_hsh_tot, IM_hsh_bas, IV_bas_tot = hsh_tbl(IV_riv_tot, IV_riv_bas)
    ZM_Net = net_mat(IV_dwn_tot, IM_hsh_tot, IV_riv_bas, IM_hsh_bas)

    # -------------------------------------------------------------------------
    # Model parameters
    # -------------------------------------------------------------------------
    ZV_kpr_bas, ZV_xpr_bas = k_x_vec(kpr_csv, xpr_csv, IV_bas_tot)
    ZM_C1m, ZM_C2m, ZM_C3m = ccc_mat(ZV_kpr_bas, ZV_xpr_bas, IS_dtR)
    ZM_Lin, ZM_Qex, ZM_Qou = rte_mat(ZM_Net, ZM_C1m, ZM_C2m, ZM_C3m)

    # -------------------------------------------------------------------------
    # Extract metadata of external inflow, get time step correspondance
    # -------------------------------------------------------------------------
    (IV_Qex_tot, ZV_lon_tot, ZV_lat_tot,
     IV_Qex_tim, IM_Qex_tim,
     ) = Qex_mdt(Qex_ncf)

    IS_Qex_tim = len(IV_Qex_tim)
    IS_TaR = IM_Qex_tim[0, 1] - IM_Qex_tim[0, 0]
    # Using IM_Qex_tim rather than IV_Qex_tim which may have only one timestep

    if IS_TaR == 0:
        print('ERROR - Values of time_bnds lead to IS_TaR = 0')
        sys.exit(1)

    IS_mus = stp_cor(IS_TaR, IS_dtR)

    # -------------------------------------------------------------------------
    # Check river IDs and upstream to downstream topology
    # -------------------------------------------------------------------------
    chk_ids(IV_riv_tot, IV_Qex_tot)
    chk_top(IV_riv_bas, IM_hsh_bas, IV_riv_tot, IV_dwn_tot, IM_hsh_tot)

    # -------------------------------------------------------------------------
    # Populate metadata for discharge output files
    # -------------------------------------------------------------------------
    Qou_new(IV_riv_tot[IV_bas_tot], ZV_lon_tot[IV_bas_tot],
            ZV_lat_tot[IV_bas_tot], Qou_ncf)
    Qfi_new(IV_Qex_tot, ZV_lon_tot, ZV_lat_tot, Qfi_ncf)

    # -------------------------------------------------------------------------
    # Open files
    # -------------------------------------------------------------------------
    e = netCDF4.Dataset(Q00_ncf, 'r')
    f = netCDF4.Dataset(Qex_ncf, 'r')
    g = netCDF4.Dataset(Qou_ncf, 'a')
    h = netCDF4.Dataset(Qfi_ncf, 'a')

    # -------------------------------------------------------------------------
    # Read initial discharge state
    # -------------------------------------------------------------------------
    ZV_Qou_ini = e.variables['Qout'][0, IV_bas_tot]

    # -------------------------------------------------------------------------
    # Run simulations
    # -------------------------------------------------------------------------
    for JS_Qex_tim in range(IS_Qex_tim):
        ZV_Qex_avg = f.variables['Qext'][JS_Qex_tim][IV_bas_tot]

        ZV_Qou_avg, ZV_Qou_fin = mus_rte(ZM_Lin, ZM_Qex, ZM_Qou, IS_mus,
                                         ZV_Qou_ini, ZV_Qex_avg)
        ZV_Qou_ini = ZV_Qou_fin

        g.variables['Qout'][JS_Qex_tim, :] = ZV_Qou_avg[:]

    # -------------------------------------------------------------------------
    # Save final discharge state
    # -------------------------------------------------------------------------
    h.variables['Qout'][0, IV_bas_tot] = ZV_Qou_fin[:]

    # -------------------------------------------------------------------------
    # Copy some global attributes
    # -------------------------------------------------------------------------
    g.setncattr('title', f.getncattr('title'))
    g.setncattr('institution', f.getncattr('institution'))
    h.setncattr('title', f.getncattr('title'))
    h.setncattr('institution', f.getncattr('institution'))

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
    print('Done')


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == '__main__':
    main()


# *****************************************************************************
# End
# *****************************************************************************
