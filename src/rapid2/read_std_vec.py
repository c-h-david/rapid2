#!/usr/bin/env python3
# *****************************************************************************
# read_std_vec.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import sys
from typing import Optional

import netCDF4  # type: ignore[import-untyped]
import numpy as np
import numpy.typing as npt


# *****************************************************************************
# Metadata of external inflow
# *****************************************************************************
def read_std_vec(
    std_ncf: str,
) -> tuple[
    npt.NDArray[np.int32],
    npt.NDArray[np.float64],
    npt.NDArray[np.float64],
    npt.NDArray[np.int32],
    Optional[npt.NDArray[np.int32]],
]:
    """Get core metadata from a RAPID-compatible netCDF file.

    Get standard metadata (river IDs, coordinates, time) from a
    RAPID-compatible netCDF file.

    Parameters
    ----------
    std_ncf : str
        Path to the RAPID netCDF file.

    Returns
    -------
    IV_riv_tot : ndarray[int32]
        The river IDs of the RAPID netCDF file.
    ZV_lon_tot : ndarray[float64]
        The longitudes of river IDs in the RAPID netCDF file.
    ZV_lat_tot : ndarray[float64]
        The latitudes of river IDs in the RAPID netCDF file.
    IV_tim_all : ndarray[int32]
        The epoch time values of the RAPID netCDF file.
    IM_tim_all : ndarray[int32]
        The epoch time bounds paired values of the RAPID netCDF file.

    Examples
    --------
    >>> std_ncf = './input/Sandbox/Qext_Sandbox_19700101_19700110.nc4'
    >>> (IV_riv_tot, ZV_lon_tot, ZV_lat_tot,\
         IV_tim_all, IM_tim_all) = read_std_vec(std_ncf)
    >>> IV_riv_tot
    array([10, 20, 30, 40, 50], dtype=int32)
    >>> ZV_lon_tot
    array([4.3 , 5.94, 5.12, 6.55, 4.3 ])
    >>> ZV_lat_tot
    array([8.2 , 8.2 , 5.12, 4.3 , 2.04])
    >>> IV_tim_all
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
    >>> IM_tim_all[:, 1]
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
    """

    s = netCDF4.Dataset(std_ncf, "r")

    # -------------------------------------------------------------------------
    # Check dimensions exist
    # -------------------------------------------------------------------------
    if "rivid" not in s.dimensions:
        print(f"ERROR - rivid dimension does not exist in {std_ncf}")
        sys.exit(1)

    if "time" not in s.dimensions:
        print(f"ERROR - time dimension does not exist in {std_ncf}")
        sys.exit(1)

    # -------------------------------------------------------------------------
    # Check variables exist
    # -------------------------------------------------------------------------
    if "rivid" not in s.variables:
        print(f"ERROR - rivid variable does not exist in {std_ncf}")
        sys.exit(1)

    if "lon" not in s.variables:
        print(f"ERROR - lon variable does not exist in {std_ncf}")
        sys.exit(1)

    if "lat" not in s.variables:
        print(f"ERROR - lat variable does not exist in {std_ncf}")
        sys.exit(1)

    if "time" not in s.variables:
        print(f"ERROR - time variable does not exist in {std_ncf}")
        sys.exit(1)

    if "Qext" not in s.variables and "Qout" not in s.variables:
        print(f"ERROR - No known main variable exist in {std_ncf}")
        sys.exit(1)

    # -------------------------------------------------------------------------
    # Retrieve variables
    # -------------------------------------------------------------------------
    IV_riv_tmp = s.variables["rivid"][:].filled()
    IV_riv_tot = np.array(IV_riv_tmp, dtype=np.int32)
    # Retrieving variables in two steps to better inform mypy

    ZV_lon_tmp = s.variables["lon"][:].filled()
    ZV_lon_tot = np.array(ZV_lon_tmp, dtype=np.float64)
    # Retrieving variables in two steps to better inform mypy

    ZV_lat_tmp = s.variables["lat"][:].filled()
    ZV_lat_tot = np.array(ZV_lat_tmp, dtype=np.float64)
    # Retrieving variables in two steps to better inform mypy

    IV_tim_tmp = s.variables["time"][:].filled()
    IV_tim_all = np.array(IV_tim_tmp, dtype=np.int32)
    # Retrieving variables in two steps to better inform mypy

    if "time_bnds" in s.variables:
        if "nv" not in s.dimensions:
            print(f"ERROR - nv dimension does not exist in {std_ncf}")
            sys.exit(1)
        if len(s.dimensions["nv"]) != 2:
            print(f"ERROR - nv dimension is not of size 2 in {std_ncf}")
            sys.exit(1)

        IM_tim_tmp = s.variables["time_bnds"][:].filled()
        IM_tim_all = np.array(IM_tim_tmp, dtype=np.int32)
        # Retrieving variables in two steps to better inform mypy
    else:
        IM_tim_all = None

    return IV_riv_tot, ZV_lon_tot, ZV_lat_tot, IV_tim_all, IM_tim_all


# *****************************************************************************
# End
# *****************************************************************************
