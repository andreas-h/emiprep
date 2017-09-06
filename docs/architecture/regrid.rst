Re-gridding to WRF grids
========================

The module :py:mod:`emiprep.regrid` will handle re-gridding emission data to WRF
grids.


Deciding which external interpolation library to use
----------------------------------------------------

The actual re-gridding code can come from a number of sources; at this point,
we have not decided yet which road to take:

1. There is the great ANTHRO_EMISS_ code developed by NCAR.  However, the
   license of ANTHRO_EMISS is not explicit, so it is unclear if we could
   include that code in *emiprep*.

2. CDO_ contains remapping routines which are based on the SCRIP_ library.  CDO
   is written in C++, and it should be possible to create a Cython wrapper for
   the remapping routine(s) needed by *emiprep*.  CDO is licensed under GPLv2,
   which means we could include CDO source code in *emiprep*.

3. We could use SCRIP_ directly, but it is not entirely clear how this would
   work.  Apparently, SCRIP relies on reading mapping information from some
   external files, which would need to be generated in a temporary folder
   first.  SCRIP is released with the following `copyright statement
   <http://oceans11.lanl.gov/trac/SCRIP/browser/trunk/SCRIP/source/copyright>`__:

      Copyright (c) 1997, 1998 the Regents of the University of California.

      This software and ancillary information (herein called software) called
      SCRIP is made available under the terms described here.  The software has
      been approved for release with associated LA-CC Number 98-45.

      Unless otherwise indicated, this software has been authored by an
      employee or employees of the University of California, operator of the
      Los Alamos National Laboratory under Contract No. W-7405-ENG-36 with the
      U.S. Department of Energy.  The U.S.  Government has rights to use,
      reproduce, and distribute this software.  The public may copy and use
      this software without charge, provided that this Notice and any statement
      of authorship are reproduced on all copies.  Neither the Government nor
      the University makes any warranty, express or implied, or assumes any
      liability or responsibility for the use of this software.

      If software is modified to produce derivative works, such modified
      software should be clearly marked, so as not to confuse it with the
      version available from Los Alamos National Laboratory.

   So it seems that we can include SCRIP source code in *emiprep*.

4. PySCRIP_ is a Python wrapper around SCRIP, licensed under BSD-3-clause.
   However, like SCRIP, it depends on some input files to be generated before
   the remapping procedure, and it is unclear how PySCRIP's `remap function
   <https://github.com/dchandan/PySCRIP/blob/master/PySCRIP/remap.py#L7>`__
   would work in our case.

Concluding, it seems that using CDO_ would be the best option.  Actually, we
could start using the `CDO Python bindings
<https://pypi.python.org/pypi/cdo/1.3.4>`__ which rely on the command-line CDO
be installed on the system.  This would make installation a bit harder (not
really, as we'll promote conda), and it would allow us to go forward without
having to spend a lot of time on incorporating the interpolation library as an
external module via f2py or Cython.  We could then at a later stage write
proper Cython bindings for the CDO routine that *emiprep* is using.  The only
requirement which we have with CDO is that we need the corners of the grid
cells of the WRF and input grids.

.. _ANTHRO_EMISS: https://www2.acom.ucar.edu/wrf-chem/wrf-chem-tools-community
.. _CDO: https://code.mpimet.mpg.de/projects/cdo
.. _SCRIP: http://oceans11.lanl.gov/trac/SCRIP
.. _PySCRIP: https://github.com/dchandan/PySCRIP


Using CDO for regridding
------------------------

Defining the WRF grid for CDO
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Looking at the `Horizontal grids
<https://code.mpimet.mpg.de/projects/cdo/embedded/index.html#x1-130001.3>`__
section of the CDO documentation, it seems that we have to create the ASCII grid
description file of the WRF (i.e., target) grid ourselves.  There are two
possible ways to do this:

1. Manually create the file, including the corners

2. Try to use the `griddes
   <https://code.mpimet.mpg.de/projects/cdo/embedded/index.html#x1-620002.1.6>`__
   operator, as ``cdo griddes INFILE``.  Probably, before doing that, we have to
   create a netCDF file which contains the grid cell boundaries and conforms to
   the `SCRIP metadata convention
   <https://code.mpimet.mpg.de/projects/cdo/embedded/index.html#x1-150001.3.2>`__
   which is understood by CDO.

The CDO documentation contains an `example
<https://code.mpimet.mpg.de/projects/cdo/embedded/index.html#x1-837000D.1>`__ of
how the bounds have to be encoded:

   Here is an example for the CDO description of a curvilinear grid. xvals/yvals
   describe the positions of the 6x5 quadrilateral grid cells. The first 4
   values of xbounds/ybounds are the corners of the first grid cell.

   .. code::

      gridtype  = curvilinear 
      gridsize  = 30 
      xsize     = 6 
      ysize     = 5 
      xvals     =  -21  -11    0   11   21   30  -25  -13    0   13 
                    25   36  -31  -16    0   16   31   43  -38  -21 
                     0   21   38   52  -51  -30    0   30   51   64 
      xbounds   =  -23  -14  -17  -28       -14   -5   -6  -17        -5    5    6   -6 
                     5   14   17    6        14   23   28   17        23   32   38   28 
                   -28  -17  -21  -34       -17   -6   -7  -21        -6    6    7   -7 
                     6   17   21    7        17   28   34   21        28   38   44   34 
                   -34  -21  -27  -41       -21   -7   -9  -27        -7    7    9   -9 
                     7   21   27    9        21   34   41   27        34   44   52   41 
                   -41  -27  -35  -51       -27   -9  -13  -35        -9    9   13  -13 
                     9   27   35   13        27   41   51   35        41   52   63   51 
                   -51  -35  -51  -67       -35  -13  -21  -51       -13   13   21  -21 
                    13   35   51   21        35   51   67   51        51   63   77   67 
      yvals     =   29   32   32   32   29   26   39   42   42   42 
                    39   35   48   51   52   51   48   43   57   61 
                    62   61   57   51   65   70   72   70   65   58 
      ybounds   =   23   26   36   32        26   27   37   36        27   27   37   37 
                    27   26   36   37        26   23   32   36        23   19   28   32 
                    32   36   45   41        36   37   47   45        37   37   47   47 
                    37   36   45   47        36   32   41   45        32   28   36   41 
                    41   45   55   50        45   47   57   55        47   47   57   57 
                    47   45   55   57        45   41   50   55        41   36   44   50 
                    50   55   64   58        55   57   67   64        57   57   67   67 
                    57   55   64   67        55   50   58   64        50   44   51   58 
                    58   64   72   64        64   67   77   72        67   67   77   77 
                    67   64   72   77        64   58   64   72        58   51   56   64
