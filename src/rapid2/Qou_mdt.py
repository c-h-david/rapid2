#!/usr/bin/env python3
# *****************************************************************************
# Qou_mdt.py
# *****************************************************************************

# Author:
# Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import numpy as np
import numpy.typing as npt
import netCDF4  # type: ignore[import-untyped]
import os
from datetime import datetime, timezone


# *****************************************************************************
# Metadata of outflow
# *****************************************************************************
def Qou_mdt(
            m3r_ncf: str,
            IV_bas_tot: npt.NDArray[np.int32],
            Qou_ncf: str
            ) -> None:
    '''Create discharge output file populated with basic metadata.

    Create discharge output file populated with basic metadata obtained from
    lateral inflow volume file: river IDs, longitudes, epoch time, epoch time
    bounds, number of time steps, value of time step. The spatial scope of the
    output file is potentially a resorted subset of the river IDs in the
    lateral inflow volume file. Global attributes are built from creation time
    and static RAPID2 information.

    Parameters
    ----------
    m3r_ncf : str
        Path to the lateral inflow volume file.
    IV_bas_tot : ndarray[int32]
        The index in domain for river IDs in basin.
    Qou_ncf : str
        Path to the discharge output file.

    Returns
    -------
    None

    Examples
    --------
    >>> m3r_ncf = './input/Test/m3_riv_Test_20000101_20000102.nc4'
    >>> IV_bas_tot = np.array([0, 1, 2, 3, 4], dtype=np.int32)
    >>> Qou_ncf = './output/Test/Qout_Test_20000101_20000102_tst.nc4'
    >>> Qou_mdt(m3r_ncf, IV_bas_tot, Qou_ncf)
    >>> Qou = netCDF4.Dataset(Qou_ncf, 'r')
    >>> Qou.variables['rivid'][:].filled()
    array([10, 20, 30, 40, 50], dtype=int32)
    >>> Qou.variables['time'][:].filled()
    array([946684800, 946695600, 946706400, 946717200, 946728000, 946738800,
           946749600, 946760400, 946771200, 946782000, 946792800, 946803600,
           946814400, 946825200, 946836000, 946846800], dtype=int32)
    >>> Qou.variables['time_bnds'][:,0].filled()
    array([946684800, 946695600, 946706400, 946717200, 946728000, 946738800,
           946749600, 946760400, 946771200, 946782000, 946792800, 946803600,
           946814400, 946825200, 946836000, 946846800], dtype=int32)
    >>> Qou.variables['time_bnds'][:,1].filled()
    array([946695600, 946706400, 946717200, 946728000, 946738800, 946749600,
           946760400, 946771200, 946782000, 946792800, 946803600, 946814400,
           946825200, 946836000, 946846800, 946857600], dtype=int32)
    >>> Qou.variables['lon'][:].filled()
    array([0.5, 2. , 1. , 2. , 0.5])
    >>> Qou.variables['lat'][:].filled()
    array([5. , 4.5, 3. , 2.5, 1. ])
    >>> os.remove(Qou_ncf)
    '''

    # -------------------------------------------------------------------------
    # Get UTC date and time
    # -------------------------------------------------------------------------
    YS_dat = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    # -------------------------------------------------------------------------
    # Open one file and create the other
    # -------------------------------------------------------------------------
    f = netCDF4.Dataset(m3r_ncf, 'r')
    g = netCDF4.Dataset(Qou_ncf, 'w', format='NETCDF4')

    # -------------------------------------------------------------------------
    # Copy dimensions
    # -------------------------------------------------------------------------
    YV_exc = ['nerr']
    for nam, dim in f.dimensions.items():
        if nam not in YV_exc:
            g.createDimension(nam, len(dim) if not dim.isunlimited() else None)

    g.createDimension('nerr', 3)

    # -------------------------------------------------------------------------
    # Create new variables
    # -------------------------------------------------------------------------
    g.createVariable('Qout', 'float32', ('time', 'rivid'))
    g['Qout'].long_name = ('average river water discharge downstream of '
                           'each river reach')
    g['Qout'].units = 'm3 s-1'
    g['Qout'].coordinates = 'lon lat'
    g['Qout'].grid_mapping = 'crs'
    g['Qout'].cell_methods = 'time: mean'

    g.createVariable('Qout_err', 'float32', ('nerr', 'rivid'))
    g['Qout_err'].long_name = ('average river water discharge uncertainty '
                               'downstream of each river reach')
    g['Qout_err'].units = 'm3 s-1'
    g['Qout_err'].coordinates = 'lon lat'
    g['Qout_err'].grid_mapping = 'crs'
    g['Qout_err'].cell_methods = 'time: mean'

    # -------------------------------------------------------------------------
    # Copy old variables
    # -------------------------------------------------------------------------
    YV_exc = ['m3_riv', 'm3_riv_err']
    YV_sub = ['rivid', 'lon', 'lat']
    for nam, var in f.variables.items():
        if nam not in YV_exc:
            if nam in YV_sub:
                g.createVariable(nam, var.datatype, var.dimensions)
                g[nam][:] = f[nam][IV_bas_tot]

            else:
                g.createVariable(nam, var.datatype, var.dimensions)
                g[nam][:] = f[nam][:]

            g[nam].setncatts(f[nam].__dict__)
            # copy variable attributes all at once via dictionary

    # -------------------------------------------------------------------------
    # Populate global attributes
    # -------------------------------------------------------------------------
    g.Conventions = f.Conventions
    g.title = f.title
    g.institution = f.institution
    g.source = 'RAPID2, ' + 'runoff: ' + os.path.basename(m3r_ncf)
    g.history = 'date created: ' + YS_dat
    g.references = 'https://github.com/c-h-david/rapid2/'
    g.comment = ''
    g.featureType = f.featureType

    # -------------------------------------------------------------------------
    # Close all files
    # -------------------------------------------------------------------------
    f.close()
    g.close()


# *****************************************************************************
# End
# *****************************************************************************
