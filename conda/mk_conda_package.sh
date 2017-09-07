#!/bin/sh

# don't do anything in case conda command isn't available
# #############################################################################
set -e
CONDA_TEST=$(conda)

# change to this script's directory
# #############################################################################
# see https://stackoverflow.com/a/16349776/152439
cd "${0%/*}"

# make sure we're on the develop branch
# #############################################################################
if [ $(git rev-parse --abbrev-ref HEAD) != 'develop' ]; then
  echo "You have to run this script from the 'develop' branch.  Aborting."
  exit 1
fi

# first we update the meta.yaml description with info from the pypi release
# #############################################################################
rm -rf emiprep
conda skeleton pypi emiprep

# extract emiprep version from meta.yaml
# #############################################################################
# the sed comes from https://stackoverflow.com/a/10212706/152439
EMIPREP_VERSION=$(grep 'set version = ' emiprep/meta.yaml | sed 's/[^"]*"\([^"]*\)".*/\1/')

# next, we fix several issues in the automatically generated meta.yaml
# #############################################################################
METAYAML=emiprep/meta.yaml

# add windows build script
perl -0777 -i -pe "s/  script: python setup.py install  --single-version-externally-managed --record=record.txt/  script: python setup.py install  --single-version-externally-managed --record=record.txt  # [not win]\n  script: \"%PYTHON%\" setup.py install && if errorlevel 1 exit 1                             # [win]/igs" $METAYAML

# fix additional metadata
perl -0777 -i -pe "s/  license_file: ''/  license_file: LICENSE/igs" $METAYAML
perl -0777 -i -pe "s/  description: ''/  description: |\n    emiprep is yet another emission pre-processor for atmospheric chemistry\n    models. While being developed with WRF-Chem in mind, there is no reason why\n    it could not be extended to be used with other models as well./igs" $METAYAML
perl -0777 -i -pe "s/  doc_url: ''/  doc_url: https:\/\/emiprep.readthedocs.io\//igs" $METAYAML
perl -0777 -i -pe "s/  dev_url: ''/  dev_url: https:\/\/github.com\/andreas-h\/emiprep\//igs" $METAYAML
perl -0777 -i -pe "s/  recipe-maintainers: ''/  recipe-maintainers:\n    - andreas-h/igs" $METAYAML

# add numpy to run dependencies.  this is needed because our setup.py doesn't necessarily add numpy to the install_requires section
perl -0777 -i -pe "s/  run:\n    - python\n    - xarray >=0.8/  run:\n    - python\n    - numpy >=1.7\n    - xarray >=0.8/igs" $METAYAML
# remove xarray and netcdf from the build dependencies
perl -0777 -i -pe "s/    - xarray >=0.8\n    - netcdf4 >=1.2.1\n  run:/  run:/igs" $METAYAML

# build package
# #############################################################################
conda build emiprep --output-folder pkgs/

CONDA_PKG_FILENAME=$(conda build emiprep --croot pkgs/ --output)

# convert package to all other platforms
# #############################################################################
conda convert --platform osx-64,linux-32,linux-64 $CONDA_PKG_FILENAME -o pkgs/

# upload all packages to Anaconda
# #############################################################################
find pkgs/ -wholename "pkgs/*/emiprep-${EMIPREP_VERSION}-py??????????_?.tar.bz2" -exec anaconda  -t $ANACONDA_TOKEN upload {} +

# commit the new meta.yaml to git
# #############################################################################
git commit emiprep/meta.yaml -m "PKG: update anaconda package to version $EMIPREP_VERSION"
git push origin develop
