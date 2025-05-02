#!/usr/bin/env python3
# *****************************************************************************
# _dgldas2.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2025


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse
import os
import sys
import earthaccess
import netCDF4  # type: ignore[import-untyped]


# *****************************************************************************
# Main
# *****************************************************************************
def main() -> None:

    # -------------------------------------------------------------------------
    # Initialize the argument parser and add valid arguments
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description='Download GLDAS2 data')

    parser.add_argument('-v', '--vsn', type=str, required=True,
                        help='Specify the version number')

    parser.add_argument('-m', '--mod', type=str, required=True,
                        help='Specify the land surface model')

    parser.add_argument('-t', '--tim', type=str, required=True,
                        help='Specify the month in yyyy-mm')

    parser.add_argument('-d', '--dir', type=str, required=True,
                        help='Specify the directory')

    parser.add_argument('-f', '--fil', type=str, required=True,
                        help='Specify the file name')

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    vsn_str = args.vsn
    mod_str = args.mod
    tim_str = args.tim
    dir_str = args.dir
    fil_str = args.fil

    print('Download data from GLDAS', vsn_str,
          'for', mod_str,
          'and', tim_str,
          'to', dir_str,
          'as', fil_str)

    # -------------------------------------------------------------------------
    # Skip if file already exists
    # -------------------------------------------------------------------------
    YS_cmb = os.path.join(dir_str, fil_str)

    if os.path.exists(YS_cmb):
        print(f'WARNING: File already exists: {YS_cmb}. Exiting without error')
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Login
    # -------------------------------------------------------------------------
    print('- Login')
    earthaccess.login()

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------
    exp_str = 'GLDAS'
    res_str = '10'
    frq_str = '3H'

    short_name = exp_str + '_' + mod_str + res_str + '_' + frq_str

    print('- Search', short_name, vsn_str, tim_str, 'max=300')

    GV_rem = earthaccess.search_data(
                                     short_name=short_name,
                                     version=vsn_str,
                                     temporal=(tim_str, tim_str),
                                     count=300
                                     )

    # -------------------------------------------------------------------------
    # Download
    # -------------------------------------------------------------------------
    print('- Download', len(GV_rem), 'files')
    earthaccess.download(GV_rem, dir_str)

    # -------------------------------------------------------------------------
    # Check files
    # -------------------------------------------------------------------------
    print('- Check files')

    IS_rem = len(GV_rem)

    YV_loc = []
    for JS_rem in range(IS_rem):
        YS_rem = GV_rem[JS_rem]['meta']['native-id'].split(':', 1)[1]
        ZS_rem = GV_rem[JS_rem]['size']
        YS_loc = os.path.join(dir_str, YS_rem)

        if not os.path.exists(YS_loc):
            print('ERROR: file not downloaded:', YS_loc)
            raise SystemExit(22)
        else:
            ZS_loc = os.path.getsize(YS_loc)/1024**2
            YV_loc.append(YS_loc)

        if abs(ZS_rem-ZS_loc) >= 1e-15:
            print('ERROR:',
                  'Remote file', YS_rem,
                  'Local file', YS_loc,
                  'Remote size', ZS_rem,
                  'Local size', ZS_loc)
            raise SystemExit(22)

    # -------------------------------------------------------------------------
    # Concatenate files
    # -------------------------------------------------------------------------
    print('- Concatenate file')

    YV_loc = sorted(YV_loc)
    YV_yes = {'time', 'time_bnds', 'lon', 'lat', 'Qs_acc', 'Qsb_acc'}

    print(type(YV_loc))

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Open first file to create the output structure
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    with netCDF4.Dataset(YV_loc[0], 'r') as src, \
         netCDF4.Dataset(YS_cmb, 'w') as dst:
        # Copy global attributes
        dst.setncatts({attr: src.getncattr(attr) for attr in src.ncattrs()})

        # Copy dimensions (time should be unlimited)
        for name, dim in src.dimensions.items():
            dst.createDimension(name, None if dim.isunlimited() else len(dim))

        # Copy variables that are in YV_yes
        for name, var in src.variables.items():
            if name in YV_yes:
                dst_var = dst.createVariable(name,
                                             var.datatype,
                                             var.dimensions
                                             )
                dst_var.setncatts({attr: var.getncattr(attr)
                                   for attr in var.ncattrs()
                                   }
                                  )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Append data from all files
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    JS_tim = 0
    for YS_loc in YV_loc:
        with netCDF4.Dataset(YS_loc, 'r') as src, \
             netCDF4.Dataset(YS_cmb, 'a') as dst:
            IS_siz = src.dimensions['time'].size
            for name, var in src.variables.items():
                if name in YV_yes:
                    if 'time' in var.dimensions:
                        beg = JS_tim
                        end = JS_tim + IS_siz
                        dst.variables[name][beg:end] = var[:]
                    else:
                        dst.variables[name][:] = var[:]
            JS_tim += IS_siz

    # -------------------------------------------------------------------------
    # Delete files
    # -------------------------------------------------------------------------
    print('- Delete files')

    for YS_loc in YV_loc:
        try:
            os.remove(YS_loc)
        except OSError as e:
            print(f'Error deleting {YS_loc}: {e}')


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == '__main__':
    main()


# *****************************************************************************
# End
# *****************************************************************************
