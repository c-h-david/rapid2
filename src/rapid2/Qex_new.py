#!/usr/bin/env python3
# *****************************************************************************
# Qex_new.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import netCDF4  # type: ignore[import-untyped]
import numpy as np
import numpy.typing as npt

from rapid2.rud_new import rud_new


# *****************************************************************************
# Make external inflow volume (Qex) file
# *****************************************************************************
def Qex_new(
            IV_riv_tot: npt.NDArray[np.int32],
            ZV_lon_tot: npt.NDArray[np.float64],
            ZV_lat_tot: npt.NDArray[np.float64],
            Qex_ncf: str,
            ) -> None:
    '''Create a external inflow file with basic metadata.

    Create a external inflow file that includes basic metadata and has
    populated values for river ID, longitude, and latitude.

    Parameters
    ----------
    IV_riv_tot : ndarray[int32]
        The river IDs of the domain.
    ZV_lon_tot : ndarray[float64]
        The longitudes related to river IDs of the domain.
    ZV_lat_tot : ndarray[float64]
        The latitudes related to river IDs of the domain.
    Qex_ncf : str
        Path to the external inflow file.

    Returns
    -------
    None

    Examples
    --------
    >>> IV_riv_tot = np.array([10, 20, 30, 40, 50], dtype=np.int32)
    >>> ZV_lon_tot = np.array([0.5, 2.0, 1.0, 2.0, 0.5])
    >>> ZV_lat_tot = np.array([5.0, 4.5, 3.0, 2.5, 1.0])
    >>> Qex_ncf = './input/Sandbox/Qext_Sandbox_19700101_19700110_tst.nc4'
    >>> Qex_new(IV_riv_tot, ZV_lon_tot, ZV_lat_tot, Qex_ncf)
    >>> f = netCDF4.Dataset(Qex_ncf, 'r')
    >>> f.variables['rivid'][:].filled()
    array([10, 20, 30, 40, 50], dtype=int32)
    >>> f.variables['lon'][:].filled()
    array([0.5, 2. , 1. , 2. , 0.5])
    >>> f.variables['lat'][:].filled()
    array([5. , 4.5, 3. , 2.5, 1. ])
    >>> 'nv' in f.dimensions
    True
    >>> all(var in f.variables for var in ['Qext', 'time_bnds'])
    True
    >>> all(var in f.variables for var in ['Qext_bia', 'Qext_var', 'Qext_cov'])
    True
    >>> import os
    >>> os.remove(Qex_ncf)
    '''

    # -------------------------------------------------------------------------
    # Create rudimentary file
    # -------------------------------------------------------------------------
    rud_new(IV_riv_tot, ZV_lon_tot, ZV_lat_tot, Qex_ncf)

    # -------------------------------------------------------------------------
    # Open file to make changes
    # -------------------------------------------------------------------------
    f = netCDF4.Dataset(Qex_ncf, 'a')

    # -------------------------------------------------------------------------
    # Create dimensions
    # -------------------------------------------------------------------------
    f.createDimension('nv', 2)

    # -------------------------------------------------------------------------
    # Create variables
    # -------------------------------------------------------------------------
    ZS_fill = float(1e20)

    Qext = f.createVariable('Qext', 'float32', ('time', 'rivid',),
                            fill_value=ZS_fill)
    Qext.long_name = 'mean external water inflow upstream of each river reach'
    Qext.units = 'm3 s-1'
    Qext.coordinates = 'lon lat'
    Qext.grid_mapping = 'crs'
    Qext.cell_methods = 'time: mean'

    time_bnds = f.createVariable('time_bnds', 'int32', ('time', 'nv',))
    time_bnds.long_name = 'time bounds'

    time = f.variables['time']
    time.bounds = 'time_bnds'

    Qext_bia = f.createVariable('Qext_bia', 'float32', 'rivid',
                                fill_value=ZS_fill)
    Qext_bia.long_name = ('mean external water inflow error upstream of each '
                          'river reach')
    Qext_bia.units = 'm3 s-1'
    Qext_bia.coordinates = 'lon lat'
    Qext_bia.grid_mapping = 'crs'
    Qext_bia.cell_methods = 'time: mean'
    Qext_bia.window = 'applicable to entire period of simulation'
    Qext_bia.interval = 'temporal resolution does not impact computation'

    Qext_var = f.createVariable('Qext_var', 'float32', 'rivid',
                                fill_value=ZS_fill)
    Qext_var.long_name = ('variance of external water inflow error upstream '
                          'of each river reach')
    Qext_var.units = 'm6 s-2'
    Qext_var.coordinates = 'lon lat'
    Qext_var.grid_mapping = 'crs'
    Qext_var.cell_methods = 'time: variance'
    Qext_var.window = 'applicable to entire period of simulation'
    Qext_var.interval = 'typically same temporal resolution as observations'

    Qext_cov = f.createVariable('Qext_cov', 'float32', 'rivid',
                                fill_value=ZS_fill)
    Qext_cov.long_name = ('indicative covariance between external water '
                          'inflow error at a given reach and at another')
    Qext_cov.units = 'm6 s-2'
    Qext_cov.coordinates = 'lon lat'
    Qext_cov.grid_mapping = 'crs'
    Qext_cov.cell_methods = 'time: covariance'
    Qext_cov.window = 'applicable to entire period of simulation'
    Qext_cov.interval = 'typically same temporal resolution as observations'

    # -------------------------------------------------------------------------
    # Close file
    # -------------------------------------------------------------------------
    f.close()
    # Closing the new netCDF file allows populating all data


# *****************************************************************************
# End
# *****************************************************************************
