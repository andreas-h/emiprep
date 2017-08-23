test:
	python setup.py test

docs:
	$(MAKE) -C docs apiclean
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

doccov: docs
	$(MAKE) -C docs coverage
	cat docs/_build/coverage/*.txt

.PHONY: test doccov docs
