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

import typing

import rdflib

NS_SH = rdflib.SH


def _load_graph(filename: str) -> rdflib.Graph:
    graph = rdflib.Graph()
    graph.parse(filename)

    conforms: typing.Optional[bool] = None
    for triple in graph.triples((None, NS_SH.conforms, None)):
        assert isinstance(triple[2], rdflib.Literal)
        conforms = triple[2].toPython()
    assert conforms is False

    return graph


def test_skos_exactMatch() -> None:
    """
    Identify expected failure pairs.
    """
    expected: typing.Set[typing.Tuple[str, str]] = {
        ("http://example.org/kb/concept-1", "http://example.org/kb/concept-2"),
        ("http://example.org/kb/concept-1", "http://example.org/kb/concept-3"),
        ("http://example.org/kb/concept-2", "http://example.org/kb/concept-1"),
        ("http://example.org/kb/concept-3", "http://example.org/kb/concept-1"),
    }
    computed: typing.Set[typing.Tuple[str, str]] = set()

    graph = _load_graph("skos_exactMatch_XFAIL_validation.ttl")

    for result in graph.query(
        """\
SELECT ?nFocusNode ?nValue
WHERE {
  ?nValidationResult
    sh:focusNode ?nFocusNode ;
    sh:value ?nValue ;
    .
}
"""
    ):
        computed.add(
            (
                str(result[0]),
                str(result[1]),
            )
        )

    assert expected == computed


def test_skos_notation() -> None:
    """
    Identify expected failure pairs.
    """
    expected: typing.Set[typing.Tuple[str, str]] = {
        ("http://example.org/kb/concept-1", "Name 1"),
        ("http://example.org/kb/concept-2", "Name 1"),
    }
    computed: typing.Set[typing.Tuple[str, str]] = set()

    graph = _load_graph("skos_notation_XFAIL_validation.ttl")

    for result in graph.query(
        """\
SELECT ?nFocusNode ?nValue
WHERE {
  ?nValidationResult
    sh:focusNode ?nFocusNode ;
    sh:value ?nValue ;
    .
}
"""
    ):
        computed.add((str(result[0]), str(result[1])))

    assert expected == computed
