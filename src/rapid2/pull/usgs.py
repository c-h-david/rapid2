#!/usr/bin/env python3
# *****************************************************************************
# usgs.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import json
import urllib.parse
import urllib.request
import warnings
from datetime import datetime, timezone
from typing import TypedDict

import netCDF4
import numpy as np
import pyarrow.parquet as pq
from tqdm import tqdm

from rapid2.base import prep_Qou_ncf


# *****************************************************************************
# Download and Preprocess USGS Daily Discharge Data
# *****************************************************************************
def usgs(
    obs_pqt: str,
    YS_tim_beg: str,
    YS_tim_end: str,
    Qob_ncf: str,
) -> None:
    """Download USGS daily discharge data into a RAPID observations file.

    Reads a Parquet file containing river IDs and USGS gauge codes, queries
    the modern USGS JSON web service for daily discharge (statCd=00003,
    parameterCd=00060), and saves the results in a RAPID-compatible Qob_ncf
    netCDF file in cubic meters per second (m3 s-1).

    Parameters
    ----------
    obs_pqt : str
        Path to the input Parquet file containing 'riv' and 'cod' columns.
    YS_tim_beg : str
        The start date for the data retrieval formatted as 'YYYY-MM-DD'.
    YS_tim_end : str
        The end date for the data retrieval formatted as 'YYYY-MM-DD'.
    Qob_ncf : str
        Path to the output observations (Qob) NetCDF file.

    Returns
    -------
    None

    Examples
    --------
    >>> obs_pqt = "input/Sandbox/obs_USGS.parquet"
    >>> YS_tim_beg = "2023-01-01"
    >>> YS_tim_end = "2023-01-02"
    >>> Qob_ncf = "output/Sandbox/Qob_USGS_20230101_20230110_tst.nc4"
    >>> usgs(obs_pqt, YS_tim_beg, YS_tim_end, Qob_ncf)  # doctest: +SKIP
    # TODO: Replace +SKIP with test execution once dummy files are mounted.
    """

    # -------------------------------------------------------------------------
    # Read observation gauge IDs and codes from Parquet
    # -------------------------------------------------------------------------
    try:
        table = pq.read_table(obs_pqt, columns=["riv", "cod"])
    except IOError as err:
        raise IOError(f"Unable to open {obs_pqt}") from err

    IV_riv_avl = table.column("riv").to_numpy().astype(np.int32)
    YV_cod_avl = table.column("cod").to_pylist()
    IS_riv_avl = len(IV_riv_avl)

    # -------------------------------------------------------------------------
    # Generate continuous daily time vectors
    # -------------------------------------------------------------------------
    # Compute beginning epoch time
    IS_beg = int(
        datetime.strptime(YS_tim_beg, "%Y-%m-%d")
        .replace(tzinfo=timezone.utc)
        .timestamp()
    )

    # Compute end epoch time
    IS_end = int(
        datetime.strptime(YS_tim_end, "%Y-%m-%d")
        .replace(tzinfo=timezone.utc)
        .timestamp()
    )

    # Generate daily steps (86400 seconds)
    IV_tim_all = np.arange(IS_beg, IS_end + 86400, 86400, dtype=np.int32)
    IS_tim_all = len(IV_tim_all)

    # Create mapping from timestamp to row index
    IT_0bi_tim = {time: idx for idx, time in enumerate(IV_tim_all)}

    # -------------------------------------------------------------------------
    # Construct and execute USGS JSON web service queries
    # -------------------------------------------------------------------------
    ObsDic = TypedDict(
        "ObsDic",
        {
            "lon": float,
            "lat": float,
            "tim": list[str],
            "val": list[float],
            "qlf": list[str],
        },
    )
    AT_obs: dict[str, ObsDic] = {}

    for YS_cod_req in tqdm(YV_cod_avl, desc="Downloading USGS Data"):
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Download individual timeseries
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        YS_url = "https://waterservices.usgs.gov/nwis/dv/"

        payload = {
            "format": "json",
            "sites": YS_cod_req,
            "startDT": YS_tim_beg,
            "endDT": YS_tim_end,
            "parameterCd": "00060",  # Discharge, cubic feet per second
            "statCd": "00003",  # Mean daily value
        }

        YS_url = f"{YS_url}?{urllib.parse.urlencode(payload)}"

        try:
            with urllib.request.urlopen(YS_url, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as err:
            warnings.warn(
                f"Failed to query USGS API: {YS_url} - {err}",
                stacklevel=2,
            )
            continue

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Clean up the bloated USGS JSON into a more simplified dictionary
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        data = data["value"]["timeSeries"]

        for item in data:
            YS_cod = item["sourceInfo"]["siteCode"][0]["value"]
            ZS_lon = float(
                item["sourceInfo"]["geoLocation"]["geogLocation"]["longitude"]
            )

            ZS_lat = float(
                item["sourceInfo"]["geoLocation"]["geogLocation"]["latitude"]
            )

            YV_tim = [
                record["dateTime"] for record in item["values"][0]["value"]
            ]

            ZV_val = [
                float(record["value"]) for record in item["values"][0]["value"]
            ]

            YV_qlf = [
                ",".join(record["qualifiers"])
                for record in item["values"][0]["value"]
            ]

            AT_obs[YS_cod] = {
                "lon": ZS_lon,
                "lat": ZS_lat,
                "tim": YV_tim,
                "val": ZV_val,
                "qlf": YV_qlf,
            }

    # -------------------------------------------------------------------------
    # Initialize arrays for discharge and coordinates
    # -------------------------------------------------------------------------
    ZM_Qob_all = np.full((IS_tim_all, IS_riv_avl), 1e20, dtype=np.float32)
    ZV_lon_avl = np.full(IS_riv_avl, 1e20, dtype=np.float64)
    ZV_lat_avl = np.full(IS_riv_avl, 1e20, dtype=np.float64)

    # -------------------------------------------------------------------------
    # Populate arrays using explicitly requested gauges
    # -------------------------------------------------------------------------
    for JS_riv_avl in range(IS_riv_avl):
        YS_cod = YV_cod_avl[JS_riv_avl]
        if YS_cod not in AT_obs:
            warnings.warn(
                f"No data returned for gauge {YS_cod}.",
                stacklevel=2,
            )
            # Skip the rest of the loop for this missing gauge. Its matrix
            # column will safely remain populated with the default 1e20.
            continue

        ZV_lon_avl[JS_riv_avl] = AT_obs[YS_cod]["lon"]
        ZV_lat_avl[JS_riv_avl] = AT_obs[YS_cod]["lat"]

        for YS_tim, ZS_val, YS_qlf in zip(
            AT_obs[YS_cod]["tim"],
            AT_obs[YS_cod]["val"],
            AT_obs[YS_cod]["qlf"],
            strict=True,
        ):
            # Strictly filter for Approved ('A') data
            if "A" not in YS_qlf:
                ZS_val = 1e20

            # Convert cubic feet per second to cubic meters per second except
            # for NoData points
            if ZS_val != 1e20:
                ZS_val = ZS_val * (0.3048**3)

            # Slice [:10] to strip local timezones. This assumes local daily
            # means represent UTC days, which is necessary to cleanly snap the
            # records to the strict UTC time vector used by the model
            IS_tim = np.int32(
                datetime.strptime(YS_tim[:10], "%Y-%m-%d")
                .replace(tzinfo=timezone.utc)
                .timestamp()
            )

            if IS_tim in IT_0bi_tim:
                JS_tim_all = IT_0bi_tim[IS_tim]
                ZM_Qob_all[JS_tim_all, JS_riv_avl] = ZS_val

    # -------------------------------------------------------------------------
    # (Testing) Print data availability summary per gauge
    # -------------------------------------------------------------------------
    for JS_riv_avl in range(IS_riv_avl):
        YS_cod = YV_cod_avl[JS_riv_avl]
        IS_tmp = np.sum(ZM_Qob_all[:, JS_riv_avl] != 1e20)
        ZS_tmp = (IS_tmp / IS_tim_all) * 100
        print(
            f"Gauge {YS_cod}: {IS_tmp}/{IS_tim_all} valid days ({ZS_tmp:.1f}%)"
        )

    # -------------------------------------------------------------------------
    # Create and populate Qob netCDF file using prep_Qou_ncf as a skeleton
    # -------------------------------------------------------------------------
    prep_Qou_ncf(IV_riv_avl, ZV_lon_avl, ZV_lat_avl, Qob_ncf)

    try:
        o = netCDF4.Dataset(Qob_ncf, "a")
    except IOError as err:
        raise IOError(f"Unable to open {Qob_ncf} for appending") from err

    # Populate arrays
    o.variables["time"][:] = IV_tim_all[:]
    o.variables["time_bnds"][:, 0] = IV_tim_all[:]
    o.variables["time_bnds"][:, 1] = IV_tim_all[:] + np.int32(86400)

    # Write full matrix
    o.variables["Qout"][:, :] = ZM_Qob_all[:, :]

    # Copy standard attributes
    o.title = "Observed discharge retrieved from USGS Water Data JSON API"
    o.institution = "United States Geological Survey"

    o.close()


# *****************************************************************************
# End
# *****************************************************************************
