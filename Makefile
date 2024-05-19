LC_ALL=C
export LC_ALL

build:
	virtualenv venv
	venv/bin/pip install -e .[dev,testing]

test:
	venv/bin/python -m pytest

style:
	export LC_ALL=C
	# stubs do not need to conform to old Python versions
	# only type checkers and IDEs needs to understand it
	# stb DO need to confom to 3.10 because that is what runs linting
	git ls-files -z "**.pyi" | xargs -0r python3 -m isort --py=310
	git ls-files -z "**.pyi" | xargs -0r python3 -m black --target-version=py310
	git ls-files -z "**.pyi" | xargs -0r python3 -m pyupgrade --py310-plus
	git ls-files -z "**.yaml" "**.yml" | xargs -0r -L 1 python3 -c "import sys,yaml; yaml.safe_load(open(sys.argv[1], 'rb'))"
	git ls-files "**.toml" | xargs -r -L 1 python3 -c "import sys,tomllib; tomllib.load(open(sys.argv[1], 'rb'))"
	{ head -6 THANKS ; tail +6 THANKS | LC_ALL=C sort --unique --ignore-case ; } | sponge THANKS
	LC_ALL=C sort .gitignore  | sponge .gitignore
	git ls-files -z -- "examples/frameworks/django_project/**/*.py" "tests/test_e2e.py" | xargs -0r python3 -m isort --py=37
	git ls-files -z -- "examples/frameworks/django_project/**/*.py" "tests/test_e2e.py" | xargs -0r python3 -m black --target-version=py37
	git ls-files -z -- "examples/frameworks/django_project/**/*.py" "tests/test_e2e.py" | xargs -0r python3 -m pyupgrade --py37-plus
	pylint gunicorn
	pycodestyle gunicorn


coverage:
	venv/bin/python -m converage run --source=gunicorn -m pytest
	venv/bin/python -m converage xml

clean:
	# unlike rm -rf, git-clean -X will only delete files ignored by git
	@git clean -X -f -- .Python MANIFEST build dist "venv*" "*.egg-info" "*.egg" __pycache__

.PHONY: build clean coverage test
