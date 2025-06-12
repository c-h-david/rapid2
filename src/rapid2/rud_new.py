#!/usr/bin/env python3
# *****************************************************************************
# rud_new.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2025


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
import numpy.typing as npt
import netCDF4  # type: ignore[import-untyped]
from datetime import datetime, timezone


# *****************************************************************************
# Make external inflow volume (rud) file
# *****************************************************************************
def rud_new(
            IV_riv: npt.NDArray[np.int32],
            ZV_lon: npt.NDArray[np.float64],
            ZV_lat: npt.NDArray[np.float64],
            rud_ncf: str,
            ) -> None:
    '''Create rudimentary netCDF file following CF conventions for RAPID.

    Create a rudimentary netCDF file following the CF conventions for
    timeseries with basic metadata and populated values for river ID,
    longitude, and latitude.

    Parameters
    ----------
    IV_riv : ndarray[int32]
        The river IDs of the domain.
    ZV_lon : ndarray[float64]
        The longitudes related to river IDs.
    ZV_lat : ndarray[float64]
        The latitudes related to river IDs.
    rud_ncf : str
        Path to the rudimentary netCDF file.

    Returns
    -------
    None

    Examples
    --------
    >>> IV_riv = np.array([10, 20, 30, 40, 50], dtype=np.int32)
    >>> ZV_lon = np.array([0.5, 2.0, 1.0, 2.0, 0.5])
    >>> ZV_lat = np.array([5.0, 4.5, 3.0, 2.5, 1.0])
    >>> rud_ncf = './input/Test/rud_Test_20000101_20000102_tst.nc4'
    >>> rud_new(IV_riv, ZV_lon, ZV_lat, rud_ncf)
    >>> f = netCDF4.Dataset(rud_ncf, 'r')
    >>> f.variables['rivid'][:].filled()
    array([10, 20, 30, 40, 50], dtype=int32)
    >>> f.variables['lon'][:].filled()
    array([0.5, 2. , 1. , 2. , 0.5])
    >>> f.variables['lat'][:].filled()
    array([5. , 4.5, 3. , 2.5, 1. ])
    >>> import os
    >>> os.remove(rud_ncf)
    '''

    # -------------------------------------------------------------------------
    # Get UTC date and time
    # -------------------------------------------------------------------------
    YS_dat = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    # -------------------------------------------------------------------------
    # Create file
    # -------------------------------------------------------------------------
    f = netCDF4.Dataset(rud_ncf, 'w', format='NETCDF4')

    # -------------------------------------------------------------------------
    # Create dimensions
    # -------------------------------------------------------------------------
    f.createDimension('time', None)
    f.createDimension('rivid', len(IV_riv))

    # -------------------------------------------------------------------------
    # Create variables
    # -------------------------------------------------------------------------
    time = f.createVariable('time', 'int32', ('time',))
    time.standard_name = 'time'
    time.long_name = 'time'
    time.units = 'seconds since 1970-01-01 00:00:00 +00:00'
    time.axis = 'T'
    time.calendar = 'gregorian'

    rivid = f.createVariable('rivid', 'int32', ('rivid',))
    rivid.long_name = 'unique identifier for each river each'
    rivid.units = '1'
    rivid.cf_role = 'timeseries_id'

    lon = f.createVariable('lon', 'float64', ('rivid',))
    lon.standard_name = 'longitude'
    lon.long_name = 'longitude of a point related to each river reach'
    lon.units = 'degrees_east'
    lon.axis = 'X'

    lat = f.createVariable('lat', 'float64', ('rivid',))
    lat.standard_name = 'latitude'
    lat.long_name = 'latitude of a point related to each river reach'
    lat.units = 'degrees_north'
    lat.axis = 'Y'

    crs = f.createVariable('crs', 'int32')
    crs.grid_mapping_name = 'latitude_longitude'
    crs.semi_major_axis = 6378137.
    crs.inverse_flattening = 298.257222101

    # -------------------------------------------------------------------------
    # Populate variables
    # -------------------------------------------------------------------------
    rivid[:] = IV_riv[:]
    lon[:] = ZV_lon[:]
    lat[:] = ZV_lat[:]

    # -------------------------------------------------------------------------
    # Metadata in netCDF global attributes
    # -------------------------------------------------------------------------
    f.Conventions = 'CF-1.6'
    f.title = ''
    f.institution = ''
    f.source = 'RAPID2'
    f.history = 'date created: ' + YS_dat
    f.references = 'https://github.com/c-h-david/rapid2/'
    f.comment = ''
    f.featureType = 'timeSeries'

    # -------------------------------------------------------------------------
    # Close file
    # -------------------------------------------------------------------------
    f.close()
    # Closing the new netCDF file allows populating all data


# *****************************************************************************
# End
# *****************************************************************************
