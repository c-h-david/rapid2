#!/usr/bin/env python3
# *****************************************************************************
# Qex_mdt.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
import numpy.typing as npt
import netCDF4  # type: ignore[import-untyped]


# *****************************************************************************
# Metadata of external inflow
# *****************************************************************************
def Qex_mdt(
            Qex_ncf: str
            ) -> tuple[
                       npt.NDArray[np.int32],
                       npt.NDArray[np.float64],
                       npt.NDArray[np.float64],
                       npt.NDArray[np.int32],
                       npt.NDArray[np.int32],
                       int,
                       np.int32
                       ]:
    '''Get metadata from external inflow file.

    Get metadata from external inflow file: river IDs, longitudes, epoch time,
    epoch time bounds, number of time steps, value of time step.

    Parameters
    ----------
    Qex_ncf : str
        Path to the external inflow file.

    Returns
    -------
    IV_Qex_tot : ndarray[int32]
        The river IDs of the external inflow file.
    ZV_lon_tot : ndarray[float64]
        The longitudes of river IDs in the external inflow file.
    ZV_lat_tot : ndarray[float64]
        The latitudes of river IDs in the external inflow file.
    IV_Qex_tim : ndarray[int32]
        The epoch time values of the external inflow file.
    IM_Qex_tim : ndarray[int32]
        The epoch time bounds paired values of the external inflow file.
    IS_Qex_tim : int
        The number of time steps of the external inflow file.
    IS_TaR : int32
       The time step of the external inflow file.

    Examples
    --------
    >>> Qex_ncf = './input/Test/Qext_Test_20000101_20000102.nc4'
    >>> (IV_Qex_tot, ZV_lon_tot, ZV_lat_tot, IV_Qex_tim, IM_Qex_tim,\
         IS_Qex_tim, IS_TaR) = Qex_mdt(Qex_ncf)
    >>> IV_Qex_tot
    array([10, 20, 30, 40, 50], dtype=int32)
    >>> ZV_lon_tot
    array([0.5, 2. , 1. , 2. , 0.5])
    >>> ZV_lat_tot
    array([5. , 4.5, 3. , 2.5, 1. ])
    >>> IV_Qex_tim
    array([946684800, 946695600, 946706400, 946717200, 946728000, 946738800,
           946749600, 946760400, 946771200, 946782000, 946792800, 946803600,
           946814400, 946825200, 946836000, 946846800], dtype=int32)
    >>> IM_Qex_tim[:, 1]
    array([946695600, 946706400, 946717200, 946728000, 946738800, 946749600,
           946760400, 946771200, 946782000, 946792800, 946803600, 946814400,
           946825200, 946836000, 946846800, 946857600], dtype=int32)
    >>> IS_Qex_tim
    16
    >>> IS_TaR
    np.int32(10800)
    '''

    f = netCDF4.Dataset(Qex_ncf, 'r')

    # -------------------------------------------------------------------------
    # Check dimensions exist
    # -------------------------------------------------------------------------
    if 'rivid' not in f.dimensions:
        print('ERROR - rivid dimension does not exist in ' + Qex_ncf)
        raise SystemExit(22)

    if 'time' not in f.dimensions:
        print('ERROR - time dimension does not exist in ' + Qex_ncf)
        raise SystemExit(22)

    if 'nv' not in f.dimensions:
        print('ERROR - nv dimension does not exist in ' + Qex_ncf)
        raise SystemExit(22)

    if len(f.dimensions['nv']) != 2:
        print('ERROR - nv dimension is not 2 ' + Qex_ncf)
        raise SystemExit(22)

    # -------------------------------------------------------------------------
    # Check variables exist
    # -------------------------------------------------------------------------
    if 'rivid' not in f.variables:
        print('ERROR - rivid variable does not exist in ' + Qex_ncf)
        raise SystemExit(22)

    if 'lon' not in f.variables:
        print('ERROR - lon variable does not exist in ' + Qex_ncf)
        raise SystemExit(22)

    if 'lat' not in f.variables:
        print('ERROR - lat variable does not exist in ' + Qex_ncf)
        raise SystemExit(22)

    if 'time' not in f.variables:
        print('ERROR - time variable does not exist in ' + Qex_ncf)
        raise SystemExit(22)

    if 'time_bnds' not in f.variables:
        print('ERROR - time_bnds variable does not exist in ' + Qex_ncf)
        raise SystemExit(22)

    if 'Qext' not in f.variables:
        print('ERROR - Qext variable does not exist in ' + Qex_ncf)
        raise SystemExit(22)

    # -------------------------------------------------------------------------
    # Retrieve variables
    # -------------------------------------------------------------------------
    IV_tmp = f.variables['rivid'][:].filled()
    IV_Qex_tot = np.array(IV_tmp, dtype=np.int32)
    # Retrieving variables in two steps to better inform mypy

    ZV_tmp = f.variables['lon'][:].filled()
    ZV_lon_tot = np.array(ZV_tmp, dtype=np.float64)
    # Retrieving variables in two steps to better inform mypy

    ZV_tmp = f.variables['lat'][:].filled()
    ZV_lat_tot = np.array(ZV_tmp, dtype=np.float64)
    # Retrieving variables in two steps to better inform mypy

    IV_tmp = f.variables['time'][:].filled()
    IV_Qex_tim = np.array(IV_tmp, dtype=np.int32)
    # Retrieving variables in two steps to better inform mypy

    IM_tmp = f.variables['time_bnds'][:].filled()
    IM_Qex_tim = np.array(IM_tmp, dtype=np.int32)
    # Retrieving variables in two steps to better inform mypy

    IS_Qex_tim = len(IV_Qex_tim)
    IS_TaR = IM_Qex_tim[0, 1] - IM_Qex_tim[0, 0]
    # Using IM_Qex_tim rather than IV_Qex_tim which may have only one timestep

    if IS_TaR == 0:
        print('ERROR - Values of time_bnds lead to IS_TaR=0 in ' + Qex_ncf)
        raise SystemExit(22)

    return (IV_Qex_tot, ZV_lon_tot, ZV_lat_tot, IV_Qex_tim, IM_Qex_tim,
            IS_Qex_tim, IS_TaR)


# *****************************************************************************
# End
# *****************************************************************************
