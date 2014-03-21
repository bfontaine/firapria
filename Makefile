# firapria's Makefile
#
SRC=firapria

.DEFAULT: check
.PHONY: check stylecheck

deps:
	pip install -qr requirements.txt

check:
	python tests/test.py

stylecheck:
	pep8 $(SRC)

publish: check
	python setup.py sdist upload
