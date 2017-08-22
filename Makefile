test:
	python setup.py test

doccov:
	$(MAKE) -C docs coverage

.PHONY: test doccov
