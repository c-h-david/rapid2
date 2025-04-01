#!/usr/bin/env python3
# *****************************************************************************
# Qfi_mdt.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2025


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import netCDF4  # type: ignore[import-untyped]
import os
from datetime import datetime, timezone


# *****************************************************************************
# Metadata of outflow
# *****************************************************************************
def Qfi_mdt(
            m3r_ncf: str,
            Qfi_ncf: str
            ) -> None:
    '''Create instantaneous discharge file populated with basic metadata.

    Create instantaneous discharge file populated with basic metadata obtained
    from lateral inflow volume file: river IDs, longitudes, latitudes, crs. The
    integer value of time step is taken as the upper bound of the final time
    step. Global attributes are built from creation time and static RAPID2
    information.

    Parameters
    ----------
    m3r_ncf : str
        Path to the lateral inflow volume file.
    Qfi_ncf : str
        Path to the instantaneous discharge file.

    Returns
    -------
    None

    Examples
    --------
    >>> m3r_ncf = './input/Test/m3_riv_Test_20000101_20000102.nc4'
    >>> Qfi_ncf = './output/Test/Qfinal_Test_20000101_20000102_tst.nc4'
    >>> Qfi_mdt(m3r_ncf, Qfi_ncf)
    >>> Qfi = netCDF4.Dataset(Qfi_ncf, 'r')
    >>> Qfi.variables['rivid'][:].filled()
    array([10, 20, 30, 40, 50], dtype=int32)
    >>> Qfi.variables['time'][:].filled()
    array([946857600], dtype=int32)
    >>> Qfi.variables['lon'][:].filled()
    array([0.5, 2. , 1. , 2. , 0.5])
    >>> Qfi.variables['lat'][:].filled()
    array([5. , 4.5, 3. , 2.5, 1. ])
    >>> os.remove(Qfi_ncf)
    '''

    # -------------------------------------------------------------------------
    # Get UTC date and time
    # -------------------------------------------------------------------------
    YS_dat = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    # -------------------------------------------------------------------------
    # Open one file and create the other
    # -------------------------------------------------------------------------
    f = netCDF4.Dataset(m3r_ncf, 'r')
    h = netCDF4.Dataset(Qfi_ncf, 'w', format='NETCDF4')

    # -------------------------------------------------------------------------
    # Copy dimensions
    # -------------------------------------------------------------------------
    YV_exc = ['nerr', 'nv']
    for nam, dim in f.dimensions.items():
        if nam not in YV_exc:
            h.createDimension(nam, len(dim) if not dim.isunlimited() else None)

    # -------------------------------------------------------------------------
    # Create new variables
    # -------------------------------------------------------------------------
    h.createVariable('Qout', 'float64', ('time', 'rivid'))
    h['Qout'].long_name = ('instantaneous river water discharge downstream of '
                           'each river reach')
    h['Qout'].units = 'm3 s-1'
    h['Qout'].coordinates = 'lon lat'
    h['Qout'].grid_mapping = 'crs'
    h['Qout'].cell_methods = 'time: point'

    h.createVariable('time', 'int32', ('time',))
    h['time'].standard_name = 'time'
    h['time'].long_name = 'time'
    h['time'].units = 'seconds since 1970-01-01 00:00:00 +00:00'
    h['time'].axis = 'T'
    h['time'].calendar = 'gregorian'
    h['time'].bounds = 'time_bnds'

    # -------------------------------------------------------------------------
    # Copy old variables
    # -------------------------------------------------------------------------
    YV_exc = ['m3_riv', 'm3_riv_err', 'time_bnds', 'time']
    for nam, var in f.variables.items():
        if nam not in YV_exc:
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # Variables kept as is (time, time_bnds, crs)
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            h.createVariable(nam, var.datatype, var.dimensions)
            h[nam][:] = f[nam][:]

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # Copy variable attributes all at once via dictionary
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            h[nam].setncatts(f[nam].__dict__)

    # -------------------------------------------------------------------------
    # Populate time value
    # -------------------------------------------------------------------------
    h['time'][0] = f['time_bnds'][-1, 1]

    # -------------------------------------------------------------------------
    # Populate global attributes
    # -------------------------------------------------------------------------
    h.Conventions = f.Conventions
    h.title = f.title
    h.institution = f.institution
    h.source = 'RAPID2, ' + 'water inflow: ' + os.path.basename(m3r_ncf)
    h.history = 'date created: ' + YS_dat
    h.references = 'https://github.com/c-h-david/rapid2/'
    h.comment = ''
    h.featureType = f.featureType

    # -------------------------------------------------------------------------
    # Close all files
    # -------------------------------------------------------------------------
    f.close()
    h.close()


# *****************************************************************************
# End
# *****************************************************************************
