Reading grid information from WRF files
=======================================

The module :py:mod:`emiprep.wrfgrid` will handles calculations regarding the WRF
horizontal gridding.

In order to do the spatial remapping of emissions to the WRF grid, we need
information on the extents of the grid cells.  By default, the ``wrfinput_d0X``
files only contain the grid cell centers (in the variables ``XLAT`` and
``XLONG``).  Information on the corners can be obtained in two ways:

1. Reading *geogrid* output files in addition to ``wrfinput_d0X`` (there, the
   grid cell corners are contained in the variables ``XLAT_C`` and
   ``XLONG_C``.)

2. Modify the WRF *registriy* so that ``XLAT_C`` and ``XLONG_C`` are contained
   in the ``wrfinput_d0X`` files.
