#!/usr/bin/env python3
# *****************************************************************************
# error.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import netCDF4
import numpy as np
from tqdm import tqdm


# *****************************************************************************
# Populate Error Standard Deviation
# *****************************************************************************
def error(
    std_ncf: str,
    ZS_scl: np.float64,
) -> None:
    """Populate the standard deviation of error field in a NetCDF file.

    Reads the main dynamic variable (Qext or Qout) from an existing RAPID
    NetCDF file iteratively to conserve memory, computes its mean absolute
    magnitude over time, and populates the corresponding standard deviation
    error field (Qext_sdv or Qout_sdv) in place as a scaled proportion.

    Parameters
    ----------
    std_ncf : str
        Path to the input and output NetCDF file to modify in place.
    ZS_scl : np.float64
        The scalar proportion used to multiply the mean magnitude.

    Returns
    -------
    None

    Examples
    --------
    >>> std_ncf = "output/Sandbox/Qou_Sandbox_19700101_19700110_tst.nc4"
    >>> ZS_scl = np.float64(0.15)
    >>> error(std_ncf, ZS_scl)  # doctest: +SKIP
    """

    # -------------------------------------------------------------------------
    # Open file to make changes
    # -------------------------------------------------------------------------
    try:
        f = netCDF4.Dataset(std_ncf, "a")
    except IOError as err:
        raise IOError(f"Unable to open {std_ncf} for appending") from err

    # -------------------------------------------------------------------------
    # Discover variable prefix
    # -------------------------------------------------------------------------
    if "Qext" in f.variables and "Qext_sdv" in f.variables:
        YS_val = "Qext"
        YS_sdv = "Qext_sdv"
    elif "Qout" in f.variables and "Qout_sdv" in f.variables:
        YS_val = "Qout"
        YS_sdv = "Qout_sdv"
    else:
        f.close()
        raise ValueError(f"No known main and error variables in {std_ncf}")

    # -------------------------------------------------------------------------
    # Get dimensions
    # -------------------------------------------------------------------------
    IS_tim_all = f.dimensions["time"].size
    IS_riv_tot = f.dimensions["rivid"].size

    # -------------------------------------------------------------------------
    # Compute mean magnitude iteratively and apply scalar
    # -------------------------------------------------------------------------
    ZV_val_avg = np.zeros(IS_riv_tot, dtype=np.float64)

    for JS_tim_all in tqdm(range(IS_tim_all), desc="Computing mean error"):
        ZV_val_avg += np.abs(f.variables[YS_val][JS_tim_all, :])

    ZV_val_avg = ZV_val_avg / IS_tim_all

    f.variables[YS_sdv][:] = ZV_val_avg * ZS_scl

    # -------------------------------------------------------------------------
    # Close file
    # -------------------------------------------------------------------------
    f.close()


# *****************************************************************************
# End
# *****************************************************************************
