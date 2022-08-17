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

top_srcdir := $(shell cd .. ; pwd)

shape_srcdirs := $(foreach shape_srcdir_makefile,$(wildcard */Makefile), $(shell dirname $(shape_srcdir_makefile)))

check_shape_srcdirs := $(foreach shape_srcdir,$(shape_srcdirs), check-$(shape_srcdir))
clean_shape_srcdirs := $(foreach shape_srcdir,$(shape_srcdirs), clean-$(shape_srcdir))

all:

check: \
  $(check_shape_srcdirs)

check-%: \
  %/Makefile
	$(MAKE) \
	  --directory $$(dirname $<) \
	  check

clean: \
  $(clean_shape_srcdirs)

clean-%: \
  %/Makefile
	@$(MAKE) \
	  --directory $$(dirname $<) \
	  clean
