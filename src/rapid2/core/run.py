#!/usr/bin/env python3
# *****************************************************************************
# run.py
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
    calc_Kal_mat,
    calc_Nmn_mat,
    chck_bas,
    make_0bi_tbl,
    make_CCC_mat,
    make_dQe_mat,
    make_dQo_mat,
    make_Msk_mat,
    make_Net_mat,
    make_SA0_mat,
    make_SAe_mat,
    make_Sel_mat,
    prep_Qfi_ncf,
    prep_Qou_ncf,
    read_con_vec,
    read_err_vec,
    read_kpr_vec,
    read_riv_vec,
    read_std_vec,
    read_xpr_vec,
    updt_Mus_Qou,
)


# *****************************************************************************
# Core matrix routing model
# *****************************************************************************
def run(
    Q00_ncf: str,
    Qex_ncf: str,
    con_pqt: str,
    kpr_pqt: str,
    xpr_pqt: str,
    bas_pqt: str,
    IS_dtR: np.int32,
    Qou_ncf: str,
    Qfi_ncf: str,
    Qob_ncf: str | None = None,
    ZS_scl_inf: np.float64 | None = None,
    ZS_scl_sdv: np.float64 | None = None,
    ZS_lkm_cov: np.float64 | None = None,
) -> None:
    """Execute the core matrix-based Muskingum routing model.

    Computes the flow of water everywhere in the river network given
    external inflows. Supports Data Assimilation (DA) if observational
    data is provided.

    Parameters
    ----------
    Q00_ncf : str
        Path to the initial discharge NetCDF file.
    Qex_ncf : str
        Path to the external inflow NetCDF file.
    con_pqt : str
        Path to the network connectivity Parquet file.
    kpr_pqt : str
        Path to the Muskingum k parameter Parquet file.
    xpr_pqt : str
        Path to the Muskingum x parameter Parquet file.
    bas_pqt : str
        Path to the basin subset Parquet file.
    IS_dtR : np.int32
        The duration of the routing time step in seconds.
    Qou_ncf : str
        Path to the output discharge NetCDF file.
    Qfi_ncf : str
        Path to the final output discharge state NetCDF file.
    Qob_ncf : str or None, optional
        Path to the observed discharge NetCDF file for assimilation.
    ZS_scl_inf : np.float64 or None, optional
        Inflation scalar for errors in assimilation.
    ZS_scl_sdv : np.float64 or None, optional
        Standard deviation scalar for assimilation.
    ZS_lkm_cov : np.float64 or None, optional
        Correlation length scale for assimilation covariance in km.

    Returns
    -------
    None

    Examples
    --------
    >>> Q00_ncf = "input/Sandbox/Q00_Sandbox_19700101_19700110_FG.nc4"
    >>> Qex_ncf = "input/Sandbox/Qex_Sandbox_19700101_19700110_FG.nc4"
    >>> con_pqt = "input/Sandbox/con_Sandbox.parquet"
    >>> kpr_pqt = "input/Sandbox/kpr_Sandbox.parquet"
    >>> xpr_pqt = "input/Sandbox/xpr_Sandbox.parquet"
    >>> bas_pqt = "input/Sandbox/bas_Sandbox_ascend.parquet"
    >>> IS_dtR = np.int32(900)
    >>> Qou_ncf = "output/Sandbox/Qou_Sandbox_19700101_19700110_OL_tst.nc4"
    >>> Qfi_ncf = "output/Sandbox/Qfi_Sandbox_19700101_19700110_OL_tst.nc4"
    >>> run(
    ...     Q00_ncf,
    ...     Qex_ncf,
    ...     con_pqt,
    ...     kpr_pqt,
    ...     xpr_pqt,
    ...     bas_pqt,
    ...     IS_dtR,
    ...     Qou_ncf,
    ...     Qfi_ncf,
    ... )
    >>> from rapid2.eval import cmpncf
    >>> Qou_ref = "output/Sandbox/Qou_Sandbox_19700101_19700110_OL.nc4"
    >>> cmpncf(Qou_ref, Qou_ncf, np.float64(1e-10), np.float64(1e-10))
    >>> Qfi_ref = "output/Sandbox/Qfi_Sandbox_19700101_19700110_OL.nc4"
    >>> cmpncf(Qfi_ref, Qfi_ncf, np.float64(1e-10), np.float64(1e-10))
    >>> import os
    >>> os.remove(Qou_ncf)
    >>> os.remove(Qfi_ncf)
    """

    # -------------------------------------------------------------------------
    # River network
    # -------------------------------------------------------------------------
    IV_riv_tot, IV_dwn_tot = read_con_vec(con_pqt)
    IV_riv_bas = read_riv_vec(bas_pqt)
    IT_0bi_tot, IT_0bi_bas, IV_0bi_bas = make_0bi_tbl(IV_riv_tot, IV_riv_bas)
    ZM_Net = make_Net_mat(IV_dwn_tot, IT_0bi_tot, IV_riv_bas, IT_0bi_bas)

    # -------------------------------------------------------------------------
    # Model parameters
    # -------------------------------------------------------------------------
    IV_riv_tmp, ZV_kpr_bas = read_kpr_vec(kpr_pqt, IV_0bi_bas)
    np.testing.assert_array_equal(IV_riv_bas, IV_riv_tmp)

    IV_riv_tmp, ZV_xpr_bas = read_xpr_vec(xpr_pqt, IV_0bi_bas)
    np.testing.assert_array_equal(IV_riv_bas, IV_riv_tmp)

    ZM_C1p, ZM_C2p, ZM_C3p = make_CCC_mat(ZV_kpr_bas, ZV_xpr_bas, IS_dtR)
    ZM_ICN, ZM_Qex, ZM_Qou = make_Msk_mat(ZM_Net, ZM_C1p, ZM_C2p, ZM_C3p)

    # -------------------------------------------------------------------------
    # Extract metadata of external inflow and check IDs
    # -------------------------------------------------------------------------
    (
        IV_riv_tmp,
        ZV_lon_tot,
        ZV_lat_tot,
        IV_tim_all,
        IM_tim_all,
    ) = read_std_vec(Qex_ncf)
    np.testing.assert_array_equal(IV_riv_tot, IV_riv_tmp)

    # -------------------------------------------------------------------------
    # Extract metadata of initial value and check IDs and time
    # -------------------------------------------------------------------------
    IV_riv_tmp, _, _, IV_tim_tmp, _ = read_std_vec(Q00_ncf)
    np.testing.assert_array_equal(IV_riv_tot, IV_riv_tmp)
    np.testing.assert_equal(IV_tim_all[0], IV_tim_tmp[0])

    # -------------------------------------------------------------------------
    # Get time step correspondance
    # -------------------------------------------------------------------------
    IS_tim_all = len(IV_tim_all)

    if IM_tim_all is None:
        raise ValueError("read_std_vec returned None for IM_tim_all")
    # Use IM_tim_all instead of IV_tim_all which may have only one timestep
    IS_dtE = IM_tim_all[0, 1] - IM_tim_all[0, 0]

    if IS_dtE == 0:
        raise ValueError("Values of time_bnds lead to IS_dtE = 0")

    if IS_dtE % IS_dtR == 0:
        IS_rat_Qex = IS_dtE // IS_dtR
    else:
        raise ValueError("IS_dtE is not a multiple of IS_dtR")

    # -------------------------------------------------------------------------
    # Check upstream to downstream topology
    # -------------------------------------------------------------------------
    chck_bas(IV_riv_bas, IT_0bi_bas, IV_riv_tot, IV_dwn_tot, IT_0bi_tot)

    # -------------------------------------------------------------------------
    # Populate metadata for discharge output files
    # -------------------------------------------------------------------------
    prep_Qou_ncf(
        IV_riv_tot[IV_0bi_bas],
        ZV_lon_tot[IV_0bi_bas],
        ZV_lat_tot[IV_0bi_bas],
        Qou_ncf,
    )
    prep_Qfi_ncf(
        IV_riv_tot,
        ZV_lon_tot,
        ZV_lat_tot,
        Qfi_ncf,
    )

    # -------------------------------------------------------------------------
    # Uncertainty or Assimilation: Locate observations in basin
    # -------------------------------------------------------------------------
    if Qob_ncf is not None:
        # Extract metadata of observed flows
        (
            IV_riv_avl,
            _,
            _,
            IV_tim_obs,
            IM_tim_obs,
        ) = read_std_vec(Qob_ncf)

        # Find gauges that physically intersect the simulated basin
        IV_riv_act = IV_riv_avl[np.isin(IV_riv_avl, IV_riv_bas)]
        if len(IV_riv_act) == 0:
            raise ValueError("No valid overlapping gauges found in the basin")

        # Get 0-based indices of active gauges relative to observations
        _, _, IV_0bi_act = make_0bi_tbl(IV_riv_avl, IV_riv_act)

        # Build the Selection matrix mapping active gauges to basin reaches
        ZM_Sel = make_Sel_mat(IV_riv_act, IT_0bi_bas)

    # -------------------------------------------------------------------------
    # Uncertainty or Assimilation: Check temporal alignment of observations
    # -------------------------------------------------------------------------
    if Qob_ncf is not None:
        # Check for existence of time bounds
        if IM_tim_obs is None:
            raise ValueError("time_bnds is missing in Qob_ncf")

        # Check start times
        if IM_tim_all[0, 0] != IM_tim_obs[0, 0]:
            raise ValueError(
                f"Start times differ. Sim: {IM_tim_all[0, 0]}, "
                f"Obs: {IM_tim_obs[0, 0]}"
            )

        # Check time step of observations
        IS_dtO = IM_tim_obs[0, 1] - IM_tim_obs[0, 0]

        if IS_dtO == 0:
            raise ValueError("Values of time_bnds lead to IS_dtO = 0")

        if IS_dtO % IS_dtE != 0:
            raise ValueError("IS_dtO is not a multiple of IS_dtE")

        if IS_dtO % IS_dtR == 0:
            IS_rat_Qob = IS_dtO // IS_dtR
        else:
            raise ValueError("IS_dtO is not a multiple of IS_dtR")

    # -------------------------------------------------------------------------
    # Uncertainty or Assimilation: Zero-State Response Operator (H×Γ)
    # -------------------------------------------------------------------------
    if Qob_ncf is not None:
        # Compute the Muskingum operator (I - C1*N)^-1
        ZM_Mus = calc_Nmn_mat(ZM_C1p @ ZM_Net)

        # Compute the selection-multiplied input-to-state average matrix
        ZM_SAe = make_SAe_mat(ZM_Sel, ZM_Mus, ZM_Qex, ZM_Qou, IS_rat_Qob)

    # -------------------------------------------------------------------------
    # Uncertainty or Assimilation: Background error covariance (Pb)
    # -------------------------------------------------------------------------
    if Qob_ncf is not None:
        if ZS_lkm_cov is None:
            raise ValueError("ZS_lkm_cov required for data assimilation.")
        _, ZV_Qex_tmp = read_err_vec(Qex_ncf)
        ZV_Qex_sdv = ZV_Qex_tmp[IV_0bi_bas]
        ZM_dQe = make_dQe_mat(
            ZV_Qex_sdv,
            ZV_lon_tot[IV_0bi_bas],
            ZV_lat_tot[IV_0bi_bas],
            ZS_lkm_cov,
        )

    # -------------------------------------------------------------------------
    # Assimilation only: Zero-Input Response Operator (H×M)
    # -------------------------------------------------------------------------
    if Qob_ncf is not None:
        # Compute the selection-multiplied initial-to-state average matrix
        ZM_SA0 = make_SA0_mat(ZM_Sel, ZM_Mus, ZM_Qou, IS_rat_Qob)

    # -------------------------------------------------------------------------
    # Assimilation only: Observation error covariance (R)
    # -------------------------------------------------------------------------
    if Qob_ncf is not None:
        _, ZV_Qob_tmp = read_err_vec(Qob_ncf)
        ZV_Qob_sdv = ZV_Qob_tmp[IV_0bi_act]
        ZM_dQo = make_dQo_mat(ZV_Qob_sdv)

    # -------------------------------------------------------------------------
    # Assimilation only: Kalman Gain (K) and initialize inflow correction
    # -------------------------------------------------------------------------
    if Qob_ncf is not None:
        ZM_Kal = calc_Kal_mat(ZM_SAe, ZM_dQe, ZM_dQo)
        ZV_dQe_bas = np.zeros(len(IV_riv_bas), dtype=np.float64)

    # -------------------------------------------------------------------------
    # Open files
    # -------------------------------------------------------------------------
    try:
        e = netCDF4.Dataset(Q00_ncf, "r")
    except IOError as err:
        raise IOError(f"Unable to open {Q00_ncf}") from err

    try:
        f = netCDF4.Dataset(Qex_ncf, "r")
    except IOError as err:
        raise IOError(f"Unable to open {Qex_ncf}") from err

    try:
        g = netCDF4.Dataset(Qou_ncf, "a")
    except IOError as err:
        raise IOError(f"Unable to open {Qou_ncf}") from err

    try:
        h = netCDF4.Dataset(Qfi_ncf, "a")
    except IOError as err:
        raise IOError(f"Unable to open {Qfi_ncf}") from err

    if Qob_ncf is not None:
        try:
            o = netCDF4.Dataset(Qob_ncf, "r")
        except IOError as err:
            raise IOError(f"Unable to open {Qob_ncf}") from err

    # -------------------------------------------------------------------------
    # Read initial discharge state
    # -------------------------------------------------------------------------
    ZV_Qou_prv = e.variables["Qout"][0, IV_0bi_bas]

    # -------------------------------------------------------------------------
    # Run simulations
    # -------------------------------------------------------------------------
    for JS_tim_all in tqdm(range(IS_tim_all), desc="Computing discharge"):
        # Read external inflow
        ZV_Qex_avg = f.variables["Qext"][JS_tim_all][IV_0bi_bas]

        # Data Assimilation
        if Qob_ncf is not None and JS_tim_all % (IS_dtO // IS_dtE) == 0:
            JS_tim_obs = JS_tim_all // (IS_dtO // IS_dtE)
            ZV_Qob_now = o.variables["Qout"][JS_tim_obs, IV_0bi_act]
            ZV_Qex_tmp = f.variables["Qext"][
                JS_tim_all : JS_tim_all + (IS_dtO // IS_dtE), IV_0bi_bas
            ].mean(axis=0)
            ZV_Qme_tmp = ZM_SAe @ ZV_Qex_tmp + ZM_SA0 @ ZV_Qou_prv
            ZV_dQo_act = ZV_Qob_now - ZV_Qme_tmp
            ZV_dQe_bas = ZM_Kal @ ZV_dQo_act
        if Qob_ncf is not None:
            ZV_Qex_avg = ZV_Qex_avg + ZV_dQe_bas

        # Compute Qout
        ZV_Qou_avg, ZV_Qou_now = updt_Mus_Qou(
            ZM_ICN, ZM_Qex, ZM_Qou, IS_rat_Qex, ZV_Qou_prv, ZV_Qex_avg
        )
        ZV_Qou_prv = ZV_Qou_now

        # Populate Qout, time, and time_bnds
        g.variables["Qout"][JS_tim_all, :] = ZV_Qou_avg[:]
        g.variables["time"][JS_tim_all] = IV_tim_all[JS_tim_all]
        g.variables["time_bnds"][JS_tim_all, :] = IM_tim_all[JS_tim_all, :]

    # -------------------------------------------------------------------------
    # Save final discharge state
    # -------------------------------------------------------------------------
    h.variables["Qout"][0, IV_0bi_bas] = ZV_Qou_now[:]
    h.variables["time"][0] = IM_tim_all[-1, 1]

    # -------------------------------------------------------------------------
    # Copy some global attributes
    # -------------------------------------------------------------------------
    for attr in ["title", "institution"]:
        if attr in f.ncattrs():
            g.setncattr(attr, f.getncattr(attr))
            h.setncattr(attr, f.getncattr(attr))

    # -------------------------------------------------------------------------
    # Close files
    # -------------------------------------------------------------------------
    e.close()
    f.close()
    g.close()
    h.close()
    if Qob_ncf is not None:
        o.close()


# *****************************************************************************
# End
# *****************************************************************************
