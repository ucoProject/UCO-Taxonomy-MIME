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

top_srcdir := $(shell cd ../.. ; pwd)

RDF_TOOLKIT_JAR := $(top_srcdir)/dependencies/UCO/lib/rdf-toolkit.jar

all: \
  mime.ttl

.PHONY: \
  check-mime-base

.check-mime-base.ttl: \
  mime-base.ttl \
  $(RDF_TOOLKIT_JAR)
	java -jar $(RDF_TOOLKIT_JAR) \
	  --inline-blank-nodes \
	  --source $< \
	  --source-format turtle  \
	  --target _$@ \
	  --target-format turtle 
	mv _$@ $@

check: \
  check-mime-base \
  mime.ttl

check-mime-base: \
  mime-base.ttl \
  .check-mime-base.ttl
	diff $^ \
	  || (echo "ERROR:taxonomy/mime/Makefile:The local mime-base.ttl does not match the normalized version. If the above reported changes look fine, run 'cp .check-$< $<' while in the sub-folder taxonomy/mime/ to get a file ready to commit to Git." >&2 ; exit 1)

clean:
	@rm -f \
	  _* \
	  media-types.xml \
	  mime-dcterms.ttl \
	  mime.ttl

media-types.xml:
	wget \
	  --output-document _$@ \
	  https://www.iana.org/assignments/media-types/media-types.xml
	touch -c _$@  # Guarantee timestamp is up to date.
	mv _$@ $@

mime-dcterms.ttl: \
  $(RDF_TOOLKIT_JAR) \
  $(top_srcdir)/.venv.done.log \
  media-types.xml \
  mime_dcterms_ttl.py
	source $(top_srcdir)/venv/bin/activate \
	  && python3 mime_dcterms_ttl.py \
	    __$@ \
	    media-types.xml
	java -jar $(RDF_TOOLKIT_JAR) \
	  --inline-blank-nodes \
	  --source __$@ \
	  --source-format turtle \
	  --target _$@ \
	  --target-format turtle
	rm __$@
	mv _$@ $@

mime.ttl: \
  $(RDF_TOOLKIT_JAR) \
  $(top_srcdir)/.venv.done.log \
  media-types.xml \
  mime-base.ttl \
  mime-dcterms.ttl \
  mime_ttl.py
	source $(top_srcdir)/venv/bin/activate \
	  && python3 mime_ttl.py \
	    __$@ \
	    mime-base.ttl \
	    mime-dcterms.ttl \
	    media-types.xml
	java -jar $(RDF_TOOLKIT_JAR) \
	  --inline-blank-nodes \
	  --source __$@ \
	  --source-format turtle \
	  --target _$@ \
	  --target-format turtle
	rm __$@
	mv _$@ $@
