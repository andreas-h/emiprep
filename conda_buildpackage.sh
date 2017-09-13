#!/bin/bash

PROJECT=emiprep
DOCURL="https://emiprep.readthedocs.io/"
DEVURL="https://gitlab.com/andreas-h/emiprep/"
DESCRIPTION="(yet another) emission pre-processor for atmospheric chemistry models"

if [ -z "${CI_PYTHON_VERSION+x}" ]; then
    echo "This script must be run from within Gitlab CI"
    exit 1
fi

echo '#########################################################################'
echo "Building conda backage for CI_PYTHON_VERSION=${CI_PYTHON_VERSION}"
echo '#########################################################################'

echo '#########################################################################'
echo 'Begin conda config / update ...'
hash -r
conda config --set always_yes yes --set changeps1 no
conda update -q conda
conda config --append channels conda-forge
conda install -q conda-build anaconda-client
echo 'End conda config / update ...'
echo '#########################################################################'

echo '#########################################################################'
echo 'Begin conda info (1) ...'
conda info -a
echo 'End conda info (1) ...'
echo '#########################################################################'

echo '#########################################################################'
echo 'Begin conda create ...'
conda create -q -n "${PROJECT}_test" python="$CI_PYTHON_VERSION"
echo 'End conda create ...'
echo '#########################################################################'

# shellcheck disable=SC1091
. activate "${PROJECT}_test"

export CONDA_PYTHON_OPTION="--python=${CI_PYTHON_VERSION}"


# make sure we don't continue in case of an error
# #############################################################################
set -e

# change to the conda directory
# #############################################################################
mkdir -p conda
rm -rf conda/*

# first we update the meta.yaml description with info from the pypi release
# #############################################################################
echo '#########################################################################'
echo 'Begin conda skeleton ...'
conda skeleton pypi --output-dir conda $PROJECT
echo 'End conda skeleton ...'
echo '#########################################################################'

echo '#########################################################################'
echo 'Begin conda info (2) ...'
conda info -a
echo 'End conda info (2) ...'
echo '#########################################################################'

# the sed comes from https://stackoverflow.com/a/10212706/152439
METAYAML=conda/$PROJECT/meta.yaml
##PROJECT_VERSION=$(grep 'set version = ' $METAYAML | sed 's/[^"]*"\([^"]*\)".*/\1/')


# add windows build script
perl -0777 -i -pe "s/  script: python setup.py install  --single-version-externally-managed --record=record.txt/  script: python setup.py install  --single-version-externally-managed --record=record.txt  # [not win]\n  script: \"%PYTHON%\" setup.py install && if errorlevel 1 exit 1                             # [win]/igs" $METAYAML

# fix additional metadata
perl -0777 -i -pe "s%  license_file: ''%  license_file: LICENSE%igs" $METAYAML
perl -0777 -i -pe "s%  description: ''%  description: |\n    $DESCRIPTION%igs" $METAYAML
perl -0777 -i -pe "s%  doc_url: ''%  doc_url: $DOCURL%igs" $METAYAML
perl -0777 -i -pe "s%  dev_url: ''%  dev_url: $DEVURL%igs" $METAYAML
perl -0777 -i -pe "s%  recipe-maintainers: ''%  recipe-maintainers:\n    - andreas-h%igs" $METAYAML


echo '#########################################################################'
echo 'Begin conda build ...'
conda build conda/$PROJECT --output-folder conda/pkgs/ --python="${CI_PYTHON_VERSION}"
echo 'End conda build ...'
echo '#########################################################################'

CONDA_PKG_FILENAME=$(conda build conda/$PROJECT --croot conda/pkgs/ --python="${CI_PYTHON_VERSION}" --output)

echo '#########################################################################'
echo 'Begin conda convert ...'
conda convert --platform all "$CONDA_PKG_FILENAME" -o conda/pkgs/
echo 'End conda convert ...'
echo '#########################################################################'

. deactivate

echo '#########################################################################'
echo "CONDA_PKG_FILENAME: ${CONDA_PKG_FILENAME}"
echo '#########################################################################'
echo "find on pkgs dir ..."
echo '#########################################################################'
find conda/pkgs/ -name $(basename "${CONDA_PKG_FILENAME}")
echo '#########################################################################'
echo '#########################################################################'
echo 'Begin anaconda upload ...'
find conda/pkgs/ -name $(basename "${CONDA_PKG_FILENAME}") -exec anaconda  -t "$ANACONDA_TOKEN" upload {} +
echo 'End anaconda upload ...'
echo '#########################################################################'
