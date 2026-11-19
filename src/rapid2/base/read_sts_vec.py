#!/usr/bin/env python3
# *****************************************************************************
# read_sts_vec.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import netCDF4
import numpy as np
import numpy.typing as npt
from tqdm import tqdm


# *****************************************************************************
# Read hydrographs and compute performance metrics
# *****************************************************************************
def read_sts_vec(
    Qob_ncf: str,
    Qme_ncf: str,
) -> tuple[
    npt.NDArray[np.int32],
    npt.NDArray[np.float64],
    npt.NDArray[np.float64],
    npt.NDArray[np.float64],
    npt.NDArray[np.float64],
    npt.NDArray[np.float64],
    npt.NDArray[np.float64],
]:
    """Calculate and return hydrograph performance metrics.

    Reads observations (Qob) and model equivalents (Qme) step-by-step to
    preserve memory, accumulates sums directly into the final variable arrays,
    scales them into metrics, and returns the aligned river IDs along with
    their corresponding error statistics vectors.

    Parameters
    ----------
    Qob_ncf : str
        Path to the input observations (Qob) NetCDF file.
    Qme_ncf : str
        Path to the input model equivalent (Qme) NetCDF file.

    Returns
    -------
    IV_riv_avl : ndarray[int32]
        The river IDs of the available observation gauges.
    ZV_bia_avl : ndarray[float64]
        The mean of errors (bias) for each gauge.
    ZV_sdv_avl : ndarray[float64]
        The standard deviation of errors for each gauge.
    ZV_rms_avl : ndarray[float64]
        The Root Mean Square Error (RMSE) for each gauge.
    ZV_cor_avl : ndarray[float64]
        The Pearson correlation coefficient for each gauge.
    ZV_nse_avl : ndarray[float64]
        The Nash-Sutcliffe Efficiency (NSE) for each gauge.
    ZV_kge_avl : ndarray[float64]
        The modified Kling-Gupta Efficiency (MKGE) for each gauge.

    Examples
    --------
    >>> Qob_ncf = "input/Sandbox/Qob_Sandbox_19700101_19700110_TR.nc4"
    >>> Qme_ncf = "output/Sandbox/Qme_Sandbox_19700101_19700110_HY.nc4"
    >>> (
    ...     IV_riv_avl,
    ...     ZV_bia_avl,
    ...     ZV_sdv_avl,
    ...     ZV_rms_avl,
    ...     ZV_cor_avl,
    ...     ZV_nse_avl,
    ...     ZV_kge_avl,
    ... ) = read_sts_vec(Qob_ncf, Qme_ncf)
    >>> IV_riv_avl
    array([30, 50], dtype=int32)
    >>> np.round(ZV_bia_avl, 2)
    array([0., 0.])
    >>> np.round(ZV_sdv_avl, 2)
    array([0., 0.])
    >>> np.round(ZV_rms_avl, 2)
    array([0., 0.])
    >>> np.round(ZV_cor_avl, 2)
    array([1., 1.])
    >>> np.round(ZV_nse_avl, 2)
    array([1., 1.])
    >>> np.round(ZV_kge_avl, 2)
    array([1., 1.])
    """

    # -------------------------------------------------------------------------
    # Open files
    # -------------------------------------------------------------------------
    try:
        o = netCDF4.Dataset(Qob_ncf, "r")
    except IOError as err:
        raise IOError(f"Unable to open {Qob_ncf}") from err

    try:
        m = netCDF4.Dataset(Qme_ncf, "r")
    except IOError as err:
        raise IOError(f"Unable to open {Qme_ncf}") from err

    # -------------------------------------------------------------------------
    # Extract structural metadata
    # -------------------------------------------------------------------------
    IV_riv_avl = np.array(o.variables["rivid"][:], dtype=np.int32)
    IS_riv_avl = len(IV_riv_avl)
    IS_tim_all = o.dimensions["time"].size

    if "Qout" not in o.variables:
        raise ValueError(f"Qout variable does not exist in {Qob_ncf}")
    if "Qout" not in m.variables:
        raise ValueError(f"Qout variable does not exist in {Qme_ncf}")

    # -------------------------------------------------------------------------
    # Initialize nomenclature-compliant accumulators
    # -------------------------------------------------------------------------
    IV_val_tmp = np.zeros(IS_riv_avl, dtype=np.int32)
    ZV_Qob_avg = np.zeros(IS_riv_avl, dtype=np.float64)
    ZV_Qme_avg = np.zeros(IS_riv_avl, dtype=np.float64)
    ZV_Qob_sig = np.zeros(IS_riv_avl, dtype=np.float64)
    ZV_Qme_sig = np.zeros(IS_riv_avl, dtype=np.float64)
    ZV_Qme_Qob = np.zeros(IS_riv_avl, dtype=np.float64)
    ZV_rms_avl = np.zeros(IS_riv_avl, dtype=np.float64)

    # -------------------------------------------------------------------------
    # Stream data step-by-step
    # -------------------------------------------------------------------------
    for JS_tim_all in tqdm(range(IS_tim_all), desc="Accumulating statistics"):
        ZV_Qob_now = o.variables["Qout"][JS_tim_all, :]
        ZV_Qme_now = m.variables["Qout"][JS_tim_all, :]

        # Standardize to dense float64 arrays with 1e20 fill values
        if isinstance(ZV_Qob_now, np.ma.MaskedArray):
            ZV_Qob_now = ZV_Qob_now.filled(1e20)
        if isinstance(ZV_Qme_now, np.ma.MaskedArray):
            ZV_Qme_now = ZV_Qme_now.filled(1e20)

        ZV_Qob_now = ZV_Qob_now.astype(np.float64)
        ZV_Qme_now = ZV_Qme_now.astype(np.float64)

        # Identify valid overlapping data points
        BV_val_tmp = (ZV_Qob_now != 1e20) & (ZV_Qme_now != 1e20)

        # Mask invalid data so it contributes exactly 0 to the sum
        ZV_Qob_now = np.where(BV_val_tmp, ZV_Qob_now, 0.0)
        ZV_Qme_now = np.where(BV_val_tmp, ZV_Qme_now, 0.0)

        # Accumulate sums directly into the final arrays
        IV_val_tmp += BV_val_tmp.astype(np.int32)
        ZV_Qob_avg += ZV_Qob_now
        ZV_Qme_avg += ZV_Qme_now
        ZV_Qob_sig += ZV_Qob_now**2
        ZV_Qme_sig += ZV_Qme_now**2
        ZV_Qme_Qob += ZV_Qob_now * ZV_Qme_now

    # -------------------------------------------------------------------------
    # Overwrite accumulators with final statistical properties
    # -------------------------------------------------------------------------
    # Means
    ZV_Qob_avg = np.divide(
        ZV_Qob_avg,
        IV_val_tmp,
        out=np.zeros_like(ZV_Qob_avg),
        where=(IV_val_tmp > 0),
    )
    ZV_Qme_avg = np.divide(
        ZV_Qme_avg,
        IV_val_tmp,
        out=np.zeros_like(ZV_Qme_avg),
        where=(IV_val_tmp > 0),
    )

    # Standard Deviations
    ZV_Qob_sig = np.sqrt(
        np.maximum(
            0.0,
            np.divide(
                ZV_Qob_sig,
                IV_val_tmp,
                out=np.zeros_like(ZV_Qob_sig),
                where=(IV_val_tmp > 0),
            )
            - (ZV_Qob_avg**2),
        )
    )
    ZV_Qme_sig = np.sqrt(
        np.maximum(
            0.0,
            np.divide(
                ZV_Qme_sig,
                IV_val_tmp,
                out=np.zeros_like(ZV_Qme_sig),
                where=(IV_val_tmp > 0),
            )
            - (ZV_Qme_avg**2),
        )
    )

    # Covariance
    ZV_Qme_Qob = np.divide(
        ZV_Qme_Qob,
        IV_val_tmp,
        out=np.zeros_like(ZV_Qme_Qob),
        where=(IV_val_tmp > 0),
    ) - (ZV_Qob_avg * ZV_Qme_avg)

    # -------------------------------------------------------------------------
    # Close files
    # -------------------------------------------------------------------------
    o.close()
    m.close()

    # -------------------------------------------------------------------------
    # Compute metrics
    # -------------------------------------------------------------------------
    # 1. Bias (Mean Error)
    ZV_bia_avl = np.where(IV_val_tmp > 0, ZV_Qme_avg - ZV_Qob_avg, np.nan)

    # 2. Root Mean Square Error (RMSE)
    # MSE = Var(M) + Var(O) - 2*Cov(M,O) + Bias^2
    ZV_rms_avl = np.sqrt(
        np.maximum(
            0.0,
            (ZV_Qme_sig**2)
            + (ZV_Qob_sig**2)
            - (2.0 * ZV_Qme_Qob)
            + (ZV_bia_avl**2),
        )
    )
    ZV_rms_avl = np.where(IV_val_tmp > 0, ZV_rms_avl, np.nan)

    # 3. Standard Deviation of Error: Var(E) = RMSE^2 - Bias^2
    ZV_sdv_avl = np.sqrt(np.maximum(0.0, (ZV_rms_avl**2) - (ZV_bia_avl**2)))
    ZV_sdv_avl = np.where(IV_val_tmp > 0, ZV_sdv_avl, np.nan)

    # 4. Pearson Correlation
    ZV_den_cor = ZV_Qob_sig * ZV_Qme_sig
    ZV_cor_avl = np.divide(
        ZV_Qme_Qob,
        ZV_den_cor,
        out=np.zeros_like(ZV_Qme_Qob),
        where=(ZV_den_cor > 0),
    )
    ZV_cor_avl = np.where(
        (IV_val_tmp > 0) & (ZV_den_cor > 0), ZV_cor_avl, np.nan
    )

    # 5. Nash-Sutcliffe Efficiency (NSE)
    ZV_nse_avl = 1.0 - np.divide(
        ZV_rms_avl**2,
        ZV_Qob_sig**2,
        out=np.zeros_like(ZV_rms_avl),
        where=(ZV_Qob_sig > 0),
    )
    ZV_nse_avl = np.where(
        (IV_val_tmp > 0) & (ZV_Qob_sig > 0), ZV_nse_avl, np.nan
    )

    # 6. Kling-Gupta Efficiency (KGE)
    ZV_Alp = np.divide(
        ZV_Qme_sig,
        ZV_Qob_sig,
        out=np.zeros_like(ZV_Qme_sig),
        where=(ZV_Qob_sig > 0),
    )
    ZV_Bet = np.divide(
        ZV_Qme_avg,
        ZV_Qob_avg,
        out=np.zeros_like(ZV_Qme_avg),
        where=(ZV_Qob_avg != 0),
    )
    ZV_Gam = np.divide(
        ZV_Alp,
        ZV_Bet,
        out=np.zeros_like(ZV_Alp),
        where=(ZV_Bet != 0),
    )

    ZV_kge_avl = 1.0 - np.sqrt(
        (ZV_cor_avl - 1.0) ** 2 + (ZV_Gam - 1.0) ** 2 + (ZV_Bet - 1.0) ** 2
    )

    ZV_kge_avl = np.where(
        (IV_val_tmp > 0)
        & (ZV_Qob_sig > 0)
        & (ZV_Qob_avg != 0)
        & (ZV_Qme_avg != 0),
        ZV_kge_avl,
        np.nan,
    )

    # -------------------------------------------------------------------------
    # Return metrics
    # -------------------------------------------------------------------------
    return (
        IV_riv_avl,
        ZV_bia_avl,
        ZV_sdv_avl,
        ZV_rms_avl,
        ZV_cor_avl,
        ZV_nse_avl,
        ZV_kge_avl,
    )


# *****************************************************************************
# End
# *****************************************************************************
