#!/usr/bin/env python3

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

import argparse
import collections
import typing

import pandas  # type: ignore
import rdflib


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("out_md")
    parser.add_argument("in_ttl")
    args = parser.parse_args()

    graph = rdflib.Graph()
    graph.parse(args.in_ttl)

    # Find all UCO-provided alternate-of relationships.
    alternate_records: typing.List[typing.Tuple[str, str]] = []
    query = """\
SELECT ?nType1 ?nType2 ?lType1 ?lType2
WHERE {
  ?nType1 prov:alternateOf ?nType2 .
  ?nType1 skos:notation ?lType1 .
  ?nType2 skos:notation ?lType2 .
  FILTER ( ?nType1 != ?nType2 ) .
}
ORDER BY ?lType1 ?lType2
"""
    for result in graph.query(query):
        alternate_records.append(
            (
                "[`uco-mime:%s`](%s)" % (result[2], result[0]),
                "[`uco-mime:%s`](%s)" % (result[3], result[1]),
            )
        )

    df_alternates = pandas.DataFrame(
        alternate_records, columns=["UCO Concept", "Alternate UCO Concept"]
    )
    table_alternates = df_alternates.to_markdown(tablefmt="github", index=False)

    # Find all UCO-provided broader-than relationships.
    broaders: typing.DefaultDict[str, typing.Set[str]] = collections.defaultdict(set)
    query = """\
SELECT ?lNarrower ?lBroader
WHERE {
  ?nNarrower skos:broader/prov:alternateOf* ?nBroader .
  ?nNarrower skos:notation ?lNarrower .
  ?nBroader skos:notation ?lBroader .
}
"""
    for result in graph.query(query):
        broaders[str(result[0])].add(str(result[1]))

    non_explicitly_listed_iana_media_types: typing.Dict[str, str] = dict()
    for result in graph.query(
        """\
SELECT ?lNotation ?nDCTFileFormat
WHERE {
  ?nDCTFileFormat dcam:memberOf dcterms:IMT .
  ?nUCOMediaType
    skos:exactMatch ?nDCTFileFormat ;
    skos:notation ?lNotation ;
    .
  FILTER NOT EXISTS {
    ?nUCOMediaType rdfs:isDefinedBy ?nIANADocument .
  }
}
"""
    ):
        assert isinstance(result[0], rdflib.Literal)
        assert isinstance(result[1], rdflib.URIRef)
        non_explicitly_listed_iana_media_types[str(result[0])] = str(result[1])

    # Limit this file (due to Github README size limitation, seems strictly under 1MB) to only:
    # * UCO non-IANA Media Types
    # * UCO Media Types that have any skos:broader relationships
    # * UCO Media Types that have an "alias" / in-scheme exact match
    # * Things that would not come up from a text search on the IANA HTML page (e.g. "image/jpeg" doesn't appear because it doesn't have a Template file)
    query = """\
CONSTRUCT {
  ?nUCOMediaType <urn:example:display> true .
}
WHERE {
  { ?nUCOMediaType a uco-types:NonIANAMediaType . }
  UNION
  { ?nUCOMediaType skos:broader ?nA . }
}
    """
    tmp_graph = rdflib.Graph()
    for result in graph.query(query):
        tmp_graph.add(result)

    graph += tmp_graph

    query = """\
SELECT DISTINCT ?lNotation ?nUCOMediaType ?nDCTFileFormat ?nIANADocument
WHERE {
  ?nUCOMediaType <urn:example:display> true .

  { ?nUCOMediaType a uco-types:IANAMediaType . }
  UNION
  { ?nUCOMediaType a uco-types:NonIANAMediaType . }

  ?nUCOMediaType skos:notation ?lNotation .
  OPTIONAL {
    ?nUCOMediaType skos:exactMatch ?nDCTFileFormat .
    ?nDCTFileFormat dcam:memberOf dcterms:IMT .
    OPTIONAL {
      ?nUCOMediaType rdfs:isDefinedBy ?nIANADocument .
    }
  }
}
ORDER BY ?lNotation
"""
    extension_records: typing.List[
        typing.Tuple[
            str,
            str,
            typing.Optional[str],
            typing.Optional[str],
            str,
        ]
    ] = []
    for result in graph.query(query):
        media_type_notation = str(result[0])

        record_cell_dcconcept: typing.Optional[str] = None
        if not result[2] is None:
            record_cell_dcconcept = "[`dcterms-mime` IRI](%s)" % str(result[2])

        record_cell_ianadoc: typing.Optional[str] = None
        if not result[3] is None:
            record_cell_ianadoc = "[IANA Document](%s)" % str(result[3])

        broader_media_type_notations: typing.List[str] = []
        for broader_notation in sorted(broaders[media_type_notation]):
            broader_media_type_notations.append("`%s`" % broader_notation)

        extension_records.append(
            (
                "`%s`" % media_type_notation,
                "[`uco-mime` IRI](%s)" % str(result[1]),
                record_cell_dcconcept,
                record_cell_ianadoc,
                ", ".join(broader_media_type_notations),
            )
        )

    variables = [
        "Notation",
        "UCO Concept",
        "Dublin Core Concept",
        "IANA documentation",
        "Broader Concepts",
    ]
    df_extensions = pandas.DataFrame(extension_records, columns=variables)
    table_extensions = df_extensions.to_markdown(tablefmt="github", index=False)

    with open(args.out_md, "w") as out_fh:
        out_fh.write(
            """\
<!--
GENERATED FILE

This file is generated from README_md.py.  If you have non-table text you wish to edit, please revise that file.
-->
# Media Types

This page lists Media Types, still frequently referred to as "MIME Types", defined in this repository's taxonomy.  A table of mappings to [IANA's Media Types Registry](https://www.iana.org/assignments/media-types/media-types.xhtml) is provided.  Also, a supplemental of some IANA Media Types is provided.

Note that due to Github page-size limitations, this page is limited to Media Types that have in some way been extended in UCO's taxonomy, and/or do not somehow appear with a certain text pattern in the IANA Registry.


## Media Type Aliases

Some Media Types are recognized from their defining documentation to be aliases of one another.

"""
        )
        out_fh.write(table_alternates)
        out_fh.write(
            """


## Media Type Knowledge Extensions

While most of UCO's Media Types are associated as an exact match with an IANA-listed media type, some are not.  Yet, they have been found to appear in tool output and/or data sets already.  UCO has defined additional Media Type IRIs, which can be seen to not have a corresponding IANA concept via lacking records from their third column onward in the following table.

The last column in this table is a second knowledge-extension, where UCO Media Types are noted as having some broader Media Type.  As a matter of domain of responsibility, UCO Media Types have these taxonomic relationships defined between themselves, but definition of the same relationships in either Dublin Core or IANA is deferred to the upstream knowledge base provider.

"""
        )
        out_fh.write(table_extensions)
        out_fh.write(
            """


## Media Type Supplemental Listing

Some Media Types appear on the IANA page, but due to lacking a templated documentation file do not appear in a flat text search following the `type/subtype` pattern.  To alleviate confusion, this list of concepts can be reviewed to confirm subtype registration before reviewing the [IANA Registry](https://www.iana.org/assignments/media-types/media-types.xhtml).

"""
        )
        for notation in sorted(non_explicitly_listed_iana_media_types.keys()):
            out_fh.write(
                "* [`%s`](%s)\n"
                % (notation, non_explicitly_listed_iana_media_types[notation])
            )


if __name__ == "__main__":
    main()
