======================
Development of emiprep
======================

Repository
==========

The emiprep repository lives at `GitLab
<https://gitlab.com/andreas-h/emiprep>`__.  Source code is managed using `Git
<https://git-scm.com/>`__ version control.  emiprep adopts the `branching model
by Vincent Driessen
<http://nvie.com/posts/a-successful-git-branching-model/>`__.


Setting up the development environment
======================================

The simplest way to set up a development environment is via conda_:

.. code:: shell

   $ git clone git@gitlab.com:YOURUSERNAME/emiprep.git
   $ cd emiprep
   $ conda create -n emiprep_dev --file requirements_dev.txt

Now, whenever you want to work on *emiprep*, you simply have to activate this
environment:

.. code:: shell

   $ source activate emiprep_dev

.. _conda: https://docs.continuum.io/docs_oss/conda/


Packaging
=========

emiprep has been uploaded to `PyPI <https://pypi.python.org/pypi/emiprep/>`__.


Links
-----

For setting up the repository, I have followed the following guides:

- https://python-packaging.readthedocs.io/en/latest/minimal.html
- https://docs.pytest.org/en/latest/goodpractices.html#integrating-with-setuptools-python-setup-py-test-pytest-runner
- https://packaging.python.org/tutorials/distributing-packages/


Version numbers
===============

emiprep uses versioneer_ for managing version numbers.

.. _versioneer: https://github.com/warner/python-versioneer


Testing
=======

emiprep uses `pytest <https://docs.pytest.org/>`__ for testing.


Making a release
================

1. branch ``release-x.y.z`` off ``develop``
2. last changes to ``release-x.y.z``
3. ``git checkout master && git merge --no-ff release-x.y.z``
4. ``git tag vx.y.z``
5. ``python setup.py sdist``
6. ``twine upload --repository pypi dist/emiprep-x-y-z.tar.gz``
7. ``git push --tags``
8. ``git checkout develop && cd conda && sh mk_conda_package.sh``
