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
URL="https://zenodo.org/records/17738091/files"


# *****************************************************************************
# Download all input files
# *****************************************************************************
folder="../input/Sandbox"
list=(
    "rapid_connect_Sandbox.csv"
    "Qext_Sandbox_19700101_19700110.nc4"
    "Qinit_Sandbox_19700101_19700110.nc4"
    "k_Sandbox.csv"
    "x_Sandbox.csv"
    "riv_bas_id_Sandbox.csv"
    "namelist_Sandbox.yml"
    "rapid_coupling_Sandbox.csv"
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
    "Qout_Sandbox_19700101_19700110.nc4"
    "Qfinal_Sandbox_19700101_19700110.nc4"
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
