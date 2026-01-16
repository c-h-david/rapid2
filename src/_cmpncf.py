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
import numpy as np
import netCDF4  # type: ignore[import-untyped]

from rapid2.Qex_mdt import Qex_mdt


# *****************************************************************************
# Main
# *****************************************************************************
def main() -> None:

    # -------------------------------------------------------------------------
    # Initialize the argument parser and add valid arguments
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description='Compare RAPID netCDF files')

    parser.add_argument('-o', '--old', type=str, required=True,
                        help='Specify the old netCDF file')

    parser.add_argument('-n', '--new', type=str, required=True,
                        help='Specify the new netCDF file')

    parser.add_argument('-r', '--rel', type=str, required=False, default='0',
                        help='Specify relative tolerance')

    parser.add_argument('-a', '--abs', type=str, required=False, default='0',
                        help='Specify the absolute tolerance')

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    old_ncf = args.old
    new_ncf = args.new
    rel_str = args.rel
    abs_str = args.abs

    print(f'Comparing{old_ncf} '
          f'with {new_ncf} '
          f'relative tolerance {rel_str} '
          f'absolute tolerance {abs_str}'
          )

    ZS_rel = np.float64(rel_str)
    ZS_abs = np.float64(abs_str)

    # -------------------------------------------------------------------------
    # Get metadata in netCDF files
    # -------------------------------------------------------------------------
    (IV_riv_old, ZV_lon_old, ZV_lat_old,
     IV_tim_old, IM_tim_old,
     ) = Qex_mdt(old_ncf)

    (IV_riv_new, ZV_lon_new, ZV_lat_new,
     IV_tim_new, IM_tim_new,
     ) = Qex_mdt(new_ncf)

    # -------------------------------------------------------------------------
    # Compare dimension sizes
    # -------------------------------------------------------------------------
    if len(IV_riv_old) == len(IV_riv_new):
        IS_riv_tot = len(IV_riv_old)
        print(f'Common number of river reaches: {IS_riv_tot}')
    else:
        print(f'ERROR - The number of river reaches differs: '
              f'{len(IV_riv_old)} <> {len(IV_riv_new)}'
              )
        sys.exit(1)

    if len(IV_tim_old) == len(IV_tim_new):
        IS_time = len(IV_tim_old)
        print(f'Common number of time steps   : {IS_time}')
    else:
        print(f'ERROR - The number of time steps differs: '
              f'{len(IV_tim_old)} <> {len(IV_tim_new)}'
              )
        sys.exit(1)

    # -------------------------------------------------------------------------
    # Compare rivid values
    # -------------------------------------------------------------------------
    if np.array_equal(IV_riv_old, IV_riv_new):
        print('The rivids and their sort are both the same')
    else:
        if np.array_equal(np.sort(IV_riv_old), np.sort(IV_riv_new)):
            print('WARNING - The rivids are the same, but sorted differently')
            IM_hsh = {}
            for JS_riv_tot in range(IS_riv_tot):
                IM_hsh[IV_riv_new[JS_riv_tot]] = JS_riv_tot
            IV_loc = []
            for JS_riv_tot in range(IS_riv_tot):
                IV_loc.append(IM_hsh[IV_riv_old[JS_riv_tot]])
        else:
            print('ERROR - The rivids differ')
            sys.exit(1)

    # -------------------------------------------------------------------------
    # Compare other metadata values
    # -------------------------------------------------------------------------
    if np.array_equal(IV_tim_old, IV_tim_new):
        print('The time values the same')
    else:
        print('ERROR - The time values differ')
        sys.exit(1)

    if np.array_equal(IM_tim_old, IM_tim_new):
        print('The time_bnds values the same')
    else:
        print('ERROR - The time_bnds values differ')
        sys.exit(1)

    if np.array_equal(ZV_lon_old, ZV_lon_new):
        print('The longitude values the same')
    else:
        print('ERROR - The longitude values differ')
        sys.exit(1)

    if np.array_equal(ZV_lat_old, ZV_lat_new):
        print('The latitude values the same')
    else:
        print('ERROR - The latitude values differ')
        sys.exit(1)

    # -------------------------------------------------------------------------
    # Get main variable in netCDF files
    # -------------------------------------------------------------------------
    old = netCDF4.Dataset(old_ncf, 'r')
    new = netCDF4.Dataset(new_ncf, 'r')

    com_var = set(old.variables) & set(new.variables)

    print(ZS_rel)
    print(ZS_abs)
    print(com_var)


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == '__main__':
    main()


# *****************************************************************************
# End
# *****************************************************************************
