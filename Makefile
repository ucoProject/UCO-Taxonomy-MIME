#!/usr/bin/make -f

# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to title 17 Section 105 of the
# United States Code this software is not subject to copyright
# protection and is in the public domain. NIST assumes no
# responsibility whatsoever for its use by other parties, and makes
# no guarantees, expressed or implied, about its quality,
# reliability, or any other characteristic.
#
# We would appreciate acknowledgement if the software is used.

SHELL := /bin/bash

PYTHON3 ?= python3

all: \
  all-documentation \
  all-taxonomy

.PHONY: \
  all-documentation \
  all-taxonomy \
  check-documentation \
  check-mypy \
  check-shapes \
  check-taxonomy

.git_submodule_init.done.log: \
  .gitmodules
	git submodule update --init
	$(MAKE) \
	  --directory dependencies/UCO \
	  .lib.done.log
	touch $@

# This virtual environment is meant to be built once and then persist, even through 'make clean'.
# If a recipe is written to remove this flag file, it should first run `pre-commit uninstall`.
.venv-pre-commit/var/.pre-commit-built.log:
	rm -rf .venv-pre-commit
	test -r .pre-commit-config.yaml \
	  || (echo "ERROR:Makefile:pre-commit is expected to install for this repository, but .pre-commit-config.yaml does not expect to exist." >&2 ; exit 1)
	$(PYTHON3) -m venv \
	  .venv-pre-commit
	source .venv-pre-commit/bin/activate \
	  && pip install \
	    --upgrade \
	    pip \
	    setuptools \
	    wheel
	source .venv-pre-commit/bin/activate \
	  && pip install \
	    pre-commit
	source .venv-pre-commit/bin/activate \
	  && pre-commit install
	mkdir -p \
	  .venv-pre-commit/var
	touch $@

.venv.done.log: \
  requirements.txt
	rm -rf venv
	$(PYTHON3) -m venv \
	  venv
	source venv/bin/activate \
	  && pip install \
	    --upgrade \
	    pip \
	    setuptools \
	    wheel
	source venv/bin/activate \
	  && pip install \
	    --requirement requirements.txt
	touch $@

all-documentation: \
  all-taxonomy
	$(MAKE) \
	  --directory documentation

all-taxonomy: \
  .git_submodule_init.done.log \
  .venv-pre-commit/var/.pre-commit-built.log \
  .venv.done.log
	$(MAKE) \
	  --directory taxonomy/mime

check: \
  check-taxonomy \
  check-mypy \
  check-shapes \
  check-documentation
	$(MAKE) \
	  --directory tests \
	  check

check-documentation: \
  all-documentation
	$(MAKE) \
	  --directory documentation \
	  check

check-mypy: \
  .venv.done.log
	source venv/bin/activate \
	  && mypy \
	    --strict \
	    documentation \
	    taxonomy \
	    tests

check-shapes: \
  .git_submodule_init.done.log \
  .venv.done.log
	$(MAKE) \
	  --directory shapes \
	  check

check-taxonomy: \
  all-taxonomy
	$(MAKE) \
	  --directory taxonomy/mime \
	  check

clean:
	@$(MAKE) \
	  --directory tests \
	  clean
	@$(MAKE) \
	  --directory documentation \
	  clean
	@$(MAKE) \
	  --directory taxonomy/mime \
	  clean
	@$(MAKE) \
	  --directory shapes \
	  clean
