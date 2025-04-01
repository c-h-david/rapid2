#!/usr/bin/env python3
# *****************************************************************************
# fak_m3r.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
import numpy.typing as npt
import netCDF4  # type: ignore[import-untyped]
from datetime import datetime, timezone


# *****************************************************************************
# Make lateral inflow volume (m3_riv) file
# *****************************************************************************
def fak_m3r(
            m3r_ncf: str,
            IV_riv_tot: npt.NDArray[np.int32],
            ZV_lon_tot: npt.NDArray[np.float64],
            ZV_lat_tot: npt.NDArray[np.float64],
            IV_tim_tot: npt.NDArray[np.int32],
            ZS_avg: np.float64,
            ZS_amp: np.float64,
            ) -> None:
    '''Create a synthetic lateral inflow volume file.

    Create a synthetic lateral inflow volume file that is spatially uniform but
    temporally variable based on a given mean and amplitude.

    Parameters
    ----------
    m3r_ncf : str
        Path to the lateral inflow volume file.
    IV_riv_tot : ndarray[int32]
        The river IDs of the domain.
    ZV_lon_tot : ndarray[float64]
        The longitudes related to river IDs of the domain.
    ZV_lat_tot : ndarray[float64]
        The latitudes related to river IDs of the domain.
    IV_tim_tot : ndarray[int32]
        The epoch times of each lateral inflow time step.
    ZS_avg : float64
        The average volume entering the river IDs of the domain.
    ZS_amp : float64
        The volume amplitude entering the river IDs of the domain.

    Returns
    -------
    None

    Examples
    --------
    >>> m3r_ncf = './input/Test/m3_riv_Test_20000101_20000102_tst.nc4'
    >>> IV_riv_tot = np.array([10, 20, 30, 40, 50], dtype=np.int32)
    >>> ZV_lon_tot = np.array([0.5, 2.0, 1.0, 2.0, 0.5])
    >>> ZV_lat_tot = np.array([5.0, 4.5, 3.0, 2.5, 1.0])
    >>> IV_tim_tot = np.array([i * 10800 for i in range(16)], dtype=np.int32)
    >>> IV_tim_tot = IV_tim_tot + np.int32(946684800)
    >>> ZS_avg = np.float64(10800)
    >>> ZS_amp = np.float64(10800)
    >>> fak_m3r(m3r_ncf, IV_riv_tot, ZV_lon_tot, ZV_lat_tot, IV_tim_tot,\
                ZS_avg, ZS_amp)
    >>> m3r = netCDF4.Dataset(m3r_ncf, 'r')
    >>> m3r.variables['rivid'][:].filled()
    array([10, 20, 30, 40, 50], dtype=int32)
    >>> m3r.variables['lon'][:].filled()
    array([0.5, 2. , 1. , 2. , 0.5])
    >>> m3r.variables['lat'][:].filled()
    array([5. , 4.5, 3. , 2.5, 1. ])
    >>> m3r.variables['time'][:].filled()
    array([946684800, 946695600, 946706400, 946717200, 946728000, 946738800,
           946749600, 946760400, 946771200, 946782000, 946792800, 946803600,
           946814400, 946825200, 946836000, 946846800], dtype=int32)
    >>> m3r.variables['time_bnds'][:, 1].filled()
    array([946695600, 946706400, 946717200, 946728000, 946738800, 946749600,
           946760400, 946771200, 946782000, 946792800, 946803600, 946814400,
           946825200, 946836000, 946846800, 946857600], dtype=int32)
    >>> m3r.variables['m3_riv'][:, 0].filled()
    array([    0.    ,  3163.2468, 10800.    , 18436.754 , 21600.    ,
           18436.754 , 10800.    ,  3163.2468,     0.    ,  3163.2468,
           10800.    , 18436.754 , 21600.    , 18436.754 , 10800.    ,
            3163.2468], dtype=float32)
    >>> import os
    >>> os.remove(m3r_ncf)
    '''

    # -------------------------------------------------------------------------
    # Get UTC date and time
    # -------------------------------------------------------------------------
    YS_dat = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    # -------------------------------------------------------------------------
    # Create file
    # -------------------------------------------------------------------------
    m3r = netCDF4.Dataset(m3r_ncf, 'w', format='NETCDF4')

    # -------------------------------------------------------------------------
    # Create dimensions
    # -------------------------------------------------------------------------
    time = m3r.createDimension('time', None)
    rivid = m3r.createDimension('rivid', len(IV_riv_tot))
    m3r.createDimension('nv', 2)
    # no need to declare nv variable, never used here

    # -------------------------------------------------------------------------
    # Create variables
    # -------------------------------------------------------------------------
    ZS_fill_m3_riv = float(1e20)
    m3_riv = m3r.createVariable('m3_riv', 'float32', ('time', 'rivid',),
                                fill_value=ZS_fill_m3_riv)
    m3_riv.standard_name = 'm3'
    m3_riv.long_name = ('accumulated external water volume inflow upstream of '
                        'each river reach'
                        )
    m3_riv.units = 'm3'
    m3_riv.coordinates = 'lon lat'
    m3_riv.grid_mapping = 'crs'
    m3_riv.cell_methods = 'time: sum'

    rivid = m3r.createVariable('rivid', 'int32', ('rivid',))
    rivid.long_name = 'unique identifier for each river each'
    rivid.units = '1'
    rivid.cf_role = 'timeseries_id'

    time = m3r.createVariable('time', 'int32', ('time',))
    time.standard_name = 'time'
    time.long_name = 'time'
    time.units = 'seconds since 1970-01-01 00:00:00 +00:00'
    time.axis = 'T'
    time.calendar = 'gregorian'
    time.bounds = 'time_bnds'

    time_bnds = m3r.createVariable('time_bnds', 'int32', ('time', 'nv',))

    lon = m3r.createVariable('lon', 'float64', ('rivid',))
    lon.standard_name = 'longitude'
    lon.long_name = 'longitude of a point related to each river reach'
    lon.units = 'degrees_east'
    lon.axis = 'X'

    lat = m3r.createVariable('lat', 'float64', ('rivid',))
    lat.standard_name = 'latitude'
    lat.long_name = 'latitude of a point related to each river reach'
    lat.units = 'degrees_north'
    lat.axis = 'Y'

    crs = m3r.createVariable('crs', 'int32')
    crs.grid_mapping_name = 'latitude_longitude'
    crs.semi_major_axis = 6378137.
    crs.inverse_flattening = 298.257222101

    # -------------------------------------------------------------------------
    # Populate variables
    # -------------------------------------------------------------------------
    rivid[:] = IV_riv_tot[:]
    lon[:] = ZV_lon_tot[:]
    lat[:] = ZV_lat_tot[:]
    time[:] = IV_tim_tot[:]
    time_bnds[:, 0] = IV_tim_tot[:]
    time_bnds[:, 1] = IV_tim_tot[:] + IV_tim_tot[1] - IV_tim_tot[0]

    ZV_avg = ZS_avg * np.ones(len(IV_riv_tot))
    for JS_tim_tot in range(len(IV_tim_tot)):
        ZV_vol = ZV_avg + ZS_amp*np.cos(JS_tim_tot * 2 * np.pi / 8 + np.pi)
        m3_riv[JS_tim_tot, :] = ZV_vol[:]

    # -------------------------------------------------------------------------
    # Metadata in netCDF global attributes
    # -------------------------------------------------------------------------
    m3r.Conventions = 'CF-1.6'
    m3r.title = 'RAPID2 data corresponding to the Test basin'
    m3r.institution = (
                       'Jet Propulsion Laboratory, California Institute of '
                       'Technology'
                       )
    m3r.source = 'RAPID2, ' + 'water inflow: synthetic'
    m3r.history = 'date created: ' + YS_dat
    m3r.references = 'https://github.com/c-h-david/rapid2/'
    m3r.comment = ''
    m3r.featureType = 'timeSeries'

    # -------------------------------------------------------------------------
    # Close file
    # -------------------------------------------------------------------------
    m3r.close()
    # Closing the new netCDF file allows populating all data


# *****************************************************************************
# End
# *****************************************************************************
