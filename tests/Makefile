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

uco_srcdir := $(top_srcdir)/dependencies/UCO

uco_ontology_files := $(wildcard $(uco_srcdir)/ontology/*/*.ttl $(uco_srcdir)/ontology/*/*/*.ttl)

RDF_TOOLKIT_JAR := $(uco_srcdir)/lib/rdf-toolkit.jar

all:

.PHONY: \
  check-shapes \
  check-pytest

# NOTE - This file is needed to supply all concepts in shapes---both
# local to this repository and in UCO---into a single argument for
# pyshacl.
.local-monolithic.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/shapes/dcam/dcam.ttl \
  $(top_srcdir)/shapes/dcterms/dcterms.ttl \
  $(top_srcdir)/shapes/skos/skos.ttl \
  $(top_srcdir)/shapes/uco/uco.ttl \
  $(uco_ontology_files)
	source $(top_srcdir)/venv/bin/activate \
	  && rdfpipe \
	    --output-format turtle \
	    $(uco_ontology_files) \
	    $(top_srcdir)/shapes/dcam/dcam.ttl \
	    $(top_srcdir)/shapes/dcterms/dcterms.ttl \
	    $(top_srcdir)/shapes/skos/skos.ttl \
	    $(top_srcdir)/shapes/uco/uco.ttl \
	    > _$@
	# Review monolithic file with itself.
	# (Build currently contains OWL review mechanisms.)
	source $(top_srcdir)/venv/bin/activate \
	  && pyshacl \
	    --data-file-format turtle \
	    --inference none \
	    --ont-file-format turtle \
	    --ont-graph _$@ \
	    --shacl _$@ \
	    --shacl-file-format turtle \
	    _$@
	mv _$@ $@

# NOTE - This file is needed to validate the sample JSON-LD file with
# taxonomy concepts available.
.taxonomy-and-sample.ttl: \
  $(top_srcdir)/taxonomy/mime/mime.ttl \
  sample.json
	source $(top_srcdir)/venv/bin/activate \
	  && rdfpipe \
	    --output-format turtle \
	    $(top_srcdir)/taxonomy/mime/mime.ttl \
	    sample.json \
	    > _$@
	mv _$@ $@

check: \
  check-shapes \
  check-pytest

check-pytest: \
  $(top_srcdir)/.venv.done.log \
  skos_exactMatch_XFAIL_validation.ttl \
  skos_notation_XFAIL_validation.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && pytest \
	    --log-level=DEBUG \
	    --verbose \
	    --verbose

check-shapes: \
  mime_validation.ttl \
  sample_validation.ttl

clean:
	@rm -f \
	  .local-monolithic.ttl \
	  .taxonomy-and-sample.ttl \
	  *_validation.ttl

mime_validation.ttl: \
  $(RDF_TOOLKIT_JAR) \
  .local-monolithic.ttl \
  $(top_srcdir)/taxonomy/mime/mime.ttl
	rm -f __$@
	source $(top_srcdir)/venv/bin/activate \
	  && pyshacl \
	    --allow-infos \
	    --data-file-format turtle \
	    --format turtle \
	    --inference none \
	    --ont-file-format turtle \
	    --ont-graph .local-monolithic.ttl \
	    --output __$@ \
	    --shacl .local-monolithic.ttl \
	    --shacl-file-format turtle \
	    $(top_srcdir)/taxonomy/mime/mime.ttl
	java -jar $(RDF_TOOLKIT_JAR) \
	  --inline-blank-nodes \
	  --source __$@ \
	  --source-format turtle \
	  --target _$@ \
	  --target-format turtle
	rm __$@
	mv _$@ $@

sample_validation.ttl: \
  $(RDF_TOOLKIT_JAR) \
  .local-monolithic.ttl \
  .taxonomy-and-sample.ttl
	rm -f __$@
	source $(top_srcdir)/venv/bin/activate \
	  && pyshacl \
	    --allow-infos \
	    --data-file-format turtle \
	    --format turtle \
	    --inference none \
	    --ont-file-format turtle \
	    --ont-graph .local-monolithic.ttl \
	    --output __$@ \
	    --shacl .local-monolithic.ttl \
	    --shacl-file-format turtle \
	    .taxonomy-and-sample.ttl
	java -jar $(RDF_TOOLKIT_JAR) \
	  --inline-blank-nodes \
	  --source __$@ \
	  --source-format turtle \
	  --target _$@ \
	  --target-format turtle
	rm __$@
	mv _$@ $@

skos_exactMatch_XFAIL_validation.ttl: \
  $(RDF_TOOLKIT_JAR) \
  $(top_srcdir)/shapes/skos/skos.ttl \
  skos_exactMatch_XFAIL.json
	rm -f __$@
	source $(top_srcdir)/venv/bin/activate \
	  && pyshacl \
	    --allow-infos \
	    --data-file-format json-ld \
	    --format turtle \
	    --inference none \
	    --output __$@ \
	    --shacl $(top_srcdir)/shapes/skos/skos.ttl \
	    --shacl-file-format turtle \
	    skos_exactMatch_XFAIL.json \
	    ; rc=$$? ; test 1 -eq $$rc
	java -jar $(RDF_TOOLKIT_JAR) \
	  --inline-blank-nodes \
	  --source __$@ \
	  --source-format turtle \
	  --target _$@ \
	  --target-format turtle
	rm __$@
	mv _$@ $@

skos_notation_XFAIL_validation.ttl: \
  $(RDF_TOOLKIT_JAR) \
  $(top_srcdir)/shapes/skos/skos.ttl \
  skos_notation_XFAIL.json
	rm -f __$@
	source $(top_srcdir)/venv/bin/activate \
	  && pyshacl \
	    --allow-infos \
	    --data-file-format json-ld \
	    --format turtle \
	    --inference none \
	    --output __$@ \
	    --shacl $(top_srcdir)/shapes/skos/skos.ttl \
	    --shacl-file-format turtle \
	    skos_notation_XFAIL.json \
	    ; rc=$$? ; test 1 -eq $$rc
	java -jar $(RDF_TOOLKIT_JAR) \
	  --inline-blank-nodes \
	  --source __$@ \
	  --source-format turtle \
	  --target _$@ \
	  --target-format turtle
	rm __$@
	mv _$@ $@
