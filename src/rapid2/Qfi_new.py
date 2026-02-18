#!/usr/bin/env python3
# *****************************************************************************
# Qfi_new.py
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
# Make lateral inflow volume (Qfi) file
# *****************************************************************************
def Qfi_new(
    IV_riv_tot: npt.NDArray[np.int32],
    ZV_lon_tot: npt.NDArray[np.float64],
    ZV_lat_tot: npt.NDArray[np.float64],
    Qfi_ncf: str,
) -> None:
    """Create instantaneous discharge file populated with basic metadata.

    Create an instantaneous discharge file that includes basic metadata and has
    populated values for river ID, longitude, and latitude.

    Parameters
    ----------
    IV_riv_tot : ndarray[int32]
        The river IDs of the domain.
    ZV_lon_tot : ndarray[float64]
        The longitudes related to river IDs of the domain.
    ZV_lat_tot : ndarray[float64]
        The latitudes related to river IDs of the domain.
    Qfi_ncf : str
        Path to the instantaneous discharge file.

    Returns
    -------
    None

    Examples
    --------
    >>> IV_riv_tot = np.array([10, 20, 30, 40, 50], dtype=np.int32)
    >>> ZV_lon_tot = np.array([0.5, 2.0, 1.0, 2.0, 0.5])
    >>> ZV_lat_tot = np.array([5.0, 4.5, 3.0, 2.5, 1.0])
    >>> Qfi_ncf = "./output/Sandbox/Qfinal_Sandbox_19700101_19700110_tst.nc4"
    >>> Qfi_new(IV_riv_tot, ZV_lon_tot, ZV_lat_tot, Qfi_ncf)
    >>> f = netCDF4.Dataset(Qfi_ncf, "r")
    >>> f.variables["rivid"][:].filled()
    array([10, 20, 30, 40, 50], dtype=int32)
    >>> f.variables["lon"][:].filled()
    array([0.5, 2. , 1. , 2. , 0.5])
    >>> f.variables["lat"][:].filled()
    array([5. , 4.5, 3. , 2.5, 1. ])
    >>> import os
    >>> os.remove(Qfi_ncf)
    """

    # -------------------------------------------------------------------------
    # Create rudimentary file
    # -------------------------------------------------------------------------
    rud_new(IV_riv_tot, ZV_lon_tot, ZV_lat_tot, Qfi_ncf)

    # -------------------------------------------------------------------------
    # Open file to make changes
    # -------------------------------------------------------------------------
    f = netCDF4.Dataset(Qfi_ncf, "a")

    # -------------------------------------------------------------------------
    # Create variables
    # -------------------------------------------------------------------------
    ZS_fill = float(1e20)

    Qout = f.createVariable(
        "Qout",
        "float64",
        (
            "time",
            "rivid",
        ),
        fill_value=ZS_fill,
    )
    Qout.long_name = (
        "instantaneous river water outflow downstream of each river reach"
    )
    Qout.units = "m3 s-1"
    Qout.coordinates = "lon lat"
    Qout.grid_mapping = "crs"
    Qout.cell_methods = "time: point"

    # -------------------------------------------------------------------------
    # Close file
    # -------------------------------------------------------------------------
    f.close()
    # Closing the new netCDF file allows populating all data


# *****************************************************************************
# End
# *****************************************************************************
