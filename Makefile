test:
	python setup.py test

docs:
	$(MAKE) -C docs apiclean
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

doccov: docs
	$(MAKE) -C docs coverage

.PHONY: test doccov docs
