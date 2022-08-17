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

import logging
import pathlib
import typing

import owlrl  # type: ignore
import pytest
import rdflib

NS_KB = rdflib.Namespace("http://example.org/kb/")
NS_RDFS = rdflib.RDFS
NS_SKOS = rdflib.SKOS


@pytest.fixture(scope="session")
def graph() -> typing.Generator[rdflib.Graph, None, None]:
    srcdir = pathlib.Path(__file__).parent
    top_srcdir = srcdir.parent

    graph = rdflib.Graph()
    graph.parse(str(srcdir / "sample.json"))
    graph.parse(str(top_srcdir / "taxonomy" / "mime" / "mime.ttl"))

    # Supplement with a SKOS definition instead of importing all SKOS.
    # https://www.w3.org/TR/skos-reference
    # Definition: S22.
    graph.add((NS_SKOS.broader, NS_RDFS.subPropertyOf, NS_SKOS.broaderTransitive))

    logging.debug("len(graph) = %d.  (Pre-closure)", len(graph))
    owlrl.RDFSClosure.RDFS_Semantics(graph, False, False, False).closure()
    logging.debug("len(graph) = %d.  (Post-closure)", len(graph))

    yield graph


def test_excel_files(graph: rdflib.Graph) -> None:
    expected: typing.Set[str] = {
        "http://example.org/kb/xls-dct-1",
        "http://example.org/kb/xls-uco-1",
    }
    computed: typing.Set[str] = set()
    for result in graph.query(
        r"""
SELECT ?nFile
WHERE {
  ?nFile
    a uco-observable:File ;
    uco-core:hasFacet/uco-observable:mimeType ?nMimeType ;
    .

  ?nMimeType
    skos:broaderTransitive*/skos:exactMatch* <http://purl.org/NET/mediatypes/application/vnd.ms-excel> ;
    .
}"""
    ):
        computed.add(result[0].toPython())
    assert expected == computed


def test_gzip_files(graph: rdflib.Graph) -> None:
    expected: typing.Set[str] = {
        "http://example.org/kb/gz-dct-1",
        "http://example.org/kb/gz-uco-1",
        "http://example.org/kb/targz-uco-1",
    }
    computed: typing.Set[str] = set()
    for result in graph.query(
        r"""
SELECT ?nFile
WHERE {
  ?nFile
    a uco-observable:File ;
    uco-core:hasFacet/uco-observable:mimeType ?nMimeType ;
    .

  ?nMimeType
    skos:exactMatch*/skos:broaderTransitive*/skos:notation "application/gzip" ;
    .
}"""
    ):
        computed.add(result[0].toPython())
    assert expected == computed


def test_jpeg_files(graph: rdflib.Graph) -> None:
    expected: typing.Set[str] = {
        "http://example.org/kb/jpeg-dct-1",
        "http://example.org/kb/jpeg-uco-1",
        "http://example.org/kb/jpg-uco-1",
    }
    computed: typing.Set[str] = set()
    for result in graph.query(
        r"""
SELECT ?nFile
WHERE {
  ?nFile
    a uco-observable:File ;
    uco-core:hasFacet/uco-observable:mimeType ?nMimeType ;
    .

  ?nMimeType
    skos:exactMatch*/skos:broaderTransitive*/prov:alternateOf*/skos:exactMatch*/skos:notation "image/jpeg" ;
    .
}"""
    ):
        computed.add(result[0].toPython())
    assert expected == computed


def test_jpg_files(graph: rdflib.Graph) -> None:
    expected: typing.Set[str] = {
        "http://example.org/kb/jpeg-dct-1",
        "http://example.org/kb/jpeg-uco-1",
        "http://example.org/kb/jpg-uco-1",
    }
    computed: typing.Set[str] = set()
    for result in graph.query(
        r"""
SELECT ?nFile
WHERE {
  ?nFile
    a uco-observable:File ;
    uco-core:hasFacet/uco-observable:mimeType ?nMimeType ;
    .

  ?nMimeType
    skos:exactMatch*/skos:broaderTransitive*/(prov:alternateOf|^prov:alternateOf)*/skos:exactMatch*/skos:notation "image/jpg" ;
    .
}"""
    ):
        computed.add(result[0].toPython())
    assert expected == computed


def test_json_files(graph: rdflib.Graph) -> None:
    expected: typing.Set[str] = {
        "http://example.org/kb/json-dct-1",
        "http://example.org/kb/json-uco-1",
        "http://example.org/kb/jsonld-dct-1",
        "http://example.org/kb/jsonld-uco-1",
    }
    computed: typing.Set[str] = set()
    for result in graph.query(
        r"""
SELECT ?nFile
WHERE {
  ?nFile
    a uco-observable:File ;
    uco-core:hasFacet/uco-observable:mimeType ?nMimeType ;
    .

  ?nMimeType
    skos:exactMatch*/skos:broaderTransitive*/skos:exactMatch* <http://purl.org/NET/mediatypes/application/json> ;
    .
}"""
    ):
        computed.add(result[0].toPython())
    assert expected == computed


def test_tar_files(graph: rdflib.Graph) -> None:
    expected: typing.Set[str] = {
        "http://example.org/kb/tar-uco-1",
        "http://example.org/kb/targz-uco-1",
    }
    computed: typing.Set[str] = set()
    for result in graph.query(
        r"""
SELECT ?nFile
WHERE {
  ?nFile
    a uco-observable:File ;
    uco-core:hasFacet/uco-observable:mimeType ?nMimeType ;
    .

  ?nMimeType
    skos:broaderTransitive*/skos:notation "application/tar" ;
    .
}"""
    ):
        computed.add(result[0].toPython())
    assert expected == computed


def test_targz_files(graph: rdflib.Graph) -> None:
    expected: typing.Set[str] = {
        "http://example.org/kb/targz-uco-1",
    }
    computed: typing.Set[str] = set()
    for result in graph.query(
        r"""
SELECT ?nFile
WHERE {
  ?nFile
    a uco-observable:File ;
    uco-core:hasFacet/uco-observable:mimeType ?nMimeType ;
    .

  ?nMimeType
    skos:broaderTransitive*/skos:notation "application/tar+gzip" ;
    .
}"""
    ):
        computed.add(result[0].toPython())
    assert expected == computed


def test_xml_application_files(graph: rdflib.Graph) -> None:
    expected: typing.Set[str] = {
        "http://example.org/kb/rdf-dct-1",
        "http://example.org/kb/rdf-uco-1",
        "http://example.org/kb/xml-a-dct-1",
        "http://example.org/kb/xml-a-uco-1",
        "http://example.org/kb/xml-t-dct-1",
        "http://example.org/kb/xml-t-uco-1",
    }
    computed: typing.Set[str] = set()
    for result in graph.query(
        r"""
SELECT ?nFile
WHERE {
  ?nFile
    a uco-observable:File ;
    uco-core:hasFacet/uco-observable:mimeType ?nMimeType ;
    .

  ?nMimeType
    skos:exactMatch*/skos:broaderTransitive*/prov:alternateOf*/skos:exactMatch*/skos:notation "application/xml" ;
    .
}"""
    ):
        computed.add(result[0].toPython())
    assert expected == computed


def test_xml_text_files(graph: rdflib.Graph) -> None:
    expected: typing.Set[str] = {
        "http://example.org/kb/rdf-dct-1",
        "http://example.org/kb/rdf-uco-1",
        "http://example.org/kb/xml-a-dct-1",
        "http://example.org/kb/xml-a-uco-1",
        "http://example.org/kb/xml-t-dct-1",
        "http://example.org/kb/xml-t-uco-1",
    }
    computed: typing.Set[str] = set()
    for result in graph.query(
        r"""
SELECT ?nFile
WHERE {
  ?nFile
    a uco-observable:File ;
    uco-core:hasFacet/uco-observable:mimeType ?nMimeType ;
    .

  ?nMimeType
    skos:exactMatch*/skos:broaderTransitive*/prov:alternateOf*/skos:exactMatch*/skos:notation "text/xml" ;
    .
}"""
    ):
        computed.add(result[0].toPython())
    assert expected == computed


def test_zip_files(graph: rdflib.Graph) -> None:
    expected: typing.Set[str] = {
        "http://example.org/kb/xlsx-dct-1",
        "http://example.org/kb/xlsx-uco-1",
        "http://example.org/kb/zip-dct-1",
        "http://example.org/kb/zip-uco-1",
    }
    computed: typing.Set[str] = set()
    for result in graph.query(
        r"""
SELECT ?nFile
WHERE {
  ?nFile
    a uco-observable:File ;
    uco-core:hasFacet/uco-observable:mimeType ?nMimeType ;
    .

  ?nMimeType
    skos:exactMatch*/skos:broaderTransitive*/skos:notation "application/zip" ;
    .
}"""
    ):
        computed.add(result[0].toPython())
    assert expected == computed
