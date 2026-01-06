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

from rapid2.con_vec import con_vec
from rapid2.crd_vec import crd_vec
from rapid2.cpl_vec import cpl_vec
from rapid2.chk_ids import chk_ids
from rapid2.chk_cpl import chk_cpl
from rapid2.Qex_new import Qex_new


# *****************************************************************************
# Main
# *****************************************************************************
def main() -> None:

    # -------------------------------------------------------------------------
    # Initialize the argument parser and add valid arguments
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description='LSM data to RAPID input')

    parser.add_argument('-l', '--lsm', type=str, required=True,
                        help='Specify the LSM file')

    parser.add_argument('-c', '--con', type=str, required=True,
                        help='Specify the connectivity file')

    parser.add_argument('-p', '--pos', type=str, required=True,
                        help='Specify the position points (coordinates)')

    parser.add_argument('-b', '--bnd', type=str, required=True,
                        help='Specify the binding (coupling) file')

    parser.add_argument('-d', '--dir', type=str, required=True,
                        help='Specify the directory')

    parser.add_argument('-f', '--fil', type=str, required=True,
                        help='Specify the file name')

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    lsm_ncf = args.lsm
    con_csv = args.con
    pos_csv = args.pos
    bnd_csv = args.bnd
    dir_str = args.dir
    fil_str = args.fil

    print('Transforming data from ', lsm_ncf,
          'for', con_csv,
          'with', pos_csv,
          'and', bnd_csv,
          'to', dir_str,
          'as', fil_str)

    # -------------------------------------------------------------------------
    # Skip if file already exists
    # -------------------------------------------------------------------------
    Qex_ncf = os.path.join(dir_str, fil_str)

    if os.path.exists(Qex_ncf):
        print(f'WARNING - File already exists {Qex_ncf}. Exit without error')
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Check if files exist
    # -------------------------------------------------------------------------
    try:
        with open(lsm_ncf):
            pass
    except IOError:
        print(f'ERROR - Unable to open {lsm_ncf}')
        sys.exit(1)

    # -------------------------------------------------------------------------
    # Read connectivity file
    # -------------------------------------------------------------------------
    print('- Read connectivity file')

    IV_riv_tot1, IV_dwn_tot1 = con_vec(con_csv)
    IS_riv_tot1 = len(IV_riv_tot1)
    print(
         '  . The number of river reaches in connectivity file is: '
         f'{IS_riv_tot1}'
         )

    # -------------------------------------------------------------------------
    # Read coordinate file
    # -------------------------------------------------------------------------
    print('- Read coordinate file')

    IV_riv_tot2, ZV_lon_tot2, ZV_lat_tot2 = crd_vec(pos_csv)
    IS_riv_tot2 = len(IV_riv_tot2)
    print(
         '  . The number of river reaches in coordinate file is: '
         f'{IS_riv_tot2}'
         )

    # -------------------------------------------------------------------------
    # Read coupling file
    # -------------------------------------------------------------------------
    print('- Read coupling file')

    IV_riv_tot3, ZV_riv_skm3, IV_riv_1bi3, IV_riv_1bj3 = cpl_vec(bnd_csv)
    IS_riv_tot3 = len(IV_riv_tot3)
    print(
         '  . The number of river reaches in coupling file is: '
         f'{IS_riv_tot3}'
         )

    # -------------------------------------------------------------------------
    # Check that IDs are the same
    # -------------------------------------------------------------------------
    print('- Check that IDs are the same')

    chk_ids(IV_riv_tot1, IV_riv_tot2)
    chk_ids(IV_riv_tot1, IV_riv_tot3)
    print(' . IDs are the same')

    # -------------------------------------------------------------------------
    # Check consistency of coupling file
    # -------------------------------------------------------------------------
    print('- Check consisitency of coupling file')

    chk_cpl(ZV_riv_skm3, IV_riv_1bi3, IV_riv_1bj3)
    print(' . OK')

    # -------------------------------------------------------------------------
    # Read LSM metadata
    # -------------------------------------------------------------------------
    print('- Read LSM metadata')

    c = netCDF4.Dataset(lsm_ncf, 'r')

    IS_lsm_lon = len(c.dimensions['lon'])
    print('  . The number of longitudes is: '+str(IS_lsm_lon))

    IS_lsm_lat = len(c.dimensions['lat'])
    print('  . The number of latitudes is: '+str(IS_lsm_lat))

    IS_lsm_tim = len(c.dimensions['time'])
    print('  . The number of time steps is: '+str(IS_lsm_tim))

    ZS_fll_rsf = netCDF4.default_fillvals['f4']
    if 'Qs_acc' in c.variables:
        var = c.variables['Qs_acc']
        if '_FillValue' in var.ncattrs():
            ZS_fll_rsf = var._FillValue
            print(f'  . The fill value for Qs_acc is: {ZS_fll_rsf}')
    else:
        raise ValueError('Qs_acc variable missing')

    ZS_fll_rsb = netCDF4.default_fillvals['f4']
    if 'Qsb_acc' in c.variables:
        var = c.variables['Qsb_acc']
        if '_FillValue' in var.ncattrs():
            ZS_fll_rsb = var._FillValue
            print('  . The fill value for Qsb_acc is: '+str(ZS_fll_rsb))
    else:
        raise ValueError('Qsb_acc variable missing')

    # -------------------------------------------------------------------------
    # Create Qext file
    # -------------------------------------------------------------------------
    print('- Create Qext file')

    Qex_new(IV_riv_tot2, ZV_lon_tot2, ZV_lat_tot2, Qex_ncf)

    f = netCDF4.Dataset(Qex_ncf, 'a')
    Qex = f.variables['Qext']
    time = f.variables['time']
    time_bnds = f.variables['time_bnds']

    # -------------------------------------------------------------------------
    # Populate dynamic data
    # -------------------------------------------------------------------------
    print('- Populate dynamic data')

    ZV_riv_scl = 1000*ZV_riv_skm3
    # Scale by 1000: the multiplication of 0.001 m/mm and 1,000,000 m2/km2

    # TODO: check scaling for time step duration to make flow units.

    IV_riv_0bi = IV_riv_1bi3 - 1
    IV_riv_0bj = IV_riv_1bj3 - 1
    # Shift to 0-based indexing; entries becoming −1 have 0 area (chk_cpl.py).

    thresholds = set(range(0, 101, 25))
    # Define 25% thresholds from 0% to 100% included

    for JS_lsm_tim in range(IS_lsm_tim):

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Print progress
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        JS_pct = int(100 * JS_lsm_tim / IS_lsm_tim)
        if JS_pct in thresholds:
            print(f' . Completed {JS_pct}%')
            thresholds.remove(JS_pct)
        # Print if JS_pct is in thresholds, remove after to print only once

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Print progress
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        ZM_lsm_rsf = c.variables['Qs_acc'][JS_lsm_tim][:][:]
        ZM_lsm_rsb = c.variables['Qsb_acc'][JS_lsm_tim][:][:]
        # netCDF data are stored following: c.variables[var][time][lat][lon]
        ZM_lsm_run = ZM_lsm_rsf+ZM_lsm_rsb
        # ZM_lsm_run is of type 'np.ma.core.MaskedArray' or 'np.ndarray'
        # The units of runoff in GLDAS2 are kg*m-2, which is equivalent to mm

        ZV_riv_Qex = ZM_lsm_run[IV_riv_0bj, IV_riv_0bi]
        # This uses the multidimensional list-of-locations indexing capability.
        # All values at given i and j indices can be obtained by giving two
        # lists of j and i indices.
        ZV_riv_Qex = ZV_riv_Qex*ZV_riv_scl
        # Scaling accounting for area and units.

        if isinstance(ZV_riv_Qex, np.ma.MaskedArray):
            ZV_riv_Qex = np.where(ZV_riv_Qex.mask, 0, ZV_riv_Qex.data)
        # Make sure the masked values are replaced by 0
        Qex[JS_lsm_tim, :] = ZV_riv_Qex[:]
        # netCDF data are stored following: g.variables[m3_riv][time][rivid]

    print(' . Completed 100%')

    time[:] = c.variables['time'][:]
    time_bnds[:] = c.variables['time_bnds'][:]
    # From the LSM netCDF file
    c.close()


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == '__main__':
    main()


# *****************************************************************************
# End
# *****************************************************************************
