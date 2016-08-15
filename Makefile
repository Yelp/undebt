.PHONY: all dev venv clean pre-commit tests test docs

all: dev pre-commit

dev: venv
	venv/bin/pip install -r requirements-dev.txt
	@echo ""
	@echo "========================================"
	@echo "Don't forget to source venv/bin/activate"

venv:
	test -s venv || { virtualenv -p python2.7 venv; }
	venv/bin/pip install -r requirements.txt

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -rf docs/build
	rm -rf .tox
	rm -rf *.egg-info
	rm -rf venv
	rm -rf build
	rm -rf dist

pre-commit:
	@tox -e pre-commit -- install -f --install-hooks

tests: test

test: pre-commit
	tox

docs:
	tox -e docs

build:
	python setup.py sdist bdist_wheel
