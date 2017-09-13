==================
Installing emiprep
==================

Required dependencies
---------------------

* Python 2.7, 3.4, 3.5, or 3.6
* `numpy <http://www.numpy.org/>`__ (1.7 or later)
* `pandas <http://pandas.pydata.org/>`__ (0.15.0 or later)
* `xarray <http://xarray.pydata.org/>`__ (0.9.0 or later)
* `netcdf4-python <https://unidata.github.io/netcdf4-python/>`__ (1.2.1 or later)


Instructions
------------

The recommended way to install emiprep is using the Anaconda_ platform.  If you
don't have Anaconda installed on your system yet, you can use the minimal
miniconda_ installation.

.. _Anaconda: https://www.continuum.io/what-is-anaconda
.. _miniconda: http://conda.pydata.org/miniconda.html

.. note::

   Currently, the Anaconda installation of emiprep only works with Python 3.5.

I *strongly* recommend to install emiprep in its own Anaconcda *environment*.
To do so, run the commands

.. code:: shell

   conda create -n emiprep_env python=3.5
   source activate emiprep_env
   conda install -c andreas-h emiprep

Now, whenever you want to use emiprep, you have to ``source activate
emiprep_env`` first.
