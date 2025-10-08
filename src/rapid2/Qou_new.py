#!/usr/bin/env python3
# *****************************************************************************
# Qou_new.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
import numpy.typing as npt
import netCDF4  # type: ignore[import-untyped]
from rapid2.rud_new import rud_new


# *****************************************************************************
# Make lateral inflow volume (Qou) file
# *****************************************************************************
def Qou_new(
            IV_riv_bas: npt.NDArray[np.int32],
            ZV_lon_bas: npt.NDArray[np.float64],
            ZV_lat_bas: npt.NDArray[np.float64],
            Qou_ncf: str,
            ) -> None:
    '''Create a lateral inflow file with basic metadata.

    Create a lateral inflow file that includes basic metadata and populated
    values for river ID, longitude, and latitude.

    Parameters
    ----------
    IV_riv_bas : ndarray[int32]
        The river IDs of the domain.
    ZV_lon_bas : ndarray[float64]
        The longitudes related to river IDs of the domain.
    ZV_lat_bas : ndarray[float64]
        The latitudes related to river IDs of the domain.
    Qou_ncf : str
        Path to the discharge output file.

    Returns
    -------
    None

    Examples
    --------
    >>> IV_riv_bas = np.array([10, 20, 30, 40, 50], dtype=np.int32)
    >>> ZV_lon_bas = np.array([0.5, 2.0, 1.0, 2.0, 0.5])
    >>> ZV_lat_bas = np.array([5.0, 4.5, 3.0, 2.5, 1.0])
    >>> Qou_ncf = './output/Sandbox/Qout_Sandbox_19700101_19700110_tst.nc4'
    >>> Qou_new(IV_riv_bas, ZV_lon_bas, ZV_lat_bas, Qou_ncf)
    >>> f = netCDF4.Dataset(Qou_ncf, 'r')
    >>> f.variables['rivid'][:].filled()
    array([10, 20, 30, 40, 50], dtype=int32)
    >>> f.variables['lon'][:].filled()
    array([0.5, 2. , 1. , 2. , 0.5])
    >>> f.variables['lat'][:].filled()
    array([5. , 4.5, 3. , 2.5, 1. ])
    >>> 'nv' in f.dimensions
    True
    >>> all(var in f.variables for var in ['Qout', 'time_bnds'])
    True
    >>> all(var in f.variables for var in ['Qout_bia', 'Qout_var', 'Qout_cov'])
    True
    >>> import os
    >>> os.remove(Qou_ncf)
    '''

    # -------------------------------------------------------------------------
    # Create rudimentary file
    # -------------------------------------------------------------------------
    rud_new(IV_riv_bas, ZV_lon_bas, ZV_lat_bas, Qou_ncf)

    # -------------------------------------------------------------------------
    # Open file to make changes
    # -------------------------------------------------------------------------
    f = netCDF4.Dataset(Qou_ncf, 'a')

    # -------------------------------------------------------------------------
    # Create dimensions
    # -------------------------------------------------------------------------
    f.createDimension('nv', 2)

    # -------------------------------------------------------------------------
    # Create variables
    # -------------------------------------------------------------------------
    ZS_fill = float(1e20)

    Qout = f.createVariable('Qout', 'float32', ('time', 'rivid',),
                            fill_value=ZS_fill)
    Qout.long_name = 'mean river water outflow downstream of each river reach'
    Qout.units = 'm3 s-1'
    Qout.coordinates = 'lon lat'
    Qout.grid_mapping = 'crs'
    Qout.cell_methods = 'time: mean'

    time_bnds = f.createVariable('time_bnds', 'int32', ('time', 'nv',))
    time_bnds.long_name = 'time bounds'

    time = f.variables['time']
    time.bounds = 'time_bnds'

    Qout_bia = f.createVariable('Qout_bia', 'float32', 'rivid',
                                fill_value=ZS_fill)
    Qout_bia.long_name = ('mean river water outflow error downstream of each '
                          'river reach')
    Qout_bia.units = 'm3 s-1'
    Qout_bia.coordinates = 'lon lat'
    Qout_bia.grid_mapping = 'crs'
    Qout_bia.cell_methods = 'time: mean'
    Qout_bia.window = 'applicable to entire period of simulation'
    Qout_bia.interval = 'temporal resolution does not impact computation'

    Qout_var = f.createVariable('Qout_var', 'float32', 'rivid',
                                fill_value=ZS_fill)
    Qout_var.long_name = ('variance of river water outflow error downstream '
                          'of each river reach')
    Qout_var.units = 'm6 s-2'
    Qout_var.coordinates = 'lon lat'
    Qout_var.grid_mapping = 'crs'
    Qout_var.cell_methods = 'time: variance'
    Qout_var.window = 'applicable to entire period of simulation'
    Qout_var.interval = 'typically same temporal resolution as observations'

    Qout_cov = f.createVariable('Qout_cov', 'float32', 'rivid',
                                fill_value=ZS_fill)
    Qout_cov.long_name = ('indicative covariance between river water outflow '
                          'error at a given reach and at another')
    Qout_cov.units = 'm6 s-2'
    Qout_cov.coordinates = 'lon lat'
    Qout_cov.grid_mapping = 'crs'
    Qout_cov.cell_methods = 'time: covariance'
    Qout_cov.window = 'applicable to entire period of simulation'
    Qout_cov.interval = 'typically same temporal resolution as observations'

    # -------------------------------------------------------------------------
    # Close file
    # -------------------------------------------------------------------------
    f.close()
    # Closing the new netCDF file allows populating all data


# *****************************************************************************
# End
# *****************************************************************************
