#!/usr/bin/env python3
# *****************************************************************************
# sandbox.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import os

import netCDF4
import numpy as np
import numpy.typing as npt

from rapid2.base import prep_Qex_ncf


# *****************************************************************************
# Generate Synthetic External Inflow Data for Sandbox
# *****************************************************************************
def sandbox(
    ZV_scl_tot: npt.NDArray[np.float32],
    ZV_Qex_avg: npt.NDArray[np.float32],
    Qex_ncf: str,
    ZV_bia_tot: npt.NDArray[np.float32] | None = None,
    ZV_sdv_tot: npt.NDArray[np.float32] | None = None,
) -> None:
    """Generate synthetic external inflow data for the RAPID Sandbox.

    Parameters
    ----------
    ZV_scl_tot : ndarray[float32]
        Five unit-amplitude scaling values.
    ZV_Qex_avg : ndarray[float32]
        Five average values.
    Qex_ncf : str
        Path to the output external inflow NetCDF file.
    ZV_bia_tot : ndarray[float32] or None, optional
        Five bias error values (default is None, stored as fill values).
    ZV_sdv_tot : ndarray[float32] or None, optional
        Five standard deviation error values (default is None, stored as fill).

    Returns
    -------
    None

    Examples
    --------
    >>> ZV_scl_tot = np.array([5, 5, 5, 10, 10], dtype=np.float32)
    >>> ZV_Qex_avg = np.array([10, 10, 10, 20, 20], dtype=np.float32)
    >>> Qex_ncf = "./output/Sandbox/Qex_Sandbox_tst.nc4"
    >>> sandbox(ZV_scl_tot, ZV_Qex_avg, Qex_ncf)
    >>> import netCDF4
    >>> f = netCDF4.Dataset(Qex_ncf, "r")
    >>> f.variables["Qext"].shape
    (80, 5)
    >>> f.close()
    >>> import os
    >>> os.remove(Qex_ncf)
    """

    # -------------------------------------------------------------------------
    # Overwrite protection
    # -------------------------------------------------------------------------
    if os.path.exists(Qex_ncf):
        raise FileExistsError(f"File already exists: {Qex_ncf}")

    # -------------------------------------------------------------------------
    # Hardcoded Sandbox values
    # -------------------------------------------------------------------------
    IV_riv_tot = np.array([10, 20, 30, 40, 50], dtype=np.int32)
    ZV_lon_tot = np.array([4.30, 5.94, 5.12, 6.55, 4.30])
    ZV_lat_tot = np.array([8.20, 8.20, 5.12, 4.30, 2.04])
    IV_tim_all = np.array(range(80), dtype=np.int32) * np.int32(10800)

    # -------------------------------------------------------------------------
    # Array sizes and checks
    # -------------------------------------------------------------------------
    IS_riv_tot = len(IV_riv_tot)
    IS_tim_all = len(IV_tim_all)

    if len(ZV_scl_tot) != IS_riv_tot:
        raise ValueError(
            f"Unit-amplitude scaling array not of size {IS_riv_tot}."
        )

    if len(ZV_Qex_avg) != IS_riv_tot:
        raise ValueError(f"Average array not of size {IS_riv_tot}.")

    if ZV_bia_tot is None:
        ZV_bia_tot = np.full(IS_riv_tot, 1e20, dtype=np.float32)

    if ZV_sdv_tot is None:
        ZV_sdv_tot = np.full(IS_riv_tot, 1e20, dtype=np.float32)

    # -------------------------------------------------------------------------
    # Create Qext file
    # -------------------------------------------------------------------------
    prep_Qex_ncf(IV_riv_tot, ZV_lon_tot, ZV_lat_tot, Qex_ncf)

    # -------------------------------------------------------------------------
    # Populate Qext file ('f' handle per NOMENCLATURE.md)
    # -------------------------------------------------------------------------
    try:
        f = netCDF4.Dataset(Qex_ncf, "a")
    except IOError as err:
        raise IOError(f"Unable to open {Qex_ncf}") from err

    f.variables["time"][:] = IV_tim_all[:]

    f.variables["time_bnds"][:, 0] = IV_tim_all[:]
    f.variables["time_bnds"][:, 1] = IV_tim_all[:] + np.int32(10800)

    f.variables["Qext_bia"][:] = ZV_bia_tot[:]
    f.variables["Qext_sdv"][:] = ZV_sdv_tot[:]

    for JS_tim_all in range(IS_tim_all):
        # The 1e-7 avoids np.sign(0) = 0
        ZV_Qex_tmp = np.sign(
            np.sin(np.pi / 86400 * IV_tim_all[JS_tim_all] + 1e-7)
        )
        ZV_Qex_tmp = ZV_Qex_tmp * ZV_scl_tot
        ZV_Qex_tmp = ZV_Qex_tmp + ZV_Qex_avg
        f.variables["Qext"][JS_tim_all, :] = ZV_Qex_tmp[:]

    f.title = "Sandbox dataset for RAPID2"
    f.institution = (
        "Jet Propulsion Laboratory, California Institute of Technology"
    )

    # -------------------------------------------------------------------------
    # Close file
    # -------------------------------------------------------------------------
    f.close()


# *****************************************************************************
# End
# *****************************************************************************
