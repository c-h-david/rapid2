#!/usr/bin/env python3
# *****************************************************************************
# _m3rivtoqext.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2025


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse
import os
import sys
import netCDF4  # type: ignore[import-untyped]
from rapid2.Qex_new import Qex_new


# *****************************************************************************
# Main
# *****************************************************************************
def main() -> None:

    # -------------------------------------------------------------------------
    # Initialize the argument parser and add valid arguments
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description='Convert m3_riv to Qext')

    parser.add_argument('-i', '--input', type=str, required=True,
                        help='Specify the input m3_riv file')

    parser.add_argument('-o', '--output', type=str, required=True,
                        help='Specify the output Qext file')

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    m3r_ncf = args.input
    Qex_ncf = args.output

    print('Converting (from/to):')
    print(f' - {m3r_ncf}')
    print(f' - {Qex_ncf}')

    # -------------------------------------------------------------------------
    # Skip if file already exists
    # -------------------------------------------------------------------------
    if os.path.isfile(Qex_ncf):
        print(f'WARNING - File already exists {Qex_ncf}. Exit without error')
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Get metadata from m3_riv file
    # -------------------------------------------------------------------------
    d = netCDF4.Dataset(m3r_ncf, 'r')

    if 'm3_riv' not in d.variables:
        print(f'ERROR - m3_riv variable does not exist in {m3r_ncf}')
        sys.exit(1)

    if 'rivid' not in d.variables:
        print(f'ERROR - rivid variable does not exist in {m3r_ncf}')
        sys.exit(1)

    if 'lon' not in d.variables:
        print(f'ERROR - lon variable does not exist in {m3r_ncf}')
        sys.exit(1)

    if 'lat' not in d.variables:
        print(f'ERROR - lat variable does not exist in {m3r_ncf}')
        sys.exit(1)

    if 'time' not in d.variables:
        print(f'ERROR - time variable does not exist in {m3r_ncf}')
        sys.exit(1)

    if 'time_bnds' not in d.variables:
        print(f'ERROR - time_bnds variable does not exist in {m3r_ncf}')
        sys.exit(1)

    IV_m3r_tot = d.variables['rivid'][:]
    ZV_lon_tot = d.variables['lon'][:]
    ZV_lat_tot = d.variables['lat'][:]

    IV_m3r_tim = d.variables['time'][:]
    IM_m3r_tim = d.variables['time_bnds'][:]

    IS_m3r_tim = len(IV_m3r_tim)
    IS_TaR = IM_m3r_tim[0, 1] - IM_m3r_tim[0, 0]

    # -------------------------------------------------------------------------
    # Create Qex file
    # -------------------------------------------------------------------------
    print(f'The transformation will divide by the value: {IS_TaR}')

    Qex_new(IV_m3r_tot, ZV_lon_tot, ZV_lat_tot, Qex_ncf)

    f = netCDF4.Dataset(Qex_ncf, 'a')

    f.variables['time'][:] = IV_m3r_tim
    f.variables['time_bnds'][:] = IM_m3r_tim
    Qex = f.variables['Qext']

    for JS_m3r_tim in range(IS_m3r_tim):
        Qex[JS_m3r_tim, :] = d.variables['m3_riv'][JS_m3r_tim, :] / IS_TaR

    # -------------------------------------------------------------------------
    # Close files
    # -------------------------------------------------------------------------
    d.close()
    f.close()


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == '__main__':
    main()


# *****************************************************************************
# End
# *****************************************************************************
