# firapria's Makefile
#
SRC=firapria

COVERFILE:=.coverage
COVERAGE_REPORT:=report -m

VENV=venv

.PHONY: deps clean check covercheck stylecheck

DEFAULT: deps stylecheck covercheck

deps: venv
	$(VENV)/bin/pip install -qr requirements.txt

venv:
	virtualenv venv

check: stylecheck
	python tests/test.py

check-versions: stylecheck
	tox

stylecheck:
	pep8 $(SRC)

covercheck:
	coverage run --source=$(SRC) tests/test.py
	coverage $(COVERAGE_REPORT)

clean:
	rm -f *~ */*~
	rm -f $(COVERFILE)

publish: check-versions
	python setup.py sdist upload
