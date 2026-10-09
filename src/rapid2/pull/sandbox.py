#!/usr/bin/env python3
# *****************************************************************************
# sandbox.py
# *****************************************************************************

# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Import Python modules
# *****************************************************************************
from pathlib import Path

import pooch  # type: ignore[import-untyped]


# *****************************************************************************
# Download Sandbox Dataset from Zenodo
# *****************************************************************************
def sandbox(tgt_dir: str) -> None:
    """Download the RAPID Sandbox sample dataset from Zenodo.

    Downloads synthetic experiment files hosted on Zenodo into the
    `input/Sandbox` and `output/Sandbox` directories within the provided
    target directory.

    Parameters
    ----------
    tgt_dir : str
        Target directory where the Sandbox folders will be created.

    Returns
    -------
    None

    Examples
    --------
    >>> tgt_dir = "."
    >>> sandbox(tgt_dir)
    >>> import os
    >>> con_pqt = os.path.join(tgt_dir, "input/Sandbox/con_Sandbox.parquet")
    >>> os.path.exists(con_pqt)
    True
    """

    # -------------------------------------------------------------------------
    # Location of the dataset
    # -------------------------------------------------------------------------
    doi = "doi:10.5281/zenodo.23044811/"

    # -------------------------------------------------------------------------
    # Download input files
    # -------------------------------------------------------------------------
    files = [
        "bas_Sandbox_ascend.parquet",
        "con_Sandbox.parquet",
        "cpl_Sandbox.parquet",
        "crd_Sandbox.parquet",
        "kpr_Sandbox.parquet",
        "nml_Sandbox_BC.yml",
        "nml_Sandbox_DA.yml",
        "nml_Sandbox_OL.yml",
        "nml_Sandbox_HY.yml",
        "nml_Sandbox_TR.yml",
        "obs_Sandbox.parquet",
        "Q00_Sandbox_19700101_19700110_FG.nc4",
        "Q00_Sandbox_19700101_19700110_TR.nc4",
        "Qex_Sandbox_19700101_19700110_BC.nc4",
        "Qex_Sandbox_19700101_19700110_FG.nc4",
        "Qex_Sandbox_19700101_19700110_TR.nc4",
        "Qob_Sandbox_19700101_19700110_TR.nc4",
        "scl_Sandbox.parquet",
        "xpr_Sandbox.parquet",
    ]

    fetcher = pooch.create(
        path=Path(tgt_dir) / "input" / "Sandbox",
        base_url=doi,
        registry={f: None for f in files},
    )

    for file in files:
        fetcher.fetch(file)

    # -------------------------------------------------------------------------
    # Download output files
    # -------------------------------------------------------------------------
    files = [
        "Qfi_Sandbox_19700101_19700110_BC.nc4",
        "Qfi_Sandbox_19700101_19700110_DA.nc4",
        "Qfi_Sandbox_19700101_19700110_HY.nc4",
        "Qfi_Sandbox_19700101_19700110_OL.nc4",
        "Qfi_Sandbox_19700101_19700110_TR.nc4",
        "Qme_Sandbox_19700101_19700110_BC.nc4",
        "Qme_Sandbox_19700101_19700110_DA.nc4",
        "Qme_Sandbox_19700101_19700110_HY.nc4",
        "Qme_Sandbox_19700101_19700110_OL.nc4",
        "Qou_Sandbox_19700101_19700110_BC.nc4",
        "Qou_Sandbox_19700101_19700110_DA.nc4",
        "Qou_Sandbox_19700101_19700110_HY.nc4",
        "Qou_Sandbox_19700101_19700110_OL.nc4",
        "Qou_Sandbox_19700101_19700110_TR.nc4",
    ]

    fetcher = pooch.create(
        path=Path(tgt_dir) / "output" / "Sandbox",
        base_url=doi,
        registry={f: None for f in files},
    )

    for file in files:
        fetcher.fetch(file)


# *****************************************************************************
# End
# *****************************************************************************
