from __future__ import annotations

import itertools
from contextlib import suppress
from typing import Tuple

from lxml import etree

from .types import StreamLike


# These tests receive the <doc-number> element and return True if it matches the source
def _is_epo(element: etree.Element) -> bool:
    doc_id = element.getparent()
    if doc_id is None:
        return False
    return doc_id.attrib.get("format") == "epo"


def _is_patent_office(element: etree.Element) -> bool:
    doc_id = element.getparent()
    if doc_id is None:
        return False
    return doc_id.attrib.get("load-source") == "patent-office"


# Order of this list determines the order of parser results
SOURCES_TESTS = [_is_epo, _is_patent_office]


def parse_stream(
    source: StreamLike,
):
    parser = etree.iterparse(
        source,
        events=(
            "start",
            "end",
        ),
        recover=True,
        huge_tree=True,
    )

    doc_numbers_by_source = [[] for _ in SOURCES_TESTS]

    try:
        in_application_reference = False
        in_document_id = False
        for event, element in parser:
            if event == "start":
                match element.tag:
                    case "application-reference":
                        in_application_reference = True
                    case "document-id" if in_application_reference:
                        in_document_id = True
            elif event == "end":
                match element.tag:
                    case "application-reference":
                        in_application_reference = False
                    case "document-id":
                        in_document_id = False
                    case "doc-number" if in_document_id:
                        index, value = _handle(element)
                        if index >= 0:
                            doc_numbers_by_source[index].append(value)
                        element.clear(keep_tail=True)
                    case _:
                        element.clear(keep_tail=True)
    finally:
        with suppress(Exception):
            source.close()
    return _flatten(doc_numbers_by_source)


def _flatten(
    lists: list[list[str]],
) -> list[str]:
    return list(
        itertools.chain.from_iterable(
            lists,
        ),
    )


def _handle(
    element: etree.Element,
) -> Tuple[int, str]:
    if element.text is None:
        return -1, ""
    for index, test in enumerate(SOURCES_TESTS):
        if test(element):
            return index, element.text or ""
    return -1, ""  # if it's not from one of our sources we can ignore it
