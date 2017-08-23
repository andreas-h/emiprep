======================
Development of emiprep
======================

Repository
==========

The emiprep repository lives at `GitHub
<https://github.com/andreas-h/emiprep>`__.  Source code is managed using `Git
<https://git-scm.com/>`__ version control.  emiprep adopts the `branching model
by Vincent Driessen
<http://nvie.com/posts/a-successful-git-branching-model/>`__.


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
4. ``git push --tags``
5. ``python setup.py sdist``
6. ``twine upload --repository pypi dist/emiprep-x-y-z.tar.gz``
7. ``git checkout develop && cd conda && sh mk_conda_package.sh``
