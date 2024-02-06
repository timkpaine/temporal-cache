build:  ## Build the repository
	python setup.py build 

tests:  ## run the tests
	python -m pytest -vvv temporalcache/tests --cov=temporalcache --junitxml=python_junit.xml --cov-report=xml --cov-branch

lint: ## run linter
	python -m ruff temporalcache setup.py

fix:  ## run autofix
	python -m ruff format temporalcache/ setup.py

clean: ## clean the repository
	find . -name "__pycache__" | xargs  rm -rf 
	find . -name "*.pyc" | xargs rm -rf 
	find . -name ".ipynb_checkpoints" | xargs  rm -rf 
	rm -rf .coverage cover htmlcov logs build dist *.egg-info
	make -C ./docs clean

install:  ## install to site-packages
	python -m pip install .

dev:
	python -m pip install .[dev]

dist:  ## create dists
	rm -rf dist build
	python setup.py sdist bdist_wheel
	python -m twine check dist/*
	
publish: dist  ## dist to pypi
	python -m twine upload dist/* --skip-existing

# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'

.PHONY: clean build run test tests help annotate annotate_l docs dist
