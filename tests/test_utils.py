import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]
_EXAMPLE_XML_FILE_PATH = os.path.join(ROOT, "assets", "example.xml")


def get_example_filepath():
    """Get the path to the example XML file."""
    return _EXAMPLE_XML_FILE_PATH if os.path.exists(_EXAMPLE_XML_FILE_PATH) else None


def read_example_xml():
    """Read the example XML file and return its content."""
    example_path = get_example_filepath()
    if example_path is None:
        raise FileNotFoundError("Example XML file not found.")
    return open(example_path, "rb")


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
