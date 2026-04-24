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

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    con_csv = args.con
    bas_csv = args.bas

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
            read_options = pv.ReadOptions(autogenerate_column_names=True)
            table = pv.read_csv(con_csv, read_options=read_options)
            table = table.select(["f0", "f1"]).rename_columns(["riv", "dwn"])
            table = table.cast(
                pa.schema([("riv", pa.int32()), ("dwn", pa.int32())])
            )

            pq.write_table(table, con_pqt)
            # Connectivity read handles potentially variable column counts

        except IOError:
            print(f"ERROR - Unable to open {con_csv}")
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
                table = pv.read_csv(bas_csv, read_options=read_options)
                table = table.cast(pa.schema([("riv", pa.int32())]))
                pq.write_table(table, bas_pqt)

            except IOError:
                print(f"ERROR - Unable to open {bas_csv}")
                sys.exit(1)

    print("Conversion complete.")


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == "__main__":
    main()


# *****************************************************************************
# End
# *****************************************************************************
