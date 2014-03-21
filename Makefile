# firapria's Makefile
#
SRC=firapria

COVERFILE:=.coverage
COVERAGE_REPORT:=report -m

.DEFAULT: covercheck
.PHONY: clean check covercheck stylecheck

deps:
	pip install -qr requirements.txt

check:
	python tests/test.py

stylecheck:
	pep8 $(SRC)

covercheck:
	coverage run --source=$(SRC) tests/test.py
	coverage $(COVERAGE_REPORT)

clean:
	rm -f *~ */*~
	rm -f $(COVERFILE)

publish: check
	python setup.py sdist upload
