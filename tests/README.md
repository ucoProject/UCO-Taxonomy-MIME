
This is the test matrix exercised by [`test_broader.py`](test_broader.py) against [`sample.json`](sample.json):
* MIME type class encoding:
   - Dublin Core Terms FileFormat: `dcterms-mime:application/json`
   - UCO IANAMediaType: `uco-mime:application/json`
   - UCO NonIANAMediaType: `uco-mime:application/tar+gzip`
   - Custom MIME type (outside UCO): `ex:some/mimeliketype`
* Broadness transitivity - IANA class found via:
   - dcterms individual direct reference: `dcterms-mime:application/json` -> `dcterms-mime:application/json`
   - UCO individual direct reference: `uco-mime:application/json` -> `dcterms-mime:application/json`
   - UCO narrower-individual reference: `uco-mime:application/ld+json` -> `dcterms-mime:application/json`
* SPARQL UX - MIME type found via:
   - IRI reference to IANA concept
   - IRI reference to UCO `*MediaType` concept
   - `skos:notation` housing untyped string.
