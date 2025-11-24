import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]
_EXAMPLE_XML_FILE_PATH = os.path.join(ROOT, "assets", "example.xml")
_MALFORMED_XML_FILE_PATH = os.path.join(ROOT, "assets", "example_malformed.xml")
_MULTIPLE_APPLICATION_REFERENCES_XML_FILE_PATH = os.path.join(
    ROOT, "assets", "example_multiple_application_refs.xml"
)
_MULTIPLE_DOC_NUMBERS_XML_FILE_PATH = os.path.join(
    ROOT, "assets", "example_multiple_doc_numbers.xml"
)
_NO_ATTRIBUTES_XML_FILE_PATH = os.path.join(ROOT, "assets", "example_no_attributes.xml")
_UNSORTED_XML_FILE_PATH = os.path.join(ROOT, "assets", "example_unsorted.xml")
_WEIRD_PLACES_XML_FILE_PATH = os.path.join(ROOT, "assets", "example_weird_places.xml")


def get_example_filepath():
    """Get the path to the example XML file."""
    return _EXAMPLE_XML_FILE_PATH if os.path.exists(_EXAMPLE_XML_FILE_PATH) else None


def read_example_xml(filepath: str | None = None):
    """Read the example XML file and return its content."""
    path = get_example_filepath() if filepath is None else filepath
    if path is None:
        raise FileNotFoundError("Example XML file not found.")
    return open(path, "rb")


def read_extra_tags_xml():
    return read_example_xml(_WEIRD_PLACES_XML_FILE_PATH)


def read_malformed_xml():
    return read_example_xml(_MALFORMED_XML_FILE_PATH)


def read_multiple_application_references_xml():
    return read_example_xml(_MULTIPLE_APPLICATION_REFERENCES_XML_FILE_PATH)


def read_multiple_doc_numbers_xml():
    return read_example_xml(_MULTIPLE_DOC_NUMBERS_XML_FILE_PATH)


def read_no_attributes_xml():
    return read_example_xml(_NO_ATTRIBUTES_XML_FILE_PATH)


def read_unsorted_xml():
    return read_example_xml(_UNSORTED_XML_FILE_PATH)


def read_weird_places_xml():
    return read_example_xml(_WEIRD_PLACES_XML_FILE_PATH)


def compare_streams_ignore_whitespace(stream1, stream2) -> bool:
    """Compare two string streams, ignoring whitespace differences."""
    content1 = stream1.read().decode("utf-8").strip()
    content2 = stream2.read().decode("utf-8").strip()
    return compare_strings_ignore_whitespace(content1, content2)


def compare_strings_ignore_whitespace(str1: str, str2: str) -> bool:
    """Compare two strings, ignoring whitespace differences."""
    normalized_str1 = "".join(str1.split())
    normalized_str2 = "".join(str2.split())
    return normalized_str1 == normalized_str2
