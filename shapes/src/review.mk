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

# This Makefile expects to execute in the context of $(top_srcdir)/shapes/*.
top_srcdir := $(shell cd ../.. ; pwd)

srcdir := $(shell pwd)

srcdir_basename := $(shell basename $$PWD)

RDF_TOOLKIT_JAR := $(top_srcdir)/dependencies/UCO/lib/rdf-toolkit.jar

all:

.check-$(srcdir_basename).ttl: \
  $(srcdir_basename).ttl \
  $(RDF_TOOLKIT_JAR)
	java -jar $(RDF_TOOLKIT_JAR) \
	  --inline-blank-nodes \
	  --source $< \
	  --source-format turtle  \
	  --target _$@ \
	  --target-format turtle 
	mv _$@ $@

check: \
  $(srcdir_basename).ttl \
  .check-$(srcdir_basename).ttl
	diff $^ \
	  || (echo "ERROR:shapes/src/review.mk:The local $< does not match the normalized version. If the above reported changes look fine, run 'cp .check-$< $<' while in the sub-folder shapes/$$(basename $< .ttl)/ to get a file ready to commit to Git." >&2 ; exit 1)

clean:
	@rm -f \
	  .check-$(srcdir_basename).ttl
