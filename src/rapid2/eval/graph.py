#!/usr/bin/env python3
# *****************************************************************************
# graph.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import os
import warnings
from pathlib import Path

import netCDF4
import toyplot  # type: ignore[import-untyped]
import toyplot.svg  # type: ignore[import-untyped]
from tqdm import tqdm


# *****************************************************************************
# Plot Hydrographs
# *****************************************************************************
def graph(
    Qob_ncf: str,
    Qme_ncf: str,
    ZS_Qou_max: float,
    hyd_svg: str,
) -> None:
    """Plot hydrographs comparing observations to model equivalents.

    Extracts timeseries data from observed and simulated discharge NetCDF files
    and generates standalone SVG hydrographs for each available river gauge.

    Parameters
    ----------
    Qob_ncf : str
        Path to the input observations (Qob) NetCDF file.
    Qme_ncf : str
        Path to the input model equivalent (Qme) NetCDF file.
    ZS_Qou_max : float
        Maximum value for the y-axis to standardize scales across plots.
    hyd_svg : str
        Path to the output SVG file (e.g., hyd.svg), which will be modified
        to append river IDs (e.g., hyd_10.svg).

    Returns
    -------
    None

    Examples
    --------
    >>> Qob_ncf = "input/Sandbox/Qob_Sandbox_19700101_19700110_TR.nc4"
    >>> Qme_ncf = "output/Sandbox/Qme_Sandbox_19700101_19700110_OL.nc4"
    >>> ZS_Qou_max = 125.0
    >>> hyd_svg = "output/Sandbox/hyd_tst.svg"
    >>> graph(Qob_ncf, Qme_ncf, ZS_Qou_max, hyd_svg)
    >>> import os
    >>> for riv in [30, 50]:
    ...     os.remove(f"output/Sandbox/hyd_tst_{riv}.svg")
    """

    # -------------------------------------------------------------------------
    # Setup path components
    # -------------------------------------------------------------------------
    trg_dir = str(Path(hyd_svg).parent)
    YS_hyd_tmp = str(Path(hyd_svg).stem)

    # -------------------------------------------------------------------------
    # Read netCDF files
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
    # Extract metadata
    # -------------------------------------------------------------------------
    IV_riv_avl = o.variables["rivid"][:]
    IV_tim_all = o.variables["time"][:]

    IS_riv_avl = len(IV_riv_avl)

    # -------------------------------------------------------------------------
    # Setup canvas dimensions
    # -------------------------------------------------------------------------
    canvas_width = 700
    canvas_height = 300

    # -------------------------------------------------------------------------
    # Plot data and render individual SVGs
    # -------------------------------------------------------------------------
    for JS_riv_avl in tqdm(range(IS_riv_avl), desc="Plotting hydrographs"):
        IS_riv = IV_riv_avl[JS_riv_avl]

        YS_hyd_svg = str(Path(trg_dir) / f"{YS_hyd_tmp}_{IS_riv}.svg")

        # Skip if this specific station's file already exists
        if os.path.exists(YS_hyd_svg):
            warnings.warn(
                f"File already exists {YS_hyd_svg} skipping.",
                stacklevel=2,
            )
            continue

        # Create a fresh canvas for this specific station
        canvas = toyplot.Canvas(
            width=canvas_width,
            height=canvas_height,
            style={"background-color": "white"},
        )

        # Slice timeseries directly from disk to save memory
        if "Qout" in o.variables:
            ZV_Qob_tmp = o.variables["Qout"][:, JS_riv_avl]
        else:
            ZV_Qob_tmp = o.variables["Qext"][:, JS_riv_avl]

        if "Qout" in m.variables:
            ZV_Qme_tmp = m.variables["Qout"][:, JS_riv_avl]
        else:
            ZV_Qme_tmp = m.variables["Qext"][:, JS_riv_avl]

        # Add axes
        axes = canvas.cartesian(
            xlabel="Date",
            ylabel="Discharge (m3 s-1)",
            label=f"Hydrograph for River ID: {IS_riv}",
            ymin=0,
            ymax=ZS_Qou_max,
        )
        axes.x.ticks.locator = toyplot.locator.Timestamp(
            timezone="UTC",
            format="{0:YYYY-MM-DD}",
        )

        axes.padding = 0

        # Observations
        mark_Qob = axes.plot(
            IV_tim_all,
            ZV_Qob_tmp,
            title="Observations",
            color="black",
            style={"stroke-width": 2},
        )

        # Model Equivalent
        mark_Qme = axes.plot(
            IV_tim_all,
            ZV_Qme_tmp,
            title="Model Equivalent",
            color="red",
            style={"stroke-width": 2, "stroke-dasharray": "5,5"},
        )

        # Add Legend
        canvas.legend(
            [
                ("Observations", mark_Qob),
                ("Model Equivalent", mark_Qme),
            ],
            corner=("top-right", 50, 100, 50),
        )

        # Render the SVG
        toyplot.svg.render(canvas, YS_hyd_svg)

    # -------------------------------------------------------------------------
    # Close
    # -------------------------------------------------------------------------
    o.close()
    m.close()


# *****************************************************************************
# End
# *****************************************************************************
