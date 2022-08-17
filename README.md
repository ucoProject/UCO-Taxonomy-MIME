# (Proposal) Unified Cyber Ontology (UCO) MIME Taxonomy

[![Project Status: Concept – Minimal or no implementation has been done yet, or the repository is only intended to be a limited example, demo, or proof-of-concept.](https://www.repostatus.org/badges/latest/concept.svg)](https://www.repostatus.org/#concept)


## Disclaimer

Participation by NIST in the creation of the documentation of mentioned software is not intended to imply a recommendation or endorsement by the National Institute of Standards and Technology, nor is it intended to imply that any specific software is necessarily the best available for the purpose.


## Software and Data description


### Repository maturity

*This repository is UNDER PROPOSAL and subject to revision and/or rejection by the UCO community.  Feedback is welcome, and can be provided in its associated Issue on the UCO Issue Tracker (https://github.com/ucoProject/UCO/issues/363), or directly on this repository as an Issue.*

IRIs and/or URLs referenced in this repository under `taxonomy.unifiedcyberontology.org` are not yet operational.


### Data purpose

This repository provides the [IANA Media Types registry](https://www.iana.org/assignments/media-types/) as a [SKOS](https://www.w3.org/TR/skos-primer/) taxonomy, as well as a parallel, specialized set of taxons that allow a user to represent Media Types as bearers of unique labels, and also sometimes to relate to one another.  The rationale for using SKOS is:

* Media Types present a use case of a vocabulary that has members of varying degrees of clarity:
   - Names registered with IANA, which are standardized values;
   - Names that follow an IANA-recommended extension pattern, such as including `x-` in the subtype;
   - Names that are neither IANA-registered nor follow an extension pattern, but have seen wide use, such as `application/tar`.

To enable interoperability with data models that use the [Dublin Core Terms MediaType concept](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#http://purl.org/dc/terms/MediaType), each media type `skos:Concept` is also designated as a subclass of `dcterms:FileFormat`, defined in [UCO's types ontology](https://ontology.unifiedcyberontology.org/uco/types/).  *(Editorial note: The ontology update that ties in `dcterms:FileFOramt` is under proposal in [UCO PR 377](https://github.com/ucoProject/UCO/pull/377).)*


#### Data documentation

See [the data README](documentation/README.md) for data usage notes and extension summaries.

See [this document](documentation/design.md) for design rationales.


#### Data usage

This repository's primary product is a monolithic ontology and taxonomy file, serialized in Turtle, [`mime.ttl`](taxonomy/mime/mime.ttl).

The expected usage pattern of this file is via importing or referencing its versioned, or unversioned, IRI as a URL.  Respective examples:

```turtle
<http://example.org/versioned-importing-ontology>
  a owl:Ontology ;
  rdfs:comment "An example ontology that imports the monolithic taxonomy via its versioned IRI."@en ;
  owl:imports <https://taxonomy.unifiedcyberontology.org/uco/mime/0.0.1> ;
  .
```

or:

```turtle
<http://example.org/unversioned-importing-ontology>
  a owl:Ontology ;
  rdfs:comment "An example ontology that imports the monolithic taxonomy via its unversioned IRI."@en ;
  owl:imports <https://taxonomy.unifiedcyberontology.org/uco/mime> ;
  .
```

Media Type individuals can be used either from their UCO IRIs or their Dublin Core Terms `FileFormat` IRIs.

```turtle
<https://taxonomy.unifiedcyberontology.org/uco/mime/application/ld+json>
	a
		prov:Entity ,
		uco-types:IANAMediaType
		;
	rdfs:isDefinedBy <https://www.iana.org/assignments/media-types/application/ld+json> ;
	skos:broader <https://taxonomy.unifiedcyberontology.org/uco/mime/application/json> ;
	skos:exactMatch <http://purl.org/NET/mediatypes/application/ld+json> ;
	skos:inScheme uco-mime:MIMEScheme ;
	skos:notation "application/ld+json" ;
	.
```

Note that the Dublin Core Terms concepts are minimally serialized within this repository, and may differ when retrieved from the Dublin Core IRI.


### Software purpose

Software is included to generate, format, and test the functionality and conformance of `mime.ttl`.  Software review mechanisms---such as syntax normalization with [`black`](https://github.com/psf/black) and static type review with [`mypy`](https://github.com/python/mypy)---are also included and run with [`pre-commit`](https://pre-commit.com/) as part of unit testing.

For review of data quality and consistency with adopted models, SHACL shapes are provided in `shapes/*/*.ttl`.  Their usage with [`pyshacl`](https://github.com/RDFLib/pySHACL) is demonstrated in the [unit tests `Makefile`](tests/Makefile).

End users of this repository should have no need to interface with this repository's software directly.  The software is provided for maintainers within the UCO community.


#### Technical installation instructions

This repository does not include installable Python software.

The SHACL files used in data quality review can be incorporated into any compilation of SHACL shapes for review of data using the referenced data models.

Unit tests can be run locally by cloning this repository, descending into it, and running `make check`.

Contributors and maintainers should review [CONTRIBUTE.md](CONTRIBUTE.md).


## Related Material

* [Unified Cyber Ontology](https://unifiedcyberontology.org/)
* [CASE Ontology](https://casecyberontology.org/)
* [SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/skos-reference/)
* [IANA Media Types Registry](https://www.iana.org/assignments/media-types/)
* [Dublin Core Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)


## Terms of Use

Certain non-public-domain software resources are used in this repository, but not re-distributed.  Their usage is governed by their respective licenses.

Portions of this repository contributed by NIST are governed by the [NIST Software Licensing Statement](LICENSE.md#nist-software-licensing-statement).
