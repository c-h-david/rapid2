#!/usr/bin/env python3
# *****************************************************************************
# snd_Qex.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
import numpy.typing as npt
import netCDF4  # type: ignore[import-untyped]
from rapid2.Qex_new import Qex_new


# *****************************************************************************
# Make external inflow (Qext) file
# *****************************************************************************
def snd_Qex(
            IV_riv_tot: npt.NDArray[np.int32],
            ZV_lon_tot: npt.NDArray[np.float64],
            ZV_lat_tot: npt.NDArray[np.float64],
            IV_tim_tot: npt.NDArray[np.int32],
            ZS_avg: np.float64,
            ZS_amp: np.float64,
            Qex_ncf: str,
            ) -> None:
    '''Create a synthetic lateral inflow volume file.

    Create a synthetic lateral inflow volume file that is spatially uniform but
    temporally variable based on a given mean and amplitude.

    Parameters
    ----------
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
    >>> IV_tim_tot = np.array([i * 10800 for i in range(16)], dtype=np.int32)
    >>> IV_tim_tot = IV_tim_tot + np.int32(946684800)
    >>> ZS_avg = np.float64(1)
    >>> ZS_amp = np.float64(1)
    >>> Qex_ncf = './input/Test/Qext_Test_20000101_20000102_tst.nc4'
    >>> snd_Qex(IV_riv_tot, ZV_lon_tot, ZV_lat_tot, IV_tim_tot,\
                ZS_avg, ZS_amp,\
                Qex_ncf)
    >>> f = netCDF4.Dataset(Qex_ncf, 'r')
    >>> f.variables['rivid'][:].filled()
    array([10, 20, 30, 40, 50], dtype=int32)
    >>> f.variables['lon'][:].filled()
    array([0.5, 2. , 1. , 2. , 0.5])
    >>> f.variables['lat'][:].filled()
    array([5. , 4.5, 3. , 2.5, 1. ])
    >>> f.variables['time'][:].filled()
    array([946684800, 946695600, 946706400, 946717200, 946728000, 946738800,
           946749600, 946760400, 946771200, 946782000, 946792800, 946803600,
           946814400, 946825200, 946836000, 946846800], dtype=int32)
    >>> f.variables['time_bnds'][:, 1].filled()
    array([946695600, 946706400, 946717200, 946728000, 946738800, 946749600,
           946760400, 946771200, 946782000, 946792800, 946803600, 946814400,
           946825200, 946836000, 946846800, 946857600], dtype=int32)
    >>> f.variables['Qext'][:, 0].filled()
    array([0.        , 0.29289323, 1.        , 1.7071068 , 2.        ,
           1.7071068 , 1.        , 0.29289323, 0.        , 0.29289323,
           1.        , 1.7071068 , 2.        , 1.7071068 , 1.        ,
           0.29289323], dtype=float32)
    >>> import os
    >>> os.remove(Qex_ncf)
    '''

    # -------------------------------------------------------------------------
    # Create new Qext file
    # -------------------------------------------------------------------------
    Qex_new(IV_riv_tot, ZV_lon_tot, ZV_lat_tot, Qex_ncf)

    # -------------------------------------------------------------------------
    # Open file to make changes
    # -------------------------------------------------------------------------
    f = netCDF4.Dataset(Qex_ncf, 'a')

    # -------------------------------------------------------------------------
    # Populate variables
    # -------------------------------------------------------------------------
    time = f.variables['time']
    time_bnds = f.variables['time_bnds']
    Qex = f.variables['Qext']

    time[:] = IV_tim_tot[:]
    time_bnds[:, 0] = IV_tim_tot[:]
    time_bnds[:, 1] = IV_tim_tot[:] + IV_tim_tot[1] - IV_tim_tot[0]

    ZV_avg = ZS_avg * np.ones(len(IV_riv_tot))
    for JS_tim_tot in range(len(IV_tim_tot)):
        ZV_vol = ZV_avg + ZS_amp*np.cos(JS_tim_tot * 2 * np.pi / 8 + np.pi)
        Qex[JS_tim_tot, :] = ZV_vol[:]

    # -------------------------------------------------------------------------
    # Close file
    # -------------------------------------------------------------------------
    f.close()
    # Closing the new netCDF file allows populating all data


# *****************************************************************************
# End
# *****************************************************************************
