"""emiprep.regrid.cdo
==================

This module contains methods to regrid to WRF grids using CDO_.

.. currentmodule:: emiprep.regrid.cdo

.. autosummary::
   :toctree: api/

   metgrid_to_cdo_griddes

   _metgrid_to_cdo_grid_info_extraction
   _mkblock

.. _CDO: https://code.mpimet.mpg.de/projects/cdo

"""

from itertools import product

# in Python3, we need to use BytesIO
try:
    from StringIO import StringIO
    from StringIO import StringIO as _StreamIO
except ImportError:
    from io import StringIO
    from io import BytesIO as _StreamIO

import numpy as np
import xarray as xr


def _metgrid_to_cdo_grid_info_extraction(fn_metgrid):
    """Extract grid information from WPS metgrid file.

    Parameters
    ----------
    fn_metgrid : str
        The full path to a WPS metgrid file from which the grid information
        shall be extracted

    Returns
    -------
    gridinfo : xarray.Dataset
        The grid information of the metgrid file

    """
    METGRID_SCRIP_TRANSFORM = {
        'XLAT_M': 'grid_center_lat', 'XLONG_M': 'grid_center_lon',
        'south_north': 'grid_ysize', 'west_east': 'grid_xsize'}

    ds = xr.open_dataset(fn_metgrid)
    ds.rename(METGRID_SCRIP_TRANSFORM, inplace=True)

    lat_center = ds['grid_center_lat'][0]
    lon_center = ds['grid_center_lon'][0]
    assert lat_center.shape == lon_center.shape

    # create corner arrays
    lat_corner_orig = ds['XLAT_C'][0].values
    lon_corner_orig = ds['XLONG_C'][0].values
    assert lat_corner_orig.shape == lon_corner_orig.shape

    lat_corner = xr.DataArray(
        np.zeros((lat_center.shape[0], lat_center.shape[1], 4),
                 dtype=np.float32),
        dims=['grid_ysize', 'grid_xsize', 'grid_corners'],
        name='grid_corner_lat')
    lon_corner = xr.DataArray(
        np.zeros((lat_center.shape[0], lat_center.shape[1], 4),
                 dtype=np.float32),
        dims=['grid_ysize', 'grid_xsize', 'grid_corners'],
        name='grid_corner_lon')

    for ii, jj in product(range(lat_center.shape[0]),
                          range(lat_center.shape[1])):
        lat_corner[ii, jj] = lat_corner_orig[[ii, ii, ii + 1, ii + 1],
                                             [jj, jj + 1, jj + 1, jj]]
        lon_corner[ii, jj] = lon_corner_orig[[ii, ii, ii + 1, ii + 1],
                                             [jj, jj + 1, jj + 1, jj]]

    # need to include data variable in nc file, else CDO will complain
    dummy = xr.DataArray(
        np.zeros((lat_center.shape[0], lat_center.shape[1]), dtype=np.float32),
        dims=['grid_ysize', 'grid_xsize'], name='dummydata')
    dummy.attrs['coordinates'] = 'grid_center_lon grid_center_lat'

    # fix metadata
    for arr in lat_center, lon_center, lat_corner, lon_corner:
        arr.attrs['units'] = 'degrees'
    lat_center.attrs['standard_name'] = 'latitude'
    lon_center.attrs['standard_name'] = 'longitude'
    lat_center.attrs['bounds'] = 'grid_corner_lat'
    lon_center.attrs['bounds'] = 'grid_corner_lon'

    grid_dims = xr.DataArray(
        np.arange(1, 3),
        {'grid_rank': np.arange(1, 3)},
        ['grid_rank'], name='grid_dims')

    n_grid_size = lat_center.shape[0] * lat_center.shape[1]
    grid_imask = xr.DataArray(
        np.ones(n_grid_size, dtype=int),
        {'grid_size': np.arange(1, n_grid_size + 1)}, ['grid_size'],
        name='grid_imask')
    grid_imask.attrs['coordinates'] = 'grid_center_lon grid_center_lat'
    grid_imask.attrs['units'] = 'unitless'

    ds_new = xr.Dataset({arr.name: arr for arr in [lat_center, lon_center,
                                                   lat_corner, lon_corner,
                                                   grid_dims, grid_imask,
                                                   dummy]})
    del ds_new['Times']
    return ds_new


def _mkblock(arr, width=10, sep=None):
    """Create a block of string-formatted floats to be saved in CDO grid file

    Parameters
    ----------
    arr : numpy.ndarray
        The array to format

    width : int
        How many numbers to put on one line

    sep : str
        The line separator.  This will usually inlcude any leading spaces
        needed in subsequent lines after the first.  By default, 12 spaces will
        be inserted after each linebreak, to generate nicely formatted griddes
        files.

    Returns
    -------
    griddes : str
        The string containing *arr*.

    """
    if sep is None:
        sep = '\n            '

    # how many rows do we need to generate?
    nrows = arr.size // width
    if arr.size % width:
        nrows += 1

    arr_slices = [arr.ravel()[i * width:(i + 1) * width] for i in range(nrows)]
    with _StreamIO() as fd:
        for sl in arr_slices:
            np.savetxt(fd, np.atleast_2d(sl), fmt='%11.7f', newline=sep)
        griddes = fd.getvalue().decode()

    # remove empty lines
    griddes = '\n'.join(
        [line for line in griddes.split('\n') if line.strip() != ''])

    return griddes


def metgrid_to_cdo_griddes(fn_metgrid, fn_griddes=None):
    """Create a CDO grid description file from a WPS metgrid file.

    Parameters
    ----------
    fn_metgrid : str
        The full path to a WPS metgrid file from which the grid information
        shall be extracted
    fn_griddes : str, optional
        If given, the grid description will be written to that location.  Any
        existing file with the same name will be overwritten.

    Returns
    -------
    griddes : str
        The CDO grid description

    """
    griddes = _metgrid_to_cdo_grid_info_extraction(fn_metgrid)

    with StringIO() as fd:
        fd.write('gridtype  = curvilinear\n')
        fd.write('gridsize  = {}\n'.format(griddes.dims['grid_size']))
        fd.write('xsize     = {}\n'.format(griddes.dims['grid_xsize']))
        fd.write('ysize     = {}\n'.format(griddes.dims['grid_ysize']))

        fd.write('xvals     = {}\n'.format(
            _mkblock(griddes['grid_center_lon'].values)))
        fd.write('xbounds   = {}\n'.format(
            _mkblock(griddes['grid_corner_lon'].values, width=8)))

        fd.write('yvals     = {}\n'.format(
            _mkblock(griddes['grid_center_lat'].values)))
        fd.write('ybounds   = {}\n'.format(
            _mkblock(griddes['grid_corner_lat'].values, width=8)))

        retval = fd.getvalue()

    if fn_griddes:
        with open(fn_griddes, 'w') as fd:
            fd.write(retval)
    return retval
