# (Proposal) Unified Cyber Ontology (UCO) MIME Taxonomy


## Disclaimer

Participation by NIST in the creation of the documentation of mentioned software is not intended to imply a recommendation or endorsement by the National Institute of Standards and Technology, nor is it intended to imply that any specific software is necessarily the best available for the purpose.


## Software and Data description


### Repository maturity

*This repository is UNDER PROPOSAL and subject to revision and/or rejection by the UCO community.  Feedback is welcome, and can be provided in UCO Jira ticket [OC-204](https://unifiedcyberontology.atlassian.net/browse/OC-204), its associated Change Proposal page, or directly on this repository as an Issue.*

IRIs and/or URLs referenced in this repository are not yet operational.


### Data purpose

This repository provides a SKOS taxonomy as a member of UCO ontological resources.  The taxonomy converts the [IANA Media Types registry](https://www.iana.org/assignments/media-types/) into SKOS under a UCO namespace, following a mostly two-tier [`skos:ConceptScheme`](https://www.w3.org/TR/skos-reference/#schemes):

* The `ConceptScheme`'s top-level concepts are each Media Type Registry, such as `application`, `image`, etc.
* The second tier of `Concept`s is the media type in each registry, such as `application/zip`, `image/gif`, etc.
* Some extension media types not part of IANA are defined for various reasons, and may or may not be submitted in the future for standardization to IANA.  These extensions follow the non-registration practice of [RFC 6838, Section 3.4], and all include the string [`/x-uco-`].

This repository's primary product is a monolithic ontology and taxonomy file, serialized in Turtle, [`mime.ttl`](taxonomy/mime/mime.ttl).

The expected usage pattern of this file is via importing or referencing its versioned or unversioned IRI as a URL, e.g.:

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
  rdfs:comment "An example ontology that imports the monolithic taxonomy via its versioned IRI."@en ;
  owl:imports <https://taxonomy.unifiedcyberontology.org/uco/mime> ;
  .
```


### Software purpose

Software is included to generate, format, and test the functionality of `mime.ttl`.  Software review mechanisms are also included.

End users of this repository should have no need to interface with the software directly.  The software is provided for maintainers within the UCO community.


#### Technical installation instructions

This repository includes no installable software.

Contributors and maintainers should review [CONTRIBUTE.md](CONTRIBUTE.md).


## Contact information

* PI name: [Alex Nelson](https://www.nist.gov/people/alexander-nelson), [Information Technology Laboratory](https://www.nist.gov/itl), [Computer Security Division](https://www.nist.gov/itl/csd), [Security Components and Mechanisms Group](https://www.nist.gov/itl/csd/security-components-and-mechanisms), [alexander.nelson@nist.gov](mailto:alexander.nelson@nist.gov).


## Related Material

* [Unified Cyber Ontology](https://unifiedcyberontology.org/)
* [CASE Ontology](https://casecyberontology.org/)
* [SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/skos-reference/)
* [IANA Media Types Registry](https://www.iana.org/assignments/media-types/)
* [Dublin Core Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)


## Directions on appropriate citation

To cite this resource, please use this DOI:

TODO


## Non-public-domain software modules

Certain non-public-domain software resources are used in this repository, but not re-distributed.  Their usage is governed by their respective licenses.


## Terms of Use

See [LICENSE.md](LICENSE.md).
