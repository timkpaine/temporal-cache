#########
# BUILD #
#########
.PHONY: develop-py develop-rust develop
develop-py:
	python -m pip install -e .[develop]

develop-rust:
	make -C rust develop

develop: develop-rust develop-py  ## setup project for development

.PHONY: build-py build-rust build dev
build-py:
	maturin build

build-rust:
	make -C rust build

dev: build  ## lightweight in-place build for iterative dev
	$(_CP_COMMAND)

build: build-rust build-py  ## build the project

.PHONY: install
install:  ## install python library
	python -m pip install .

UNAME := $(shell uname)
ifeq ($(UNAME), Darwin)
	_CP_COMMAND := cp target/debug/libtemporal_cache.dylib temporal_cache/temporal_cache.abi3.so
else
	_CP_COMMAND := cp target/debug/libtemporal_cache.so temporal_cache/temporal_cache.abi3.so
endif

#########
# LINTS #
#########
.PHONY: lint-py lint-rust lint lints
lint-py:  ## run python linter with ruff
	python -m ruff check temporal_cache
	python -m ruff format --check temporal_cache

lint-rust:  ## run rust linter
	make -C rust lint

lint: lint-rust lint-py  ## run project linters

# alias
lints: lint

.PHONY: fix-py fix-rust fix format
fix-py:  ## fix python formatting with ruff
	python -m ruff check --fix temporal_cache
	python -m ruff format temporal_cache

fix-rust:  ## fix rust formatting
	make -C rust fix

fix: fix-rust fix-py  ## run project autoformatters

# alias
format: fix

################
# Other Checks #
################
.PHONY: check-manifest checks check

check-manifest:  ## check python sdist manifest with check-manifest
	check-manifest -v

checks: check-manifest

# alias
check: checks

#########
# TESTS #
#########
.PHONY: test-py tests-py coverage-py
test-py:  ## run python tests
	python -m pytest -v temporal_cache/tests

# alias
tests-py: test-py

coverage-py:  ## run python tests and collect test coverage
	python -m pytest -v temporal_cache/tests --cov=temporal_cache --cov-report term-missing --cov-report xml

.PHONY: test-rust tests-rust coverage-rust
test-rust:  ## run rust tests
	make -C rust test

# alias
tests-rust: test-rust

coverage-rust:  ## run rust tests and collect test coverage
	make -C rust coverage

.PHONY: test coverage tests
test: test-py test-rust  ## run all tests
coverage: coverage-py coverage-rust  ## run all tests and collect test coverage

# alias
tests: test

###########
# VERSION #
###########
.PHONY: show-version patch minor major

show-version:  ## show current library version
	@bump-my-version show current_version

patch:  ## bump a patch version
	@bump-my-version bump patch

minor:  ## bump a minor version
	@bump-my-version bump minor

major:  ## bump a major version
	@bump-my-version bump major

########
# DIST #
########
.PHONY: dist-py-wheel dist-py-sdist dist-rust dist-check dist publish

dist-py-wheel:  # build python wheel
	python -m cibuildwheel --output-dir dist

dist-py-sdist:  # build python sdist
	python -m build --sdist -o dist

dist-rust:  # build rust dists
	make -C rust dist

dist-check:  ## run python dist checker with twine
	python -m twine check dist/*

dist: clean build dist-rust dist-py-wheel dist-py-sdist dist-check  ## build all dists

publish: dist  # publish python assets

#########
# CLEAN #
#########
.PHONY: deep-clean clean

deep-clean: ## clean everything from the repository
	git clean -fdx

clean: ## clean the repository
	rm -rf .coverage coverage cover htmlcov logs build dist *.egg-info

############################################################################################

.PHONY: help

# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'
