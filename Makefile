# firapria's Makefile
#
SRC=firapria

COVERFILE:=.coverage
COVERAGE_REPORT:=report -m

VENV=venv
BINPREFIX=$(VENV)/bin/

.PHONY: deps clean check covercheck stylecheck

DEFAULT: deps stylecheck covercheck

deps: venv
	$(BINPREFIX)pip install -qr requirements.txt

venv:
	virtualenv venv

check: stylecheck
	$(BINPREFIX)python tests/test.py

check-versions: stylecheck
	$(BINPREFIX)tox

stylecheck:
	$(BINPREFIX)pep8 $(SRC)

covercheck:
	$(BINPREFIX)coverage run --source=$(SRC) tests/test.py
	$(BINPREFIX)coverage $(COVERAGE_REPORT)

clean:
	rm -f *~ */*~
	rm -f $(COVERFILE)

publish: check-versions
	$(BINPREFIX)python setup.py sdist upload
