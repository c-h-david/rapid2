#!/usr/bin/env python3
# *****************************************************************************
# read_nml_tbl.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2025


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import sys
from typing import Any, Dict

import numpy as np
import yaml


# *****************************************************************************
# Namelist function
# *****************************************************************************
def read_nml_tbl(nml_yml: str) -> Dict[str, Any]:
    """Read YAML file with model configuration and return a dictionary.

    Read a YAML namelist file with model configuration and return a dictionary
    with mandatory values. Optional values may be included as well.

    Parameters
    ----------
    nml_yml : str
        Path to the YAML namelist file.

    Returns
    -------
    AT_nml : Dict[str, Any]
        Dictionary containing the parsed YAML content.

    Examples
    --------
    >>> nml_yml = "./input/Sandbox/nml_Sandbox_TR.yml"
    >>> AT_nml = read_nml_tbl(nml_yml)
    >>> AT_nml["Q00_ncf"]
    './input/Sandbox/Q00_Sandbox_19700101_19700110_TR.nc4'
    >>> AT_nml["Qex_ncf"]
    './input/Sandbox/Qex_Sandbox_19700101_19700110_TR.nc4'
    >>> AT_nml["con_pqt"]
    './input/Sandbox/con_Sandbox.parquet'
    >>> AT_nml["kpr_pqt"]
    './input/Sandbox/kpr_Sandbox.parquet'
    >>> AT_nml["xpr_pqt"]
    './input/Sandbox/xpr_Sandbox.parquet'
    >>> AT_nml["bas_pqt"]
    './input/Sandbox/bas_Sandbox_ascend.parquet'
    >>> AT_nml["IS_dtR"]
    np.int32(900)
    >>> AT_nml["Qou_ncf"]
    './output/Sandbox/Qou_Sandbox_19700101_19700110_TR_tst.nc4'
    >>> AT_nml["Qfi_ncf"]
    './output/Sandbox/Qfi_Sandbox_19700101_19700110_TR_tst.nc4'
    """

    try:
        # ---------------------------------------------------------------------
        # Load namelist
        # ---------------------------------------------------------------------
        with open(nml_yml, "r") as ymlfile:
            AT_nml: Dict[str, Any] = yaml.safe_load(ymlfile)
        # ---------------------------------------------------------------------
        # Check for required keys
        # ---------------------------------------------------------------------
        AT_nml_tmp = {
            "Q00_ncf": None,
            "Qex_ncf": None,
            "con_pqt": None,
            "kpr_pqt": None,
            "xpr_pqt": None,
            "bas_pqt": None,
            "IS_dtR": None,
            "Qou_ncf": None,
            "Qfi_ncf": None,
        }

        if AT_nml_tmp.keys() - AT_nml.keys():
            raise ValueError(
                f"Missing required keys: {AT_nml_tmp.keys() - AT_nml.keys()}"
            )

        # ---------------------------------------------------------------------
        # Check that timestep is integer and make it np.int32
        # ---------------------------------------------------------------------
        if not isinstance(AT_nml["IS_dtR"], int):
            raise ValueError("IS_dtR must be an integer")

        AT_nml["IS_dtR"] = np.int32(AT_nml["IS_dtR"])

        # ---------------------------------------------------------------------
        # Return dictionary
        # ---------------------------------------------------------------------
        return AT_nml

    except IOError:
        print(f"ERROR - Unable to open {nml_yml}")
        sys.exit(1)


# *****************************************************************************
# End
# *****************************************************************************
