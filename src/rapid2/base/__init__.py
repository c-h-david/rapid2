# *****************************************************************************
# __init__.py
# *****************************************************************************

# Purpose:
# Define the low-level base module namespace and export core building blocks.
# Author:
# Cedric H. David, 2026-2026


# *****************************************************************************
# Initialization
# *****************************************************************************

# -----------------------------------------------------------------------------
# Base API Facade
# -----------------------------------------------------------------------------
from .calc_GCt_vec import calc_GCt_vec
from .calc_Kal_mat import calc_Kal_mat
from .calc_MBy_sca import calc_MBy_sca
from .calc_Nmn_mat import calc_Nmn_mat
from .calc_scl_vec import calc_scl_vec
from .chck_bas import chck_bas
from .chck_cpl import chck_cpl
from .make_0bi_tbl import make_0bi_tbl
from .make_CCC_mat import make_CCC_mat
from .make_dQe_mat import make_dQe_mat
from .make_dQo_mat import make_dQo_mat
from .make_Msk_mat import make_Msk_mat
from .make_Net_mat import make_Net_mat
from .make_SA0_mat import make_SA0_mat
from .make_SAe_mat import make_SAe_mat
from .make_Sel_mat import make_Sel_mat
from .prep_Qex_ncf import prep_Qex_ncf
from .prep_Qfi_ncf import prep_Qfi_ncf
from .prep_Qou_ncf import prep_Qou_ncf
from .prep_skl_ncf import prep_skl_ncf
from .read_con_vec import read_con_vec
from .read_cpl_vec import read_cpl_vec
from .read_crd_vec import read_crd_vec
from .read_err_vec import read_err_vec
from .read_kpr_vec import read_kpr_vec
from .read_nml_tbl import read_nml_tbl
from .read_riv_vec import read_riv_vec
from .read_std_vec import read_std_vec
from .read_xpr_vec import read_xpr_vec
from .updt_Mus_Qou import updt_Mus_Qou

# -----------------------------------------------------------------------------
# Explicit Public Interface
# -----------------------------------------------------------------------------
__all__ = [
    "calc_GCt_vec",
    "calc_Kal_mat",
    "calc_MBy_sca",
    "calc_Nmn_mat",
    "calc_scl_vec",
    "chck_bas",
    "chck_cpl",
    "make_0bi_tbl",
    "make_CCC_mat",
    "make_dQe_mat",
    "make_dQo_mat",
    "make_Msk_mat",
    "make_Net_mat",
    "make_SA0_mat",
    "make_SAe_mat",
    "make_Sel_mat",
    "prep_Qex_ncf",
    "prep_Qfi_ncf",
    "prep_Qou_ncf",
    "prep_skl_ncf",
    "read_con_vec",
    "read_cpl_vec",
    "read_crd_vec",
    "read_err_vec",
    "read_kpr_vec",
    "read_nml_tbl",
    "read_riv_vec",
    "read_std_vec",
    "read_xpr_vec",
    "updt_Mus_Qou",
]


# *****************************************************************************
# End
# *****************************************************************************
