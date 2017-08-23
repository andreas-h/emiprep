from setuptools import setup

import versioneer


def _check_requirements():
    """Prepare a list of requirements to be passed to setup().

    We don't want to add required libraries to ``install_requires``
    unconditionally, because then we would risk updating an installed
    numpy/xarray/netCDF4/..., which is prone to cause trouble.  So we try to
    import the requirements first and only add them to the ``_requires`` in
    case they are not installed.  See

    """
    requirements = []

    try:
        import numpy
    except ImportError:
        requirements += ['numpy>=1.7']

    try:
        import xarray
    except ImportError:
        requirements += ['xarray>=0.8']

    try:
        import netCDF4
    except ImportError:
        requirements += ['netCDF4>=1.2.1']

    return requirements


setup(name='emiprep',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description=('(yet another) emission pre-processor for '
                   'atmospheric chemistry models'),
      url='https://emiprep.readthedocs.io/',
      author='Andreas Hilboll',
      author_email='hilboll@uni-bremen.de',
      license='AGPLv3',
      classifiers=[
          # How mature is this project? Common values are
          'Development Status :: 1 - Planning',
          # Indicate who your project is intended for
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Atmospheric Science',
          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: GNU Affero General Public License v3',
          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      packages=['emiprep'],
      install_requires=_check_requirements(),
      setup_requires=[
          'pytest-runner',
          'pytest-cov',
          'pytest-flake8',
          'versioneer',
      ],
      tests_require=[
          'pytest',
          'pytest-cov',
          'pytest-flake8',
      ],
      zip_safe=False)
