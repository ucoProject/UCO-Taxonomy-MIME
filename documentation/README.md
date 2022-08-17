<!--
GENERATED FILE

This file is generated from README_md.py.  If you have non-table text you wish to edit, please revise that file.
-->
# Media Types

This page lists Media Types, still frequently referred to as "MIME Types", defined in this repository's taxonomy.  A table of mappings to [IANA's Media Types Registry](https://www.iana.org/assignments/media-types/media-types.xhtml) is provided.  Also, a supplemental of some IANA Media Types is provided.

Note that due to Github page-size limitations, this page is limited to Media Types that have in some way been extended in UCO's taxonomy, and/or do not somehow appear with a certain text pattern in the IANA Registry.


## Media Type Aliases

Some Media Types are recognized from their defining documentation to be aliases of one another.

| UCO Concept                                                                                                                                    | Alternate UCO Concept                                                                                                                          |
|------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| [`uco-mime:application/tar`](https://taxonomy.unifiedcyberontology.org/uco/mime/application/tar)                                               | [`uco-mime:application/x-tar`](https://taxonomy.unifiedcyberontology.org/uco/mime/application/x-tar)                                           |
| [`uco-mime:application/tar+gzip`](https://taxonomy.unifiedcyberontology.org/uco/mime/application/tar+gzip)                                     | [`uco-mime:application/x-tar+gzip`](https://taxonomy.unifiedcyberontology.org/uco/mime/application/x-tar+gzip)                                 |
| [`uco-mime:application/xml`](https://taxonomy.unifiedcyberontology.org/uco/mime/application/xml)                                               | [`uco-mime:text/xml`](https://taxonomy.unifiedcyberontology.org/uco/mime/text/xml)                                                             |
| [`uco-mime:application/xml-external-parsed-entity`](https://taxonomy.unifiedcyberontology.org/uco/mime/application/xml-external-parsed-entity) | [`uco-mime:text/xml-external-parsed-entity`](https://taxonomy.unifiedcyberontology.org/uco/mime/text/xml-external-parsed-entity)               |
| [`uco-mime:image/jpg`](https://taxonomy.unifiedcyberontology.org/uco/mime/image/jpg)                                                           | [`uco-mime:image/jpeg`](https://taxonomy.unifiedcyberontology.org/uco/mime/image/jpeg)                                                         |
| [`uco-mime:text/xml`](https://taxonomy.unifiedcyberontology.org/uco/mime/text/xml)                                                             | [`uco-mime:application/xml`](https://taxonomy.unifiedcyberontology.org/uco/mime/application/xml)                                               |
| [`uco-mime:text/xml-external-parsed-entity`](https://taxonomy.unifiedcyberontology.org/uco/mime/text/xml-external-parsed-entity)               | [`uco-mime:application/xml-external-parsed-entity`](https://taxonomy.unifiedcyberontology.org/uco/mime/application/xml-external-parsed-entity) |


## Media Type Knowledge Extensions

While most of UCO's Media Types are associated as an exact match with an IANA-listed media type, some are not.  Yet, they have been found to appear in tool output and/or data sets already.  UCO has defined additional Media Type IRIs, which can be seen to not have a corresponding IANA concept via lacking records from their third column onward in the following table.

The last column in this table is a second knowledge-extension, where UCO Media Types are noted as having some broader Media Type.  As a matter of domain of responsibility, UCO Media Types have these taxonomic relationships defined between themselves, but definition of the same relationships in either Dublin Core or IANA is deferred to the upstream knowledge base provider.

| Notation                                                                    | UCO Concept                                                                                                                                    | Dublin Core Concept                                                                                                            | IANA documentation                                                                                                                      | Broader Concepts                                           |
|-----------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| `application/ld+json`                                                       | [`uco-mime` IRI](https://taxonomy.unifiedcyberontology.org/uco/mime/application/ld+json)                                                       | [`dcterms-mime` IRI](http://purl.org/NET/mediatypes/application/ld+json)                                                       | [IANA Document](https://www.iana.org/assignments/media-types/application/ld+json)                                                       | `application/json`                                         |
| `application/rdf+xml`                                                       | [`uco-mime` IRI](https://taxonomy.unifiedcyberontology.org/uco/mime/application/rdf+xml)                                                       | [`dcterms-mime` IRI](http://purl.org/NET/mediatypes/application/rdf+xml)                                                       | [IANA Document](https://www.iana.org/assignments/media-types/application/rdf+xml)                                                       | `application/xml`, `text/xml`                              |
| `application/tar`                                                           | [`uco-mime` IRI](https://taxonomy.unifiedcyberontology.org/uco/mime/application/tar)                                                           |                                                                                                                                |                                                                                                                                         |                                                            |
| `application/tar+gzip`                                                      | [`uco-mime` IRI](https://taxonomy.unifiedcyberontology.org/uco/mime/application/tar+gzip)                                                      |                                                                                                                                |                                                                                                                                         | `application/gzip`, `application/tar`, `application/x-tar` |
| `application/vnd.openxmlformats-officedocument.presentationml.presentation` | [`uco-mime` IRI](https://taxonomy.unifiedcyberontology.org/uco/mime/application/vnd.openxmlformats-officedocument.presentationml.presentation) | [`dcterms-mime` IRI](http://purl.org/NET/mediatypes/application/vnd.openxmlformats-officedocument.presentationml.presentation) | [IANA Document](https://www.iana.org/assignments/media-types/application/vnd.openxmlformats-officedocument.presentationml.presentation) | `application/zip`                                          |
| `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`         | [`uco-mime` IRI](https://taxonomy.unifiedcyberontology.org/uco/mime/application/vnd.openxmlformats-officedocument.spreadsheetml.sheet)         | [`dcterms-mime` IRI](http://purl.org/NET/mediatypes/application/vnd.openxmlformats-officedocument.spreadsheetml.sheet)         | [IANA Document](https://www.iana.org/assignments/media-types/application/vnd.openxmlformats-officedocument.spreadsheetml.sheet)         | `application/zip`                                          |
| `application/vnd.openxmlformats-officedocument.wordprocessingml.document`   | [`uco-mime` IRI](https://taxonomy.unifiedcyberontology.org/uco/mime/application/vnd.openxmlformats-officedocument.wordprocessingml.document)   | [`dcterms-mime` IRI](http://purl.org/NET/mediatypes/application/vnd.openxmlformats-officedocument.wordprocessingml.document)   | [IANA Document](https://www.iana.org/assignments/media-types/application/vnd.openxmlformats-officedocument.wordprocessingml.document)   | `application/zip`                                          |
| `application/x-tar`                                                         | [`uco-mime` IRI](https://taxonomy.unifiedcyberontology.org/uco/mime/application/x-tar)                                                         |                                                                                                                                |                                                                                                                                         |                                                            |
| `application/x-tar+gzip`                                                    | [`uco-mime` IRI](https://taxonomy.unifiedcyberontology.org/uco/mime/application/x-tar+gzip)                                                    |                                                                                                                                |                                                                                                                                         | `application/gzip`, `application/x-tar`                    |
| `image/jpg`                                                                 | [`uco-mime` IRI](https://taxonomy.unifiedcyberontology.org/uco/mime/image/jpg)                                                                 |                                                                                                                                |                                                                                                                                         |                                                            |


## Media Type Supplemental Listing

Some Media Types appear on the IANA page, but due to lacking a templated documentation file do not appear in a flat text search following the `type/subtype` pattern.  To alleviate confusion, this list of concepts can be reviewed to confirm subtype registration before reviewing the [IANA Registry](https://www.iana.org/assignments/media-types/media-types.xhtml).

* [`image/gif`](http://purl.org/NET/mediatypes/image/gif)
* [`image/ief`](http://purl.org/NET/mediatypes/image/ief)
* [`image/jpeg`](http://purl.org/NET/mediatypes/image/jpeg)
* [`message/external-body`](http://purl.org/NET/mediatypes/message/external-body)
* [`message/partial`](http://purl.org/NET/mediatypes/message/partial)
* [`message/rfc822`](http://purl.org/NET/mediatypes/message/rfc822)
* [`model/mesh`](http://purl.org/NET/mediatypes/model/mesh)
* [`model/vrml`](http://purl.org/NET/mediatypes/model/vrml)
* [`multipart/alternative`](http://purl.org/NET/mediatypes/multipart/alternative)
* [`multipart/digest`](http://purl.org/NET/mediatypes/multipart/digest)
* [`multipart/mixed`](http://purl.org/NET/mediatypes/multipart/mixed)
* [`multipart/parallel`](http://purl.org/NET/mediatypes/multipart/parallel)
* [`text/enriched`](http://purl.org/NET/mediatypes/text/enriched)
* [`text/plain`](http://purl.org/NET/mediatypes/text/plain)
* [`text/richtext`](http://purl.org/NET/mediatypes/text/richtext)
* [`video/mpeg`](http://purl.org/NET/mediatypes/video/mpeg)
