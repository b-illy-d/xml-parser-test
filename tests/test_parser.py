import io

from parser.parse import parse_stream
from tests.test_utils import (
    read_example_xml,
    read_malformed_xml,
    read_multiple_doc_numbers_xml,
    read_no_attributes_xml,
    read_unsorted_xml,
    read_weird_places_xml,
)

_EXPECTED_DOC_NUMBERS = ["999000888", "66667777"]


def test_parse_basic():
    source = read_example_xml()
    result = parse_stream(source)

    assert len(result) == 2
    assert result == _EXPECTED_DOC_NUMBERS


def test_parse_empty():
    source = b"<root></root>"
    result = parse_stream(io.BytesIO(source))

    assert len(result) == 0
    expected = []
    assert result == expected


def test_parse_malformed():
    """Malformed XML is missing a closing tag on one of the entries"""
    source = read_malformed_xml()
    result = parse_stream(source)
    assert len(result) == 2
    assert result == _EXPECTED_DOC_NUMBERS


def test_multiple_doc_numbers_per_entry():
    """If there are multiple doc numbers per entry, get them all."""
    source = read_multiple_doc_numbers_xml()
    result = parse_stream(source)

    assert len(result) == 4
    expected = ["999000888", "123456789", "66667777", "98765432"]
    assert result == expected


def test_unsorted_entries():
    """
    Any doc numbers found in an epo entry should precede any doc numbers found
    in patent-office entries.
    """
    source = read_unsorted_xml()
    result = parse_stream(source)

    assert len(result) == 4
    assert result == ["999000888", "111222333", "66667777", "44445555"]


def test_weird_places():
    """
    Doc numbers found outside of <document-id> tags should be ignored.
    <document-id> tags found outside of <application-reference> tags should be ignored.
    """
    source = read_weird_places_xml()
    result = parse_stream(source)

    assert len(result) == 2
    assert result == _EXPECTED_DOC_NUMBERS


def test_no_attributes():
    """Entries without expected attributes should be ignored."""
    source = read_no_attributes_xml()
    result = parse_stream(source)
    assert len(result) == 0
    assert result == []


def test_extra_tags():
    """Entries outside of <application-reference> should be ignored."""
    source = read_example_xml()
    result = parse_stream(source)

    assert len(result) == 2
    assert result == _EXPECTED_DOC_NUMBERS
