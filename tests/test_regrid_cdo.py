import os.path

import numpy as np
from numpy.testing import assert_allclose, assert_almost_equal

from .context import emiprep
import emiprep.regrid.cdo


TESTDATA_PATH = os.path.join(os.path.dirname(__file__), 'testdata')


def test_mkblock():
    arr1 = np.arange(8)
    actual = emiprep.regrid.cdo._mkblock(arr1, width=4, sep='\n')
    desired = '\n'.join(
        ['  0.0000000   1.0000000   2.0000000   3.0000000',
         '  4.0000000   5.0000000   6.0000000   7.0000000'])
    assert actual == desired

    arr2 = np.arange(7)
    actual = emiprep.regrid.cdo._mkblock(arr2, width=4, sep='\n')
    desired = '\n'.join(
        ['  0.0000000   1.0000000   2.0000000   3.0000000',
         '  4.0000000   5.0000000   6.0000000'])
    assert actual == desired

    arr3 = np.arange(7)
    actual = emiprep.regrid.cdo._mkblock(arr3, width=4)
    desired = '\n'.join(
        ['  0.0000000   1.0000000   2.0000000   3.0000000',
         '              4.0000000   5.0000000   6.0000000'])
    assert actual == desired

    arr4 = np.arange(11)
    actual = emiprep.regrid.cdo._mkblock(arr4)
    desired = '\n'.join(
        ['  0.0000000   1.0000000   2.0000000   3.0000000   4.0000000 '
         '  5.0000000   6.0000000   7.0000000   8.0000000   9.0000000',
         '             10.0000000'])
    assert actual == desired


def test_metgrid_to_cdo_griddes():
    fn_metgrid = os.path.join(TESTDATA_PATH, 'metgrid_coords.nc')
    griddes = emiprep.regrid.cdo.metgrid_to_cdo_griddes(fn_metgrid)
    gridlines = griddes.split('\n')

    actual = [l for l in gridlines if l.startswith('xsize')][0]
    actual = int(actual.split('=')[1].strip())
    assert actual == 210

    actual = [l for l in gridlines if l.startswith('ysize')][0]
    actual = int(actual.split('=')[1].strip())
    assert actual == 210

    actual = [l for l in gridlines if l.startswith('gridsize')][0]
    actual = int(actual.split('=')[1].strip())
    assert actual == 210 ** 2

    actual = [l for l in gridlines if l.startswith('gridtype')][0]
    actual = actual.split('=')[1].strip()
    assert actual == 'curvilinear'

    # test x order
    actual = [l for l in gridlines if l.startswith('xvals')][0]
    actual = actual.split('=')[1]
    actual = np.genfromtxt([actual.encode()])
    assert_allclose(actual,
                    [-12.16183, -12.00418, -11.84634, -11.68835, -11.53021,
                     -11.37192, -11.21347, -11.05484, -10.89609, -10.73715],
                    rtol=1e-6)

    # test xbound order
    actual = [l for l in gridlines if l.startswith('xbounds')][0]
    actual = actual.split('=')[1]
    actual = np.genfromtxt([actual.encode()])
    assert_allclose(actual,
                    [-12.22168, -12.06427, -12.10181, -12.25955, -12.06427,
                     -11.90668, -11.94391, -12.10181], rtol=1e-6)

    # test y order
    actual = [l for l in gridlines if l.startswith('yvals')][0]
    actual = actual.split('=')[1]
    actual = np.genfromtxt([actual.encode()])
    assert_allclose(actual,
                    [36.38695, 36.41717, 36.44714, 36.47681, 36.50623,
                     36.53537, 36.56424, 36.59283, 36.62114, 36.64919],
                    rtol=1e-6)

    # test ybound order
    actual = [l for l in gridlines if l.startswith('ybounds')][0]
    actual = actual.split('=')[1]
    actual = np.genfromtxt([actual.encode()])
    assert_allclose(actual,
                    [36.30832, 36.33865, 36.46554, 36.43514, 36.33865, 36.3687,
                     36.49568, 36.46554], rtol=1e-6)


def test_metgrid_to_cdo_grid_info_extraction():
    fn = os.path.join(TESTDATA_PATH, 'metgrid_coords.nc')
    griddata = emiprep.regrid.cdo._metgrid_to_cdo_grid_info_extraction(fn)

    # grid cell centers
    # lower left grid cell, centers manually extracted from ncdump output
    desired = np.float32(-12.16183)
    assert_allclose(griddata['grid_center_lon'][0, 0].values, desired,
                    rtol=1e-6)
    desired = np.float32(36.38695)
    assert_allclose(griddata['grid_center_lat'][0, 0].values, desired,
                    rtol=1e-6)
    # another grid cell, centers manually extracted from ncdump output
    desired = np.float32(34.6387)
    assert_allclose(griddata['grid_center_lon'][-1, -7].values, desired,
                    rtol=1e-6)
    desired = np.float32(63.24022)
    assert_allclose(griddata['grid_center_lat'][-1, -7].values, desired,
                    rtol=1e-6)

    # grid cell corners
    # lower left grid cell, corners manually extracted from ncdump output
    desired = np.float32([36.30832, 36.33865, 36.46554, 36.43514])
    assert_allclose(griddata['grid_corner_lat'][0, 0].values, desired,
                    rtol=1e-6)
    desired = np.float32([-12.22168, -12.06427, -12.10181, -12.25955])
    assert_allclose(griddata['grid_corner_lon'][0, 0].values, desired,
                    rtol=1e-6)
    # another grid cell, corners manually extracted from ncdump output
    desired = np.float32([34.44604, 34.71484, 34.83176, 34.56216])
    assert_allclose(griddata['grid_corner_lon'][-1, -7].values, desired,
                    rtol=1e-6)
    desired = np.float32([63.20573, 63.15335, 63.27447, 63.32701])
    assert_allclose(griddata['grid_corner_lat'][-1, -7].values, desired,
                    rtol=1e-6)
