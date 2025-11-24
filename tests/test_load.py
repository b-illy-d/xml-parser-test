import io
import sys

from xml_parser.load import _GCS_HTTP_BASE, read_file, read_gcs, read_stdin

from .test_utils import (
    compare_streams_ignore_whitespace,
    get_example_filepath,
    read_example_xml,
)


def test_read_gcs():
    url = _GCS_HTTP_BASE + "/billys_xml_example_test/example.xml"
    expected_content = read_example_xml()
    response = read_gcs(url)
    assert response is not None
    assert compare_streams_ignore_whitespace(response, expected_content)


def test_read_gcs_not_found():
    url = _GCS_HTTP_BASE + "/billys_xml_example_test/non_existent_file.xml"
    try:
        read_gcs(url)
    except Exception as e:
        assert "HTTP Error 404: Not Found" in str(e)
    else:
        assert False, "Expected error was not raised"


def test_read_stdin(monkeypatch):
    test_input = b"<root><child>Test</child></root>"

    class FakeStdin:
        def __init__(self, data: bytes):
            self.buffer = io.BytesIO(data)

    monkeypatch.setattr(sys, "stdin", FakeStdin(test_input))

    result_stream = read_stdin()
    assert result_stream.read() == test_input


def test_read_file():
    test_path = get_example_filepath()
    if test_path is None:
        raise FileNotFoundError("Example XML file not found.")
    result_stream = read_file(test_path)
    expected_stream = read_example_xml()
    assert compare_streams_ignore_whitespace(result_stream, expected_stream)
