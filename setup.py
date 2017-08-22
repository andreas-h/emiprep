from setuptools import setup

setup(name='emiprep',
      version='0.0.0',
      description='(yet another) emission pre-processor for atmospheric chemistry models',
      url='http://github.com/andreas-h/emiprep',
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
      setup_requires=[
          'pytest-runner',
           ],
      tests_require=[
          'pytest',
           ],
      zip_safe=False)
