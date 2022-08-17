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

# Section 4: Vocabulary Encoding Schemes
# http://purl.org/dc/terms/IMT

import argparse
import logging
import xml.etree.ElementTree as ET

import rdflib

NS_DCAM = rdflib.Namespace("http://purl.org/dc/dcam/")
NS_DCTERMS = rdflib.DCTERMS
NS_DCTERMS_MT = rdflib.Namespace("http://purl.org/NET/mediatypes/")
NS_RDF = rdflib.RDF
NS_RDFS = rdflib.RDFS
NS_SKOS = rdflib.SKOS
NS_XSD = rdflib.XSD


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("out_graph")
    parser.add_argument("media_types_xml")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    graph = rdflib.Graph()
    graph.bind("dcam", NS_DCAM)
    graph.bind("dcterms", NS_DCTERMS)
    graph.bind("mime", NS_DCTERMS_MT)
    graph.bind("xsd", NS_XSD)

    tree = ET.parse(args.media_types_xml)

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

            n_record = NS_DCTERMS_MT[subtype_name]

            graph.add((n_record, NS_RDF.type, NS_DCTERMS.FileFormat))
            graph.add((n_record, NS_DCAM.memberOf, NS_DCTERMS.IMT))

            date_date = record_elem.attrib.get("date")
            if date_date is not None:
                graph.add(
                    (
                        n_record,
                        NS_DCTERMS.date,
                        rdflib.Literal(date_date, datatype=NS_XSD.date),
                    )
                )

            updated_date = record_elem.attrib.get("updated")
            if updated_date is not None:
                graph.add(
                    (
                        n_record,
                        NS_DCTERMS.modified,
                        rdflib.Literal(updated_date, datatype=NS_XSD.date),
                    )
                )

    graph.serialize(args.out_graph)


if __name__ == "__main__":
    main()
