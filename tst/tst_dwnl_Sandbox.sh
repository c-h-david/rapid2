#!/bin/bash
# *****************************************************************************
# tst_dwnl_Sandbox.sh
# *****************************************************************************

# Purpose:
# This script downloads all files from:
# David, Cédric H. (2025), RAPID Sandbox, Zenodo.
# DOI: 10.5281/zenodo.17298742.
# The script returns the following exit codes
# - 0  if all downloads are successful 
# - 22 if there was a conversion problem
# - 44 if one download is not successful
# Author:
# Cedric H. David, 2025-2025.


# *****************************************************************************
# Best practices
# *****************************************************************************
set -euo pipefail
IFS=$'\n\t'
# Ensures the script exits on errors or undefined variables.
# Makes pipelines fail if any command fails.
# Protects loops and string splitting from breaking on spaces.


# *****************************************************************************
# Publication message
# *****************************************************************************
echo "********************"
echo "Downloading files from:   https://doi.org/10.5281/zenodo.17298742"
echo "These files are under a Creative Commons Attribution (CC BY) license."
echo "Please cite the DOI if using these files for your publications."
echo "********************"


# *****************************************************************************
# Location of the dataset
# *****************************************************************************
URL="https://zenodo.org/records/21085813/files"


# *****************************************************************************
# Download all input files
# *****************************************************************************
folder="../input/Sandbox"
list=(
    "con_Sandbox.parquet"
    "Qex_Sandbox_19700101_19700110_TR.nc4"
    "Q00_Sandbox_19700101_19700110_TR.nc4"
    "kpr_Sandbox.parquet"
    "xpr_Sandbox.parquet"
    "bas_Sandbox_ascend.parquet"
    "nml_Sandbox.yml"
    "cpl_Sandbox.parquet"
    "crd_Sandbox.parquet"
    "obs_Sandbox.parquet"
    "Qob_Sandbox_19700101_19700110_TR.nc4"
    "Qex_Sandbox_19700101_19700110_FG.nc4"
    "Q00_Sandbox_19700101_19700110_FG.nc4"
)

mkdir -p $folder
for file in "${list[@]}"; do
    if ! wget -nv -nc "$URL"/"$file" -P "$folder"; then
        echo "Problem downloading $file" >&2
        exit 44
    fi
done


# *****************************************************************************
# Download all output files
# *****************************************************************************
folder="../output/Sandbox"
list=(
    "Qou_Sandbox_19700101_19700110_TR.nc4"
    "Qfi_Sandbox_19700101_19700110_TR.nc4"
    "Qou_Sandbox_19700101_19700110_OL.nc4"
    "Qfi_Sandbox_19700101_19700110_OL.nc4"
)

mkdir -p $folder
for file in "${list[@]}"; do
    if ! wget -nv -nc "$URL"/"$file" -P "$folder"; then
        echo "Problem downloading $file" >&2
        exit 44
    fi
done


# *****************************************************************************
# Convert legacy files
# *****************************************************************************
# N/A


# *****************************************************************************
# End
# *****************************************************************************
