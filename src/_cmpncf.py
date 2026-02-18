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
from numpy.ma import MaskedArray
import netCDF4  # type: ignore[import-untyped]

from rapid2 import __version__
from rapid2.Qex_mdt import Qex_mdt


# *****************************************************************************
# Main
# *****************************************************************************
def main() -> None:

    # -------------------------------------------------------------------------
    # Initialize the argument parser and add valid arguments
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description='Compare RAPID output files for regression testing '
                    'and validation',
        epilog='\nExamples:\n'
               '  cmpncf -o old_output.nc -n new_output.nc '
               '-r 0.01 -a 0.001\n'
               '  cmpncf --old baseline.nc --new current.nc '
               '--rel 1e-6 --abs 1e-9\n'
    )

    parser.add_argument('--version', action='version',
                        version=f'rapid2 {__version__}')

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

    print(f'Comparing {old_ncf} '
          f'with {new_ncf} '
          f'relative tolerance {rel_str} '
          f'absolute tolerance {abs_str}'
          )

    ZS_rtl = np.float64(rel_str)
    ZS_atl = np.float64(abs_str)

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
        IS_tim = len(IV_tim_old)
        print(f'Common number of time steps   : {IS_tim}')
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
    if np.array_equal(ZV_lon_old, ZV_lon_new):
        print('The longitude values are the same')
    else:
        print('ERROR - The longitude values differ')
        sys.exit(1)

    if np.array_equal(ZV_lat_old, ZV_lat_new):
        print('The latitude values are the same')
    else:
        print('ERROR - The latitude values differ')
        sys.exit(1)

    if np.array_equal(IV_tim_old, IV_tim_new):
        print('The time values are the same')
    else:
        print('ERROR - The time values differ')
        sys.exit(1)

    if (IM_tim_old is None) != (IM_tim_new is None):
        print('ERROR - time_bnds present in only one file')
        sys.exit(1)

    if (IM_tim_old is not None) and (IM_tim_new is not None):
        if np.array_equal(IM_tim_old, IM_tim_new):
            print('The time_bnds values are the same')
        else:
            print('ERROR - The time_bnds values differ')
            sys.exit(1)
    else:
        print('WARNING - time_bnds variable missing: skipping comparison')

    # -------------------------------------------------------------------------
    # Get main variable in netCDF files
    # -------------------------------------------------------------------------
    old = netCDF4.Dataset(old_ncf, 'r')
    new = netCDF4.Dataset(new_ncf, 'r')

    com_var = set(old.variables) & set(new.variables)

    if 'Qext' in com_var:
        ncf_var = 'Qext'
    elif 'Qout' in com_var:
        ncf_var = 'Qout'
    else:
        print('ERROR - Neither Qext nor Qout is common variable')
        sys.exit(1)
    print(f'The main variable names are the same: {ncf_var}')

    # -------------------------------------------------------------------------
    # Compute differences
    # -------------------------------------------------------------------------
    ZS_rdf_max = 0
    ZS_adf_max = 0
    BS_msk_old = False
    BS_msk_new = False

    for JS_tim in range(IS_tim):
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Initializing
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        ZS_rdf = 0
        ZS_adf = 0

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Getting values
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        ZV_old = old.variables[ncf_var][JS_tim, :]
        ZV_new = new.variables[ncf_var][JS_tim, :]
        if 'IV_loc' in locals():
            ZV_new = ZV_new[IV_loc]

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Converting masked values to -9999
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if isinstance(ZV_old, MaskedArray) and np.any(ZV_old.mask):
            ZV_old = ZV_old.filled(fill_value=-9999)  # type: ignore
            # 'filled triggers mypy
            BS_msk_old = True
        if isinstance(ZV_new, MaskedArray) and np.any(ZV_new.mask):
            ZV_new = ZV_new.filled(fill_value=-9999)  # type: ignore
            # 'filled triggers mypy
            BS_msk_new = True

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Comparing difference values
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Tried computations with regular Python lists but they are very slow.
        # Also tried using map(operator.sub,V,W) or [x-y for x,y in zip(V,W)],
        # but this still results in slow computations.
        # The best performance seems to be with Numpy.
        ZV_mag_dif = np.absolute(ZV_old-ZV_new)
        ZS_adf_max = max(np.max(ZV_mag_dif), ZS_adf_max)

        ZS_rdf = np.sqrt(np.sum(ZV_mag_dif*ZV_mag_dif)
                         / np.sum(ZV_old*ZV_old)
                         )
        ZS_rdf_max = max(ZS_rdf, ZS_rdf_max)

    # ------------------------------------------------------------------------
    # Print difference values and compare to tolerances
    # ------------------------------------------------------------------------
    if BS_msk_old:
        print(f'WARNING - masked values replaced by -9999 in {old_ncf}')
    if BS_msk_new:
        print(f'WARNING - masked values replaced by -9999 in {new_ncf}')
    if BS_msk_old or BS_msk_new:
        print('-------------------------------')

    print('Max relative difference       :'+'{0:.2e}'.format(ZS_rdf_max))
    print('Max absolute difference       :'+'{0:.2e}'.format(ZS_adf_max))
    print('-------------------------------')

    if ZS_rdf_max > ZS_rtl:
        print('Unacceptable rel. difference!!!')
        print('-------------------------------')
        sys.exit(1)

    if ZS_adf_max > ZS_atl:
        print('Unacceptable abs. difference!!!')
        print('-------------------------------')
        sys.exit(1)

    print('netCDF files similar!!!')
    print('-------------------------------')


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == '__main__':
    main()


# *****************************************************************************
# End
# *****************************************************************************
