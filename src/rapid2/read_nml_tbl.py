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
    >>> nml_yml = "./input/Sandbox/namelist_Sandbox.yml"
    >>> AT_nml = read_nml_tbl(nml_yml)
    >>> AT_nml["Q00_ncf"]
    './input/Sandbox/Qinit_Sandbox_19700101_19700110.nc4'
    >>> AT_nml["Qex_ncf"]
    './input/Sandbox/Qext_Sandbox_19700101_19700110.nc4'
    >>> AT_nml["con_csv"]
    './input/Sandbox/rapid_connect_Sandbox.csv'
    >>> AT_nml["kpr_csv"]
    './input/Sandbox/k_Sandbox.csv'
    >>> AT_nml["xpr_csv"]
    './input/Sandbox/x_Sandbox.csv'
    >>> AT_nml["bas_csv"]
    './input/Sandbox/riv_bas_id_Sandbox.csv'
    >>> AT_nml["IS_dtR"]
    np.int32(900)
    >>> AT_nml["Qou_ncf"]
    './output/Sandbox/Qout_Sandbox_19700101_19700110_tst.nc4'
    >>> AT_nml["Qfi_ncf"]
    './output/Sandbox/Qfinal_Sandbox_19700101_19700110_tst.nc4'
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
            "con_csv": None,
            "kpr_csv": None,
            "xpr_csv": None,
            "bas_csv": None,
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
