#!/usr/bin/env python3
# *****************************************************************************
# nml_cfg.py
# *****************************************************************************

# Author:
# Cedric H. David, 2025-2025


# *****************************************************************************
# Import Python modules
# *****************************************************************************
from typing import Any, Dict
import yaml  # type: ignore[import-untyped]
import numpy as np


# *****************************************************************************
# Namelist function
# *****************************************************************************
def nml_cfg(
            nml_yml: str
            ) -> Dict[str, Any]:
    '''Read YAML file with model configuration and return a dictionary.

    Read a YAML namelist file with model configuration and return a dictionary
    with mandatory values. Optional values may be included as well.

    Parameters
    ----------
    nml_yml : str
        Path to the YAML namelist file.

    Returns
    -------
    nml_dic : Dict[str, Any]
        Dictionary containing the parsed YAML content.

    Examples
    --------
    >>> nml_yml = './input/Test/namelist_Test.yml'
    >>> nml_dic = nml_cfg(nml_yml)
    >>> nml_dic['Q00_ncf']
    './input/Test/Qinit_Test_20000101_20000102.nc4'
    >>> nml_dic['Qex_ncf']
    './input/Test/Qext_Test_20000101_20000102.nc4'
    >>> nml_dic['con_csv']
    './input/Test/rapid_connect_Test.csv'
    >>> nml_dic['kpr_csv']
    './input/Test/k_Test.csv'
    >>> nml_dic['xpr_csv']
    './input/Test/x_Test.csv'
    >>> nml_dic['bas_csv']
    './input/Test/riv_bas_id_Test.csv'
    >>> nml_dic['IS_dtR']
    np.int32(900)
    >>> nml_dic['Qou_ncf']
    './output/Test/Qout_Test_20000101_20000102_tst.nc4'
    >>> nml_dic['Qfi_ncf']
    './output/Test/Qfinal_Test_20000101_20000102_tst.nc4'
    '''

    try:
        # ---------------------------------------------------------------------
        # Load namelist
        # ---------------------------------------------------------------------
        with open(nml_yml, 'r') as ymlfile:
            nml_dic: Dict[str, Any] = yaml.safe_load(ymlfile)

        # ---------------------------------------------------------------------
        # Check for required keys
        # ---------------------------------------------------------------------
        req_key = {'Q00_ncf',
                   'Qex_ncf',
                   'con_csv',
                   'kpr_csv',
                   'xpr_csv',
                   'bas_csv',
                   'IS_dtR',
                   'Qou_ncf',
                   'Qfi_ncf',
                   }
        mis_key = req_key - nml_dic.keys()
        if mis_key:
            raise ValueError('Missing required keys: '+str(mis_key))

        # ---------------------------------------------------------------------
        # Check that timestep is integer and make it np.int32
        # ---------------------------------------------------------------------
        if not isinstance(nml_dic['IS_dtR'], int):
            raise ValueError('IS_dtR must be an integer')

        nml_dic['IS_dtR'] = np.int32(nml_dic['IS_dtR'])

        # ---------------------------------------------------------------------
        # Return dictionary
        # ---------------------------------------------------------------------
        return nml_dic

    except IOError:
        print('ERROR - Unable to open '+nml_yml)
        raise SystemExit(22)


# *****************************************************************************
# End
# *****************************************************************************
