# *****************************************************************************
# __init__.py
# *****************************************************************************

# Purpose:
# This file used in Python to define packages and initialize their namespaces.
# Author:
# Cedric H. David, 2025-2025


# *****************************************************************************
# Initialization
# *****************************************************************************

# -----------------------------------------------------------------------------
# Dynamic Package Versioning
# -----------------------------------------------------------------------------
import importlib.metadata

try:
    __version__ = importlib.metadata.version("rapid2")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

# -----------------------------------------------------------------------------
# Top-Level API Facade
# -----------------------------------------------------------------------------
from .core.chck_bas import chck_bas
from .core.chck_cpl import chck_cpl
from .core.make_0bi_tbl import make_0bi_tbl
from .core.make_CCC_mat import make_CCC_mat
from .core.make_Mus_mat import make_Mus_mat
from .core.make_Net_mat import make_Net_mat
from .core.make_Wdw_mat import make_Wdw_mat
from .core.prep_Qex_ncf import prep_Qex_ncf
from .core.prep_Qfi_ncf import prep_Qfi_ncf
from .core.prep_Qou_ncf import prep_Qou_ncf
from .core.prep_skl_ncf import prep_skl_ncf
from .core.read_bas_vec import read_bas_vec
from .core.read_con_vec import read_con_vec
from .core.read_cpl_vec import read_cpl_vec
from .core.read_crd_vec import read_crd_vec
from .core.read_kpr_vec import read_kpr_vec
from .core.read_nml_tbl import read_nml_tbl
from .core.read_std_vec import read_std_vec
from .core.read_xpr_vec import read_xpr_vec
from .core.updt_Mus_Qou import updt_Mus_Qou

# -----------------------------------------------------------------------------
# Explicit Public Interface
# -----------------------------------------------------------------------------
__all__ = [
    "__version__",
    "chck_bas",
    "chck_cpl",
    "make_0bi_tbl",
    "make_CCC_mat",
    "make_Mus_mat",
    "make_Net_mat",
    "make_Wdw_mat",
    "prep_Qex_ncf",
    "prep_Qfi_ncf",
    "prep_Qou_ncf",
    "prep_skl_ncf",
    "read_bas_vec",
    "read_con_vec",
    "read_cpl_vec",
    "read_crd_vec",
    "read_kpr_vec",
    "read_nml_tbl",
    "read_std_vec",
    "read_xpr_vec",
    "updt_Mus_Qou",
]


# *****************************************************************************
# End
# *****************************************************************************
