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
import numpy as np
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

    print('Comparing ', old_ncf,
          'with', new_ncf,
          'relative tolerance', rel_str,
          'absolute tolerance', abs_str,
          )

    ZS_rel = np.float64(rel_str)
    ZS_abs = np.float64(abs_str)

    # -------------------------------------------------------------------------
    # Open netCDF files
    # -------------------------------------------------------------------------
    (IV_riv_old, ZV_lon_old, ZV_lat_old,
     IV_tim_old, IM_tim_old,
     ) = Qex_mdt(old_ncf)

    (IV_riv_new, ZV_lon_new, ZV_lat_new,
     IV_tim_new, IM_tim_new,
     ) = Qex_mdt(new_ncf)

    print('temp', ZS_rel)
    print('temp', ZS_abs)


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == '__main__':
    main()


# *****************************************************************************
# End
# *****************************************************************************
