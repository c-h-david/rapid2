#!/usr/bin/env python3
# *****************************************************************************
# sample.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import netCDF4
import numpy as np
from tqdm import tqdm

from rapid2.base import (
    make_0bi_tbl,
    prep_Qou_ncf,
    read_riv_vec,
    read_std_vec,
)


# *****************************************************************************
# Sub-sample discharge output
# *****************************************************************************
def sample(
    Qou_ncf: str,
    obs_pqt: str,
    IS_dtO: np.int32,
    Qme_ncf: str,
) -> None:
    """Spatially and temporally sub-sample a discharge output (Qou) file.

    Creates model equivalents (Qme) for observations by matching spatial
    locations of gauges and temporally averaging high-resolution routing
    outputs.

    Parameters
    ----------
    Qou_ncf : str
        Path to the input outflow (Qou) NetCDF file.
    obs_pqt : str
        Path to the input observations (obs) Parquet file containing gauge IDs.
    IS_dtO : np.int32
        The observational time cadence in seconds (e.g., 86400).
    Qme_ncf : str
        Path to the output model equivalent (Qme) NetCDF file.

    Returns
    -------
    None

    Examples
    --------
    >>> Qou_ncf = "output/Sandbox/Qou_Sandbox_19700101_19700110_TR.nc4"
    >>> obs_pqt = "input/Sandbox/obs_Sandbox.parquet"
    >>> IS_dtO = np.int32(86400)
    >>> Qme_ncf = "output/Sandbox/Qme_Sandbox_19700101_19700110_tst.nc4"
    >>> sample(Qou_ncf, obs_pqt, IS_dtO, Qme_ncf)
    >>> from rapid2.eval import cmpncf
    >>> Qme_ref = "input/Sandbox/Qob_Sandbox_19700101_19700110_TR.nc4"
    >>> cmpncf(Qme_ref, Qme_ncf, np.float64(1e-10), np.float64(1e-10))
    >>> import os
    >>> os.remove(Qme_ncf)
    """

    # -------------------------------------------------------------------------
    # Read observational gauge IDs
    # -------------------------------------------------------------------------
    IV_riv_avl = read_riv_vec(obs_pqt)

    # -------------------------------------------------------------------------
    # Extract metadata from Qou_ncf and check spatial topology
    # -------------------------------------------------------------------------
    (
        IV_riv_bas,
        ZV_lon_bas,
        ZV_lat_bas,
        IV_tim_all,
        IM_tim_all,
    ) = read_std_vec(Qou_ncf)

    if IM_tim_all is None:
        raise ValueError(f"time_bnds is missing in {Qou_ncf}")

    # Map the observation IDs to their 0-based indices in the Qou file
    _, _, IV_0bi_avl = make_0bi_tbl(IV_riv_bas, IV_riv_avl)

    # Spatially subset coordinates
    ZV_lon_avl = ZV_lon_bas[IV_0bi_avl]
    ZV_lat_avl = ZV_lat_bas[IV_0bi_avl]

    # -------------------------------------------------------------------------
    # Determine temporal ratios
    # -------------------------------------------------------------------------
    IS_dtE = IM_tim_all[0, 1] - IM_tim_all[0, 0]
    IS_tim_all = len(IV_tim_all)

    if IS_dtO % IS_dtE != 0:
        raise ValueError(
            f"Target timestep ({IS_dtO}) is not a multiple of the "
            f"input timestep ({IS_dtE})"
        )

    IS_rat_Qob = IS_dtO // IS_dtE
    IS_tim_Qob = IS_tim_all // IS_rat_Qob

    # -------------------------------------------------------------------------
    # Create Qme file
    # -------------------------------------------------------------------------
    prep_Qou_ncf(IV_riv_avl, ZV_lon_avl, ZV_lat_avl, Qme_ncf)

    # -------------------------------------------------------------------------
    # Sub-sample data
    # -------------------------------------------------------------------------
    try:
        g = netCDF4.Dataset(Qou_ncf, "r")
    except IOError as err:
        raise IOError(f"Unable to open {Qou_ncf}") from err

    try:
        m = netCDF4.Dataset(Qme_ncf, "a")
    except IOError as err:
        raise IOError(f"Unable to open {Qme_ncf}") from err

    for JS_tim_Qob in tqdm(range(IS_tim_Qob), desc="Averaging discharge"):
        JS_tim_now = JS_tim_Qob * IS_rat_Qob

        # Extract the chunk and apply spatial filter simultaneously
        ZM_Qou_tmp = g.variables["Qout"][
            JS_tim_now : JS_tim_now + IS_rat_Qob, IV_0bi_avl
        ]

        # Calculate temporal mean across the specified window (axis 0)
        ZV_Qme_avg = np.mean(ZM_Qou_tmp, axis=0)

        # Write to Qme output
        m.variables["Qout"][JS_tim_Qob, :] = ZV_Qme_avg[:]

        # Write aligned time and bounds
        m.variables["time"][JS_tim_Qob] = g.variables["time"][JS_tim_now]
        m.variables["time_bnds"][JS_tim_Qob, 0] = g.variables["time_bnds"][
            JS_tim_now, 0
        ]
        m.variables["time_bnds"][JS_tim_Qob, 1] = g.variables["time_bnds"][
            JS_tim_now + IS_rat_Qob - 1, 1
        ]

    # -------------------------------------------------------------------------
    # Copy some global attributes
    # -------------------------------------------------------------------------
    for attr in ["title", "institution"]:
        if attr in g.ncattrs():
            m.setncattr(attr, g.getncattr(attr))

    # -------------------------------------------------------------------------
    # Close files
    # -------------------------------------------------------------------------
    g.close()
    m.close()


# *****************************************************************************
# End
# *****************************************************************************
