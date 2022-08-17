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
import logging
import typing
import xml.etree.ElementTree as ET

import rdflib

NS_DCTERMS = rdflib.DCTERMS
NS_DCTERMS_MT = rdflib.Namespace("http://purl.org/NET/mediatypes/")
NS_PROV = rdflib.PROV
NS_RDF = rdflib.RDF
NS_RDFS = rdflib.RDFS
NS_SKOS = rdflib.SKOS
NS_UCO_MIME = rdflib.Namespace("https://taxonomy.unifiedcyberontology.org/uco/mime/")
NS_UCO_TYPES = rdflib.Namespace("https://ontology.unifiedcyberontology.org/uco/types/")
NS_XSD = rdflib.XSD


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("out_graph")
    parser.add_argument("mime_base_ttl")
    parser.add_argument("mime_dcterms_ttl")
    parser.add_argument("media_types_xml")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    base_graph = rdflib.Graph()
    base_graph.parse(args.mime_base_ttl)

    graph = rdflib.Graph()
    graph.bind("prov", NS_PROV)
    graph.bind("skos", NS_SKOS)
    graph.bind("uco-mime", NS_UCO_MIME)
    graph.bind("uco-types", NS_UCO_TYPES)
    graph.bind("xsd", NS_XSD)
    graph.parse(args.mime_dcterms_ttl)

    graph += base_graph

    tree = ET.parse(args.media_types_xml)

    # This dictionary is used to verify uniqueness of the "basename"s of subtypes.
    # E.g. "application/zip" would have the "basename" of "zip".
    record_name_to_subtypes: typing.Dict[
        str, typing.Set[str]
    ] = collections.defaultdict(set)

    root = tree.getroot()
    for registry_elem in root.findall(".//{http://www.iana.org/assignments}registry"):
        registry_id = registry_elem.attrib["id"]

        for record_elem in registry_elem.findall(
            ".//{http://www.iana.org/assignments}record"
        ):
            name_elem = record_elem.find("./{http://www.iana.org/assignments}name")
            if name_elem is None:
                continue
            if name_elem.text is None:
                continue

            if "DEPRECATED" in name_elem.text or "OBSOLETE" in name_elem.text:
                logging.info("Skipping deprecated record: %r." % name_elem.text)
                continue

            subtype_name = "%s/%s" % (registry_id, name_elem.text)

            # Prepare uniqueness confirmation after loop.
            record_name_to_subtypes[name_elem.text].add(subtype_name)

            n_record_dcterms = NS_DCTERMS_MT[subtype_name]
            n_record_uco_mt = NS_UCO_MIME[subtype_name]

            graph.add((n_record_dcterms, NS_RDF.type, NS_SKOS.Concept))
            graph.add((n_record_uco_mt, NS_RDF.type, NS_PROV.Entity))
            graph.add((n_record_uco_mt, NS_RDF.type, NS_UCO_TYPES.IANAMediaType))

            file_elem = record_elem.find(
                "./{http://www.iana.org/assignments}file[@type='template']"
            )
            if file_elem is not None and file_elem.text is not None:
                n_documentation = rdflib.URIRef(
                    "https://www.iana.org/assignments/media-types/" + file_elem.text
                )
                graph.add((n_record_uco_mt, NS_RDFS.isDefinedBy, n_documentation))

            # skos:exactMatch is an owl:SymmetricProperty.  Build one degree of the SKOS closure that an OWL inferencing engine would build by generating the symmetric triple here.  This will save on SPARQL query complexity for the end user.  A later step will continue exactMatch expansion based on definitions in mime-base.ttl.
            graph.add((n_record_uco_mt, NS_SKOS.exactMatch, n_record_dcterms))
            graph.add((n_record_dcterms, NS_SKOS.exactMatch, n_record_uco_mt))

            graph.add(
                (
                    n_record_uco_mt,
                    NS_SKOS.notation,
                    rdflib.Literal("%s/%s" % (registry_id, name_elem.text)),
                )
            )
            graph.add((n_record_uco_mt, NS_SKOS.inScheme, NS_UCO_MIME.MIMEScheme))

    # This code block was used to check an example in the Dublin Core documentation.
    # The result was that some names are in multiple subtypes.  Excerpt:
    # ERROR:root:record_name = 1d-interleaved-parityfec:
    # ERROR:root:  * application/1d-interleaved-parityfec
    # ERROR:root:  * audio/1d-interleaved-parityfec
    # ERROR:root:  * text/1d-interleaved-parityfec
    # ERROR:root:  * video/1d-interleaved-parityfec
    # ERROR:root:record_name = 3gpp:
    # ERROR:root:  * audio/3gpp
    # ERROR:root:  * video/3gpp
    # ...
    #
    # record_name_to_multiple_subtypes: typing.Dict[str, typing.Set[str]] = dict()
    # for record_name in record_name_to_subtypes.keys():
    #     if len(record_name_to_subtypes[record_name]) > 1:
    #         record_name_to_multiple_subtypes[record_name] = record_name_to_subtypes[record_name]
    # for record_name in sorted(record_name_to_multiple_subtypes.keys()):
    #     logging.error("record_name = %s:" % record_name)
    #     for subtype_name in sorted(record_name_to_multiple_subtypes[record_name]):
    #         logging.error("  * %s" % subtype_name)
    # assert len(record_name_to_multiple_subtypes) == 0, "Assumed uniqueness of record names invalidated."

    # Continue skos:exactMatch expansion based on definitions in mime-base.ttl.
    concepts_with_exact_match_in_base_graph: typing.Set[rdflib.URIRef] = set()
    for triple in base_graph.triples((None, NS_SKOS.exactMatch, None)):
        assert isinstance(triple[0], rdflib.URIRef)
        assert isinstance(triple[2], rdflib.URIRef)
        concepts_with_exact_match_in_base_graph.add(triple[0])
        concepts_with_exact_match_in_base_graph.add(triple[2])
    logging.debug(
        "concepts_with_exact_match_in_base_graph = %r.",
        concepts_with_exact_match_in_base_graph,
    )
    expansion_graph = rdflib.Graph()
    for n_concept in sorted(concepts_with_exact_match_in_base_graph):
        # Add symmetric triple for original concept exactMatch.
        for triple in base_graph.triples((n_concept, NS_SKOS.exactMatch, None)):
            assert isinstance(triple[2], rdflib.URIRef)
            graph.add((triple[2], NS_SKOS.exactMatch, n_concept))
        # Expand exactMatch through built graph.
        for result in graph.query(
            """\
SELECT ?nMatchingConcept
WHERE {
  ?nConcept skos:exactMatch+ ?nMatchingConcept .
  FILTER (?nConcept != ?nMatchingConcept)
}
""",
            initBindings={"nConcept": n_concept},
        ):
            expansion_graph.add((n_concept, NS_SKOS.exactMatch, result[0]))
    if args.debug:
        logging.debug("expansion_graph:")
        for triple in sorted(expansion_graph.triples((None, None, None))):
            logging.debug("  %s", (triple,))
    graph += expansion_graph

    graph.serialize(args.out_graph)


if __name__ == "__main__":
    main()
