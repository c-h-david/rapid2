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
import importlib.metadata

try:
    __version__ = importlib.metadata.version('rapid2')
except importlib.metadata.PackageNotFoundError:
    __version__ = 'unknown'


# *****************************************************************************
# End
# *****************************************************************************
