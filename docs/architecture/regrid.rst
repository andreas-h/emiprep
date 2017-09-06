Re-gridding to WRF grids
========================

The module :py:mod:`emiprep.regrid` will handle re-gridding emission data to WRF
grids.

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
