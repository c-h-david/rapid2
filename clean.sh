#!/bin/bash
# *****************************************************************************
# clean.sh
# *****************************************************************************

# Purpose:
# Remove files and directories created during browsing, building and linting.
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
# Clean up
# *****************************************************************************
targets=(
    ".DS_Store"
    "*/.DS_Store"
    "*/*/.DS_Store"
    "build"
    "src/*.egg-info"
    ".mypy_cache"
    "src/.mypy_cache"
    "src/rapid2/.mypy_cache"
    "__pycache__"
    "src/__pycache__"
    "src/rapid2/__pycache__"
)

for target in "${targets[@]}"; do
    rm -rf "$target"
done


# *****************************************************************************
# End
# *****************************************************************************
