#!/usr/bin/env python3
# *****************************************************************************
# _ltir_scl.py
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
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from rapid2 import (
    __version__,
    calc_scl_vec,
    make_0bi_tbl,
    make_Net_mat,
    make_Sel_mat,
    read_con_vec,
    read_riv_vec,
    read_std_vec,
)


# *****************************************************************************
# Main
# *****************************************************************************
def main() -> None:
    # -------------------------------------------------------------------------
    # Initialize the argument parser
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description=(
            "Compute Long-Term Inverse Routing (LTIR) scaling factors for "
            "external inflows using gauge observations."
        ),
        epilog=(
            "examples:\n"
            "  ltir_scl --connectivity con_Sandbox.parquet "
            "--basin bas_Sandbox_ascend.parquet "
            "--external_inflow Qex_historic.nc4 "
            "--observations Qob_historic.nc4 "
            "--scalar scl_historic.parquet"
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
        help="specify the input con_pqt file",
    )

    parser.add_argument(
        "-bas",
        "--basin",
        dest="bas",
        metavar="BASIN",
        type=str,
        required=True,
        help="specify the input bas_pqt file",
    )

    parser.add_argument(
        "-Qex",
        "--external_inflow",
        dest="Qex",
        metavar="EXTERNAL_INFLOW",
        type=str,
        required=True,
        help="specify the input Qex_ncf file",
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
        "-scl",
        "--scalar",
        dest="scl",
        metavar="SCALAR",
        type=str,
        required=True,
        help="specify the output scl_pqt file",
    )

    # -------------------------------------------------------------------------
    # Parse arguments and assign to variables
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    con_pqt = args.con
    bas_pqt = args.bas
    Qex_ncf = args.Qex
    Qob_ncf = args.Qob
    scl_pqt = args.scl

    # -------------------------------------------------------------------------
    # Skip if file already exists
    # -------------------------------------------------------------------------
    if os.path.exists(scl_pqt):
        print(f"WARNING - File already exists {scl_pqt}. Skipping.")
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Execute main logic
    # -------------------------------------------------------------------------
    try:
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # River network
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print("- Process river network")
        IV_riv_tot, IV_dwn_tot = read_con_vec(con_pqt)
        IV_riv_bas = read_riv_vec(bas_pqt)

        IT_0bi_tot, IT_0bi_bas, IV_0bi_bas = make_0bi_tbl(
            IV_riv_tot, IV_riv_bas
        )
        ZM_Net = make_Net_mat(IV_dwn_tot, IT_0bi_tot, IV_riv_bas, IT_0bi_bas)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Active observations
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print("- Process active observations")
        IV_riv_avl, _, _, _, _ = read_std_vec(Qob_ncf)

        IV_riv_act = np.array(
            [riv for riv in IV_riv_avl if riv in IT_0bi_bas], dtype=np.int32
        )
        if len(IV_riv_act) == 0:
            raise ValueError("No valid overlapping gauges found in the basin")

        _, _, IV_0bi_act = make_0bi_tbl(IV_riv_avl, IV_riv_act)
        ZM_Sel = make_Sel_mat(IV_riv_act, IT_0bi_bas)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Average external inflows
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print("- Average external inflows")
        IV_riv_tmp, _, _, _, _ = read_std_vec(Qex_ncf)

        if not np.array_equal(IV_riv_tot, IV_riv_tmp):
            raise ValueError(f"River IDs in {Qex_ncf} must match {con_pqt}")

        f = netCDF4.Dataset(Qex_ncf, "r")
        ZM_Qex_tmp = f.variables["Qext"][:, IV_0bi_bas]
        ZV_Qex_avg = np.mean(ZM_Qex_tmp, axis=0)
        f.close()

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Average observations
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print("- Average observations")
        o = netCDF4.Dataset(Qob_ncf, "r")

        if "Qout" in o.variables:
            YS_ob_var = "Qout"
        elif "Qext" in o.variables:
            YS_ob_var = "Qext"
        else:
            raise ValueError(f"No known observation variable in {Qob_ncf}")

        ZM_Qob_tmp = o.variables[YS_ob_var][:, IV_0bi_act]
        ZV_Qob_avg = np.mean(ZM_Qob_tmp, axis=0)
        o.close()

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Compute LTIR Scaling Factors
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print("- Compute LTIR scaling factors")
        ZV_scl_bas = calc_scl_vec(ZM_Net, ZM_Sel, ZV_Qex_avg, ZV_Qob_avg)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Export scalars to Parquet
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print("- Export scalars to Parquet")
        ZV_scl_tot = np.full_like(IV_riv_tot, np.nan, dtype=np.float64)
        ZV_scl_tot[IV_0bi_bas] = ZV_scl_bas

        table = pa.table([IV_riv_tot, ZV_scl_tot], names=["riv", "scl"])

        # Ensure correct types mapping with rapid2 nomenclature
        schema = pa.schema(
            [
                field.with_nullable(False) if field.name == "riv" else field
                for field in table.schema
            ]
        )
        table = table.cast(schema)
        pq.write_table(table, scl_pqt)

        print("Done")

    except (IOError, ValueError, KeyError) as e:
        print(f"ERROR - {e}", file=sys.stderr)
        sys.exit(1)


# *****************************************************************************
# If executed as a script
# *****************************************************************************
if __name__ == "__main__":
    main()


# *****************************************************************************
# End
# *****************************************************************************
