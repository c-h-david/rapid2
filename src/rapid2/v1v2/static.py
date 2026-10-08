#!/usr/bin/env python3
# *****************************************************************************
# static.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import os

import pyarrow as pa
import pyarrow.csv as pv
import pyarrow.parquet as pq


# *****************************************************************************
# Convert Legacy RAPID1 CSV Static Files to RAPID2 Parquet Files
# *****************************************************************************
def static(
    con_csv: str,
    bas_csv: str | None = None,
    kpr_csv: str | None = None,
    xpr_csv: str | None = None,
    crd_csv: str | None = None,
    cpl_csv: str | None = None,
) -> None:
    """Convert legacy RAPID1 CSV static files to RAPID2 Parquet files.

    Parameters
    ----------
    con_csv : str
        Path to the legacy connectivity CSV file.
    bas_csv : str or None, optional
        Path to the legacy basin CSV file (default is None).
    kpr_csv : str or None, optional
        Path to the legacy k parameter CSV file (default is None).
    xpr_csv : str or None, optional
        Path to the legacy x parameter CSV file (default is None).
    crd_csv : str or None, optional
        Path to the legacy coordinates CSV file (default is None).
    cpl_csv : str or None, optional
        Path to the legacy coupling CSV file (default is None).

    Returns
    -------
    None

    Examples
    --------
    >>> con_csv = "./input/Sandbox/rapid_connect.csv"
    >>> bas_csv = "./input/Sandbox/riv_bas_id.csv"
    >>> static(con_csv, bas_csv=bas_csv)  # doctest: +SKIP
    """

    # -------------------------------------------------------------------------
    # Process connectivity (mandatory)
    # -------------------------------------------------------------------------
    con_pqt = os.path.splitext(con_csv)[0] + ".parquet"

    if not os.path.isfile(con_pqt):
        read_options = pv.ReadOptions(autogenerate_column_names=True)
        convert_options = pv.ConvertOptions(
            column_types={
                "f0": pa.int32(),
                "f1": pa.int32(),
            },
        )
        try:
            table = pv.read_csv(
                con_csv,
                read_options=read_options,
                convert_options=convert_options,
            )
        except IOError as err:
            raise IOError(f"Unable to open {con_csv}") from err

        table = table.select(["f0", "f1"]).rename_columns(["riv", "dwn"])
        schema = pa.schema(
            [field.with_nullable(False) for field in table.schema]
        )
        table = table.cast(schema)
        pq.write_table(table, con_pqt)

    # -------------------------------------------------------------------------
    # Get master river IDs from connectivity
    # -------------------------------------------------------------------------
    try:
        IV_riv_tot = pq.read_table(con_pqt, columns=["riv"]).column("riv")
    except IOError as err:
        raise IOError(f"Unable to open {con_pqt}") from err

    # -------------------------------------------------------------------------
    # Process basin (optional)
    # -------------------------------------------------------------------------
    if bas_csv:
        bas_pqt = os.path.splitext(bas_csv)[0] + ".parquet"

        if not os.path.isfile(bas_pqt):
            read_options = pv.ReadOptions(column_names=["riv"])
            convert_options = pv.ConvertOptions(
                column_types={
                    "riv": pa.int32(),
                },
            )
            try:
                table = pv.read_csv(
                    bas_csv,
                    read_options=read_options,
                    convert_options=convert_options,
                )
            except IOError as err:
                raise IOError(f"Unable to open {bas_csv}") from err

            schema = pa.schema(
                [field.with_nullable(False) for field in table.schema]
            )
            table = table.cast(schema)
            pq.write_table(table, bas_pqt)

    # -------------------------------------------------------------------------
    # Process k parameter (optional)
    # -------------------------------------------------------------------------
    if kpr_csv:
        kpr_pqt = os.path.splitext(kpr_csv)[0] + ".parquet"

        if not os.path.isfile(kpr_pqt):
            read_options = pv.ReadOptions(column_names=["kpr"])
            convert_options = pv.ConvertOptions(
                column_types={
                    "kpr": pa.float64(),
                },
            )
            try:
                table = pv.read_csv(
                    kpr_csv,
                    read_options=read_options,
                    convert_options=convert_options,
                )
            except IOError as err:
                raise IOError(f"Unable to open {kpr_csv}") from err

            table = pa.table(
                [IV_riv_tot, table.column("kpr")], names=["riv", "kpr"]
            )
            schema = pa.schema(
                [field.with_nullable(False) for field in table.schema]
            )
            table = table.cast(schema)
            pq.write_table(table, kpr_pqt)

    # -------------------------------------------------------------------------
    # Process x parameter (optional)
    # -------------------------------------------------------------------------
    if xpr_csv:
        xpr_pqt = os.path.splitext(xpr_csv)[0] + ".parquet"

        if not os.path.isfile(xpr_pqt):
            read_options = pv.ReadOptions(column_names=["xpr"])
            convert_options = pv.ConvertOptions(
                column_types={
                    "xpr": pa.float64(),
                },
            )
            try:
                table = pv.read_csv(
                    xpr_csv,
                    read_options=read_options,
                    convert_options=convert_options,
                )
            except IOError as err:
                raise IOError(f"Unable to open {xpr_csv}") from err

            table = pa.table(
                [IV_riv_tot, table.column("xpr")], names=["riv", "xpr"]
            )
            schema = pa.schema(
                [field.with_nullable(False) for field in table.schema]
            )
            table = table.cast(schema)
            pq.write_table(table, xpr_pqt)

    # -------------------------------------------------------------------------
    # Process coordinates (optional)
    # -------------------------------------------------------------------------
    if crd_csv:
        crd_pqt = os.path.splitext(crd_csv)[0] + ".parquet"

        if not os.path.isfile(crd_pqt):
            read_options = pv.ReadOptions(column_names=["riv", "lon", "lat"])

            convert_options = pv.ConvertOptions(
                column_types={
                    "riv": pa.int32(),
                    "lon": pa.float64(),
                    "lat": pa.float64(),
                },
            )
            try:
                table = pv.read_csv(
                    crd_csv,
                    read_options=read_options,
                    convert_options=convert_options,
                )
            except IOError as err:
                raise IOError(f"Unable to open {crd_csv}") from err

            schema = pa.schema(
                [field.with_nullable(False) for field in table.schema]
            )
            table = table.cast(schema)
            pq.write_table(table, crd_pqt)

    # -------------------------------------------------------------------------
    # Process coupling (optional)
    # -------------------------------------------------------------------------
    if cpl_csv:
        cpl_pqt = os.path.splitext(cpl_csv)[0] + ".parquet"

        if not os.path.isfile(cpl_pqt):
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
            try:
                table = pv.read_csv(
                    cpl_csv,
                    read_options=read_options,
                    convert_options=convert_options,
                )
            except IOError as err:
                raise IOError(f"Unable to open {cpl_csv}") from err

            schema = pa.schema(
                [field.with_nullable(False) for field in table.schema]
            )
            table = table.cast(schema)
            pq.write_table(table, cpl_pqt)


# *****************************************************************************
# End
# *****************************************************************************
