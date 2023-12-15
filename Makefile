build:
	virtualenv venv
	venv/bin/pip install -e .
	venv/bin/pip install -r requirements_dev.txt

test:
	venv/bin/python -m pytest

coverage:
	venv/bin/python -m coverage run -m pytest
	venv/bin/python -m coverage xml

clean:
	# like @rm -rf, but safer: only untracked git-ignored
	# any desirable difference between the two should instead be added to .gitignore
	@git clean -X -f -- .Python MANIFEST build dist "venv*" "*.egg-info" "*.egg" __pycache__

.PHONY: build clean coverage test
