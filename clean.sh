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
# Clean Python Caches and Build Artifacts
# *****************************************************************************
targets=(
    "build"
    "src/rapid2.egg-info"
    ".mypy_cache"
    "src/.mypy_cache"
    "src/rapid2/.mypy_cache"
    "src/rapid2/core/.mypy_cache"
    "src/rapid2/cli/.mypy_cache"
    "__pycache__"
    "src/__pycache__"
    "src/rapid2/__pycache__"
    "src/rapid2/core/__pycache__"
    "src/rapid2/cli/__pycache__"
)

for target in "${targets[@]}"; do
    rm -rf "$target"
done

find . -name .DS_Store -delete

# *****************************************************************************
# Nuke and Rebuild Virtual Environment
# *****************************************************************************
# Run these commands only if your local environment becomes hopelessly
# corrupted or if you want to test a completely clean installation from
# scratch.
#
# rm -rf ~/venv/
# /usr/bin/python3 -m venv ~/venv/


# *****************************************************************************
# Update Editable Install
# *****************************************************************************
# Run this command ONLY if you modify `pyproject.toml` (e.g., adding a new
# dependency or a new CLI tool). Because we use the "-e" development mode,
# standard day-to-day code changes in the src/ directory are immediately live
# through path at ~/venv/lib/python3.11/site-packages/__editable__.rapid2-*.pth
#
# ~/venv/bin/python3 -m pip install -e ".[dev]"


# *****************************************************************************
# Persistent Environment Activation Reminder
# *****************************************************************************
# We do not use the standard "source ~/venv/bin/activate" command. Instead,
# ensure the following line is placed in your ~/.bash_aliases (or ~/.bashrc)
# so your terminal always looks in the virtual environment first:
#
# export PATH=$HOME/venv/bin:$PATH


# *****************************************************************************
# End
# *****************************************************************************
