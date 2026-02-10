#!/usr/bin/env python3
# *****************************************************************************
# _sandboxqext.py
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
import numpy as np

from rapid2 import __version__
from rapid2.Qex_new import Qex_new


# *****************************************************************************
# Main
# *****************************************************************************
def main() -> None:

    # -------------------------------------------------------------------------
    # Initialize the argument parser and add valid arguments
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description='Generate synthetic external inflow data for sandbox testing',
        epilog='\nExamples:\n'
               '  sandboxqext -m 10 20 30 40 50 -a 5 5 5 5 5 -o Qext_sandbox.nc\n'
               '  sandboxqext --mean 10 20 30 40 50 --amplitude 5 5 5 5 5 --output Qext.nc\n'
    )

    parser.add_argument('--version', action='version',
                        version=f'rapid2 {__version__}')

    parser.add_argument('-m', '--mean', type=float, required=True,
                        nargs=5,
                        help='Specify five mean values: m1 m2 m3 m4 m5')

    parser.add_argument('-a', '--amplitude', type=float, required=True,
                        nargs=5,
                        help='Specify five amplitude values: a1 a2 a3 a4 a5')

    parser.add_argument('-o', '--output', type=str, required=True,
                        help='Specify the output Qext file')

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    ZV_mea = np.array(args.mean, dtype=np.float32)
    ZV_amp = np.array(args.amplitude, dtype=np.float32)
    Qex_ncf = args.output

    print('Creating (from/to):')
    print(f' - {ZV_mea}')
    print(f' - {ZV_amp}')
    print(f' - {Qex_ncf}')

    # -------------------------------------------------------------------------
    # Skip if file already exists
    # -------------------------------------------------------------------------
    if os.path.isfile(Qex_ncf):
        print(f'WARNING - File already exists {Qex_ncf}. Exit without error')
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Hardcoded Sandbox values
    # -------------------------------------------------------------------------
    IV_riv_tot = np.array([10, 20, 30, 40, 50], dtype=np.int32)
    ZV_lon_tot = np.array([4.30, 5.94, 5.12, 6.55, 4.30])
    ZV_lat_tot = np.array([8.20, 8.20, 5.12, 4.30, 2.04])
    IV_Qex_tim = np.array(range(80), dtype=np.int32) * np.int32(10800)

    # -------------------------------------------------------------------------
    # Array sizes
    # -------------------------------------------------------------------------
    IS_riv_tot = len(IV_riv_tot)
    IS_Qex_tim = len(IV_Qex_tim)

    # -------------------------------------------------------------------------
    # Check size of provided mean and amplitude arrays
    # -------------------------------------------------------------------------
    if len(ZV_mea) != IS_riv_tot:
        print('ERROR - Mean array not of size 5.')
        sys.exit(1)

    if len(ZV_amp) != IS_riv_tot:
        print('ERROR - Amplitude array not of size 5.')
        sys.exit(1)

    # -------------------------------------------------------------------------
    # Create Qext file
    # -------------------------------------------------------------------------
    Qex_new(IV_riv_tot, ZV_lon_tot, ZV_lat_tot, Qex_ncf)

    # -------------------------------------------------------------------------
    # Populate Qext file
    # -------------------------------------------------------------------------
    f = netCDF4.Dataset(Qex_ncf, 'a')

    f.variables['time'][:] = IV_Qex_tim[:]

    f.variables['time_bnds'][:, 0] = IV_Qex_tim[:]
    f.variables['time_bnds'][:, 1] = IV_Qex_tim[:] + np.int32(10800)

    Qex = f.variables['Qext']
    for JS_Qex_tim in range(IS_Qex_tim):
        ZV_tmp = np.sign(np.sin(np.pi / 86400 * IV_Qex_tim[JS_Qex_tim] + 1e-7))
        ZV_tmp = ZV_tmp * ZV_amp
        ZV_tmp = ZV_tmp + ZV_mea
        Qex[JS_Qex_tim, :] = ZV_tmp[:]
    # The 1e-7 avoids np.sign(0) = 0

    f.title = 'Sandbox dataset for RAPID2'
    f.institution = ('Jet Propulsion Laboratory, '
                     'California Institute of Technology')

    # -------------------------------------------------------------------------
    # Close file
    # -------------------------------------------------------------------------
    f.close()


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == '__main__':
    main()


# *****************************************************************************
# End
# *****************************************************************************
