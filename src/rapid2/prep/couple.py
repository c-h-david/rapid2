#!/usr/bin/env python3
# *****************************************************************************
# couple.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import netCDF4
import numpy as np
from tqdm import tqdm

from rapid2.base import (
    chck_cpl,
    prep_Qex_ncf,
    read_con_vec,
    read_cpl_vec,
    read_crd_vec,
)


# *****************************************************************************
# Map Land Surface Model grids to river networks
# *****************************************************************************
def couple(
    lsm_ncf: str,
    con_pqt: str,
    crd_pqt: str,
    cpl_pqt: str,
    Qex_ncf: str,
) -> None:
    """Transform Land Surface Model data into RAPID external inflow input.

    Reads 2D Land Surface Model (LSM) runoff grids and calculates the flow into
    the 1D river network using pre-computed connectivity, coordinates, and
    coupling index arrays.

    Parameters
    ----------
    lsm_ncf : str
        Path to the input Land Surface Model (LSM) NetCDF file.
    con_pqt : str
        Path to the input connectivity Parquet file.
    crd_pqt : str
        Path to the input coordinates Parquet file.
    cpl_pqt : str
        Path to the input coupling Parquet file.
    Qex_ncf : str
        Path to the output external inflow (Qex) NetCDF file.

    Returns
    -------
    None

    Examples
    --------
    >>> lsm_ncf = "input/Tutorial/GLDAS_2.1_VIC_2010-01.nc4"
    >>> con_pqt = "input/Sandbox/con_Sandbox.parquet"
    >>> crd_pqt = "input/Sandbox/crd_Sandbox.parquet"
    >>> cpl_pqt = "input/Sandbox/cpl_Sandbox.parquet"
    >>> Qex_ncf = "output/Sandbox/Qex_Sandbox_tst.nc4"
    >>> couple(lsm_ncf, con_pqt, crd_pqt, cpl_pqt, Qex_ncf)  # doctest: +SKIP
    """

    # -------------------------------------------------------------------------
    # Read connectivity file
    # -------------------------------------------------------------------------
    IV_riv_tot, IV_dwn_tot = read_con_vec(con_pqt)

    # -------------------------------------------------------------------------
    # Read coordinate file
    # -------------------------------------------------------------------------
    IV_riv_tmp, ZV_lon_tot, ZV_lat_tot = read_crd_vec(crd_pqt)
    np.testing.assert_array_equal(IV_riv_tot, IV_riv_tmp)

    # -------------------------------------------------------------------------
    # Read coupling file
    # -------------------------------------------------------------------------
    IV_riv_tmp, ZV_skm_tot, IV_1bi_tot, IV_1bj_tot = read_cpl_vec(cpl_pqt)
    np.testing.assert_array_equal(IV_riv_tot, IV_riv_tmp)

    # -------------------------------------------------------------------------
    # Check consistency of coupling file
    # -------------------------------------------------------------------------
    chck_cpl(ZV_skm_tot, IV_1bi_tot, IV_1bj_tot)

    # -------------------------------------------------------------------------
    # Read LSM metadata
    # -------------------------------------------------------------------------
    try:
        c = netCDF4.Dataset(lsm_ncf, "r")
    except IOError as err:
        raise IOError(f"Unable to open {lsm_ncf}") from err

    IS_tim_all = len(c.dimensions["time"])

    if "Qs_acc" not in c.variables:
        raise ValueError("Qs_acc variable missing")

    if "Qsb_acc" not in c.variables:
        raise ValueError("Qsb_acc variable missing")

    # -------------------------------------------------------------------------
    # Create Qext file
    # -------------------------------------------------------------------------
    prep_Qex_ncf(IV_riv_tot, ZV_lon_tot, ZV_lat_tot, Qex_ncf)

    try:
        f = netCDF4.Dataset(Qex_ncf, "a")
    except IOError as err:
        raise IOError(f"Unable to open {Qex_ncf} for appending") from err

    # -------------------------------------------------------------------------
    # Populate dynamic data
    # -------------------------------------------------------------------------
    # Scale by 1000: product of 0.001 m/mm and 1,000,000 m^2/km^2.
    # This directly converts an input flux of mm/s (or kg*m^-2*s-1) and an
    # input area of km^2 into an output flow rate of m^3/s.
    ZV_scl_tot = 1000 * ZV_skm_tot

    # Shift to 0-based indexing; -1 entries have 0 area (chck_cpl.py).
    IV_0bi_tot = IV_1bi_tot - 1
    IV_0bj_tot = IV_1bj_tot - 1

    for JS_tim_all in tqdm(range(IS_tim_all), desc="Processing LSM data"):
        # netCDF data are stored as: c.variables[var][time][lat][lon]
        # ZM_run_lsm is of type 'np.ma.core.MaskedArray' or 'np.ndarray'
        # We here assume that runoff data inputs are in kg/m^2/s.
        ZM_rsf_lsm = c.variables["Qs_acc"][JS_tim_all][:][:]
        ZM_rsb_lsm = c.variables["Qsb_acc"][JS_tim_all][:][:]
        ZM_run_lsm = ZM_rsf_lsm + ZM_rsb_lsm

        # Uses the multidimensional list-of-locations indexing capability.
        # All values at given i and j indices can be obtained by giving two
        # lists of j and i indices.
        ZV_Qex_tot = ZM_run_lsm[IV_0bj_tot, IV_0bi_tot]

        # Result is now a true flow rate (m3/s) because input was a rate.
        ZV_Qex_tot = ZV_Qex_tot * ZV_scl_tot

        # Make sure the masked values are replaced by 0
        if isinstance(ZV_Qex_tot, np.ma.MaskedArray):
            ZV_Qex_tot = np.where(ZV_Qex_tot.mask, 0, ZV_Qex_tot.data)

        # netCDF data are stored following: f.variables[Qext][time][rivid]
        f.variables["Qext"][JS_tim_all, :] = ZV_Qex_tot[:]

    # From the LSM netCDF file
    f.variables["time"][:] = c.variables["time"][:]
    f.variables["time_bnds"][:] = c.variables["time_bnds"][:]

    # -------------------------------------------------------------------------
    # Copy global attributes
    # -------------------------------------------------------------------------
    for attr in ["title", "institution"]:
        if attr in c.ncattrs():
            f.setncattr(attr, c.getncattr(attr))

    # -------------------------------------------------------------------------
    # Close files
    # -------------------------------------------------------------------------
    c.close()
    f.close()


# *****************************************************************************
# End
# *****************************************************************************
