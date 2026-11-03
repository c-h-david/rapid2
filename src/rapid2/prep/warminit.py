#!/usr/bin/env python3
# *****************************************************************************
# warminit.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import os

import netCDF4
import numpy as np
from scipy.sparse import identity
from scipy.sparse.linalg import spsolve
from tqdm import tqdm

from rapid2.base import (
    make_0bi_tbl,
    make_Net_mat,
    prep_Qfi_ncf,
    read_con_vec,
    read_riv_vec,
    read_std_vec,
)


# *****************************************************************************
# Generate Warm-Start State using Lumped Routing
# *****************************************************************************
def warminit(
    Qex_ncf: str,
    con_pqt: str,
    bas_pqt: str,
    Q00_ncf: str,
) -> None:
    """Create a warm initial discharge file from lumped routing of average Qex.

    Computes the long-term temporal average of external inflows, routes it
    through the river network assuming infinite wave celerity (lumped routing),
    and saves the resulting steady-state discharge as an initial state.

    Parameters
    ----------
    Qex_ncf : str
        Path to the input external inflow NetCDF file.
    con_pqt : str
        Path to the input connectivity Parquet file.
    bas_pqt : str
        Path to the input basin Parquet file.
    Q00_ncf : str
        Path to the output initial discharge NetCDF file.

    Returns
    -------
    None

    Examples
    --------
    >>> Qex_ncf = "./input/Sandbox/Qex_Sandbox_19700101_19700110_TR.nc4"
    >>> con_pqt = "./input/Sandbox/con_Sandbox.parquet"
    >>> bas_pqt = "./input/Sandbox/bas_Sandbox_ascend.parquet"
    >>> Q00_ncf = "./input/Sandbox/Q00_Sandbox_19700101_19700110_warm.nc4"
    >>> warminit(Qex_ncf, con_pqt, bas_pqt, Q00_ncf)
    >>> import os
    >>> os.path.exists(Q00_ncf)
    True
    >>> os.remove(Q00_ncf)
    """

    # -------------------------------------------------------------------------
    # Overwrite protection
    # -------------------------------------------------------------------------
    if os.path.exists(Q00_ncf):
        raise FileExistsError(f"File already exists: {Q00_ncf}")

    # -------------------------------------------------------------------------
    # River network and indexing
    # -------------------------------------------------------------------------
    IV_riv_tot, IV_dwn_tot = read_con_vec(con_pqt)
    IV_riv_bas = read_riv_vec(bas_pqt)
    IT_0bi_tot, IT_0bi_bas, IV_0bi_bas = make_0bi_tbl(IV_riv_tot, IV_riv_bas)
    ZM_Net = make_Net_mat(IV_dwn_tot, IT_0bi_tot, IV_riv_bas, IT_0bi_bas)

    # -------------------------------------------------------------------------
    # Extract metadata of external inflow
    # -------------------------------------------------------------------------
    (
        IV_riv_tmp,
        ZV_lon_tot,
        ZV_lat_tot,
        IV_tim_all,
        IM_tim_all,
    ) = read_std_vec(Qex_ncf)

    if not np.array_equal(IV_riv_tot, IV_riv_tmp):
        raise ValueError(f"River IDs in {Qex_ncf} must match {con_pqt}")

    # -------------------------------------------------------------------------
    # Compute average external inflow for the basin
    # -------------------------------------------------------------------------
    try:
        f = netCDF4.Dataset(Qex_ncf, "r")
    except IOError as err:
        raise IOError(f"Unable to open {Qex_ncf}") from err

    IS_tim_all = len(IV_tim_all)
    ZV_Qex_avg = np.zeros(len(IV_riv_bas), dtype=np.float64)

    for JS_tim_all in tqdm(range(IS_tim_all), desc="Averaging Qex"):
        ZV_Qex_avg += f.variables["Qext"][JS_tim_all][IV_0bi_bas]

    ZV_Qex_avg = ZV_Qex_avg / IS_tim_all

    # -------------------------------------------------------------------------
    # Perform lumped routing: (I - N) * Qou = Qex
    # -------------------------------------------------------------------------
    IS_riv_bas = len(IV_riv_bas)
    ZM_Idt = identity(IS_riv_bas, format="csc", dtype=np.float64)
    ZM_ImN = ZM_Idt - ZM_Net

    ZV_Qou_avg = spsolve(ZM_ImN, ZV_Qex_avg)

    # -------------------------------------------------------------------------
    # Create initial discharge file
    # -------------------------------------------------------------------------
    prep_Qfi_ncf(IV_riv_tot, ZV_lon_tot, ZV_lat_tot, Q00_ncf)

    try:
        e = netCDF4.Dataset(Q00_ncf, "a")
    except IOError as err:
        raise IOError(f"Unable to open {Q00_ncf}") from err

    e.variables["time"][0] = IV_tim_all[0]

    # Initialize all to zero, then overwrite basin reaches with lumped flows
    ZV_Q00_tot = np.zeros(len(IV_riv_tot), dtype=np.float64)
    ZV_Q00_tot[IV_0bi_bas] = ZV_Qou_avg[:]

    e.variables["Qout"][0, :] = ZV_Q00_tot[:]

    # -------------------------------------------------------------------------
    # Copy global attributes
    # -------------------------------------------------------------------------
    for attr in ["title", "institution"]:
        if attr in f.ncattrs():
            e.setncattr(attr, f.getncattr(attr))

    # -------------------------------------------------------------------------
    # Close files
    # -------------------------------------------------------------------------
    e.close()
    f.close()


# *****************************************************************************
# End
# *****************************************************************************
