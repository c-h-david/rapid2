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
from datetime import datetime, timezone

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
    # Construct and execute USGS JSON web service query
    # -------------------------------------------------------------------------
    YS_url = "https://waterservices.usgs.gov/nwis/dv/"

    payload = {
        "format": "json",
        "sites": ",".join(YV_cod_avl),
        "startDT": YS_tim_beg,
        "endDT": YS_tim_end,
        "parameterCd": "00060",  # Discharge, cubic feet per second
        "statCd": "00003",  # Mean daily value
    }

    YS_url = f"{YS_url}?{urllib.parse.urlencode(payload)}"

    try:
        with urllib.request.urlopen(YS_url) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as err:
        raise IOError(f"Failed to query USGS API: {YS_url}") from err

    # -------------------------------------------------------------------------
    # Clean up the bloated USGS JSON into a more simplified dictionary
    # -------------------------------------------------------------------------
    data = data["value"]["timeSeries"]

    AT_obs = {}
    for item in data:
        YS_cod = item["sourceInfo"]["siteCode"][0]["value"]

        ZS_lon = float(
            item["sourceInfo"]["geoLocation"]["geogLocation"]["longitude"]
        )

        ZS_lat = float(
            item["sourceInfo"]["geoLocation"]["geogLocation"]["latitude"]
        )

        YV_tim = [record["dateTime"] for record in item["values"][0]["value"]]

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


# *****************************************************************************
# End
# *****************************************************************************
