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
import sys


# *****************************************************************************
# Metadata of external inflow
# *****************************************************************************
def Qex_mdt(
            fil_ncf: str
            ) -> tuple[
                       npt.NDArray[np.int32],
                       npt.NDArray[np.float64],
                       npt.NDArray[np.float64],
                       npt.NDArray[np.int32],
                       npt.NDArray[np.int32],
                       ]:
    '''Get metadata from a RAPID netCDF file.

    Get metadata from a RAPID netCDF file: river IDs, longitudes, epoch time,
    epoch time bounds.

    Parameters
    ----------
    fil_ncf : str
        Path to the RAPID netCDF file.

    Returns
    -------
    IV_Qex_tot : ndarray[int32]
        The river IDs of the RAPID netCDF file.
    ZV_lon_tot : ndarray[float64]
        The longitudes of river IDs in the RAPID netCDF file.
    ZV_lat_tot : ndarray[float64]
        The latitudes of river IDs in the RAPID netCDF file.
    IV_Qex_tim : ndarray[int32]
        The epoch time values of the RAPID netCDF file.
    IM_Qex_tim : ndarray[int32]
        The epoch time bounds paired values of the RAPID netCDF file.

    Examples
    --------
    >>> fil_ncf = './input/Sandbox/Qext_Sandbox_19700101_19700110.nc4'
    >>> (IV_Qex_tot, ZV_lon_tot, ZV_lat_tot,\
         IV_Qex_tim, IM_Qex_tim) = Qex_mdt(fil_ncf)
    >>> IV_Qex_tot
    array([10, 20, 30, 40, 50], dtype=int32)
    >>> ZV_lon_tot
    array([4.3 , 5.94, 5.12, 6.55, 4.3 ])
    >>> ZV_lat_tot
    array([8.2 , 8.2 , 5.12, 4.3 , 2.04])
    >>> IV_Qex_tim
    array([     0,  10800,  21600,  32400,  43200,  54000,  64800,  75600,
            86400,  97200, 108000, 118800, 129600, 140400, 151200, 162000,
           172800, 183600, 194400, 205200, 216000, 226800, 237600, 248400,
           259200, 270000, 280800, 291600, 302400, 313200, 324000, 334800,
           345600, 356400, 367200, 378000, 388800, 399600, 410400, 421200,
           432000, 442800, 453600, 464400, 475200, 486000, 496800, 507600,
           518400, 529200, 540000, 550800, 561600, 572400, 583200, 594000,
           604800, 615600, 626400, 637200, 648000, 658800, 669600, 680400,
           691200, 702000, 712800, 723600, 734400, 745200, 756000, 766800,
           777600, 788400, 799200, 810000, 820800, 831600, 842400, 853200],
          dtype=int32)
    >>> IM_Qex_tim[:, 1]
    array([ 10800,  21600,  32400,  43200,  54000,  64800,  75600,  86400,
            97200, 108000, 118800, 129600, 140400, 151200, 162000, 172800,
           183600, 194400, 205200, 216000, 226800, 237600, 248400, 259200,
           270000, 280800, 291600, 302400, 313200, 324000, 334800, 345600,
           356400, 367200, 378000, 388800, 399600, 410400, 421200, 432000,
           442800, 453600, 464400, 475200, 486000, 496800, 507600, 518400,
           529200, 540000, 550800, 561600, 572400, 583200, 594000, 604800,
           615600, 626400, 637200, 648000, 658800, 669600, 680400, 691200,
           702000, 712800, 723600, 734400, 745200, 756000, 766800, 777600,
           788400, 799200, 810000, 820800, 831600, 842400, 853200, 864000],
          dtype=int32)
    '''

    f = netCDF4.Dataset(fil_ncf, 'r')

    # -------------------------------------------------------------------------
    # Check dimensions exist
    # -------------------------------------------------------------------------
    if 'rivid' not in f.dimensions:
        print('ERROR - rivid dimension does not exist in ' + fil_ncf)
        sys.exit(1)

    if 'time' not in f.dimensions:
        print('ERROR - time dimension does not exist in ' + fil_ncf)
        sys.exit(1)

    if 'nv' not in f.dimensions:
        print('ERROR - nv dimension does not exist in ' + fil_ncf)
        sys.exit(1)

    if len(f.dimensions['nv']) != 2:
        print('ERROR - nv dimension is not 2 ' + fil_ncf)
        sys.exit(1)

    # -------------------------------------------------------------------------
    # Check variables exist
    # -------------------------------------------------------------------------
    if 'rivid' not in f.variables:
        print('ERROR - rivid variable does not exist in ' + fil_ncf)
        sys.exit(1)

    if 'lon' not in f.variables:
        print('ERROR - lon variable does not exist in ' + fil_ncf)
        sys.exit(1)

    if 'lat' not in f.variables:
        print('ERROR - lat variable does not exist in ' + fil_ncf)
        sys.exit(1)

    if 'time' not in f.variables:
        print('ERROR - time variable does not exist in ' + fil_ncf)
        sys.exit(1)

    if 'time_bnds' not in f.variables:
        print('ERROR - time_bnds variable does not exist in ' + fil_ncf)
        sys.exit(1)

    if 'Qext' not in f.variables and 'Qout' not in f.variables:
        print('ERROR - No known main variable exist in ' + fil_ncf)
        sys.exit(1)

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

    return IV_Qex_tot, ZV_lon_tot, ZV_lat_tot, IV_Qex_tim, IM_Qex_tim


# *****************************************************************************
# End
# *****************************************************************************
