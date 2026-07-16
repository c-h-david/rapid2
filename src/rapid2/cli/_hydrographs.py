#!/usr/bin/env python3
# *****************************************************************************
# _hydrographs.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse
import os
import sys

import netCDF4
import toyplot  # type: ignore[import-untyped]
import toyplot.svg  # type: ignore[import-untyped]
from tqdm import tqdm

from rapid2 import __version__


# *****************************************************************************
# Main
# *****************************************************************************
def main() -> None:

    # -------------------------------------------------------------------------
    # Initialize the argument parser and add valid arguments
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description=(
            "Plot hydrographs comparing observations (Qob) to model "
            "equivalents (Qme) and save as individual SVG files."
        ),
        epilog=(
            "examples:\n"
            "  hydrographs "
            "--observations input/Sandbox/"
            "Qob_Sandbox_19700101_19700110_TR.nc4 "
            "--model_equivalent output/Sandbox/"
            "Qme_Sandbox_19700101_19700110_OL.nc4 "
            "--hyd_svg output/Sandbox/hyd.svg"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    parser.add_argument(
        "-Qob",
        "--observations",
        dest="Qob",
        metavar="OBSERVATIONS",
        type=str,
        required=True,
        help="specify the input Qob_ncf file",
    )

    parser.add_argument(
        "-Qme",
        "--model_equivalent",
        dest="Qme",
        metavar="MODEL_EQUIVALENT",
        type=str,
        required=True,
        help="specify the input Qme_ncf file",
    )

    parser.add_argument(
        "-max",
        "--maximum",
        dest="max",
        metavar="MAXIMUM",
        type=float,
        required=True,
        help="specify a maximum value for the y-axis to standardize scales",
    )

    parser.add_argument(
        "-hyd",
        "--hyd_svg",
        dest="hyd",
        metavar="HYD_SVG",
        type=str,
        required=True,
        help="specify the output SVG file (e.g., hyd.svg), which will be "
        "modified to append river IDs (e.g., hyd_10.svg)",
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    Qob_ncf = args.Qob
    Qme_ncf = args.Qme
    hyd_svg = args.hyd
    ZS_Qou_max = args.max

    # Split the output path into base and extension to inject river ID later
    YS_base, YS_ext = os.path.splitext(hyd_svg)

    print("Plotting hydrographs (from/to):")
    print(f" - {Qob_ncf}")
    print(f" - {Qme_ncf}")
    print(f"   -> {YS_base}_<rivid>{YS_ext}")

    # -------------------------------------------------------------------------
    # Read netCDF files
    # -------------------------------------------------------------------------
    print("- Read netCDF files")
    o = netCDF4.Dataset(Qob_ncf, "r")
    m = netCDF4.Dataset(Qme_ncf, "r")

    # -------------------------------------------------------------------------
    # Extract metadata
    # -------------------------------------------------------------------------
    print("- Extract metadata")
    IV_riv_avl = o.variables["rivid"][:]
    IV_tim_all = o.variables["time"][:]

    IS_riv_avl = len(IV_riv_avl)
    print(f"  . Found {IS_riv_avl} observation locations")

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

        YS_hyd_svg = f"{YS_base}_{IS_riv}{YS_ext}"

        # Skip if this specific station's file already exists
        if os.path.exists(YS_hyd_svg):
            tqdm.write(f"WARNING - File already exists {YS_hyd_svg} skipping.")
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
        Qob_mark = axes.plot(
            IV_tim_all,
            ZV_Qob_tmp,
            title="Observations",
            color="black",
            style={"stroke-width": 2},
        )

        # Model Equivalent
        Qme_mark = axes.plot(
            IV_tim_all,
            ZV_Qme_tmp,
            title="Model Equivalent",
            color="red",
            style={"stroke-width": 2, "stroke-dasharray": "5,5"},
        )

        # Add Legend
        canvas.legend(
            [
                ("Observations", Qob_mark),
                ("Model Equivalent", Qme_mark),
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

    print("Done")


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == "__main__":
    main()


# *****************************************************************************
# End
# *****************************************************************************
