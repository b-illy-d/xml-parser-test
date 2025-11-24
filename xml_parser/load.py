import os
import sys
from urllib.parse import urlparse
from urllib.request import urlopen

from .types import _PathLike, _StreamLike

_GCS_HTTP_BASE = "https://storage.googleapis.com"


def _normalize_stream(stream: _StreamLike | None) -> _StreamLike:
    if stream is None:
        raise ValueError("A stream must be provided")
    buffer_stream = getattr(stream, "buffer", None)
    return buffer_stream if buffer_stream is not None else stream


def read_stdin(stream: _StreamLike | None = None) -> _StreamLike:
    """Read XML data from stdin (or a provided stream) and return the parser."""
    active_stream = _normalize_stream(stream if stream is not None else sys.stdin)
    return active_stream


def read_file(path: _PathLike) -> _StreamLike:
    """Read XML data from a local file path and return the parser."""
    file_path = os.fspath(path)
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)
    if not os.path.isfile(file_path):
        raise IsADirectoryError(file_path)

    if file_path is None:
        raise FileNotFoundError("Example XML file not found.")
    return open(file_path, "rb")


def _normalize_gcs_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme in {"http", "https"}:
        return url
    if parsed.scheme != "gs":
        raise ValueError(f"Unsupported scheme for GCS url: {url}")
    if not parsed.netloc or not parsed.path:
        raise ValueError(f"Malformed GCS url: {url}")
    object_path = parsed.path.lstrip("/")
    compiled = f"{_GCS_HTTP_BASE}/{parsed.netloc}/{object_path}"
    if parsed.query:
        compiled = f"{compiled}?{parsed.query}"
    if parsed.fragment:
        compiled = f"{compiled}#{parsed.fragment}"
    return compiled


def read_gcs(url: str) -> _StreamLike:
    """Read XML data from a public Google Cloud Storage URL."""
    normalized_url = _normalize_gcs_url(url)
    try:
        response = urlopen(normalized_url)  # noqa: S310 - Public data only
    except ValueError as e:
        raise ValueError(f"Invalid URL {normalized_url}: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error while reading GCS URL {normalized_url}: {e}")

    return response
