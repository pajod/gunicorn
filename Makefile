VIRTUAL_ENV ?= venv
PYTHON = ${VIRTUAL_ENV}/bin/python

build:
	virtualenv ${VIRTUAL_ENV}
	${PYTHON} -m pip install -e .
	${PYTHON} -m pip install -r requirements_dev.txt

test:
	cd docs && ${PYTHON} -m sphinx.cmd.build -b "dummy" -d _build/doctrees source "_build/dummy"
	${PYTHON} -m pytest

coverage:
	${PYTHON} -m converage run --source=gunicorn -m pytest
	${PYTHON} -m converage xml

clean:
	# unlike rm -rf, git-clean -X will only delete files ignored by git
	@git clean -X -f -- .Python MANIFEST build dist "venv*" "*.egg-info" "*.egg" __pycache__

.PHONY: build clean coverage test
