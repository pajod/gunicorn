
# ?= sets unless inherited
VIRTUAL_ENV ?= venv/
# = expands variables late
PY = $(VIRTUAL_ENV)/bin/python
style: LC_ALL:=C

$(PY):
	virtualenv $(VIRTUAL_ENV)

build: $(VIRTUAL_ENV)/bin/python
	$(VIRTUAL_ENV)/bin/python -m pip install -e .[dev,testing]

test:
	$(PY) --version
	$(PY) -m pytest

lint: docs/source/settings.rst
	$(VIRTUAL_ENV)/bin/python -m pip install -e .[dev,testing,lint-types,lint-code,lint-docs]
	$(PY) -m mypy --exclude=tests/requests/ -- gunicorn tests
	$(PY) -m mypy.stubtest -- gunicorn
	$(PY) -m pylint gunicorn
	$(PY) -m pycodestyle gunicorn
	$(PY) -m restructuredtext_lint.cli --encoding utf-8 docs/source/*.rst docs/README.rst docs/README.rst

style:
	# stubs do not need to conform to old Python versions
	# only type checkers and IDEs needs to understand it
	# stb DO need to confom to 3.10 because that is what runs linting
	# currently requires python 3.11
	$(VIRTUAL_ENV)/bin/python -m pip install -e .[style-types,style-contrib]
	$(PY) --version
	git ls-files -z "**.pyi" | xargs -0r $(PY) -m isort --py=310
	git ls-files -z "**.pyi" | xargs -0r $(PY) -m black --target-version=py310
	git ls-files -z "**.pyi" | xargs -0r $(PY) -m pyupgrade --py310-plus
	git ls-files -z "**.yaml" "**.yml" | xargs -0r -L 1 $(PY) -c "import sys,yaml; yaml.safe_load(open(sys.argv[1], 'rb'))"
	git ls-files "**.toml" | xargs -r -L 1 $(PY) -c "import sys,tomllib; tomllib.load(open(sys.argv[1], 'rb'))"
	{ head -6 THANKS ; tail +6 THANKS | LC_ALL=C sort --unique --ignore-case ; } | sponge THANKS
	LC_ALL=C sort .gitignore | sponge .gitignore
	git ls-files -z -- "examples/frameworks/django_project/**/*.py" "tests/test_e2e.py" | xargs -0r $(PY) -m isort --py=37
	git ls-files -z -- "examples/frameworks/django_project/**/*.py" "tests/test_e2e.py" | xargs -0r $(PY) -m black --target-version=py37
	git ls-files -z -- "examples/frameworks/django_project/**/*.py" "tests/test_e2e.py" | xargs -0r $(PY) -m pyupgrade --py37-plus

coverage:
	$(PY) -m converage run --source=gunicorn -m pytest
	$(PY) -m converage xml

clean:
	# unlike rm -rf, git-clean -X will only delete files ignored by git
	@git clean -X -f -- .Python MANIFEST build dist "venv*" "*.egg-info" "*.egg" __pycache__

.PHONY: build clean coverage test style lint
