# Data design


## Selection of SKOS versus OWL

* Some RDF data models (ontologies and otherwise) incorporate Media Types as individuals, e.g. as OWL Object Properties instead of as untyped strings.  However, IANA does not itself provide an RDF endpoint or vocabulary for Media Types.
* There is value in modeling Media Types as individuals, namely in relating them to one another in some kind of hierarchy.  For instance, `application/ld+json` is a more specific form of `application/json`, so syntactic constraints and security review that apply to `application/json` content would also apply to `application/ld+json` content.  Likewise for the many specialized forms of `application/zip`.  Such hierarchical modeling is difficult to transmit if the data model's usage of Media Types has them as untyped strings.
* Multiple RDF-based models provided some mechanism to represent a hierarchy.  RDFS provides `rdfs:Class` and `rdfs:subClassOf`; SKOS provides `skos:Concept` and `skos:broader`/`skos:narrower`; and OWL provides `owl:Class` while also using `rdfs:subClassOf`.

This repository chooses SKOS to make minimal hierarchical statements about Media Types as concepts that aren't necessarily classes.  There is an argument that could be explored that each Media Type is a class of data, and thus should be represented with RDFS or OWL `Class`es.  Some Media Types would then be subclasses of others by merit of being a specialization, such as `application/ld+json` being a specialized form of `application/json`, and being treatable as any arbitrary `application/json`, *without* transformation.

However, other Media Types are subclasses of others *with* a transformation applied.  `application/tar+gzip` (at the time of this writing, a non-IANA Media Type) is a `application/gzip` without transformation, but a `application/tar` (also present a non-IANA Media Type) with transformation via, e.g., the `gunzip` tool.  Further, the contents of the `.tar` file might follow yet another specification.  Assume some format `application/example+tar+gzip` exists.  To represent its relationships with `application/tar` and `application/gzip`, not only would `rdfs:subClassOf` be needed, but a representation for modeling transformation methods would be needed.

Instead of attempting to use OWL or RDFS to classify such formats as having a "Is-a-X" versus "Is-a-X-with-transformation-Y" relationship with their supertypes, this repository chooses to use SKOS to represent the hierarchical relationship.  


### Hierarchy representation restriction

The usage of `skos:broader` in this taxonomy applies to only "Is-a" style relationships.  These can be "Is-a" relationships with or without a transformation function involved, such as applying the INFLATE algorithm to undo a gzip DEFLATE transformation.

Some Media Types have "Has-a" style relationships with others.  For instance, `.deb` files have the Media Type [`application/vnd.debian.binary-package`](https://www.iana.org/assignments/media-types/application/vnd.debian.binary-package).  A `.deb` file is a specialization of the archive format processed by the `ar` utility, and contains two `.tar` archive files.  This taxonomy does NOT encode this as a `skos:broader` relationship between `application/vnd.debian.binary-package` and `application/tar`.


### Future OWL Compatibility

Another decision point for using SKOS instead of OWL is for allowing for future usage of concepts in this taxonomy to also be represented as OWL Clases.  For instance, the `.deb` format could be encoded as an OWL class that entails the existence of two different related tar files.  Per SKOS documentation, [Reference section 3.5.1 SKOS Concepts, OWL Classes and OWL Properties](https://www.w3.org/TR/skos-reference/#L896), it is consistent within the SKOS model for a `skos:Concept` to also be an `owl:Class`.

Usage of SKOS to encode `skos:broader` between Media Types can inform future development of OWL-based subclass hierarchies.


## Extension of Dublin Core

This repository makes use of Dublin Core concepts that have been available to support IANA Media Types as graph individuals, including:

* The [`dcterms:FileFormat`](http://purl.org/dc/terms/FileFormat) class, but no superclass.
* The Vocabulary Encoding Scheme [`dcterms:IMT`](http://purl.org/dc/terms/IMT)
* The `mediatypes` namespace, `http://purl.org/NET/mediatypes`, demonstrated in the ["Publishing metadata" user guide](https://www.dublincore.org/resources/userguide/publishing_metadata/) with the prefix `mime:`.
   - At the time of this writing, the `mediatypes` namespace does not resolve as a web-accessible resource.

The Dublin Core concepts were selected to avoid UCO needing to invent a base concept for IANA Media Types.  [DCAT](https://www.w3.org/TR/vocab-dcat-2/), an ontology being used in [CASE-Corpora](https://github.com/casework/CASE-Corpora/), [uses the Dublin Core concept `dcterms:MediaType`](https://www.w3.org/TR/vocab-dcat-2/#Property:distribution_media_type).  In short, for the UCO MIME Types Taxonomy, `dcterms:FileFormat` was selected due to first encounter with another ontology using IANA Media Type individuals.

Due to lack of demonstrative documentation, this repository makes a guess at how the Dublin Core terms could be used to represent the IANA Media Types Registry, and comes to concept definitions such as this:


```turtle
@prefix dcam: <http://purl.org/dc/dcam/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix mime: <http://purl.org/NET/mediatypes> .

<http://purl.org/NET/mediatypes/application/ld+json>
	a dcterms:FileFormat ;
	dcam:memberOf dcterms:IMT ;
	dcterms:modified "2020-03-17"^^xsd:date ;
	.
```

(Note that though the `mime:` prefix is defined, serializations might still opt to use the expanded IRI form due to [subtle differences](https://github.com/RDFLib/rdflib/pull/1872) in various RDF serializations with handling back- and forward-slash characters.)

However, UCO's design goals of providing an extensible vocabulary of MIME types (in a "Semi-open" vocabulary design pattern that prescribes certain literal, non-IRI values) has further wants for this node than Dublin Core Terms itself provides.  In particular, SKOS concepts for relating and labeling concepts are desired, in order to provide concept hierarchy, alias-style relationships, and "unique" plain-text (literal, non-IRI) labels with an understanding of the scope of uniqueness.

Some of the SKOS concepts desired have significant entailments on their applicability.

* `skos:exactMatch` only relates concepts between different concept schemes.  ([source](https://www.w3.org/TR/skos-reference/#mapping))
* `skos:notation`s apply a language-less string label to a concept, but the uniqueness of that label is only scoped to within a concept scheme.  ([source](https://www.w3.org/TR/skos-reference/#notations))

With those constraints, attempting to apply a `skos:notation` to the concept in the `mime:` namespace could cause a significant interoperability issue with an end user that imports another taxonomy that had attempted nearly the same practices on the same nodes.

To balance extensibility versus domain of responsibility, the UCO MIME Types Taxonomy creates extension concepts.

```turtle
<https://taxonomy.unifiedcyberontology.org/uco/mime/application/ld+json>
	a
		prov:Entity ,
		uco-types:IANAMediaType
		;
	rdfs:isDefinedBy <https://www.iana.org/assignments/media-types/application/ld+json> ;
	skos:exactMatch <http://purl.org/NET/mediatypes/application/ld+json> ;
	skos:inScheme uco-mime:MIMEScheme ;
	skos:notation "application/ld+json" ;
	.
```

Users desiring a set of unique string labels can use the UCO concepts' `skos:notation` values.  Continuous Integration testing that confirms that uniqueness will not see conflicts with other ontologies attempting property-level extensions on shared concepts.

The `prov:Entity` usage is to support `prov:alternateOf` for concepts that are somehow defined as aliases of another.

```turtle
<https://taxonomy.unifiedcyberontology.org/uco/mime/0.0.1/text/xml>
	rdfs:comment "text/xml is defined in RFC 7303 as an alias for application/xml."@en ;
	rdfs:seeAlso <https://www.rfc-editor.org/rfc/rfc7303.html> ;
	prov:alternateOf <https://taxonomy.unifiedcyberontology.org/uco/mime/0.0.1/application/xml> ;
	.
```
