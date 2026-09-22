#!/usr/bin/env python3
# *****************************************************************************
# read_err_vec.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import netCDF4
import numpy as np
import numpy.typing as npt


# *****************************************************************************
# Read error statistics
# *****************************************************************************
def read_err_vec(
    std_ncf: str,
) -> tuple[
    npt.NDArray[np.float64],
    npt.NDArray[np.float64],
]:
    """Get bias and standard deviation vectors from a RAPID netCDF file.

    Get static error metadata (bias and standard deviation) mapped to river
    IDs from a RAPID-compatible netCDF file.

    Parameters
    ----------
    std_ncf : str
        Path to the RAPID netCDF file.

    Returns
    -------
    ZV_bia_tot : ndarray[float64]
        The bias vector for the domain.
    ZV_sdv_tot : ndarray[float64]
        The standard deviation vector for the domain.

    Examples
    --------
    >>> std_ncf = "./input/Sandbox/Qex_Sandbox_19700101_19700110_FG.nc4"
    >>> ZV_bia, ZV_sdv = read_err_vec(std_ncf)
    >>> ZV_bia
    array([  5.,   5.,   5., -15., -15.])
    >>> ZV_sdv
    array([10., 10., 10.,  5.,  5.])
    """

    s = netCDF4.Dataset(std_ncf, "r")

    # -------------------------------------------------------------------------
    # Discover variable prefix
    # -------------------------------------------------------------------------
    if "Qext_bia" in s.variables:
        YS_bia = "Qext_bia"
        YS_sdv = "Qext_sdv"
    elif "Qout_bia" in s.variables:
        YS_bia = "Qout_bia"
        YS_sdv = "Qout_sdv"
    else:
        raise ValueError(f"No known error variables exist in {std_ncf}")

    # -------------------------------------------------------------------------
    # Check standard deviation exists (bias presence confirmed above)
    # -------------------------------------------------------------------------
    if YS_sdv not in s.variables:
        raise ValueError(f"{YS_sdv} variable does not exist in {std_ncf}")

    # -------------------------------------------------------------------------
    # Retrieve variables and enforce float64 precision
    # -------------------------------------------------------------------------
    ZV_bia_tot = np.array(s.variables[YS_bia][:].filled(), dtype=np.float64)
    ZV_sdv_tot = np.array(s.variables[YS_sdv][:].filled(), dtype=np.float64)

    s.close()

    return ZV_bia_tot, ZV_sdv_tot


# *****************************************************************************
# End
# *****************************************************************************
