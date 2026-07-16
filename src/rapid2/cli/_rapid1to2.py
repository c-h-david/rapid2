#!/usr/bin/env python3
# *****************************************************************************
# _rapid1to2.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import argparse
import os
import sys

import pyarrow as pa
import pyarrow.csv as pv
import pyarrow.parquet as pq

from rapid2 import __version__


# *****************************************************************************
# Main
# *****************************************************************************
def main() -> None:

    # -------------------------------------------------------------------------
    # Initialize the argument parser and add valid arguments
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description="Convert legacy RAPID1 files to RAPID2 files",
        epilog=(
            "examples:\n"
            "  rapid1to2 "
            "--connectivity input/Sandbox/rapid_connect.csv "
            "--basin input/Sandbox/riv_bas_id.csv"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"rapid2 {__version__}"
    )

    parser.add_argument(
        "-con",
        "--connectivity",
        dest="con",
        metavar="CONNECTIVITY",
        type=str,
        required=True,
        help="specify the legacy connectivity CSV file",
    )

    parser.add_argument(
        "-bas",
        "--basin",
        dest="bas",
        metavar="BASIN",
        type=str,
        required=False,
        help="specify the legacy basin CSV file",
    )

    parser.add_argument(
        "-kpr",
        "--k_parameter",
        dest="kpr",
        metavar="K_PARAMETER",
        type=str,
        required=False,
        help="specify the legacy k parameter CSV file",
    )

    parser.add_argument(
        "-xpr",
        "--x_parameter",
        dest="xpr",
        metavar="X_PARAMETER",
        type=str,
        required=False,
        help="specify the legacy x parameter CSV file",
    )

    parser.add_argument(
        "-crd",
        "--coordinates",
        dest="crd",
        metavar="COORDINATES",
        type=str,
        required=False,
        help="specify the legacy coordinates CSV file",
    )

    parser.add_argument(
        "-cpl",
        "--coupling",
        dest="cpl",
        metavar="COUPLING",
        type=str,
        required=False,
        help="specify the legacy coupling CSV file",
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    con_csv = args.con
    bas_csv = args.bas
    kpr_csv = args.kpr
    xpr_csv = args.xpr
    crd_csv = args.crd
    cpl_csv = args.cpl

    print("Converting legacy files (from/to):")

    # -------------------------------------------------------------------------
    # Process connectivity (mandatory)
    # -------------------------------------------------------------------------
    con_pqt = os.path.splitext(con_csv)[0] + ".parquet"

    print(f" - {con_csv}")
    print(f"   -> {con_pqt}")

    if os.path.isfile(con_pqt):
        print(f"WARNING - File already exists {con_pqt}. Skipping.")
    else:
        try:
            # Connectivity read handles potentially variable column counts
            read_options = pv.ReadOptions(autogenerate_column_names=True)
            convert_options = pv.ConvertOptions(
                column_types={
                    "f0": pa.int32(),
                    "f1": pa.int32(),
                },
            )
            table = pv.read_csv(
                con_csv,
                read_options=read_options,
                convert_options=convert_options,
            )
            table = table.select(["f0", "f1"]).rename_columns(["riv", "dwn"])
            schema = pa.schema(
                [field.with_nullable(False) for field in table.schema]
            )
            table = table.cast(schema)
            pq.write_table(table, con_pqt)

        except IOError:
            print(f"ERROR - Unable to open {con_csv}", file=sys.stderr)
            sys.exit(1)

    # -------------------------------------------------------------------------
    # Get "master" river IDs from connectivity (always loaded for simplicity)
    # -------------------------------------------------------------------------
    try:
        IV_riv_tot = pq.read_table(con_pqt, columns=["riv"]).column("riv")
    except IOError:
        print(
            f"ERROR - Unable to read river IDs from {con_pqt}", file=sys.stderr
        )
        sys.exit(1)

    # -------------------------------------------------------------------------
    # Process basin (optional)
    # -------------------------------------------------------------------------
    if bas_csv:
        bas_pqt = os.path.splitext(bas_csv)[0] + ".parquet"

        print(f" - {bas_csv}")
        print(f"   -> {bas_pqt}")

        if os.path.isfile(bas_pqt):
            print(f"WARNING - File already exists {bas_pqt}. Skipping.")
        else:
            try:
                read_options = pv.ReadOptions(column_names=["riv"])
                convert_options = pv.ConvertOptions(
                    column_types={
                        "riv": pa.int32(),
                    },
                )
                table = pv.read_csv(
                    bas_csv,
                    read_options=read_options,
                    convert_options=convert_options,
                )
                schema = pa.schema(
                    [field.with_nullable(False) for field in table.schema]
                )
                table = table.cast(schema)
                pq.write_table(table, bas_pqt)

            except IOError:
                print(f"ERROR - Unable to open {bas_csv}", file=sys.stderr)
                sys.exit(1)

    # -------------------------------------------------------------------------
    # Process k parameter (optional)
    # -------------------------------------------------------------------------
    if kpr_csv:
        kpr_pqt = os.path.splitext(kpr_csv)[0] + ".parquet"

        print(f" - {kpr_csv}")
        print(f"   -> {kpr_pqt}")

        if os.path.isfile(kpr_pqt):
            print(f"WARNING - File already exists {kpr_pqt}. Skipping.")
        else:
            try:
                read_options = pv.ReadOptions(column_names=["kpr"])
                convert_options = pv.ConvertOptions(
                    column_types={
                        "kpr": pa.float64(),
                    },
                )
                table = pv.read_csv(
                    kpr_csv,
                    read_options=read_options,
                    convert_options=convert_options,
                )
                # Stitch the river IDs to the parameter array
                table = pa.table(
                    [IV_riv_tot, table.column("kpr")], names=["riv", "kpr"]
                )
                schema = pa.schema(
                    [field.with_nullable(False) for field in table.schema]
                )
                table = table.cast(schema)
                pq.write_table(table, kpr_pqt)

            except IOError:
                print(f"ERROR - Unable to open {kpr_csv}", file=sys.stderr)
                sys.exit(1)

    # -------------------------------------------------------------------------
    # Process x parameter (optional)
    # -------------------------------------------------------------------------
    if xpr_csv:
        xpr_pqt = os.path.splitext(xpr_csv)[0] + ".parquet"

        print(f" - {xpr_csv}")
        print(f"   -> {xpr_pqt}")

        if os.path.isfile(xpr_pqt):
            print(f"WARNING - File already exists {xpr_pqt}. Skipping.")
        else:
            try:
                read_options = pv.ReadOptions(column_names=["xpr"])
                convert_options = pv.ConvertOptions(
                    column_types={
                        "xpr": pa.float64(),
                    },
                )
                table = pv.read_csv(
                    xpr_csv,
                    read_options=read_options,
                    convert_options=convert_options,
                )
                # Stitch the river IDs to the parameter array
                table = pa.table(
                    [IV_riv_tot, table.column("xpr")], names=["riv", "xpr"]
                )
                schema = pa.schema(
                    [field.with_nullable(False) for field in table.schema]
                )
                table = table.cast(schema)
                pq.write_table(table, xpr_pqt)

            except IOError:
                print(f"ERROR - Unable to open {xpr_csv}", file=sys.stderr)
                sys.exit(1)

    # -------------------------------------------------------------------------
    # Process coordinates (optional)
    # -------------------------------------------------------------------------
    if crd_csv:
        crd_pqt = os.path.splitext(crd_csv)[0] + ".parquet"

        print(f" - {crd_csv}")
        print(f"   -> {crd_pqt}")

        if os.path.isfile(crd_pqt):
            print(f"WARNING - File already exists {crd_pqt}. Skipping.")
        else:
            try:
                read_options = pv.ReadOptions(
                    column_names=["riv", "lon", "lat"]
                )
                convert_options = pv.ConvertOptions(
                    column_types={
                        "riv": pa.int32(),
                        "lon": pa.float64(),
                        "lat": pa.float64(),
                    },
                )
                table = pv.read_csv(
                    crd_csv,
                    read_options=read_options,
                    convert_options=convert_options,
                )
                schema = pa.schema(
                    [field.with_nullable(False) for field in table.schema]
                )
                table = table.cast(schema)
                pq.write_table(table, crd_pqt)

            except IOError:
                print(f"ERROR - Unable to open {crd_csv}", file=sys.stderr)
                sys.exit(1)

    # -------------------------------------------------------------------------
    # Process coupling (optional)
    # -------------------------------------------------------------------------
    if cpl_csv:
        cpl_pqt = os.path.splitext(cpl_csv)[0] + ".parquet"

        print(f" - {cpl_csv}")
        print(f"   -> {cpl_pqt}")

        if os.path.isfile(cpl_pqt):
            print(f"WARNING - File already exists {cpl_pqt}. Skipping.")
        else:
            try:
                read_options = pv.ReadOptions(
                    column_names=["riv", "skm", "1bi", "1bj"]
                )
                convert_options = pv.ConvertOptions(
                    column_types={
                        "riv": pa.int32(),
                        "skm": pa.float64(),
                        "1bi": pa.int32(),
                        "1bj": pa.int32(),
                    },
                )
                table = pv.read_csv(
                    cpl_csv,
                    read_options=read_options,
                    convert_options=convert_options,
                )
                schema = pa.schema(
                    [field.with_nullable(False) for field in table.schema]
                )
                table = table.cast(schema)
                pq.write_table(table, cpl_pqt)

            except IOError:
                print(f"ERROR - Unable to open {cpl_csv}", file=sys.stderr)
                sys.exit(1)

    # -------------------------------------------------------------------------
    # End process
    # -------------------------------------------------------------------------
    print("Conversion complete.")


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == "__main__":
    main()


# *****************************************************************************
# End
# *****************************************************************************
